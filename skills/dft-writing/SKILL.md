---
name: dft-writing
description: Generate long-form prose with the Rosmine DFT Writing Demo through direct Gradio API calls. Use when the user asks to use dft.rosmine.ai, Distribution Fine Tuning, DFT writing, or wants article/blog/document prose generated from a prompt, outline, style, use case, and target token length without browser automation.
---

# DFT Writing

## Overview

Use the API client in `scripts/dft_write.py` to call the public Gradio backend for `https://dft.rosmine.ai/`. Do not use browser automation unless the API contract has changed and needs to be rediscovered.

## Quick Start

```bash
python3 scripts/dft_write.py \
  --mode fast \
  --prompt "Write a concise article about how urban libraries help communities learn practical technology skills." \
  --outline "- Public computer access for residents\n- Workshops for common software and job applications\n- Trusted local staff who can answer follow-up questions" \
  --style "Clear, informative" \
  --use-case "Short blog post" \
  --tokens 300
```

Use `--mode good` when quality matters and the user can tolerate a slower request. Use `--mode fast` for drafts, quick probes, or when the service is under load.

## Input Shape

- `prompt`: Ask for a long-form article, blog post, explanation, or document. This is not a chat model, so avoid conversational Q&A prompts.
- `outline`: Prefer bullets or section headings. Keep each bullet descriptive, ideally at least 5 words.
- `style`: Tone and writing style, such as `Clear, informative`, `Inquisitive, Analytical, Conversational`, or `Advocacy, Urgent, Ethical`.
- `use-case`: Intended context, such as `News Article`, `Academic Article`, `Advocacy Document`, `Short blog post`, or `None`.
- `tokens`: Approximate output length from 100 to 1000, rounded to the nearest 100.
- `allow-emdash`: Default false. Leave false unless the user explicitly asks to allow em dashes.

The combined prompt, outline, style, use case, and wrapper prompt must stay under the app's approximate 1024-token limit. If the API returns a length warning, shorten the outline first.

## API Contract

Read `references/api-contract.md` before changing the client. The current direct API path is:

- `POST https://dft.rosmine.ai/gradio_api/run/predict`
- Fast generation: `fn_index: 7`
- Good generation: `fn_index: 6`
- Examples: `fn_index: 14`, `15`, and `16`

The app hides named endpoints, so call by `fn_index`. The `/gradio_api/call/<id>` path can fail for these hidden endpoints; use `/gradio_api/run/predict`.

## Examples

Fetch the app's canonical examples:

```bash
python3 scripts/dft_write.py --example 1 --json
python3 scripts/dft_write.py --example 2 --json
python3 scripts/dft_write.py --example 3 --json
```

The examples show the intended prompt style: a topical question or directive, followed by a compact factual outline, a style string, a use-case string, and a target length.

## Output Handling

Return the generated prose directly when the user asked for text. If the output needs editing, preserve the user's requested intent and use normal writing/editing judgment after generation.

If the service is slow, say that the upstream demo is hosted on slower GPUs and may take about a minute. If it errors, report the HTTP status or API error and do not invent DFT output.
