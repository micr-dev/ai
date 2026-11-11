# Bounded entity discovery

Use when the user requests a structured list of matching companies, people or products, not pages or a narrative report. Adding fields to an existing list belongs to the retained `parallel-data-enrichment` skill.

Agree on practical scope: geography, date, criteria and match limit. "All" does not prove a provider can enumerate the world. Explain coverage limitations rather than claiming completeness.

## Verified-match workflow

```bash
parallel-cli findall run 'Entities and match criteria' -g core -n 10 --no-wait --json
parallel-cli findall poll FINDALL_ID -o /tmp/topic-entities.json --timeout 540
```

Installed defaults are `core` and 10 matches; supported limits are 5–1000. Use an explicit bounded count appropriate to the request. `pro` is a more expensive generator, not an automatic retry after sparse results. Use `--exclude '[{"name":"Example","url":"example.com"}]'` for known exclusions.

Record `findall_id`; retrieve that run instead of recreating it after a wait timeout. `--dry-run` still calls the ingest API to infer the schema, so it is not an offline validation flag. Follow the host's background waiting policy instead of writing sleep/poll loops.

Read the saved output. Reject query-echo placeholders and missing URLs, and verify each important match criterion against evidence. For company/product identity, prefer its own domain; a directory entry can be a discovery lead but is not proof of the requested attributes. Record excluded/noisy rows and why. Dates, geography and categories need factual verification, not just plausible names.

## Explicit quick preview

For a user-requested rough preview of companies or people:

```bash
parallel-cli findall entity-search 'Criteria' -t companies -n 10 -o /tmp/topic-preview.json
```

This synchronous path supports only `companies` or `people`, no generator, exclusions or enrichment, and results are not individually verified. Its `entity_set_id` cannot be passed to FindAll enrich/extend. Directory/profile links are expected on this path; do not discard them solely for not being the entity's homepage. Still reject empty URLs and query echoes, and verify attributes before presenting them as facts.

Extending an existing full FindAll run or enriching it starts additional work. Do so only within the user's requested scope; inspect the current subcommand help first. Do not silently rerun a preview as a full paid job to obtain unsupported capabilities.

Evidence: installed `findall run --help` and existing provider workflow. No FindAll job was started during consolidation. Parallel credit was unavailable in the live search check.
