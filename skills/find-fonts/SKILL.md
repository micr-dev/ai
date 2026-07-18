---
name: find-fonts
description: Scout fonts from a design brief and return a license-checked shortlist.
disable-model-invocation: true
---

# Find fonts

Scout toward a decision. A useful search ends with a font that fits the work and can legally ship, not a pile of attractive links.

## 1. Frame the brief

Extract these constraints from the request:

- use case and intended reading size
- sample text, tone, and visual references
- required scripts, languages, glyphs, weights, and styles
- desktop, print, web, app, logo, or other delivery context
- open-source or commercial preference, budget, and intended license owner

Ask one focused question only when a missing answer could reverse the shortlist, especially the use case, required script, or license scope. Otherwise state the working assumptions and continue.

Complete this step when every hard constraint is explicit and no known ambiguity can invalidate the search.

## 2. Search broadly

Start with `moji` so local font discovery and acquisition use one verified path:

```bash
moji "<compact family or style query>" --json --max 12
```

Add `--format`, `--weight`, or `--provider` only when the brief requires them. Run several meaningfully different queries when the brief describes a style rather than a known family. Search by category, proportions, contrast, mood, and historical model instead of repeating synonyms.

For a known family or exact match, preview the resolved file without downloading it:

```bash
moji get "<family and weight>" --dry-run
```

For paid, boutique, brand, logo, or independently drawn type, or when `moji` produces a weak field, read [references/foundry-sources.md](references/foundry-sources.md). Use current web search for discovery, then read the primary foundry page for any candidate that survives.

Complete this step with at least eight plausible candidates from at least two independent sources, unless the user requested an exact family.

## 3. Verify finalists

Narrow to three to five candidates, then verify each on its official source:

- designer or foundry and canonical family name
- available formats, weights, italics, optical sizes, and variable axes
- required language, script, and glyph coverage
- license scope, price, restrictions, and who must own the license
- a specimen using the user's text at approximately the intended size

Treat "free to try," a public download, and an open-source license as different claims. Confirm the actual terms for the intended desktop, web, app, logo, trademark, or client use. Mark an unavailable fact as `unconfirmed` and link the foundry contact or license page. Conversion between font formats does not grant a new license.

For web work, require WOFF2 or a licensed source file that can be converted. Distinguish text and display cuts, reject missing real weights or italics, and prefer a complete family when the design needs a durable type system. When pairing is requested, pair for contrast and rarely recommend more than three families.

Complete this step only when every finalist satisfies every hard constraint, or the remaining exception is visible as `unconfirmed`.

## 4. Decide and report

Rank candidates by fitness for the actual use case, not general popularity. Compare legibility, personality, distinctiveness, family completeness, language coverage, technical fit, and licensing cost. Name one recommendation and one runner-up, with the tradeoff between them.

Use this structure:

```markdown
**Brief**
[Constraints and stated assumptions]

**Shortlist**

| Rank | Family | Why it fits | Coverage and files | License and price | Official source |
| --- | --- | --- | --- | --- | --- |

**Recommendation**
[Best choice, runner-up, and the decisive tradeoff]

**Open questions**
[Only unresolved facts that could still block use, or "None"]
```

Complete the search when the shortlist is source-linked, license status is explicit, and the recommendation follows from the brief.

## 5. Acquire only when requested

Keep a search request read-only. When the user also asks to obtain a font, preview the exact download first:

```bash
moji get "<family and weight>" --dry-run
```

Then download to the requested directory with `moji get`. Prefer WOFF2 for web delivery and OTF or TTF for desktop work. If conversion is needed, confirm that the license permits the intended web use before running `moji convert`.

Complete acquisition only after reporting the downloaded file path and confirming it opens as the requested family, weight, style, and format.
