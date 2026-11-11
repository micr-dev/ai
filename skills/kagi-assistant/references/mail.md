# Kagi Mail: search and read

Use this reference for mailbox search and reading messages or threads, not public web research or Assistant conversations. Reuse existing mail access; keep mail content out of web-search queries and external AI services unless the user authorizes that disclosure.

## Access

Mail has its own OAuth credentials. Search API keys and `KAGI_SESSION_TOKEN` do not grant mailbox access. Start with `kagi mail status`, which reports configuration without contacting the service or exposing private settings.

The private Kagi config's `[mail]` section needs the service-supplied `endpoint` and `client_id`. Reuse them rather than guessing endpoints or printing the config. `KAGI_MAIL_ENDPOINT` and `KAGI_MAIL_CLIENT_ID` override those settings. An existing `KAGI_MAIL_ACCESS_TOKEN` is an OAuth bearer-token override, not a Search API key; the CLI does not save or refresh that override. Pass secrets through the existing private configuration, never command arguments.

If access is missing and account setup is authorized, run `kagi mail login` and let the owner complete its verification flow. Login stores OAuth tokens; do not log out, replace credentials or start account setup merely to inspect a skill. Check `kagi mail --help` on the installed version before assuming newer checkout features are available.

## Find and read

```bash
kagi mail boxes
kagi mail search --mailbox Inbox --unread --limit 10
kagi mail search 'contract renewal' --semantic --format toon
kagi mail search 'invoice' --from billing@example.com --after 2026-01-01 --before 2026-02-01
kagi mail read MESSAGE_ID --format pretty
kagi mail read --thread THREAD_ID --new-text-only
```

Use a mailbox path returned by `boxes`, not an assumed translated folder name. Use literal text and sender/subject/date filters for known messages; use `--semantic` for a topic described in natural language. Read returned message IDs before summarizing their content. `read` accepts either one message ID or `--thread`, not both. Threads are oldest first; omit `--new-text-only` when quoted context is necessary.

Search accepts a limit of 1–50 and has no pagination. Narrow dates, sender or topic when the limit is reached; do not call a capped result exhaustive. `--after` is inclusive and `--before` exclusive. Preserve message IDs and relevant dates in findings without exposing unrelated private mail.

## Boundaries

The mail MCP's search/read operations do not send, delete, move or mark messages read, and do not download attachments. The CLI excludes these message responses from its own history and response cache; terminal logs or saved artifacts can still contain private content. Do not claim broader privacy guarantees or save unrelated messages.

Sending or changing account state requires separate authorization and is outside this read-only workflow. A newer source checkout may describe SMTP sending that the installed executable does not expose; this guide does not assume it exists.

Verified against installed `kagi mail`, `search`, `read`, and `login` help plus the local CLI mail documentation. No mailbox was accessed while restoring this reference.
