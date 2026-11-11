# Parallel search and extraction

Ordinary `search` and `extract` do not start narrative deep-research jobs. Use objective-driven search when several keyword queries contribute to one question.

```bash
parallel-cli auth --json
parallel-cli search 'Find official documentation and limitations for TOPIC' \
  -q 'site:example.com TOPIC docs' -q 'site:example.com TOPIC limits' \
  --mode basic --max-results 5 --excerpt-max-chars-total 12000 \
  --json -o /tmp/topic-search.json
parallel-cli extract 'https://example.com/first' 'https://example.com/second' \
  --objective 'Find the relevant limits' --full-content \
  --full-content-max-chars 40000 --json -o /tmp/topic-pages.json
```

Read the saved JSON when terminal output truncates. Pass each URL separately, at most 20 per extraction. Extraction objectives have a 5,000-character limit.

## Controls

- Search modes: `turbo`, `basic`, `advanced`. Start with `basic`; use the current command help to choose a different mode for a concrete need, not as automatic escalation.
- Domain controls: repeat `--include-domains` / `--exclude-domains` or pass comma-separated values. Combined maximum: 200 domains.
- Search freshness: `--after-date YYYY-MM-DD`; geography: `--location us`.
- Search and extraction accept `--max-age-seconds`, `--timeout-seconds`, and `--disable-cache-fallback`. The documented minimum max age is 600 seconds. Use the last flag when stale fallback would invalidate the answer.
- `--no-excerpts` strips excerpts locally; it does not stop V1 from producing them server-side.
- Optional `--session-id` groups related calls; `--client-model` identifies the consuming model.

## Access and failure

`PARALLEL_API_KEY` overrides saved credentials. `parallel-cli auth --json` reports credential sources without exposing their values. Control-API account operations require additional OAuth access; a working search key does not establish that access.

On credit or authentication errors, report the exact condition. Do not purchase credit, initiate login or create repeated jobs automatically. During 2026-10-28 verification, live search failed for insufficient credit, although installed syntax was verified.

For entity lists read [Entity discovery](entities.md). For deep research requested by the user or warranted by the task, read [Starting deep research](deep-research.md#starting-deep-research). Keep bulk enrichment and recurring monitors in `parallel-data-enrichment` and `parallel-monitor`.

Evidence: installed parallel-cli 0.8.2 command definitions and executed search/extract/research help; https://docs.parallel.ai/integrations/cli .
