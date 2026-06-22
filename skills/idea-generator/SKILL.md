---
name: idea-generator
description: Generate concrete, codebase-grounded improvement ideas as an issue-style report. Use when the user asks for improvement ideas, backlog ideas, product or engineering opportunities, roadmap options, codebase opportunities, or mentions idea-generator.
---

# Idea Generator

## Purpose

Use this skill to analyze a repository and generate useful improvement ideas. The output is advisory only: do not edit files, create branches, commit, or open issues unless the user explicitly asks for that follow-up.

This is adapted from the Nightshift `idea-generator` task: options category, medium effort, low risk, issue output, no implementation review loop.

## Quick Start

1. Identify the repository or area the user wants ideas for.
2. Read the relevant code, docs, tests, package metadata, and recent project context.
3. Generate a structured report with prioritized, actionable ideas.
4. Include file paths and line numbers when an idea is grounded in specific code.

## Workflow

1. Scope the scan.
   - If the user names a subsystem, stay inside it unless dependencies reveal a direct impact.
   - If no subsystem is named, sample the main app entry points, public APIs, core domain modules, tests, docs, and configuration.
   - State any material assumptions before analysis if the intended product direction is ambiguous.

2. Look for idea sources.
   - Repeated manual workflows that could become tools, scripts, or UI affordances.
   - Friction in setup, onboarding, testing, debugging, release, or deployment.
   - Features implied by domain models, TODOs, docs, tests, analytics, or error handling.
   - Reliability, observability, performance, accessibility, security, and documentation gaps.
   - Places where current code reveals user needs but the product has no direct workflow yet.

3. Filter ideas.
   - Prefer ideas grounded in existing code or docs over generic wishlist items.
   - Prefer small and medium ideas with clear owner value over speculative rewrites.
   - Do not recommend compatibility bridges, migration shims, or dual behavior unless the user asked for old-state support.
   - Avoid suggesting new dependencies unless the benefit clearly beats the maintenance cost.

4. Report results.
   - Group ideas by priority or theme.
   - For each idea, include evidence, proposed change, expected value, rough effort, and risk.
   - Use severity-style priority labels:
     - P0: urgent correctness, security, data-loss, or outage-prevention opportunity.
     - P1: high-value product, reliability, or workflow improvement.
     - P2: useful quality, maintainability, or ergonomics improvement.
     - P3: opportunistic polish or low-urgency cleanup.
   - If nothing worthwhile is found, say that explicitly and list the areas inspected.

## Output Template

```md
# Idea Generator Report

## Summary
[One paragraph describing the most important opportunities.]

## Ideas

### P1: [Idea title]
- Evidence: [file path:line or observed project signal]
- Proposal: [specific change]
- Value: [who benefits and how]
- Effort: [small | medium | large]
- Risk: [low | medium | high]
- Next step: [first concrete action]

## Areas Inspected
- [paths, docs, tests, commands, or modules reviewed]

## Not Recommended
- [ideas considered and rejected, with short reasons]
```

## Quality Bar

- Ideas must be concrete enough that a developer can turn each one into an issue or small plan.
- Every high-priority idea should cite repo evidence.
- Keep speculation labeled as speculation.
- Keep implementation details light unless the user asks for a plan.
