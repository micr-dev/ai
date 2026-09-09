---
name: oracle
description: "Oracle CLI browser workflow for ChatGPT, with a direct recovery path for model picker but no prompt submit." 
---

# Oracle (CLI) — browser recovery workflow

This skill keeps `--engine browser` and the active ChatGPT thinking-effort state as the default behavior. Do not rely on `gpt-6-astra` label matching to select GPT-6 Pro.

## Non-negotiable defaults

- Engine: `browser`
- Model selection: `--browser-model-strategy current` when the signed-in ChatGPT tab already has `6 Pro` / `Pro thinking` active
- Thinking effort: select the top `6 Pro` step in ChatGPT's slider; do not assume a CLI model ID selects it
- Manual login: use only when refreshing the profile interactively
- Do not switch model/provider unless the operator approves a change

## Installed CLI verification

Before a real run, verify the installed Oracle version and flags with `oracle --version` and `oracle --help`. Oracle `0.16.1` accepts `gpt-6-astra` as a model string in dry-run output, but that is not proof that ChatGPT selected GPT-6 Pro. A valid attachment is also required. `Missing file or directory` is a local preflight failure and means no browser prompt was submitted.

The live browser path was verified with the protected inline-cookie file:

```bash
oracle --engine browser \
  --browser-model-strategy current \
  --browser-inline-cookies-file /home/ubuntu/.oracle/chatgpt-inline-cookies.json \
  --browser-attachments never \
  --file /absolute/path/to/existing-file \
  -p "<task>"
```

A browser run without inline cookies failed with `No ChatGPT cookies were applied from your Chrome profile`.

## GPT-6 Pro is a thinking-effort level

GPT-6 Pro is real and is selected as the top `6 Pro` step in ChatGPT's thinking-effort slider. It is not necessarily exposed as a distinct model-picker label or model ID. Oracle label matching can therefore fail even when the browser consult is valid.

When the browser directly accepts the prompt with `Pro thinking` active, treat the consult as submitted and real. The answer remains in the ChatGPT conversation even if Oracle later reports a local timeout or state error. Verify browser/session evidence before declaring failure, and do not retry with a different model merely because label matching failed.

For CLI defaults, keep `--browser-model-strategy current` when the browser is already on the `6 Pro` effort level. Do not claim that `gpt-6-astra` selected Pro unless the ChatGPT UI confirms it.

## Browser login and recovery

The installed Oracle `0.16.1` can use the protected inline-cookie file with `--browser-inline-cookies-file`. Use it for authenticated browser runs. Do not print or expose the cookie contents.

If picker matching fails, first inspect the browser itself. If the prompt was accepted and `Pro thinking` is active, the consult succeeded. If the prompt was not accepted, retry with the active tab preserved:

```bash
oracle --engine browser \
  --browser-model-strategy current \
  --browser-inline-cookies-file /home/ubuntu/.oracle/chatgpt-inline-cookies.json \
  --browser-attachments never \
  --file /absolute/path/to/existing-file \
  -p "<task>"
```

## Standard run command

```bash
oracle --engine browser --browser-model-strategy current \
  --browser-inline-cookies-file /home/ubuntu/.oracle/chatgpt-inline-cookies.json \
  --browser-attachments never \
  -p "<task>" \
  --file "src/**"
```

## Deep Research run command

Use the same authenticated path and add `--browser-research deep`:

```bash
oracle --engine browser --browser-model-strategy current \
  --browser-research deep \
  --browser-inline-cookies-file /home/ubuntu/.oracle/chatgpt-inline-cookies.json \
  --browser-attachments never \
  -p "<research task>" \
  --file "src/**"
```

Verify `researchMode: deep`, `promptSubmitted: true`, and the completed browser session before reporting success.

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
