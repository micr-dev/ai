# Octen

Use mounted Octen tools when their schemas support the operation. Otherwise use the HTTP API with existing secure authentication. There is no assumed `octen` CLI. The configured Octen MCP launcher starts a stdio server; it is not a search subcommand.

## HTTP operations

POST JSON to `https://api.octen.ai` with `Content-Type: application/json` and `X-Api-Key` from existing configuration. Never paste or print the key. Load credentials from the existing secure configuration without displaying them; use the approved HTTP client and configured User-Agent. Do not put secret values in command arguments or artifacts.

| Endpoint | Body example | Use |
| --- | --- | --- |
| `/search` | `{"query":"focused question","count":5,"highlight":{"enable":true,"max_tokens":500}}` | Focused web discovery |
| `/broad-search` | `{"query":"multi-part question","max_queries":3,"search_options":{"count":5,"language":["en"]}}` | Deliberate query expansion |
| `/extract` | `{"urls":["https://example.com/article"],"format":"markdown","mode":"standard"}` | Read known pages |
| `/image-search` | `{"inputs":[{"type":"text","data":"image subject"}],"count":5}` | Text-to-image discovery |
| `/image-search` | `{"inputs":[{"type":"image","url":"https://example.com/reference.png"}],"count":5}` | Reference-image discovery |
| `/video-search` | `{"inputs":[{"type":"text","data":"tutorial subject"}],"count":5,"time_range":"month"}` | Find videos and matching segments |

Consult current endpoint documentation before using additional filters. The old skill package's endpoint contracts are not proof of a live entitlement.

### Extract page links

For outbound citations or discovering pages within a site, use `/extract` with an `include_links` object, not a boolean:

```json
{
  "urls": ["https://example.com/article"],
  "include_links": {"scope": "prefer_external", "max_links": 50}
}
```

`scope` is `prefer_external` for outbound references or `prefer_internal` for same-site links first (the default). These are ordering preferences, not exclusion filters; page order is preserved within each group. `max_links` accepts 1–1000, defaults to 200, and out-of-range values return HTTP 400 rather than being clamped. An empty object uses both defaults.

Returned links contain `url`, `anchor_text` and `is_external`. A discovered link is not extracted evidence: retrieve its target before citing its contents. Use HTTP for this request while the installed MCP adapter omits `include_links`.

## Constraints that change the workflow

- Search query length is limited to 500 characters; result count is 1–100.
- Broad search costs roughly per subquery. Set a bounded `max_queries` for the actual subquestions; up to 30 is supported, but do not use the maximum by default. Results are grouped, not deduplicated across groups.
- HTTP broad-search options are nested inside `search_options`; the MCP broad-search schema flattens filters. Do not copy one payload into the other transport.
- Extraction accepts 1–20 URLs. A `query` requests highlights instead of full body text. Inspect per-result failures and returned content, not just top-level success.
- Default extraction caching is one day; the documented minimum is 300 seconds. Request freshness when necessary and distinguish old cached content from current observations.
- Extraction supports `standard`, `advanced`, and `auto` in the newer HTTP contract. A successful standard extraction can contain only an empty page skeleton. Inspect `page_structure` and actual text before claiming the page was read.
- Image and video search require beta access. A 403 may indicate missing entitlement or balance; do not retry it with broader queries.
- Image input is exactly one text input or one image, never both. Image count is 1–10; base64 input is limited to 5 MB after encoding. Image time filters are ignored by the documented endpoint; do not claim a dated image search succeeded.
- Video input is text-only, count 1–10. Preserve returned segment timestamps; obtain a transcript before claiming what a speaker said.
- UI references with design tokens/snippets remain in `octen-design`, not this general media workflow. Reddit inspection remains exclusively in [Reddit](reddit.md).

## Installed adapter limitations

Inspected MCP version 0.4.1 does not forward extraction `mode` or `include_links`. Its image adapter requires text and combines it with `image_url`, violating the newer single-input contract. Use the HTTP endpoint for those capabilities instead of silently dropping options. Inspect a newly upgraded schema before applying this version-specific warning.

Evidence: installed MCP JavaScript; https://docs.octen.ai and https://github.com/Octen-Team/octen-mcp . HTTP search succeeded on 2026-10-28; other endpoints and beta entitlements were not live-tested in that check.
