---
name: dft-writing
description: Generate long-form prose with Deft Writing through direct API calls. Use when the user asks for DFT writing, Deft Writing, Distribution Fine-Tuning prose, or article/blog/document drafts with a target word count.
---

# DFT Writing

## Overview

Use `scripts/dft_write.py` to call the current Deft Writing API at `https://deftwriting.com/api/generate`. Do not use browser automation unless the API contract has changed and direct calls fail.

## Quick Start

```bash
python3 scripts/dft_write.py \
  --prompt "Write a concise article about how urban libraries help communities learn practical technology skills." \
  --outline "- Public computer access for residents\n- Workshops for common software and job applications\n- Trusted local staff who can answer follow-up questions" \
  --style "Clear, informative" \
  --use-case "Short blog post" \
  --words 300
```

Use `--mode rewrite` with `--rewrite-instructions` when the input is an existing draft to revise. Omit `--mode` for new prose.

## Input Shape

- `prompt`: Ask for a long-form article, blog post, explanation, or document. This is not a chat model, so avoid conversational Q&A prompts.
- `outline`: Prefer bullets or section headings. Keep each bullet descriptive, ideally at least 5 words.
- `style`: Tone and writing style, such as `Clear, informative`, `Inquisitive, Analytical, Conversational`, or `Advocacy, Urgent, Ethical`.
- `use-case`: Intended context, such as `News Article`, `Academic Article`, `Advocacy Document`, `Short blog post`, or `None`.
- `words`: Approximate output length. This is prompt steering, not a hard API parameter. The live API has produced 1800+ words when asked for a 1600-word article.
- `allow-emdash`: Default false. Leave false unless the user explicitly asks to allow em dashes.

The API chooses chunk count from the prompt and can be slow for long drafts. Expect about 1 minute for short output and several minutes for 1500+ words.

## API Contract

Read `references/api-contract.md` before changing the client. The current direct API path is:

- `POST https://deftwriting.com/api/generate`
- New draft mode: `generationMode: "simple"`
- Rewrite mode: `generationMode: "rewrite"`

The retired `https://dft.rosmine.ai/` Gradio API redirects to `https://deftwriting.com` and is not the canonical path.

## Proxy Use

The free API tier tracks quota per source IP and is frequently exhausted on shared datacenter ranges (Oracle Cloud, AWS, GCP). On those hosts a direct call returns `{"error":"free_generations_exhausted"}` (HTTP 403) even though the same request succeeds from a residential or Mullvad exit IP. When the user asks to run DFT "through a proxy" or "via mullgate", route the request through a Mullvad exit.

The script is stdlib `urllib`, so it honors the standard proxy env vars. Set them in the same shell as the call:

```bash
HTTPS_PROXY="socks5h://se:1234@0.0.0.0:1180" \
HTTP_PROXY="socks5h://se:1234@0.0.0.0:1180" \
python3 scripts/dft_write.py --prompt "..." --json
```

On this machine the canonical proxy path is Mullgate, whose WireGuard-backed listeners sit at:

- SOCKS5: `socks5h://<selector>:1234@0.0.0.0:1180`
- HTTP:   `http://<selector>:1234@0.0.0.0:8180`

The `<selector>` chooses the Mullvad exit (e.g. `se`, `se-got`, `es`, `es-mad-wg-101`). Inspect live selectors with `mullgate proxy access`.

Fallback when Mullgate's WireGuard tunnels are down: the Mullvad exit nodes are also reachable through Tailscale as `*.mullvad.ts.net`. Tailscale tunnels over TCP/DERP and bypasses the UDP-to-Mullvad-relay block seen on some hosts (notably Oracle Cloud Ashburn, where UDP handshakes to every Mullvad WG port return no reply). To use it, set the host exit node before the call and clear it after:

```bash
tailscale set --accept-dns=true --exit-node se-got-wg-003.mullvad.ts.net --exit-node-allow-lan-access=true
python3 scripts/dft_write.py --prompt "..." --json
tailscale set --exit-node=
```

List available Mullvad Tailscale exits with `tailscale exit-node list | grep -i mullvad.ts.net`. Verify the egress before the call with `curl -sS https://ipv4.am.i.mullvad.net/json` (expect `mullvad_exit_ip: true`). Always restore the prior exit-node setting when done.

Verify the proxy cleared the 403 before running a long job: a short `--words 20` probe costs almost nothing and confirms the route has quota.

## Examples

Generate a longer article:

```bash
python3 scripts/dft_write.py \
  --prompt "Write a detailed article about how small engineering teams should design reliable internal tools." \
  --outline "- Scope control\n- Observability\n- Clear ownership\n- Failure handling\n- Documentation" \
  --style "Practical, concrete, plainspoken" \
  --use-case "Engineering blog post" \
  --words 1600 \
  --json
```

Rewrite an existing draft:

```bash
python3 scripts/dft_write.py \
  --mode rewrite \
  --prompt-file draft.md \
  --rewrite-instructions "Make this clearer and more direct while preserving every factual claim." \
  --style "Clear, concise" \
  --json
```

## Output Handling

Return the generated prose directly when the user asked for text. If the output needs editing, preserve the user's requested intent and use normal writing/editing judgment after generation.

If the service is slow, say the upstream generation is still running and long drafts can take several minutes. If it errors, report the HTTP status or API error and do not invent DFT output.
