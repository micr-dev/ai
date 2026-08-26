---
name: tui-design
description: Design, build, refactor, or review terminal interfaces—full-screen TUIs, interactive prompts, and command-line tools. Use for terminal-app layout and UX, CLI behavior, ncurses-style tools, dashboards, REPLs, fzf-like pickers, and libraries such as Bubble Tea, Ratatui, Textual, or Ink, including requests that name a known TUI such as lazygit, k9s, btop, helix, or yazi instead of saying “TUI.” Do not use for browser or web UI, native GUI, editor or font configuration, or backend and shell work that has no terminal interface.
---

# TUI & CLI Design

Design terminal software that is calm, predictable, fast, and honest about the medium. Treat this file as the workflow and cross-cutting contract. Load detailed guidance from the one reference that owns it instead of reconstructing or repeating it here.

## Route before answering

| Need | Authoritative reference |
|---|---|
| Go, Bubble Tea, Lipgloss, Bubbles, tview, gocui | `references/ecosystem-go.md` |
| Rust, Ratatui, crossterm, Cursive | `references/ecosystem-rust.md` |
| Python, Textual, Rich, prompt_toolkit, urwid | `references/ecosystem-python.md` |
| TypeScript/JavaScript, Ink, OpenTUI, Clack, Inquirer | `references/ecosystem-typescript.md` |
| One-shot commands, arguments, streams, exit codes, automation | `references/cli-basics.md` |
| Layouts, buffers, borders, hierarchy, color, density, responsive behavior, tables, themes, accessibility | `references/visual-patterns.md` |
| Keys, focus, navigation, modes, forms, mouse, confirmation, undo, OSC features | `references/interaction-patterns.md` |
| Case studies: lazygit, k9s, fzf, btop, helix, yazi, atuin | `references/exemplar-apps.md` |
| Screenshots or demo recordings | Use the separate `vhs-cli-demos` skill |

Load only the references the task needs. When the prompt names a framework or ecosystem, always load its ecosystem reference before making API, lifecycle, implementation, or testing claims. Ecosystem references own those specifics. The visual and interaction references own their domains for every ecosystem. Exemplar apps are evidence and inspiration, not substitutes for the pattern references.

If no language is named, ask only when ecosystem choice would materially change the answer or implementation. Otherwise state a reasonable recommendation and proceed: Go for polished single binaries, Rust for control and reliability, Python for rapid product work, and TypeScript when React or npm distribution is already an advantage.

## Classify the product first

Choose the output contract before choosing a framework or layout:

| Product shape | Default contract |
|---|---|
| One-shot CLI | No live full-screen UI. Stable stdout for results, stderr for diagnostics, meaningful exit codes. Load `cli-basics.md`. |
| Summon–choose–exit tool | Prefer inline when shell context matters. Put interactive chrome on stderr or `/dev/tty` and the selected result on stdout. Use full-screen only when a large preview or working set needs stable space. |
| Full-screen session | Use the alternate screen and a stable spatial model. Treat terminal restoration, resize, suspend, and redraw behavior as product requirements. |

Then name the workflow shape—persistent panels, Miller columns, drill-down stack, dashboard, IDE-style panes, overlay, or tabs—and verify it against `visual-patterns.md`. Sketch the states and layout before writing code: initial, loading, empty, partial, success, error, disconnected, and too-small.

## Work the task

1. Classify the product shape and its stdout/stderr contract.
2. Identify the dominant user loop and the 5–8 most common actions.
3. Select the ecosystem and load its reference plus any relevant pattern reference.
4. Sketch the layout and state transitions at wide, standard, narrow, and minimum sizes.
5. Implement in the ecosystem's native architecture; keep state/update/event work separate from rendering where the framework permits.
6. Verify lifecycle cleanup, input discoverability, output behavior, width handling, and async work.
7. Test the cheapest stable layer first, then rendered frames, then a small PTY smoke path only if its integration risk justifies it.

For design questions, make the recommendation before explaining it. For implementation, inspect the existing architecture and dependencies before introducing a new framework or abstraction. For reviews, cite concrete observations and prioritize changes by user harm.

## Preserve these cross-cutting contracts

### Terminal lifecycle

- Use the alternate screen for full-screen sessions; keep bounded and one-shot workflows inline when possible.
- Prefer framework-managed terminal cleanup. Restore raw mode, screen buffer, cursor, and input modes on every exit path, including errors and panics. Do not invent custom signal handling when the framework already owns it.
- Re-layout from the current frame or window size on resize. Coalesce bursts only when layout work is expensive.
- Treat final shutdown and temporary handoff as different boundaries. For an editor, shell, or supported suspend, prefer the framework's handoff API: pause UI input, restore the shell-facing terminal, wait, re-enter modes, reload externally mutable data, and force a full redraw. Redrawing only repaints the current model; it does not refresh changed data. Do not final-unmount an app that must resume, and do not assume POSIX signals exist on Windows.
- Keep logs and debug output away from the screen the TUI owns. Use a file, framework console, or separate diagnostic stream.

### Rendering, data, and performance

- Never block the UI/event thread on disk, network, or subprocess work. Return results through commands, messages, tasks, channels, or framework events.
- Render on input, data, resize, or intentional ticks; do not redraw unchanged state in an unconditional loop.
- Measure terminal cell width, not bytes, code points, `len()`, or JavaScript string length. Test CJK, combining marks, and emoji.
- Virtualize collections that can grow beyond a few hundred rows. Truncate rather than wrap inside tables; reveal full values in a detail view.
- Keep panel positions stable unless the user explicitly changes the layout. Spatial memory is part of navigation.

### Meaning and access

- Define semantic style tokens rather than scattering color literals. Honor `NO_COLOR` in automatic color mode and preserve meaning in monochrome.
- Never use color alone. Pair it with text, shape, position, or symbols, and provide an ASCII fallback when Unicode support is uncertain.
- Make every action keyboard-reachable. Mouse support may accelerate an action but must not gate it.
- Offer familiar navigation aliases only where they do not conflict with text entry or a complete bounded prompt keymap. Preserve terminal-reserved behavior such as interrupt, suspend, and flow control.
- Match discoverability to complexity: complete inline controls for bounded prompts; contextual hints, help, and optionally a command palette for action-rich full-screen apps.
- Provide a plain `--no-tui` or equivalent mode when automation or serious accessibility needs require linear output.

## Apply two review reflexes unprompted

