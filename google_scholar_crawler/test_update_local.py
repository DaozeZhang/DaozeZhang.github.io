#!/usr/bin/env python3  # daoze modified
# Test: /Users/daoze/.workbuddy/binaries/python/envs/scholar-local/bin/python -B /Users/daoze/Desktop/DaozeZhang.github.io/google_scholar_crawler/test_update_local.py
"""Offline tests: mocked HTTP + local bare Git remote; never contacts Scholar/GitHub."""
import copy
import json
import os
from pathlib import Path
import subprocess
import types
import unittest
from unittest.mock import patch
import uuid
import update_local as updater

SID = updater.SCHOLAR_ID
HTML = """<div id="gsc_prf_in">Daoze ZHANG</div><button id="gsc_bpf_more" disabled></button>
<tr class="gsc_a_tr"><td><a class="gsc_a_at">Paper</a></td><td><a class="gsc_a_ac">1</a></td></tr>
<span class="gsc_g_t">2026</span><span class="gsc_g_al">1</span>""" + '<td class="gsc_rsb_std">1</td>' * 6
AUTHOR = {"scholar_id": SID, "name": "Daoze ZHANG", "filled": updater.SECTIONS.copy(),
          "citedby": 1, "publications": [{"author_pub_id": SID + ":paper"}]}


class HTTPTests(unittest.TestCase):
    def session(self, status=200, text=HTML):
        from unittest.mock import Mock
        return Mock(get=Mock(return_value=types.SimpleNamespace(status_code=status, text=text)))

    def test_budget_and_timeout(self):
        session = self.session()
        nav = updater.LocalNavigator(session)
        for _ in range(3):
            nav._get_soup("/citations?user=" + SID)
        with self.assertRaisesRegex(RuntimeError, "budget"):
            nav._get_soup("/citations?user=" + SID)
        self.assertEqual(session.get.call_count, 3)
        self.assertEqual(session.get.call_args.kwargs["timeout"], (10, 30))
        self.assertFalse(session.get.call_args.kwargs["allow_redirects"])

    def test_http_fail_fast(self):
        for status in (302, 403, 404, 429, 500):
            session = self.session(status)
            with self.assertRaisesRegex(RuntimeError, str(status)):
                updater.LocalNavigator(session)._get_soup("/citations?user=" + SID)
            self.assertEqual(session.get.call_count, 1)

    def test_captcha_and_missing_elements(self):
        pages = [HTML + '<div id="recaptcha"></div>',
                 HTML.replace('class="gsc_a_ac"', 'class="absent"'),
                 HTML.replace('class="gsc_rsb_std"', 'class="absent"'),
                 HTML.replace('<span class="gsc_g_al">1</span>', ''),
                 '<div id="gsc_prf_in">Name</div><button id="gsc_bpf_more" disabled></button>']
        for html in pages:
            with self.assertRaises(RuntimeError):
                updater.LocalNavigator(self.session(text=html))._get_soup("/citations?user=" + SID)

    def test_network_error_redacted(self):
        session = self.session()
        session.get.side_effect = RuntimeError("secret-proxy-password")
        with self.assertRaisesRegex(RuntimeError, "network error: RuntimeError") as error:
            updater.LocalNavigator(session)._get_soup("/citations?user=" + SID)
        self.assertNotIn("secret", str(error.exception))

    def test_author_validation(self):
        self.assertEqual(updater.validate_author(copy.deepcopy(AUTHOR), SID)["citedby"], 1)
        for key, value in (("citedby", None), ("citedby", -1), ("citedby", True),
                           ("publications", []), ("filled", []), ("scholar_id", "wrong")):
            author = copy.deepcopy(AUTHOR)
            author[key] = value
            with self.assertRaises(RuntimeError):
                updater.validate_author(author, SID)
        author = copy.deepcopy(AUTHOR)
        author["publications"] *= 2
        with self.assertRaisesRegex(RuntimeError, "Duplicate"):
            updater.validate_author(author, SID)


class GitTests(unittest.TestCase):
    def test_safe_publish_isolated(self):
        root = updater.REPO / ".workbuddy" / "scholar-local" / "tests" / uuid.uuid4().hex
        root.mkdir(parents=True)
        remote, seed, state, results = (root / name for name in ("remote.git", "seed", "state", "results"))
        state.mkdir()
        updater.git(root, "init", "--bare", str(remote))
        updater.git(root, "init", "--initial-branch=" + updater.BRANCH, str(seed))
        updater.git(seed, "config", "user.name", "Offline Test")
        updater.git(seed, "config", "user.email", "test@example.invalid")
        for name in updater.FILES:
            (seed / name).write_text("{}\n")
        (seed / "keep.txt").write_text("Do not replace unrelated data\n")
        updater.git(seed, "add", ".")
        updater.git(seed, "commit", "-m", "Seed local remote")
        updater.git(seed, "remote", "add", "origin", str(remote))
        updater.git(seed, "push", "origin", updater.BRANCH)
        author = copy.deepcopy(AUTHOR)
        author["publications"] = {p["author_pub_id"]: p for p in author["publications"]}
        author["updated"] = "2026-11-03 00:00:00"
        updater.write_results(author, results)
        original_head = updater.git(updater.REPO, "rev-parse", "HEAD")
        original_index = (updater.REPO / ".git" / "index").read_bytes()
        with patch.object(updater, "REMOTE", str(remote)), patch.dict(os.environ, {
                "GIT_INDEX_FILE": str(updater.REPO / ".git" / "index"),
                "GIT_DIR": str(updater.REPO / ".git"), "GIT_WORK_TREE": str(updater.REPO)}):
            commit = updater.publish(results, state)
        self.assertEqual(updater.git(remote, "rev-parse", updater.BRANCH), commit)
        self.assertEqual(updater.git(remote, "show", commit + ":keep.txt"), "Do not replace unrelated data")
        parsed = json.loads(updater.git(remote, "show", commit + ":gs_data.json"))
        self.assertEqual(parsed["citedby"], 1)
        self.assertEqual(updater.git(updater.REPO, "rev-parse", "HEAD"), original_head)
        self.assertEqual((updater.REPO / ".git" / "index").read_bytes(), original_index)
        (state / "stats-checkout" / "keep.txt").write_text("Uncommitted change\n")
        with patch.object(updater, "REMOTE", str(remote)):
            with self.assertRaisesRegex(RuntimeError, "uncommitted changes"):
                updater.publish(results, state)
        self.assertEqual(updater.git(remote, "rev-parse", updater.BRANCH), commit)


if __name__ == "__main__":
    unittest.main(verbosity=2)
