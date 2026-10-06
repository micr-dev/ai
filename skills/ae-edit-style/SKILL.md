---
name: ae-edit-style
description: After Effects edit-style (anime/AMV, music-synced) craft from Shea5Editing's tutorials. Use when planning, building, critiquing, or teaching an AE edit — movement and dead frames, graph/easing, pacing to music, shakes, blurs, impact, 3D camera, text, shape layers, color, lighting, blend modes, wipes/transitions, compositing, or a time-boxed edit workflow.
---

# AE edit style

Distilled from Shea5Editing's *Editing Outlines* (1–5), *AE Essentials* (1–10), and *Aimless Edits* (1–3). The principles below apply to every edit; exact recipes and values live in `references/`.

## Principles

- **Every frame moves.** A frame where the subject is static is a *dead frame*, even if the background pans. Cut it or compress it out before any effect goes on.
- **Graphs sit in the middle.** Replace default F9 easing on every keyframe. Handles live between the walls: enough tension to punch, enough tail that the effect lingers across the shot. Stiff graphs for close keyframes and hard hits; loose graphs for ambient motion and long decays.
- **Non-zero floor.** Ambient shake, drift, and decays end above zero and carry momentum into the cut; the shot never settles.
- **Two shakes.** A short aggressive impact shake over a low-frequency ambient shake that runs the whole shot.
- **Hits land on the beat.** Peak values (blur, shake, exposure, flash) sit on the audio transient; decays span to the next cut.
- **Sampled palette.** Colors are eyedropped from hero assets; competing backgrounds are desaturated; accents are varied, never uniform.
- **One force unifies.** A shared camera move, shake, blur, or texture across all layers makes separate assets read as one image.
- **Readability scales with duration.** Short shots (~10 frames) carry little; long shots carry the full stack.

## Workflow

1. **Clean motion** — strip dead frames; Twixtor smooth motion, time-remap explosive action. → `motion-and-timing.md`
2. **Pace to music** — lay cuts and speed ramps on the beat structure. → `motion-and-timing.md`
3. **Movement layer** — 3D camera moves, shakes, blurs, impact frames. → `camera-text-shapes.md`, `shakes-impact-blur.md`
4. **Graphics** — text and shape layers. → `camera-text-shapes.md`
5. **Look** — color, lighting, blend modes, textures. → `color-light-blending.md`
6. **Joins** — wipes and transitions; composite with the five-pillar checklist. → `transitions-compositing.md`
7. **Assess** — play back at full speed; every shot moves, every hit lands, text reads, one-framers placed.

Done when every shot passes step 7. Time-boxed or constraint-driven edits follow `references/fast-edit-workflow.md` instead of this order.

## References

Read the file for the step in hand; each is self-contained.

- `references/motion-and-timing.md` — dead frames, Twixtor vs time remap, graph/Flow curves, pacing, Posterize Time.
- `references/shakes-impact-blur.md` — S_Shake systems, blurs, flashes, impact frames.
- `references/camera-text-shapes.md` — 3D camera rigs, text animation, shape layers.
- `references/color-light-blending.md` — creative color, lighting effects, blend modes.
- `references/transitions-compositing.md` — wipes, compositing checklist, textures.
- `references/fast-edit-workflow.md` — 90-minute and random-constraint edit process.

## Tooling

Recipes name third-party tools; mark them to the user and offer the built-in fallback when one is missing: Twixtor (RE:Vision), Sapphire (Boris FX: S_Shake, S_DissolveShake…), BCC (Boris FX Continuum), Flow (easing panel; fallback: Graph Editor), FX Console (search; fallback: Effects & Presets).
