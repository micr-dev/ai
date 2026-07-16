# AI Stack Showcase

This context describes the public page for presenting Microck's current AI working setup and the changes to that setup over time. The current stack is the authoritative snapshot; the changelog explains how that snapshot has changed.

## Language

**Stack Showcase Page**:
The fully public page titled `AI Stack` and hosted at `ai.micr.dev` that presents the current AI stack as the primary experience and its recent evolution as supporting context. On desktop, the changelog is slightly narrower on the left and the stack is slightly wider on the right. The changelog area scrolls independently with its scrollbar on the left edge, while the stack area remains fixed in the viewport with dense content handled by internal scroll regions. On mobile, the current stack appears before the changelog and a compact sticky text navigator provides direct access to both regions. The page and its OG image use text directly on a dark background and avoid visible boxes, cards, or panel containers except for AGENTS.md. Content renders immediately without a page-load reveal sequence. Motion stays subtle and purposeful: historical snapshots crossfade, modal surfaces share a short symmetric scale-and-fade transition, and small state changes may use quick fades.
_Avoid_: Dashboard, landing page, card layout, boxed layout

**Stack Entry**:
A single structured public item in the stack, such as a model, harness, MCP, skill, CLI tool, or supporting workflow tool. A **Stack Entry** may have an optional canonical link, optional description of what it is, optional reason for why it is used, and optional metadata such as a version or date when useful. On the page, optional description, reason, and metadata appear as quiet secondary text rather than as visibly labeled fields. Linked entries reveal a small link icon to the right on hover or focus.
_Avoid_: Card, tile, resource

**MCP**:
A tool integration exposed to a harness through the Model Context Protocol.
_Avoid_: CLI tool

**Active MCP**:
An **MCP** configured for the current operator environment and not explicitly disabled. Active MCPs may be listed publicly by name, but credentials, tokens, host secrets, and environment values must never appear on the Stack Showcase Page.
_Avoid_: Installed MCP, available MCP

**CLI / Local Tool**:
A direct operator tool used from the local environment.
_Avoid_: MCP

**Skill Label**:
A subtle low-emphasis label used inside the Skills section, such as `Handmade` or `Favorite`.
_Avoid_: Skill section, category

**Skill Interaction**:
A skill with a committed public source file opens that source in the read-only skill dialog. A skill without a committed public source file opens its canonical upstream GitHub location as a link instead of presenting fallback or partial dialog content.
_Avoid_: Empty skill dialog, fallback description dialog

**Gatekept Skill**:
A **Stack Entry** in the Skills section whose name and purpose may be shown publicly, while the underlying prompt, private rubric, or implementation details remain unpublished.
_Avoid_: Hidden skill, secret skill

**Image Generation**:
The stack section for the preferred image generation model or workflow. It is separate from the Models section, which focuses on coding and chat models.
_Avoid_: Model subsection

**Workspace**:
The stack section for the surrounding working environment, such as terminal tools, remote access, networking, agent surfaces, and machine context. Machine specs may appear as tooltip detail, but provider and location do not belong here.
_Avoid_: Other, Supporting Environment

**Primary**:
The editorial role for a model or harness that most commonly aligns with being the default, most-used, and strongest current choice. It is assigned intentionally, not inferred from metrics.
_Avoid_: Main

**Secondary**:
The role for a model or harness that supports the current workflow but is not the default choice.
_Avoid_: Backup, fallback

**Change Entry**:
A dated structured public note describing a stack or workflow change that already happened, including small operational tweaks. Every **Change Entry** has a date, may include an optional why, may include an optional description, and may optionally refer to related **Stack Entries**. On the page, optional why and description text appears as quiet secondary text rather than as visibly labeled fields.
_Avoid_: Release note, highlights post

**Chronological Setup History**:
The evidence-backed changelog for the current operator stack. Dates should come from `Microck/cli-backup` commit history or other checked local artifacts; when exact adoption timing is uncertain, the page should describe the first observed backup snapshot rather than inventing a precise adoption event.
_Avoid_: Placeholder timeline, fictional history

**Change Group**:
A date-grouped set of **Change Entries** shown under one `DD/MM/YYYY` date header in the changelog.
_Avoid_: Timeline card, terminal log

**Stack Snapshot**:
The reconstructed public stack immediately after a selected **Change Group**. A snapshot replays additions, removals, replacements, and version transitions so its visible entries reflect that date rather than merely hiding recently added items from the current stack. When a removal has no recorded introduction, the item appears only in the immediately preceding observable snapshot instead of being projected backward without evidence.
_Avoid_: Filtered current stack, URL-only snapshot

**AGENTS.md**:
The committed public, redacted rendering of the global `AGENTS.md` file. It keeps the original structure and tone while omitting sensitive or machine-specific details, and its user-facing section label is exactly `AGENTS.md`. It appears as a constrained raw code preview, with a read-only modal overlay that renders the content as readable markdown. AGENTS.md is the only content area allowed to use a visible boxed treatment.
_Avoid_: Agent Operating Manual, Prompt, system prompt, policy dump

## Example Dialogue

Dev: "Should the Stack Showcase Page include every local skill?"

Domain expert: "No. Each Stack Entry should be something intentionally presented as part of the current public stack."

Dev: "Are models and harnesses the same kind of entry?"

Domain expert: "No. Models and harnesses are separate sections, even when a harness description mentions its usual model pairing."

Dev: "Which stack sections should lead the current stack?"

Domain expert: "Models come first, followed by Harnesses, followed by AGENTS.md."

Dev: "Are hooks part of the Harnesses section?"

Domain expert: "No. Hooks are presented as their own stack section."

Dev: "Are MCPs and CLI tools the same section?"

Domain expert: "No. MCPs are harness integrations, while CLI / Local Tools are direct operator tools."

Dev: "Should handmade skills and favorite skills be separate sections?"

Domain expert: "No. Skills are one section, with smaller low-opacity labels when useful."

Dev: "Should image generation live under Models?"

Domain expert: "No. Image Generation is its own stack section."

Dev: "Where should terminal apps, networking, agent surfaces, and machine context go?"

Domain expert: "They belong in Workspace."

Dev: "How should Primary and Secondary model or harness entries be presented?"

Domain expert: "Show Primary entries on the left and Secondary entries on the right, with explicit text labels."

Dev: "Should the changelog only include major stack changes?"

Domain expert: "No. A Change Entry can capture small operational tweaks as long as they are intentionally public."

Dev: "How should Change Entries appear in the changelog?"

Domain expert: "Group them by date, with bold change titles and optional smaller details below a title."

Dev: "Should sections be visually boxed?"

Domain expert: "No. The page should read as text on a dark background, without visible boxes, cards, or panel containers. AGENTS.md is the only exception."

Dev: "Can interactions fade elements in or out?"

Domain expert: "Yes, when the fade is quick, restrained, and makes state changes easier to follow."

Dev: "Should the AGENTS.md section be rewritten as marketing copy?"

Domain expert: "No. It should read like the raw operating manual, with redactions where public exposure would be unnecessary or risky."
