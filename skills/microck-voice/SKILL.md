---
name: microck-voice
description: Use when intentionally drafting text to be attributed to Microck/JustMicrock/Marcos, including personal messages, public posts, replies, apologies, refusals, praise, boundaries, incidents, or any draft the user asks to be in Microck's voice. Do not use for normal assistant conversation, neutral artifacts, summaries, reports, PRs, commits, or code/docs unless the user explicitly asks for Microck's voice.
---

# Microck Voice

## Mandatory Reference

Before every draft, read the full canonical guide:

`references/voice-guide.md`

Do not draft from memory. The guide contains the evidence, modes, examples,
boundaries, and confidence levels this skill depends on.

## Core Rules

Treat drafting as separate from permission to send. Output drafts only. Do not
send, post, approve, schedule, publish, commit public copy, or imply permission
to send unless the user explicitly gives that separate instruction.

Never invent Microck's opinions, commitments, approvals, deadlines, emotions,
conclusions, ownership, admissions of fault, legal position, medical state,
private facts, or promises. If the source context does not prove it, leave it
out or write a bracketed placeholder.

Match the context before matching the surface style. Casual Discord voice,
public X voice, long-form blog voice, marketplace voice, and professional
messages are different modes. Use the guide to choose the mode.

Do not copy private insults, slurs, shock humor, or aggressive joking into
public or professional drafts. Only use edgy casual mode when the user
explicitly asks for it and the target audience/context is clearly private and
already uses that register.

## Draft Workflow

1. Read `references/voice-guide.md` completely.
2. Identify the target surface, audience, stakes, language, and whether the
   user is asking for a draft or an actual send.
3. Extract only facts supplied in the current request or provided source
   material. Mark unknown facts with placeholders.
4. Choose the voice mode from the guide.
5. Draft in Microck's voice without overpolishing.
6. Briefly note any assumptions or placeholders after the draft when they
   materially affect correctness.

Complete only when the draft uses the selected mode, includes no unsupported
facts or invented stance, marks unknowns as placeholders, and no send, publish,
approval, scheduling, or external action was taken.

## Non-Triggers

Do not use this skill for:

- normal assistant replies to Microck
- code comments, README prose, reports, PR descriptions, or commit messages
  unless the user explicitly says they should sound like Microck
- neutral business or legal text where an institutional voice is safer
- messages written on behalf of someone else
- summaries of Microck's views where no outgoing text is being drafted
