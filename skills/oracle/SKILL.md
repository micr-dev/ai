---
name: oracle
description: "Oracle CLI browser workflow for ChatGPT, with a direct recovery path for model picker but no prompt submit."
---

# Oracle (CLI) — browser recovery workflow

This skill keeps `--engine browser` and `--model gpt-5.6-sol` as default behavior.

## Non-negotiable defaults

- Engine: `browser`
- Model: `gpt-5.6-sol`
- Thinking time: `--browser-thinking-time heavy`
- Manual login: keep enabled unless you explicitly approve turning it off
- Do not switch model/provider unless the operator approves a change

## Fast fix when picker loads but prompt never submits

If you see picker UI for `GPT-5.6 Sol` but Oracle marks a run as failed and `promptSubmitted:false`, run these exact steps.

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
oracle --engine browser --model gpt-5.6-sol \
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
oracle --engine browser --model gpt-5.6-sol \
  --browser-inline-cookies-file /tmp/chatgpt-inline-cookies.json \
  --browser-manual-login-profile-dir /home/ubuntu/snap/chromium/common/oracle-browser-profile \
  --browser-model-strategy ignore \
  --force -p "Reply with exactly: setup ok" \
  --write-output /tmp/oracle-setup-check.md
```

`ignore` is a safe temporary fallback when picker state is flaky.

## Standard run command

```bash
oracle --engine browser --model gpt-5.6-sol \
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
