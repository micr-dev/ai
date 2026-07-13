---
name: authormist
description: Connect to the Yoga Windows host and operate the installed AuthorMist model. Use when the user wants to rewrite text with AuthorMist, run AuthorMist remotely, verify its installation, or troubleshoot its Yoga runtime.
---

# AuthorMist

Operate the quantized AuthorMist installation on the Yoga Windows host. Probe
first: do not assume the laptop is online, the path is unchanged, or a prior
model process is healthy.

## Installed Runtime

- Tailscale device: `yoga` (Windows 11 ARM64)
- Runtime root: `%LOCALAPPDATA%\AuthorMist`
- Launcher: `%LOCALAPPDATA%\AuthorMist\bin\authormist.cmd`
- Model: `%LOCALAPPDATA%\AuthorMist\models\authormist-originality.i1-Q4_K_M.gguf`
- Engine: native Windows ARM64 llama.cpp
- Quantization: Q4_K_M

The launcher opens conversational mode. A validated baseline on Yoga is about
17 tokens/second, but current load and prompt length affect performance.

## Connect From This Ubuntu Host

The existing Crabbox provider file owns Yoga connection metadata. Never print,
copy, commit, or include its credential in output. Read values silently into
shell variables and pass the password through `SSHPASS`, not argv:

```bash
provider="$HOME/.config/crabbox/hyperv-yoga-provider.sh"
yoga_host=$(sed -n 's/^YOGA_HOST="\(.*\)"/\1/p' "$provider")
yoga_user=$(sed -n 's/^YOGA_USER="\(.*\)"/\1/p' "$provider")
yoga_pass=$(sed -n 's/^YOGA_PASS="\(.*\)"/\1/p' "$provider")

SSHPASS="$yoga_pass" sshpass -e ssh \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o ConnectTimeout=15 \
  "$yoga_user@$yoga_host" '<command>'
```

Keep these variables only for the current operation. Run
`unset yoga_pass yoga_host yoga_user` immediately after the final SSH command.

Before use, run `tailscale status` and require the `yoga` Windows peer to be
online. Then probe without loading the model:

```powershell
$root = Join-Path $env:LOCALAPPDATA "AuthorMist"
Test-Path (Join-Path $root "bin\authormist.cmd")
Test-Path (Join-Path $root "models\authormist-originality.i1-Q4_K_M.gguf")
Get-Process llama-cli -ErrorAction SilentlyContinue
```

The connection step is complete only when Yoga is online, SSH succeeds, and
both path probes return `True`.

## Use Interactively

On Yoga, open a new PowerShell or Command Prompt so the user PATH is current:

```powershell
authormist
```

Paste the text and request a rewrite. Use `/clear` between unrelated texts and
`/exit` when finished.

From this Ubuntu host, reuse the secure connection variables above and request
a TTY:

```bash
SSHPASS="$yoga_pass" sshpass -e ssh -tt \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  "$yoga_user@$yoga_host" \
  'cmd.exe /d /s /c "%LOCALAPPDATA%\AuthorMist\bin\authormist.cmd"'
```

Do not claim a rewrite succeeded until the model emits non-empty text and the
session exits cleanly or remains available for the user's next prompt.

## Use Non-Interactively

For agent-driven use, send one prompt followed by `/exit` over stdin. Keep user
text out of command arguments:

```bash
prompt_file=$(mktemp)
chmod 600 "$prompt_file"
trap 'rm -f "$prompt_file"' EXIT
printf '%s\n/exit\n' "$prompt" > "$prompt_file"

SSHPASS="$yoga_pass" sshpass -e ssh -T \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  "$yoga_user@$yoga_host" \
  'cmd.exe /d /s /c "%LOCALAPPDATA%\AuthorMist\bin\authormist.cmd"' \
  < "$prompt_file"

rm -f "$prompt_file"
trap - EXIT
unset yoga_pass prompt
```

Treat llama.cpp banners, timing lines, and prompts as transport output, not
rewritten content. Preserve the generated wording exactly unless the user asks
for another editorial pass.

## Troubleshoot

1. If Yoga is absent or offline in `tailscale status`, stop and report that
   reachability is the blocker. Do not modify Crabbox VMs.
2. If SSH fails, use the existing provider metadata and report the exact SSH
   error without exposing credentials.
3. If the launcher is missing, inspect `%LOCALAPPDATA%\AuthorMist\bin`; do not
   redownload until the model path and free disk have also been checked.
4. If a stale `llama-cli` process holds memory, identify it before stopping it.
   Stop it automatically only when it belongs to the current failed run.
5. If inference fails, capture the runtime error, available RAM, model size,
   and model SHA-256. The expected model hash is
   `a0fbacfe77df68d08dc03191a48cddcb82b46f2e5599ac31dbf6b0a91d824542`.

Troubleshooting is complete only when inference succeeds or one concrete
external blocker is identified with the failed probe that proves it.
