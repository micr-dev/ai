---
name: opentui
description: OpenTUI skill for building terminal user interfaces with the Core, React, or Solid APIs. Use for any TUI task including components, layout, keyboard and keymap handling, animations, and testing.
metadata:
   references: core, react, solid, components, layout, keyboard, keymap, animation, testing
---

# OpenTUI Platform Skill

Consolidated skill for building terminal user interfaces with OpenTUI. Use decision trees below to find the right framework and components, then load detailed references.

## Critical Rules

**Follow these rules in all OpenTUI code:**

1. **Use `create-tui` for new projects.** See framework `REFERENCE.md` quick starts.
2. **`create-tui` options must come before arguments.** `bunx create-tui -t react my-app` works, `bunx create-tui my-app -t react` does NOT.
3. **Never call `process.exit()` directly.** Use `renderer.destroy()` (see `core/gotchas.md`).
4. **Text styling requires nested tags in React/Solid.** Use modifier elements, not props (see `components/text-display.md`).

## How to Use This Skill

### Reference File Structure

Framework references follow a 5-file pattern. Cross-cutting concepts are single-file guides.

Each framework in `./references/<framework>/` contains:

| File | Purpose | When to Read |
|------|---------|--------------|
| `REFERENCE.md` | Overview, when to use, quick start | **Always read first** |
| `api.md` | Runtime API, components, hooks | Writing code |
| `configuration.md` | Setup, tsconfig, bundling | Configuring a project |
| `patterns.md` | Common patterns, best practices | Implementation guidance |
| `gotchas.md` | Pitfalls, limitations, debugging | Troubleshooting |

Cross-cutting concepts in `./references/<concept>/` have `REFERENCE.md` as the entry point.

### Reading Order

1. Start with `REFERENCE.md` for your chosen framework
2. Then read additional files relevant to your task:
   - Building components -> `api.md` + `components/<category>.md`
   - Setting up project -> `configuration.md`
   - Layout/positioning -> `layout/REFERENCE.md`
   - Keyboard/input handling -> `keyboard/REFERENCE.md`
   - Layered keybindings/commands -> `keymap/REFERENCE.md`
   - Animations -> `animation/REFERENCE.md`
   - Troubleshooting -> `gotchas.md` + `testing/REFERENCE.md`

### Example Paths

```
./references/react/REFERENCE.md           # Start here for React
./references/react/api.md              # React components and hooks
./references/solid/configuration.md    # Solid project setup
./references/components/inputs.md      # Input, Textarea, Select docs
./references/core/gotchas.md           # Core debugging tips
```

### Runtime Notes

OpenTUI runs on Bun and uses Zig for native builds. Read `./references/core/gotchas.md` for runtime requirements and build guidance.

## Quick Decision Trees

### "Which framework should I use?"

```
Which framework?
├─ I want full control, maximum performance, no framework overhead
│  └─ core/ (imperative API)
├─ I know React, want familiar component patterns
│  └─ react/ (React reconciler)
├─ I want fine-grained reactivity, optimal re-renders
│  └─ solid/ (Solid reconciler)
└─ I'm building a library/framework on top of OpenTUI
   └─ core/ (imperative API)
```

