#!/usr/bin/env python3  # daoze modified
# Launch / resume (same command; no branch switch in the homepage checkout):
# /Users/daoze/.workbuddy/binaries/python/envs/scholar-local/bin/python /Users/daoze/Desktop/DaozeZhang.github.io/google_scholar_crawler/update_local.py
# Fetch only: append --no-push. Resume publish without another HTTP request: --publish-only.
# Logs/cache: <repo>/.workbuddy/scholar-local/ (ignored).
"""Fetch public Scholar data on this Mac, then fast-forward the stats branch.

No ScraperAPI / free-proxy discovery / CAPTCHA solver. Uses the existing network
and standard HTTP(S)_PROXY environment if present. The original scholarly 1.5.1
AuthorParser handles all fields; only its HTTP transport is replaced with bounded
requests. A separate stats checkout keeps the main checkout and its index intact.
"""
import argparse
import fcntl
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
SCHOLAR_ID = "5beC28QAAAAJ"
BRANCH = "google-scholar-stats"
REMOTE = "git@github.com:DaozeZhang/DaozeZhang.github.io.git"
SECTIONS = ["basics", "indices", "counts", "publications"]
FILES = ("gs_data.json", "gs_data_shieldsio.json")
LOG = logging.getLogger("scholar_local")


class LocalNavigator:
    """Minimum transport interface consumed by the official AuthorParser."""

    def __init__(self, session, max_requests=3):
        self.session = session
        self.max_requests = max_requests
        self.requests = 0

    def _get_soup(self, path):
        from bs4 import BeautifulSoup
        if not path.startswith("/citations?"):
            raise RuntimeError("Refusing unexpected Scholar request path")
        if self.requests >= self.max_requests:
            raise RuntimeError("Scholar request budget exhausted; no partial data published")
        self.requests += 1
        try:
            response = self.session.get("https://scholar.google.com" + path,
                                        timeout=(10, 30), allow_redirects=False)
        except Exception as exc:
            # Do not print exception URLs: a configured local proxy may contain credentials.
            raise RuntimeError(f"Scholar network error: {type(exc).__name__}") from None
        LOG.info("Scholar request %d/%d: HTTP %d", self.requests,
                 self.max_requests, response.status_code)
        if response.status_code != 200:
            raise RuntimeError(f"Scholar HTTP {response.status_code}; stopping without retry")
        soup = BeautifulSoup(response.text.replace("\xa0", " "), "html.parser")
        if soup.select_one("#gs_captcha_ccl, #recaptcha, #captcha-form, .rc-doscaptcha-body"):
            raise RuntimeError("Scholar CAPTCHA: resolve manually in a browser; no automatic retry")
        if soup.find("div", id="gsc_prf_in") is None or soup.find("button", id="gsc_bpf_more") is None:
            raise RuntimeError("Scholar response is not a complete author profile")
        rows = soup.select("tr.gsc_a_tr")
        if not rows:
            raise RuntimeError("Empty publication page; refusing partial results")
        for row in rows:
            if row.select_one("a.gsc_a_at") is None or row.select_one(".gsc_a_ac") is None:
                raise RuntimeError("Missing publication title/citation element; refusing implicit zero")
        if self.requests == 1:
            indices = soup.select("td.gsc_rsb_std")
            years, counts = soup.select("span.gsc_g_t"), soup.select("span.gsc_g_al")
            if len(indices) != 6 or not all(td.get_text(strip=True).isdigit() for td in indices):
                raise RuntimeError("Missing citation indices; refusing implicit zero")
            if len(years) != len(counts) or not years:
                raise RuntimeError("Incomplete citations-per-year chart")
        return soup


def validate_author(author, scholar_id):
    if author.get("scholar_id") != scholar_id or not author.get("name"):
        raise RuntimeError("Missing or mismatched Scholar identity")
    if not set(SECTIONS).issubset(author.get("filled", [])):
        raise RuntimeError("Required Scholar sections are incomplete")
    citedby = author.get("citedby")
    if type(citedby) is not int or citedby < 0:
        raise RuntimeError("Missing or invalid citation count; not substituting zero")
    publications = author.get("publications")
    if not isinstance(publications, list) or not publications:
        raise RuntimeError("Missing publication list; refusing to overwrite old data")
    ids = [pub.get("author_pub_id") for pub in publications]
    if any(not isinstance(pid, str) or not pid.startswith(scholar_id + ":") for pid in ids):
        raise RuntimeError("Missing or mismatched publication IDs")
    if len(set(ids)) != len(ids):
        raise RuntimeError("Duplicate publication IDs; refusing lossy conversion")
    return author


def fetch_author(scholar_id, max_requests):
    import requests
    from scholarly.author_parser import AuthorParser
    LOG.info("Network: %s", "configured environment proxy" if any(
        os.environ.get(k) for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"))
        else "direct local connection")
    with requests.Session() as session:
        session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
        navigator = LocalNavigator(session, max_requests)
        parser = AuthorParser(navigator)
        author = parser.get_author(scholar_id)  # Same initial object as the existing crawler.
        parser.fill(author, sections=SECTIONS.copy())
        validate_author(author, scholar_id)
        author["updated"] = str(datetime.now())  # Preserve existing JSON timestamp format.
        author["publications"] = {p["author_pub_id"]: p for p in author["publications"]}
        LOG.info("Fetched %s: %d citations, %d publications, %d HTTP requests",
                 author["name"], author["citedby"], len(author["publications"]), navigator.requests)
        return author


def write_results(author, directory):
    # Only called after ALL profile sections and publication pages passed validation.
    directory.mkdir(parents=True, exist_ok=True)
    badge = {"schemaVersion": 1, "label": "citations", "message": str(author["citedby"])}
    for name, value in ((FILES[0], author), (FILES[1], badge)):
        temporary = directory / (name + ".pending")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, directory / name)


def git(cwd, *args, timeout=60):
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"):
        env.pop(name, None)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes -o ConnectTimeout=15"
    result = subprocess.run(["git", "-C", str(cwd), *args], env=env,
                            capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"git {args[0]} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def validate_results(directory):
    author = json.loads((directory / FILES[0]).read_text(encoding="utf-8"))
    publications = author.get("publications")
    if not isinstance(publications, dict) or any(
            key != value.get("author_pub_id") for key, value in publications.items()):
        raise RuntimeError("Cached publication keys do not match author_pub_id")
    validator = dict(author, publications=list(publications.values()))
    validate_author(validator, author.get("scholar_id"))
    if not author.get("updated"):
        raise RuntimeError("Cached author timestamp is missing")
    badge = json.loads((directory / FILES[1]).read_text(encoding="utf-8"))
    if badge != {"schemaVersion": 1, "label": "citations", "message": str(author["citedby"])}:
        raise RuntimeError("Cached badge does not match validated citation data")
    return author


def publish(directory, state):
    validate_results(directory)
    checkout = state / "stats-checkout"
    if not checkout.exists():
        git(state, "clone", "--single-branch", "--branch", BRANCH, "--no-tags", REMOTE, str(checkout))
    if git(checkout, "remote", "get-url", "origin") != REMOTE:
        raise RuntimeError("Unexpected origin in isolated stats checkout")
    if git(checkout, "branch", "--show-current") != BRANCH:
        raise RuntimeError("Unexpected branch in isolated stats checkout")
    if git(checkout, "status", "--porcelain"):
        raise RuntimeError("Stats checkout has uncommitted changes; preserving them for inspection")
    git(checkout, "fetch", "--no-tags", "origin", BRANCH)
    git(checkout, "merge", "--ff-only", "FETCH_HEAD")
    # Keep remote files unrelated to these two JSON outputs. No force-push or reset.
    for name in FILES:
        (checkout / name).write_bytes((directory / name).read_bytes())
    git(checkout, "add", "--", *FILES)
    if git(checkout, "diff", "--cached", "--name-only"):
        # Reuse the identity and signing configuration from the source repository.
        for setting in ("user.name", "user.email", "user.signingkey", "commit.gpgsign", "gpg.format", "gpg.program", "core.hooksPath"):
            probe = subprocess.run(["git", "-C", str(REPO), "config", "--get", setting],
                                   capture_output=True, text=True, timeout=10)
            if probe.returncode == 0 and probe.stdout.strip():
                value = probe.stdout.strip()
                if setting == "core.hooksPath" and not Path(value).is_absolute():
                    value = str(REPO / value)
                git(checkout, "config", "--local", setting, value)
        git(checkout, "commit", "-m", "Updated Citation Data (local Mac)")
    commit = git(checkout, "rev-parse", "HEAD")
    git(checkout, "push", "origin", f"HEAD:refs/heads/{BRANCH}")
    remote_head = git(checkout, "ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    if remote_head != commit:
        raise RuntimeError("Remote stats head changed during verification; inspect before rerunning")
    LOG.info("Published and verified %s at %s", BRANCH, commit)
    return commit


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--scholar-id", default=SCHOLAR_ID)
    modes = args.add_mutually_exclusive_group()
    modes.add_argument("--no-push", action="store_true", help="Fetch validated JSON without committing/pushing")
    modes.add_argument("--publish-only", action="store_true", help="Validate/publish cached JSON without fetching again")
    args.add_argument("--max-requests", type=int, default=3, help="Total HTTP budget, including pagination, no retries")
    args.add_argument("--fetch-timeout", type=int, default=180, help="Hard timeout for the entire fetch subprocess")
    args.add_argument("--state-dir", type=Path, default=REPO / ".workbuddy" / "scholar-local")
    args.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    options = args.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{12}", options.scholar_id):
        args.error("scholar-id must be the 12-character public profile ID")
    if not 1 <= options.max_requests <= 3 or not 1 <= options.fetch_timeout <= 180:
        args.error("max-requests must be 1..3 and fetch-timeout 1..180")
    state = options.state_dir.resolve()
    state.mkdir(parents=True, exist_ok=True)
    log_path = state / ("run-" + datetime.now().strftime("%Y-%m-%d") + ".log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")])
    logging.getLogger("scholarly").setLevel(logging.WARNING)
    results = state / "latest"
    if options.worker:
        write_results(fetch_author(options.scholar_id, options.max_requests), results)
        return
    with (state / "update.lock").open("a+") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another local Scholar update is running") from None
        # ScraperAPI is never called, even if a key is inherited from the environment.
        env = os.environ.copy()
        env.pop("SCRAPER_API_KEY", None)
        if not options.publish_only:
            command = [sys.executable, "-B", str(Path(__file__).resolve()), "--worker", "--scholar-id",
                       options.scholar_id, "--max-requests", str(options.max_requests), "--state-dir", str(state)]
            worker = subprocess.run(command, env=env, timeout=options.fetch_timeout)
            if worker.returncode:
                raise RuntimeError("Fetch failed; remote stats were not touched. See local run log.")
        if options.publish_only and validate_results(results)["scholar_id"] != options.scholar_id:
            raise RuntimeError("Cached author differs from requested scholar-id")
        commit = None if options.no_push else publish(results, state)
        summary = {"status": "fetched-only" if options.no_push else "published", "commit": commit,
                   "log": str(log_path), "finished_at": datetime.now().isoformat()}
        (state / "last_success.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        LOG.info("Update complete: %s; log=%s", summary["status"], log_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        if isinstance(exc, subprocess.TimeoutExpired):
            message = "Operation timed out; no automatic retry. Inspect the run log and stats checkout."
        else:
            message = str(exc)
        logging.getLogger("scholar_local").error("%s", message)
        sys.exit(1)
