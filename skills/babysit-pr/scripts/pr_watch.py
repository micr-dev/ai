#!/usr/bin/env python3
"""Deterministic PR babysitting helper for the babysit-pr skill.

One shared implementation of "is this PR done?" so agents stop hand-writing
poll loops. It reads everything in one GraphQL query per poll and judges the
PR against the *current head commit*:

  - CI: every check on the head finished; failures listed (required or not).
  - Review bots: each bot reviewed the exact head SHA. Triggers them when they
    did not auto-run, waits out CodeRabbit rate limits until the stated reset,
    detects unresponsive or erroring bots instead of waiting forever. A bot
    that cannot review lands in `blocked_bots` and stops being required; the
    watch carries on with CI and the remaining bots.
  - Review threads: every thread resolved (outdated ones too).
  - Bot findings outside the diff: answered by an agent comment.
  - Human comments: answered by an agent comment.
  - Merge state: no conflicts, not behind base.

Subcommands
  status  [PR]   one read-only evaluation, prints JSON
  watch   [PR]   block until something needs the agent, the PR is ready, or
                 the PR closes; posts bot triggers itself; prints JSON once
  comment [PR]   post an issue comment with the agent disclosure header
  reply THREAD   reply to a review thread (disclosure header), optionally resolve
  resolve THREAD resolve review threads

Exit codes (status and watch)
  0 ready   10 action_needed   20 merged/closed   30 still waiting
  2 gh/API error   3 another watcher already owns this PR

Only needs `gh` (authenticated) and Python 3.9+. Never merges or pushes.
"""

from __future__ import annotations

import argparse
import fcntl
import fnmatch
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

EXIT_READY, EXIT_ACTION, EXIT_CLOSED, EXIT_WAITING = 0, 10, 20, 30
EXIT_ERROR, EXIT_LOCKED = 2, 3

# Marker every agent-authored comment carries (see SKILL.md disclosure format).
# Agents post as the user's own login, so this is the only way to tell an agent
# reply from a human instruction written by the owner.
AGENT_MARK = "responding on behalf of"

BOTS = {
    "coderabbit": {"login": "coderabbitai", "trigger": "@coderabbitai review"},
    "codex": {"login": "chatgpt-codex-connector", "trigger": "@codex review"},
}
# Check contexts owned by review bots are judged through the bot logic, not CI.
BOT_CHECK_NAMES = ("coderabbit",)

ACK_TIMEOUT = timedelta(minutes=10)  # bot never acknowledged a trigger -> unresponsive
STALL_AFTER = {"coderabbit": timedelta(minutes=45), "codex": timedelta(minutes=40)}
AUTO_REVIEW_GRACE = timedelta(minutes=3)  # let CodeRabbit auto-review a fresh push first
CHECKS_START_GRACE = timedelta(minutes=3)  # CI may not have registered yet after a push
MAX_TRIGGERS_PER_HEAD = 3
RATE_LIMIT_FALLBACK = timedelta(minutes=30)  # reply said "rate limited" without a reset time

FAILED = {"FAILURE", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED", "STARTUP_FAILURE", "ERROR", "STALE"}
PASSED = {"SUCCESS", "NEUTRAL", "SKIPPED"}

QUERY = """
query($owner:String!,$name:String!,$pr:Int!){
 viewer{login}
 repository(owner:$owner,name:$name){
  pullRequest(number:$pr){
   id number url state isDraft mergeable mergeStateStatus baseRefName headRefOid
   commits(last:1){nodes{commit{oid committedDate
    statusCheckRollup{contexts(first:100){nodes{
     __typename
     ... on CheckRun{name status conclusion detailsUrl isRequired(pullRequestNumber:$pr) checkSuite{workflowRun{workflow{name}}}}
     ... on StatusContext{context state targetUrl isRequired(pullRequestNumber:$pr)}
    }}}}}}
   timelineItems(last:20,itemTypes:[HEAD_REF_FORCE_PUSHED_EVENT]){nodes{... on HeadRefForcePushedEvent{createdAt afterCommit{oid}}}}
   reviews(last:100){nodes{author{__typename login} state submittedAt body url commit{oid}}}
   headComments: comments(first:10){nodes{...C}}
   tailComments: comments(last:100){nodes{...C}}
   reviewThreads(first:100){pageInfo{hasNextPage endCursor} nodes{...T}}
  }}}
fragment C on IssueComment{id author{__typename login} body createdAt updatedAt url reactions(first:20){nodes{content user{login}}}}
fragment T on PullRequestReviewThread{id isResolved isOutdated path line
 firstComment: comments(first:1){nodes{author{__typename login} body url}}
 lastComment: comments(last:1){nodes{author{login} body createdAt}}}
"""

THREADS_PAGE = """
query($owner:String!,$name:String!,$pr:Int!,$after:String!){
 repository(owner:$owner,name:$name){pullRequest(number:$pr){
  reviewThreads(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{...T}}}}}
fragment T on PullRequestReviewThread{id isResolved isOutdated path line
 firstComment: comments(first:1){nodes{author{__typename login} body url}}
 lastComment: comments(last:1){nodes{author{login} body createdAt}}}
"""


class GhError(Exception):
    pass


def log(msg: str) -> None:
    print(f"[pr_watch {datetime.now(timezone.utc):%H:%M:%SZ}] {msg}", file=sys.stderr, flush=True)


def gh(args: list[str]) -> str:
    """Run gh; retry only transient network/5xx/secondary-rate-limit failures."""
    for attempt in range(4):
        proc = subprocess.run(["gh", *args], capture_output=True, text=True)
        if proc.returncode == 0:
            return proc.stdout
        err = proc.stderr.strip() or f"gh exited {proc.returncode}"
        transient = re.search(r"(?i)timed? ?out|50[234]|connection (reset|refused)|\bEOF\b|secondary rate limit|submitted too quickly|i/o", err)
        if not transient or attempt == 3:
            raise GhError(err)
        log(f"transient gh failure, retrying: {err.splitlines()[0][:160]}")
        time.sleep(5 * 2**attempt)
    raise AssertionError("unreachable")


def graphql(query: str, **variables) -> dict:
    args = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        args += ["-F" if isinstance(value, int) else "-f", f"{key}={value}"]
    return json.loads(gh(args))["data"]


def ts(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def iso(value: datetime | None) -> str | None:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if value else None


def login(node: dict | None) -> str:
    author = (node or {}).get("author") or (node or {}).get("user") or {}
    return (author.get("login") or "ghost").removesuffix("[bot]")


def excerpt(body: str, limit: int = 300) -> str:
    text = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + ("…" if len(text) > limit else "")


# ---------------------------------------------------------------- resolution


def resolve_target(pr: str | None, repo: str | None) -> tuple[str, str, int]:
    """Accept a PR number, a PR URL, or nothing (current branch)."""
    if pr and (m := re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", pr)):
        return m.group(1), m.group(2), int(m.group(3))
    args = ["pr", "view", *([pr] if pr else []), "--json", "number,url"]
    if repo:
        args += ["-R", repo]
    info = json.loads(gh(args))
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", info["url"])
    return m.group(1), m.group(2), int(m.group(3))


def fetch(owner: str, name: str, number: int) -> tuple[dict, str]:
    data = graphql(QUERY, owner=owner, name=name, pr=number)
    pr = data["repository"]["pullRequest"]
    threads = pr["reviewThreads"]
    while threads["pageInfo"]["hasNextPage"]:
        page = graphql(THREADS_PAGE, owner=owner, name=name, pr=number, after=threads["pageInfo"]["endCursor"])
        more = page["repository"]["pullRequest"]["reviewThreads"]
        threads["nodes"] += more["nodes"]
        threads["pageInfo"] = more["pageInfo"]
    return pr, data["viewer"]["login"]


# ---------------------------------------------------------------- evaluation


def head_pushed_at(pr: dict) -> datetime:
    """Best available push time of the head: commit date or a later force-push."""
    commit = pr["commits"]["nodes"][0]["commit"]
    pushed = ts(commit["committedDate"])
    for event in pr["timelineItems"]["nodes"]:
        if (event.get("afterCommit") or {}).get("oid") == pr["headRefOid"]:
            pushed = max(pushed, ts(event["createdAt"]))
    return pushed


def all_comments(pr: dict) -> list[dict]:
    seen = {}
    for c in pr["headComments"]["nodes"] + pr["tailComments"]["nodes"]:
        seen[c["id"]] = c
    return sorted(seen.values(), key=lambda c: c["createdAt"])


def evaluate_checks(pr: dict, pushed: datetime, now: datetime, ignore: list[str]) -> tuple[dict, list, list]:
    contexts = pr["commits"]["nodes"][0]["commit"].get("statusCheckRollup") or {}
    contexts = (contexts.get("contexts") or {}).get("nodes") or []
    summary = {"passed": 0, "pending": [], "failed": [], "ignored": []}
    for ctx in contexts:
        if ctx["__typename"] == "CheckRun":
            name = ctx["name"]
            workflow = (((ctx.get("checkSuite") or {}).get("workflowRun") or {}).get("workflow") or {}).get("name")
            label = f"{workflow} / {name}" if workflow else name
            done = ctx["status"] == "COMPLETED"
            outcome = ctx.get("conclusion") or ctx["status"]
            url = ctx.get("detailsUrl")
        else:
            name = label = ctx["context"]
            outcome = ctx["state"]
            done = outcome not in ("PENDING", "EXPECTED")
            url = ctx.get("targetUrl")
        if any(b in name.lower() for b in BOT_CHECK_NAMES):
            continue
        if any(fnmatch.fnmatch(label, pat) or fnmatch.fnmatch(name, pat) for pat in ignore):
            summary["ignored"].append(label)
            continue
        entry = {"name": label, "required": bool(ctx.get("isRequired")), "outcome": outcome, "url": url}
        # push and pull_request runs of one workflow report the same check twice
        if any(e["name"] == label and e["outcome"] == outcome for e in summary["pending"] + summary["failed"]):
            continue
        if not done:
            summary["pending"].append(entry)
        elif outcome in PASSED:
            summary["passed"] += 1
        else:
            summary["failed"].append(entry)
    actions = [{"kind": "check_failed", **c} for c in summary["failed"]]
    waiting = [{"kind": "check_pending", "name": c["name"], "required": c["required"]} for c in summary["pending"]]
    if not contexts and now - pushed < CHECKS_START_GRACE:
        waiting.append({"kind": "checks_not_started", "until": iso(pushed + CHECKS_START_GRACE)})
    return summary, actions, waiting


def parse_duration(text: str) -> timedelta | None:
    m = re.search(r"available in\s+(?:(\d+)\s*hours?)?\s*(?:and\s*)?(?:(\d+)\s*minutes?)?(?:\s*and\s*(\d+)\s*seconds?)?", text)
    if not m or not any(m.groups()):
        return None
    hours, minutes, seconds = (int(g or 0) for g in m.groups())
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def trigger_plan(bot: str, triggers: list[dict], acknowledged, now: datetime) -> dict:
    """Shared trigger bookkeeping: decide trigger / wait / escalate for one bot on this head."""
    if not triggers:
        return {"status": "not_requested", "trigger": True, "reason": "no review requested for this head"}
    last = triggers[-1]
    last_at = ts(last["createdAt"])
    if not acknowledged(last):
        if now - last_at > ACK_TIMEOUT:
            return {"status": "unresponsive", "action": f"{bot} did not acknowledge `{BOTS[bot]['trigger']}` within {ACK_TIMEOUT.seconds // 60} min; check the app is installed on this repo or drop it with --bots", "trigger_url": last["url"]}
        return {"status": "requested", "since": iso(last_at)}
    if now - last_at > STALL_AFTER[bot]:
        if len(triggers) >= MAX_TRIGGERS_PER_HEAD:
            return {"status": "stalled", "action": f"{bot} acknowledged {len(triggers)} review requests for this head but never reviewed it"}
        return {"status": "stalled", "trigger": True, "reason": f"acknowledged but silent for {STALL_AFTER[bot].seconds // 60} min"}
    return {"status": "in_progress", "since": iso(last_at)}


def capped(plan: dict, bot: str, triggers: list[dict]) -> dict:
    if plan.get("trigger") and len(triggers) >= MAX_TRIGGERS_PER_HEAD:
        return {"status": plan["status"], "action": f"{bot}: {len(triggers)} review requests for this head already; not requesting again ({plan.get('reason')})"}
    return plan


def coderabbit_state(pr: dict, comments: list[dict], pushed: datetime, now: datetime) -> dict:
    head = pr["headRefOid"]
    bot = "coderabbit"
    mine = [c for c in comments if login(c) == BOTS[bot]["login"]]
    summary = max((c for c in mine if "summarize by coderabbit.ai" in c["body"]), key=lambda c: c["updatedAt"], default=None)
    reviews = [r for r in pr["reviews"]["nodes"] if login(r) == BOTS[bot]["login"] and (r.get("commit") or {}).get("oid") == head and r["state"] != "DISMISSED"]
    covered = bool(summary and re.search(r'"coveredCommitId":"%s","kind":"reviewed"' % head, summary["body"]))
    if reviews or covered:
        latest = reviews[-1] if reviews else None
        outside = 0
        if latest and (m := re.search(r"Outside diff range comments \((\d+)\)", latest["body"] or "")):
            outside = int(m.group(1))
        return {"status": "reviewed", "review_state": latest["state"] if latest else "SUMMARY_ONLY", "outside_diff_findings": outside, "review": latest}

    triggers = [c for c in comments if BOTS[bot]["trigger"] in c["body"] and ts(c["createdAt"]) >= pushed]
    replies = [c for c in mine if "auto-generated reply by CodeRabbit" in c["body"] and ts(c["createdAt"]) >= pushed]
    after_last = [c for c in replies if triggers and c["createdAt"] >= triggers[-1]["createdAt"]]
    last_reply = after_last[-1]["body"] if after_last else ""
    summary_body = summary["body"] if summary else ""

    if m := re.search(r"Review skipped: ([^\n<]+)", last_reply) or re.search(r"(\d+ files exceed the limit[^\n<]*)", summary_body):
        if "files exceed" in m.group(1):
            return {"status": "unreviewable", "action": f"CodeRabbit cannot review this PR: {m.group(1).strip()}. Tell the user; do not keep triggering."}

    retry_at = None
    if summary and "rate limited by coderabbit.ai" in summary_body:
        retry_at = ts(summary["updatedAt"]) + (parse_duration(summary_body) or RATE_LIMIT_FALLBACK)
    elif "Review rate limited" in last_reply:
        retry_at = ts(after_last[-1]["updatedAt"]) + RATE_LIMIT_FALLBACK
    if retry_at:
        if now < retry_at:
            return {"status": "rate_limited", "retry_at": iso(retry_at)}
        if not triggers or ts(triggers[-1]["createdAt"]) < retry_at:
            return capped({"status": "rate_limit_over", "trigger": True, "reason": "rate limit window passed"}, bot, triggers)

    if "review in progress by coderabbit.ai" in summary_body:
        return {"status": "in_progress"}
    if "Review finished" in last_reply:
        # CodeRabbit is incremental: "finished" with nothing new posted means the
        # head produced no findings. Findings, if any, arrive as a review on the head.
        return {"status": "reviewed", "review_state": "FINISHED_NO_REVIEW", "outside_diff_findings": 0, "review": None}
    if "base or head changed" in last_reply:
        return capped({"status": "head_changed", "trigger": True, "reason": "CodeRabbit aborted: head changed"}, bot, triggers)
    if not triggers and "fewer than 10 stars" not in summary_body and now - pushed < AUTO_REVIEW_GRACE:
        return {"status": "auto_review_grace", "until": iso(pushed + AUTO_REVIEW_GRACE)}

    def acknowledged(trigger):
        return any(r["createdAt"] >= trigger["createdAt"] for r in replies)

    return capped(trigger_plan(bot, triggers, acknowledged, now), bot, triggers)


CODEX_COMMIT = re.compile(r"Reviewed commit:\*{0,2}\s*`([0-9a-f]{7,40})`")
CODEX_SUMMARY = "codex-pull-request-review-summary"
# Row of the sticky summary table, e.g. "| 📝 **Code Review** | ✅ **Completed** <time …> | `9a3b4ff` | Manual request |"
CODEX_SUMMARY_ROW = re.compile(r"\|\s*\S*\s*\*\*Code Review\*\*\s*\|\s*\S*\s*\*\*(\w[\w ]*)\*\*[^|]*\|\s*`([0-9a-f]{7,40})`")


def codex_state(pr: dict, comments: list[dict], pushed: datetime, now: datetime) -> dict:
    head = pr["headRefOid"]
    bot = "codex"
    bot_login = BOTS[bot]["login"]

    def reviewed_sha(body):
        m = CODEX_COMMIT.search(body or "")
        return m.group(1) if m else None

    # Findings arrive as a PR review on the reviewed commit.
    reviews = [r for r in pr["reviews"]["nodes"] if login(r) == bot_login and ((r.get("commit") or {}).get("oid") == head or (reviewed_sha(r["body"]) and head.startswith(reviewed_sha(r["body"]))))]
    if reviews:
        return {"status": "reviewed", "review_state": "FINDINGS", "review": reviews[-1]}

    mine = [c for c in comments if login(c) == bot_login]
    # Older format: a "Didn't find any major issues" comment naming the commit.
    for c in reversed(mine):
        sha = reviewed_sha(c["body"])
        if sha and head.startswith(sha) and re.search(r"find any major issues", c["body"]):
            return {"status": "reviewed", "review_state": "CLEAN", "review": None}

    # Current format: one sticky summary comment, edited in place as reviews run.
    # Its createdAt is the first review ever, so freshness comes from updatedAt.
    summary = next((c for c in reversed(mine) if CODEX_SUMMARY in c["body"]), None)
    row = CODEX_SUMMARY_ROW.search(summary["body"]) if summary else None
    if row and head.startswith(row.group(2)):
        status = row.group(1).strip().lower()
        if status == "completed":
            return {"status": "reviewed", "review_state": "CLEAN", "review": None}
        if status in ("running", "queued", "pending", "in progress"):
            return {"status": "in_progress", "since": summary["updatedAt"]}
        return {"status": "error", "action": f"Codex review of {row.group(2)} ended as '{row.group(1)}'", "url": summary["url"]}

    triggers = [c for c in comments if BOTS[bot]["trigger"] in c["body"] and ts(c["createdAt"]) >= pushed]
    if triggers:
        last_at = triggers[-1]["createdAt"]
        replies = [c for c in mine if c["createdAt"] >= last_at and CODEX_SUMMARY not in c["body"]]
        for reply in replies:
            sha = reviewed_sha(reply["body"])
            if sha and not head.startswith(sha):
                return capped({"status": "reviewed_other_commit", "trigger": True, "reason": f"Codex reviewed {sha}, not head"}, bot, triggers)
            if not sha:
                # e.g. "To use Codex here, create an environment for this repo"
                return {"status": "error", "action": f"Codex replied without reviewing: {excerpt(reply['body'], 240)}", "url": reply["url"]}

    def acknowledged(trigger):
        reacted = any(login({"author": r["user"]}) == bot_login for r in trigger["reactions"]["nodes"])
        summary_moved = bool(summary) and summary["updatedAt"] >= trigger["createdAt"]
        return reacted or summary_moved or any(c["createdAt"] >= trigger["createdAt"] for c in mine)

    return capped(trigger_plan(bot, triggers, acknowledged, now), bot, triggers)


def is_human(node: dict) -> bool:
    author = node.get("author") or {}
    return author.get("__typename") != "Bot" and not (author.get("login") or "").endswith("[bot]")


def evaluate(pr: dict, viewer: str, now: datetime, bots: list[str], ignore: list[str], third_party_triggers: bool = False) -> dict:
    head = pr["headRefOid"]
    report = {"pr": pr["url"], "head": head[:12], "state": pr["state"], "verdict": None, "actions": [], "waiting": [], "blocked_bots": [], "info": [], "bots": {}, "checks": None}
    if pr["state"] != "OPEN":
        report["verdict"] = pr["state"].lower()
        return report

    pushed = head_pushed_at(pr)
    report["head_pushed_at"] = iso(pushed)
    comments = all_comments(pr)
    # Agent answers: disclosed comments that say more than a bare review trigger.
    trigger_only = re.compile(r"^\s*(@coderabbitai|@codex)\s+(full\s+)?review\s*$", re.I)
    agent_comments = [c for c in comments if AGENT_MARK in c["body"] and not trigger_only.match(c["body"].split("\n\n", 1)[-1])]
    last_agent_at = agent_comments[-1]["createdAt"] if agent_comments else ""

    summary, actions, waiting = evaluate_checks(pr, pushed, now, ignore)
    report["checks"] = {"passed": summary["passed"], "pending": len(summary["pending"]), "failed": len(summary["failed"]), "ignored": summary["ignored"]}
    report["actions"] += actions
    report["waiting"] += waiting

    # Someone else's repo: their bots are optional, and posting review triggers
    # there needs an explicit user request (--third-party-triggers).
    own_repo = pr["url"].split("/")[3].lower() == viewer.lower()
    active = {login(n) for n in comments + pr["reviews"]["nodes"]}
    state_fns = {"coderabbit": coderabbit_state, "codex": codex_state}
    for bot in bots:
        if not own_repo and BOTS[bot]["login"] not in active:
            report["info"].append(f"{bot} not active on this third-party PR; not required")
            continue
        st = state_fns[bot](pr, comments, pushed, now)
        if st.get("trigger") and not own_repo and not third_party_triggers:
            st = {"status": st["status"], "action": f"{bot} needs `{BOTS[bot]['trigger']}` but this is a third-party repo; ask the user, then rerun with --third-party-triggers"}
        review = st.pop("review", None)
        if review:
            st["review_url"] = review["url"]
            # Findings in the review body (not threads) need an explicit agent answer.
            if st.get("outside_diff_findings") and not any(c["createdAt"] > review["submittedAt"] for c in agent_comments):
                report["actions"].append({"kind": "body_findings", "bot": bot, "count": st["outside_diff_findings"], "url": review["url"], "hint": "fix or answer each finding in one disclosed PR comment"})
        report["bots"][bot] = st
        if "action" in st:
            # One bot being unable to review must not stall the PR: keep watching
            # CI and the other bots, and surface the blocked bot in the final report.
            report["blocked_bots"].append({"bot": bot, "detail": st["action"], **({"url": st["url"]} if st.get("url") else {})})
        elif st["status"] != "reviewed":
            report["waiting"].append({"kind": "bot_review", "bot": bot, "status": st["status"], **{k: st[k] for k in ("retry_at", "until", "since") if k in st}})

    for thread in pr["reviewThreads"]["nodes"]:
        if thread["isResolved"]:
            continue
        first = thread["firstComment"]["nodes"][0] if thread["firstComment"]["nodes"] else {}
        last = thread["lastComment"]["nodes"][0] if thread["lastComment"]["nodes"] else {}
        report["actions"].append({
            "kind": "unresolved_thread", "thread_id": thread["id"], "author": login(first),
            "path": thread["path"], "line": thread["line"], "outdated": thread["isOutdated"],
            "agent_replied": AGENT_MARK in (last.get("body") or ""), "url": first.get("url"),
            "excerpt": excerpt(first.get("body", "")),
        })

    bot_logins = {b["login"] for b in BOTS.values()}
    human = [c for c in comments if is_human(c) and login(c) not in bot_logins and AGENT_MARK not in c["body"] and not trigger_only.match(c["body"])]
    human += [{**r, "createdAt": r["submittedAt"]} for r in pr["reviews"]["nodes"] if is_human(r) and (r["body"] or "").strip() and AGENT_MARK not in r["body"]]
    for c in human:
        if c["createdAt"] > last_agent_at:
            report["actions"].append({"kind": "human_comment", "author": login(c), "at": c["createdAt"], "url": c["url"], "excerpt": excerpt(c["body"], 500)})

    if pr["mergeable"] == "CONFLICTING" or pr["mergeStateStatus"] == "DIRTY":
        report["actions"].append({"kind": "merge_conflict", "base": pr["baseRefName"]})
    elif pr["mergeStateStatus"] == "BEHIND":
        report["actions"].append({"kind": "behind_base", "base": pr["baseRefName"], "hint": "rebase on the base branch and push"})
    elif pr["mergeable"] == "UNKNOWN":
        report["waiting"].append({"kind": "mergeability_computing"})
    report["info"].append(f"mergeStateStatus={pr['mergeStateStatus']}" + (" (draft)" if pr["isDraft"] else ""))

    report["verdict"] = "action_needed" if report["actions"] else "waiting" if report["waiting"] else "ready"
    return report


def exit_code(report: dict) -> int:
    return {"ready": EXIT_READY, "action_needed": EXIT_ACTION, "waiting": EXIT_WAITING}.get(report["verdict"], EXIT_CLOSED)


# ---------------------------------------------------------------- mutations


def disclosure(model: str, viewer: str, body: str) -> str:
    return f"> [!NOTE]\n> 🤖 {model} {AGENT_MARK} {viewer}\n\n{body}"


def post_comment(owner: str, name: str, number: int, body: str) -> None:
    gh(["pr", "comment", str(number), "-R", f"{owner}/{name}", "--body", body])


def next_wake(report: dict, now: datetime, interval: int) -> float:
    """Sleep the poll interval, or until the earliest known bot retry time if sooner."""
    wake = now + timedelta(seconds=interval)
    for item in report["waiting"]:
        for key in ("retry_at", "until"):
            if item.get(key):
                wake = min(wake, max(ts(item[key]), now + timedelta(seconds=15)))
    return (wake - now).total_seconds()


def watch(args, owner: str, name: str, number: int) -> int:
    lock_dir = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "babysit-pr")
    os.makedirs(lock_dir, exist_ok=True)
    lock = open(os.path.join(lock_dir, f"{owner}__{name}__{number}.lock"), "a+")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.seek(0)
        print(json.dumps({"verdict": "locked", "detail": f"another watcher owns this PR: {lock.read().strip()}"}))
        return EXIT_LOCKED
    lock.seek(0)
    lock.truncate()
    lock.write(f"pid {os.getpid()} since {iso(datetime.now(timezone.utc))}")
    lock.flush()

    deadline = time.monotonic() + args.timeout
    while True:
        pr, viewer = fetch(owner, name, number)
        now = datetime.now(timezone.utc)
        report = evaluate(pr, viewer, now, args.bots, args.ignore_check, args.third_party_triggers)
        to_trigger = [b for b, st in report["bots"].items() if st.get("trigger")]
        if to_trigger and not args.no_trigger:
            for bot in to_trigger:
                log(f"requesting {bot} review on {report['head']} ({report['bots'][bot]['reason']})")
                post_comment(owner, name, number, disclosure(args.model, viewer, BOTS[bot]["trigger"]))
            time.sleep(20)
            continue
        if report["verdict"] != "waiting" or args.once or time.monotonic() >= deadline:
            print(json.dumps(report, indent=1, ensure_ascii=False))
            return exit_code(report)
        time.sleep(max(1, min(next_wake(report, now, args.interval), deadline - time.monotonic())))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def target(p):
        p.add_argument("pr", nargs="?", help="PR number or URL (default: current branch)")
        p.add_argument("-R", "--repo", help="owner/name when PR is a number outside the repo checkout")

    def evaluation(p):
        p.add_argument("--bots", default="coderabbit,codex", help="comma list of review bots to require (coderabbit,codex)")
        p.add_argument("--ignore-check", action="append", default=[], metavar="GLOB", help="check name to ignore after you justified it (repeatable)")
        p.add_argument("--third-party-triggers", action="store_true", help="allow bot review requests on repos you do not own (only when the user asked)")

    def model(p):
        p.add_argument("--as", dest="model", default=os.environ.get("BABYSIT_MODEL", "AI agent"), help="model name for the disclosure header")

    p_status = sub.add_parser("status", help="one read-only evaluation")
    target(p_status)
    evaluation(p_status)

    p_watch = sub.add_parser("watch", help="block until ready / action needed / closed / timeout")
    target(p_watch)
    evaluation(p_watch)
    model(p_watch)
    p_watch.add_argument("--interval", type=int, default=60, help="poll seconds (default 60)")
    p_watch.add_argument("--timeout", type=int, default=3300, help="give up after N seconds with exit 30 (default 3300)")
    p_watch.add_argument("--once", action="store_true", help="evaluate and trigger once, then exit")
    p_watch.add_argument("--no-trigger", action="store_true", help="never post bot review requests")

    p_comment = sub.add_parser("comment", help="post a disclosed PR comment")
    target(p_comment)
    model(p_comment)
    p_comment.add_argument("--body", required=True)

    p_reply = sub.add_parser("reply", help="reply to a review thread with the disclosure header")
    p_reply.add_argument("thread_id")
    p_reply.add_argument("--body", required=True)
    p_reply.add_argument("--resolve", action="store_true", help="resolve the thread after replying")
    model(p_reply)

    p_resolve = sub.add_parser("resolve", help="resolve review threads")
    p_resolve.add_argument("thread_ids", nargs="+")

    args = parser.parse_args()
    try:
        if args.cmd in ("status", "watch"):
            args.bots = [b.strip() for b in args.bots.split(",") if b.strip()]
            unknown = set(args.bots) - set(BOTS)
            if unknown:
                parser.error(f"unknown bots: {', '.join(sorted(unknown))}")
            owner, name, number = resolve_target(args.pr, args.repo)
            if args.cmd == "watch":
                return watch(args, owner, name, number)
            pr, viewer = fetch(owner, name, number)
            report = evaluate(pr, viewer, datetime.now(timezone.utc), args.bots, args.ignore_check, args.third_party_triggers)
            print(json.dumps(report, indent=1, ensure_ascii=False))
            return exit_code(report)
        if args.cmd == "comment":
            owner, name, number = resolve_target(args.pr, args.repo)
            viewer = graphql("query{viewer{login}}")["viewer"]["login"]
            post_comment(owner, name, number, disclosure(args.model, viewer, args.body))
            return 0
        if args.cmd == "reply":
            viewer = graphql("query{viewer{login}}")["viewer"]["login"]
            graphql("mutation($id:ID!,$body:String!){addPullRequestReviewThreadReply(input:{pullRequestReviewThreadId:$id,body:$body}){comment{url}}}", id=args.thread_id, body=disclosure(args.model, viewer, args.body))
            if args.resolve:
                graphql("mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}", id=args.thread_id)
            return 0
        if args.cmd == "resolve":
            for thread_id in args.thread_ids:
                graphql("mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}", id=thread_id)
            return 0
    except GhError as err:
        print(json.dumps({"verdict": "error", "detail": str(err)[:2000]}))
        return EXIT_ERROR
    return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
