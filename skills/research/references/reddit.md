# Reddit research

Use `reddit-mcp-buddy` for all Reddit post/comment inspection, subreddit browsing, searches and user activity. General web search can discover thread URLs, but it does not replace reading the threads through this server.

## Workflow

1. Define the topic, date range and relevant communities. For discovery, use Kagi or another ordinary engine with `site:reddit.com`, or the MCP's `search_reddit` directly.
2. Inspect the strongest relevant threads with `get_post_details`. Pass the full URL when available; a bare post ID can require an extra subreddit lookup.
3. Compare multiple discussions and dates. Distinguish the post's claim from commenters' experiences. Upvotes and karma measure reception, not expertise or factual truth.
4. Cite direct post/comment links and dates. State sampling and community bias; verify factual claims against primary sources outside Reddit.

## MCP calls

Read the mounted tool schema before calling it. Current tool names:

```json
{"name":"search_reddit","arguments":{"query":"TOPIC","subreddits":["SUBREDDIT"]}}
{"name":"get_post_details","arguments":{"url":"REDDIT_POST_URL"}}
{"name":"browse_subreddit","arguments":{"subreddit":"SUBREDDIT","sort":"top","time":"month"}}
{"name":"user_analysis","arguments":{"username":"USERNAME"}}
{"name":"reddit_explain","arguments":{"term":"TERM"}}
```

Use subreddit names without `r/` and usernames without `u/`. Leave result/comment limits at their defaults unless the user requests different limits. Inspected defaults: search/browse 25, comment limit 20, depth 3, top comments 5, user posts/comments 10 each. Do not inflate all limits merely to appear thorough.

## When MCP tools are not mounted

The configured server launches with:

```bash
node <reddit-mcp-buddy-install>/dist/cli.js
```

This is an MCP stdio server, **not** a CLI accepting `search_reddit` as a subcommand. Use an MCP client to send `initialize`, then `notifications/initialized`, then `tools/list` and `tools/call`. Transport is newline-delimited JSON-RPC. A tools/call request uses the same name/arguments object shown above:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"research","version":"1"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_post_details","arguments":{"url":"REDDIT_POST_URL"}}}
```

Wait for each response before the dependent request; match IDs, handle JSON-RPC errors, and close the child process when done. Use the mounted schema or `tools/list` response rather than assuming examples remain complete forever.

Reuse existing authentication. The server checks its environment and its configured credential store; do not print, copy or export those credentials. Its local rate limiter varies by authentication mode and does not guarantee Reddit's current limits. Let the server handle throttling; report authentication/transport/access failures instead of switching to direct Reddit HTTP, Firecrawl, Scrapling or another scraper.

Evidence: installed the installed Reddit MCP source and `src/core/auth.ts`; live MCP initialize/tools-list on 2026-10-28 returned server version 1.1.12 and all five tools. Content retrieval was not tested by that capability check.
