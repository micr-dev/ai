# Writing rules for framework files

Every framework file is read by agents. Apply these on every edit.

- **App-agnostic.** No app names, domains, PR numbers, agent names, or dates as content. Generalize the incident into the rule; a short "Why:" clause may name the generalized failure.
- **Positive target first.** State what to do. Prohibitions only as hard guardrails, paired with the positive target.
- **Leading words.** Reuse the framework's terms (*evidence ladder*, *owner blocker*, *deploy truth*, *fail-closed*, *lesson*). Define a new one once, in the doc that owns it.
- **Single source of truth.** One home per rule. Elsewhere, link to it by relative path.
- **Replace, do not layer.** When a rule is wrong or stale, rewrite it. Delete sediment.
- **Verify at use.** Prices, fees, limits, guideline numbers, tool versions, and legal thresholds carry "verify at use" plus a primary-source URL, and "verified YYYY-MM" when checked.
- **Behavior test.** Each line must change what a competent agent would do by default. Cut lines that do not.
- **Style.** Dense bullets and tables. No em dashes. No emojis.
- **Pointers.** A new doc needs one line in `AGENTS.md` that front-loads when to read it.
