---
name: babysit-pr
description: Use when the user asks to monitor, watch, or babysit a PR
metadata:
  harness: [claude, codex]
  platform: [darwin, linux]
---

# Babysit PR

All the repos we work in have AI review bots (CodeRabbit, Codex review). They're helpful, even if they are not always right.

The watcher `scripts/pr_watch.py` (next to this file) owns all PR polling: CI on the head commit, bot reviews of the exact head SHA, bot triggers, CodeRabbit rate-limit waits, review threads, unanswered human comments, and conflicts. Use it for every wait and every "is it done?" question. It needs only `gh` and `python3`.

## Loop

1. **Watch.** Run the watcher in the background and keep working or idle until it exits:

   ```bash
   python3 <skill-dir>/scripts/pr_watch.py watch <PR number or URL> [-R owner/repo] --as "<MODEL NAME>"
   ```

   - omp: `bash` with `async: true` and `timeout: 3600`; the result arrives on its own.
   - Claude Code: `Bash` with `run_in_background: true`; you are notified on exit.
   - Codex: `exec_command` with the largest `yield_time_ms` allowed; while it runs, `write_stdin` with empty input and the largest yield.
   - Other harnesses: run it in the foreground with `--timeout` under the tool's limit.

   It prints one JSON report on exit. Exit codes: `0` ready, `10` action needed, `20` merged or closed, `30` timed out while still waiting (run the same command again), `3` another watcher already owns this PR (wait for that one), `2` gh/API error (read `detail`).

2. **Act** on every item in `actions`, then go back to step 1. A push changes the head; the watcher then requests fresh bot reviews by itself.

   | `kind` | Do |
   |---|---|
   | `check_failed` | Read the logs (`gh run view <id> --log-failed`). Fix repository failures. Rerun infrastructure flakes (`gh run rerun <id> --failed`). For a non-required check you judge unrelated, rerun the watcher with `--ignore-check "<name>"` and say why in your report. |
   | `unresolved_thread` | Verify the finding against the source. Fix it and push, then `reply <thread_id> --body "<what changed>" --resolve`. If you reject it, reply with the reason and `--resolve`. Outdated threads count too. |
   | `body_findings` | Findings in the review body that GitHub could not attach inline. Fix them, then answer all of them in one `comment`. |
   | `human_comment` | Instructions from the user or a reviewer. Follow them; answer with `comment`. A hold or stop instruction ends the loop: report and wait for the user. |
   | `merge_conflict`, `behind_base` | Rebase on the base branch and push. |

   Helpers, all posting with the disclosure header:

   ```bash
   python3 <skill-dir>/scripts/pr_watch.py reply <thread_id> --body "..." [--resolve] --as "<MODEL NAME>"
   python3 <skill-dir>/scripts/pr_watch.py comment <PR> --body "..." --as "<MODEL NAME>"
   python3 <skill-dir>/scripts/pr_watch.py resolve <thread_id>...
   python3 <skill-dir>/scripts/pr_watch.py status <PR>   # one read-only evaluation
   ```

3. **Done** when the watcher exits `0`: CI finished and passing, every working bot reviewed the current head, no unresolved threads, nothing unanswered, no conflicts. Report the PR as ready with the head SHA from the report. Merge only when the user explicitly asked for it, and only on the head the watcher approved. Exit `20` means someone else merged or closed it; report that.

   A bot that cannot review (Codex has no environment for the repo, CodeRabbit hits its file limit, a bot never answers or errors after 3 requests) appears in `blocked_bots`. The watcher stops requiring it and keeps watching CI and the other bots, so keep the loop going. Name each blocked bot and its `detail` in the final report, so the user can fix the setup; a PR reviewed by fewer bots than usual is still ready.

Only the watcher's exit `0` makes a PR ready. CI passing alone, a bot review of an earlier commit, or a quiet PR is still `waiting`.

## Judging findings

Act only on checks and comments for the latest push; the watcher already filters by head SHA. Verify every bot finding against the source before changing code. Weigh each finding against the PR's original goal: fix real shortcomings, push back on scope creep, and reply with a written reason when dismissing a false positive.

The watcher reports an `unresolved_thread` until the thread is resolved in GitHub; a reply alone leaves it open. Use `reply --resolve`.

If an overlapping PR makes this one obsolete, stop watching, report it to the user, and ask before closing the PR unless closure was explicitly authorized.

### chatgpt-codex-connector reviews

The Codex review bot is notoriously bad at judging severity: a comment it labels P1 could really be a P3, or not a real issue at all. Use your own judgement on whether a finding is real and worth fixing.

## Comments on Microck's behalf

Every comment you post carries a one-line GitHub `NOTE` alert with the disclosure, the reply unquoted below it. The helpers add it from `--as` (or `BABYSIT_MODEL`); write it by hand only when you post some other way:

```md
> [!NOTE]
> 🤖 [MODEL NAME] responding on behalf of Microck

[actual reply]
```

The watcher relies on this marker to tell your replies from Microck's own instructions, so keep the exact wording.

Post only when you have something to say: a fix, a reason, or an answer. Screenshots and videos help; use the `file-upload` skill to host them.

## Repos you don't own

On third-party repos the watcher requires only the bots already active on the PR and never posts review requests. If a review request is needed there, ask the user first, then pass `--third-party-triggers`.
