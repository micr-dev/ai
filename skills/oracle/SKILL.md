---
name: oracle
description: "Oracle CLI browser workflow for ChatGPT, with a direct recovery path for model picker but no prompt submit."
---

# Oracle (CLI) — browser recovery workflow

This skill keeps `--engine browser` and `--model gpt-6-astra` as default behavior.

## Non-negotiable defaults

- Engine: `browser`
- Model: `gpt-6-astra`
- Thinking time: `--browser-thinking-time heavy`
- Manual login: use only when refreshing the profile interactively; prefer the protected inline-cookie file for agent runs
- Do not switch model/provider unless the operator approves a change

## GPT-6 Pro is a thinking-effort level

GPT-6 Pro is real and is selected as the top `6 Pro` step in ChatGPT's thinking-effort slider. It is not necessarily exposed as a distinct model-picker label or model ID. Oracle label matching can therefore fail even when the browser consult is valid.

When the browser directly accepts the prompt with `Pro thinking` active, treat the consult as submitted and real. The answer remains in the ChatGPT conversation even if Oracle later reports a local timeout or state error. Verify browser/session evidence before declaring failure, and do not retry with a different model merely because label matching failed.

For CLI defaults, keep `gpt-6-astra` as the model identifier and `--browser-thinking-time heavy` as the setting that requests the top Pro effort level.

## Persistent security-key login

The Oracle browser profile cannot receive a physical USB security key through VNC. Authenticate to ChatGPT with the security key in a local browser, export the `chatgpt.com` cookies, and store the protected export at:

```text
/home/ubuntu/.oracle/chatgpt-inline-cookies.json
```

Use the cookie file for agent runs. Do not add `--browser-manual-login` when using it, because that flag intentionally skips cookie import and waits for an interactive profile login:

```bash
oracle --engine browser --model gpt-6-astra \
  --browser-inline-cookies-file /home/ubuntu/.oracle/chatgpt-inline-cookies.json \
  --browser-model-strategy current \
  --force -p "<task>"
```

Refresh the file when ChatGPT invalidates the session cookies. Keep it mode `600` and never print its contents.

## Fast fix when picker or label matching fails before prompt submission

If Oracle cannot match a `6 Pro` label, do not infer that GPT-6 Pro is unavailable. Check whether the browser directly accepted the prompt and shows `Pro thinking` first. Only run the recovery steps below when the prompt was not accepted.

### 1) Turn a browser-exported ChatGPT cookie dump into Oracle inline cookies

```bash
python - <<'PY'
import json
from pathlib import Path

src = Path('/path/to/chatgpt-cookie-export.json')
out = Path('/tmp/chatgpt-inline-cookies.json')

with src.open() as f:
    data = json.load(f)

# most exports are object with "cookies" array
cookies = data['cookies'] if isinstance(data, dict) and 'cookies' in data else data
out.write_text(json.dumps(cookies, separators=(",", ":")))
print(out)
PY
```

### 2) Enable cookie sync in Oracle config (keeps manual login profile unchanged)

```bash
python - <<'PY'
import json
p = '/home/ubuntu/.oracle/config.json'
cfg = json.loads(open(p).read())
b = cfg.setdefault('browser', {})
b['manualLogin'] = True
b['manualLoginCookieSync'] = True
# keep this pointing at your signed-in Chromium profile
b['manualLoginProfileDir'] = '/home/ubuntu/snap/chromium/common/oracle-browser-profile'
open(p, 'w').write(json.dumps(cfg, indent=2) + '\n')
print('updated', p)
PY
```

### 3) Verify one minimal call using the same profile + inline cookies

```bash
oracle --engine browser --model gpt-6-astra \
  --browser-inline-cookies-file /tmp/chatgpt-inline-cookies.json \
  --browser-model-strategy current \
  --browser-manual-login \
  --browser-manual-login-profile-dir /home/ubuntu/snap/chromium/common/oracle-browser-profile \
  --force -p "current" \
  --write-output /tmp/oracle-setup-check-current.md
```

If this succeeds, continue with your normal command style.

### 4) Use this exact fallback until stable

```bash
oracle --engine browser --model gpt-6-astra \
  --browser-inline-cookies-file /tmp/chatgpt-inline-cookies.json \
  --browser-manual-login-profile-dir /home/ubuntu/snap/chromium/common/oracle-browser-profile \
  --browser-model-strategy ignore \
  --force -p "Reply with exactly: setup ok" \
  --write-output /tmp/oracle-setup-check.md
```

`ignore` is a safe temporary fallback when picker state is flaky.

## Standard run command

```bash
oracle --engine browser --model gpt-6-astra \
  --browser-inline-cookies-file /home/ubuntu/.oracle/chatgpt-inline-cookies.json \
  --browser-thinking-time heavy \
  -p "<task>" \
  --file "src/**"
```

## Session checks for hard failures

```bash
# latest sessions + key runtime flags
for s in $(ls -1t ~/.oracle/sessions 2>/dev/null | head -n 10); do
  echo "--- $s"
  jq -r '"status=" + (.status // "") + " | desiredModel=" + (.browser.config.desiredModel // "") + " | promptSubmitted=" + ((.browser.runtime.promptSubmitted // false) | tostring) + " | tabUrl=" + (.browser.runtime.tabUrl // "")' \
    ~/.oracle/sessions/$s/meta.json
 done
```

A blocked run often shows:

- `status=error`
- `promptSubmitted=false`
- `tabUrl=https://chatgpt.com/`

## Config and profile sanity checks

```bash
cat /home/ubuntu/.oracle/config.json
ls -la /home/ubuntu/snap/chromium/common/oracle-browser-profile/Default | head
```

If you need a non-picker baseline run (no picker selection), use `--browser-model-strategy ignore`.
