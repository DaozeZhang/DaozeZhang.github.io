This is my personal homepage: 

Style referenced from http://hexianghu.com/.

## Google Scholar citations: local Mac updates

Citation updates use `google_scholar_crawler/update_local.py`. The old cloud crawler
is retained for reference but its GitHub workflow has no automatic triggers and
its job is disabled. No ScraperAPI account or credits are required by the local updater.

### Run / resume

```bash
# Installed isolated Python environment on this Mac (do not use system pip):
/Users/daoze/.workbuddy/binaries/python/envs/scholar-local/bin/python /Users/daoze/Desktop/DaozeZhang.github.io/google_scholar_crawler/update_local.py

# Fetch and validate only; do not commit or push:
/Users/daoze/.workbuddy/binaries/python/envs/scholar-local/bin/python /Users/daoze/Desktop/DaozeZhang.github.io/google_scholar_crawler/update_local.py --no-push

# Resume publishing a successful cached fetch; no additional Scholar requests:
/Users/daoze/.workbuddy/binaries/python/envs/scholar-local/bin/python /Users/daoze/Desktop/DaozeZhang.github.io/google_scholar_crawler/update_local.py --publish-only
```

- Default public author ID: `5beC28QAAAAJ` (override with `--scholar-id`).
- Uses the existing Mac network and standard `HTTP_PROXY` / `HTTPS_PROXY` variables
  if configured. No proxy URL or API key is saved in this repository. Ability to
  access Scholar is not guaranteed; manually resolve a CAPTCHA if one appears.
- Uses the original `scholarly==1.5.1` AuthorParser for basics, indices, counts and
  publications. `bibtexparser` must remain on 1.x; the installed version is 1.4.4.
- HTTP connect/read timeouts: 10/30 seconds. Maximum 3 requests including publication
  pagination, no HTTP retries. Entire fetch has a hard 180-second timeout.
- Only a complete, validated result can update `gs_data.json` and
  `gs_data_shieldsio.json`. Missing counts are errors, never converted to zero.
- Uses an isolated Git checkout to commit/push **only** these two JSON files to
  `google-scholar-stats`, preserving other files and the main checkout/index.
  No force-push, automatic reset or credential prompts. Existing SSH authentication
  and source repository commit/signing settings are used.
- If a push fails, the commit/changes remain in the isolated stats checkout. A later
  run can push an unpushed commit if it can fast-forward; conflicts or dirty state
  stop with an error and require inspection, not automatic deletion.

### Local state and scheduling

Ignored runtime directory: `<repo>/.workbuddy/scholar-local/`:

- `latest/`: most recent successfully validated JSON output.
- `stats-checkout/`: isolated checkout of the data branch.
- `run-YYYY-MM-DD.log`: daily run log (includes failures).
- `last_success.json`: last fully successful fetch/publish status.
- `update.lock`: OS file lock prevents overlapping runs (not a stale PID lock).

The WorkBuddy recurring task is scheduled daily at **08:00 Asia/Shanghai** and
initially PAUSED until the first Git push is verified and WorkBuddy permits normal
Git lock-file operations. Enable it after resolving that permission blocker.
WorkBuddy and this Mac need to be available with network access; it is not a system
`launchd` job and cannot run while the Mac is off. On failure, report the error and
preserve existing remote data; do not keep retrying that day.
The website continues to read the same `google-scholar-stats` JSON URLs.

The local workflow-disable changes must be committed and pushed to `main` before
the cloud crawler is actually disabled on GitHub. No automatic main-branch code
push is performed by the daily data updater.
