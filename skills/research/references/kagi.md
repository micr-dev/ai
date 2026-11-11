# Kagi

Use focused search for finding sources, extraction for reading them, and generated answers only as leads to verify. Inspect `kagi <command> --help` before adding options not shown here.

```bash
kagi auth status
kagi search 'site:docs.example.com exact topic' --limit 5 --format json
kagi search 'topic' --region us --time month --order recency --format json
kagi search 'topic' --from-date 2026-01-01 --to-date 2026-06-30 --format json
kagi search 'topic' --news --time week --limit 5 --format json
kagi search 'image subject' --images --limit 5 --format json
kagi extract 'https://example.com/article' --format markdown
kagi extract 'https://example.com/article' --format json
```

Installed help verifies `--images`; it uses subscriber-session authentication, not the paid search API. `extract --format json` retains link metadata. Use an HTTPS URL.

For distinct subquestions, `kagi batch 'query one' 'query two' --format toon --limit 5` batches searches. `kagi quick 'question' --format markdown` returns a generated cited answer. `kagi search 'topic' --follow 3` summarizes the first three results; summaries are not exact source text. `kagi news` and `kagi smallweb` are separate discovery feeds; inspect their help for supported categories and output controls.

## Page questions and transformations

Choose the operation by the requested output, not by whichever credential is available:

| Need | Command | Authentication |
| --- | --- | --- |
| Source text for quotations or factual verification | `kagi extract URL` | Current `KAGI_API_KEY` |
| Summary of supplied URL or text | `kagi summarize --subscriber` | Subscriber session |
| Focused question about one supplied page | `kagi ask-page URL QUESTION` | Subscriber session |
| Translation of supplied text | `kagi translate TEXT --to LANGUAGE` | Subscriber session |

```bash
kagi summarize --subscriber --url 'https://example.com/article' --summary-type keypoints
kagi summarize --subscriber --text 'Text to summarize'
kagi ask-page 'https://example.com/article' 'What evidence supports the main claim?'
kagi translate 'Bonjour tout le monde' --to en
```

The installed `ask-page` accepts positional URL/question arguments, without `--format`. Translation uses positional text and `--to`, not the archived `--text`/`--target-language` syntax. State the target language and preserve code, URLs and product names that must remain unchanged.

Use `ask-page` for a single-source question; use search when outside evidence or comparison is needed. Summaries and generated answers do not replace extracted source passages for exact quotations or consequential claims. Do not silently replace extraction with a summary when API access is unavailable.

Public-API summarization is a separate paid path using legacy `KAGI_API_TOKEN`: `kagi summarize --url 'https://example.com/article'`. Prefer subscriber mode when available; use the API only when the task requires its engine controls or that paid path is authorized. Keep private supplied text within the user's authorized service scope.

## Access and constraints

- Reuse the existing config/session. Environment credentials override configuration. Never print the config or credential values to diagnose access; use `kagi auth status`, then `kagi auth check` if a request fails.
- Subscriber-session and API authentication have different capabilities. Quick Answer, news search, image search and some filters require the subscriber session. Extraction uses `KAGI_API_KEY`, not the old `KAGI_API_TOKEN` name.
- A lens index belongs to this user's account; do not copy another user's index. Search supports `--snap`, `--lens`, domain query operators and `--verbatim` where the selected vertical allows them.
- News search conflicts with lenses, snaps, explicit date bounds, personalization, verbatim, follow and templates; it also rejects the year window and tracker ordering.
- Avoid `--local-cache` when a question depends on current prices, outages, policies or release state.
- Assistant threads, attachments, model selection and AI allowance belong to the retained `kagi-assistant` and `kagi-ai` skills. Scheduled/bulk Kagi operations belong to `kagi-monitoring`. Choose a research assistant's deep mode using the shared [deep-research selection criteria](deep-research.md#starting-deep-research).

Evidence: installed `kagi search --help` and `kagi extract --help`; source and CLI documentation at https://github.com/Microck/kagi-cli . Live focused search verified 2026-10-28.
