# Keenable

Use Keenable first for ordinary web search while the configured free allowance remains. Keep specialist routes in [Providers](providers.md) for news/image verticals, code, Reddit and deep research. The allowance motivates this preference; it does not establish better coverage or accuracy.

## Search and read

Inspect `keenable search --help` or `keenable fetch --help` before unfamiliar options. Default output is YAML. Describe the page you want, such as official documentation, release notes or an outage postmortem. Start with 3–5 results and bounded snippets; broaden only for a named evidence gap.

```sh
keenable search 'official Python asyncio documentation' --site docs.python.org --max-results 3 --snippet-max-length 500
keenable fetch 'https://docs.python.org/3/library/asyncio' --live
```

Search results contain `title`, `url`, `snippet`, `acquired_at` and optional `published_at`. Acquisition time is not publication time. Follow relevant URLs and verify the requested software version; one search can return several versions of the same documentation.

Use publication filters for publication dates and acquisition filters for index dates. Publication filters exclude pages without a known publication date, so avoid them when that would hide relevant documentation. With `--query-time`, use absolute date boundaries: relative filters still count from now, not from the historical query time. This option selects an older index view, not recent results, and can require Time Machine entitlement. Historical index availability does not prove a subsequently fetched page contains its historical text.

The search modes `pro` and `realtime` are retrieval modes, not hosted deep-research jobs. Choose `realtime` when latency matters; do not infer freshness from its name. Configured forced mode can override the command flag.

Fetch returns Markdown under `content`; check `truncated` before treating it as complete. `--live` bypasses the cached copy. An unindexed page also triggers live retrieval and the `fetch.live` SKU without that flag. `--prompt` returns LLM-directed extraction instead of the full page, so omit it when gathering primary-source text. Use raw readers for code, JSON and exact bytes, and the dedicated Reddit workflow for Reddit content.

## Access and allowance

The CLI reads its saved key from its private configuration, protected with mode `0600`. Reuse it without printing the file or passing the key in command arguments. Do not run login, logout or MCP configuration as an incidental research step. Anonymous access uses a shared IP pool and is not a replacement for exhausted account quota.

Use the existing free allowance only; purchased-credit use, top-ups and billing changes need explicit approval. Inspect each response's `usage`: `credits` is the call's cost, `paid` identifies free versus purchased credits, and `credits_remaining` combines both balances. The remaining balance can lag concurrent calls or be omitted. It is not proof of free credits remaining, and `paid: false` describes only the completed call, not the next one.

Before bulk work or when the free balance is uncertain, verify the free allowance separately in the console and budget for concurrent use and the operation's cost. If free-only usage cannot be established, pause Keenable calls rather than make a potentially paid probe. Stop and report unexpected `paid: true`; an after-the-call check cannot prevent that first charge.

Keenable's default data policy stores queries, fetched URLs, fetch prompts and results. Keep secrets, personal data and private URLs out of requests. Do not assume this organization has zero data retention.

For errors, follow [Recover before replacing](deep-research.md#recover-before-replacing). Stop on `402 insufficient_credits` rather than retry or buy credits. On `429`, honor `Retry-After` and bound retries. For `403 time_machine_not_enabled`, report the missing entitlement; remove `--query-time` only if historical scope is not required. A coverage gap can justify another index, but duplicated search results are not independent evidence.

## Structured research

[SELECT](https://docs.keenable.ai/select.md) is a separate MCP service for SQL over web searches and model-extracted fields. It is not installed by this CLI setup. Before adopting it, establish authenticated pricing and free-allowance coverage, then obtain authorization for the separate integration. Verify extracted claims against sources; model extraction does not fact-check them.

## Installation and sources

Installed with `brew install keenableai/tap/keenable-cli`; update with `brew upgrade keenable-cli`. Keep provider-specific details here rather than copying the vendor skill into the main research router.

Sources: [best practices](https://docs.keenable.ai/best-practices.md), [credits](https://docs.keenable.ai/credits.md), [data policy](https://docs.keenable.ai/data-privacy.md), [errors](https://docs.keenable.ai/errors.md), [fetch](https://docs.keenable.ai/products/fetch.md), and installed 0.4.0 command help. The vendor documents 100,000 free requests per month; use the console's free-allowance breakdown rather than the combined API balance when establishing a free-only budget.
