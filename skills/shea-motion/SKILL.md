---
name: shea-motion
description: Motion-design craft for launch, showcase, product, and promo videos, in any tool (AE, Remotion, Motion Canvas, Rive, CSS/JS, Figma, Premiere/Resolve). Use when planning, animating, pacing to music, or critiquing a motion graphics video.
---

# Shea motion

Edit-style craft from Shea5Editing's tutorials, translated for motion graphics: the **subject** is the product, UI, logo, or message; **shots** are scenes or screens. Timings are in frames at 30 fps (×2 at 60 fps; 1 f ≈ 33 ms). Recipes and tool mappings live in [`references/recipes.md`](references/recipes.md).

## Principles

- **Every frame moves.** A *dead frame* is one where the subject is static, even if the background drifts. Static screenshots, held logos, and pauses while text sits there are dead frames; give each one a push-in, drift, parallax, or cut it.
- **Curves sit in the middle.** Every keyframe pair gets a deliberate cubic-bezier from the curve table below; default ease and linear read robotic. Handles sit between the walls: enough tension to punch, enough tail that the motion lingers. **Stiff** curves for hits and close keyframes; **loose** curves for ambient motion and long decays.
- **Non-zero floor.** Ambient drift, shake, and glow decay to a small residual, never to zero, so each scene carries momentum into the cut.
- **Two layers of motion.** A short sharp *hit* (6–8 f) on top of a slow *ambient* motion that runs the whole scene.
- **Hits land on the beat.** Map the track first. Peaks (scale punch, flash, blur, shake) land on the transient; decays run to the next cut. Eased arrivals decelerate, so start the move before the beat and nudge 1 f earlier if it lands late.
- **Fast, slow, fast, slow.** Pace by contrast: bursts of equal-length 1–3 f micro-cuts into a hit, then multi-beat anchor scenes with clear exit motion. Pace inside a scene too — fire events (flash + punch-in, swap, reveal) without cutting.
- **Overlap hand-offs.** The next move starts before the previous one lands (≈5 f overlap on a 15 f move), so the camera never stop-starts.
- **Cascade, never clone.** Elements entering together stagger by a few frames; copy the hero curve, then offset and vary. Identical timing on every layer reads flavorless.
- **Sampled palette.** Eyedrop colors from the hero asset (product, brand mark, UI accent); desaturate or neutralize competing backgrounds; 1–2 vivid hues per frame against black, white, or gray; vary accent distribution.
- **One force unifies.** A shared camera move, shake, blur, grain, or texture across all layers makes separate assets read as one image.
- **Readability scales with duration.** A ~10 f scene carries one subject, one line of text, one accent; a multi-second scene carries the full stack. Text holds long enough to read aloud once.

## Curve table

Recorded curves, usable directly as `cubic-bezier()` / bezier handles:

| Use | Curve | Feel |
|---|---|---|
| Camera / scene glide between subjects | `0.67, 0.04, 0.16, 0.99` | balanced S, long soft landing |
| Wipes, reveals snapping in on a hit | `0.67, 0.04, 0.28, 0.99` | hard in/out, snaps into place |
| Shape morphs, scale bursts | `0.90, 0.00, 0.10, 1.00` | explosive, snappy stop |
| Line draw-ons, strokes | `0.25, 0.08, 0.26, 0.94` | softer, even |
| Crossfade that spikes on the beat | `0.75, 0.05, 0.90, 0.98` | stays low, jumps at the end (avoids mid-fade mush) |
| Speed ramp (fast–slow–fast) | `0.25, 0.00, 0.25, 1.00` | plateau in the middle |
| Post-cut blur/glow decay | `0.15, 0.99, 0.27, 0.98` | front-loaded drop, gentle tail |

Tune per shot; these are starting points, not presets to paste everywhere.

## Workflow

1. **Map the audio** — mark sections (intro, build, drop/main, outro), downbeats, and trailing accents. Done when every planned hit has a marker.
2. **Over-collect assets** — gather ≥2× the shots/screens/type you will use, sorted into establishing, hero/feature, fast fragments, and anchor scenes with exit motion.
3. **Block the cut** — place scenes on markers following fast/slow contrast; intro beat 1 = establish, beat 2 = hero reveal.
4. **Motion pass** — camera glides, hits + ambient layers, cascades, curves from the table. → `recipes.md` §Motion
5. **Graphics pass** — type, shapes, lines, UI callouts. → `recipes.md` §Type and shapes
6. **Look pass** — palette, lighting/flashes, blend and texture. → `recipes.md` §Color and texture
7. **Joins** — transitions and one-framers at every cut. → `recipes.md` §Transitions and impact
8. **Assess** — play at full speed, then step frame by frame. Done when every scene has no dead frames, every marker carries a hit, all text reads, and each cut has a join.

For time-boxed work, follow the triage in `recipes.md` §Time-boxed.

## Critique

When reviewing someone's video, walk the Principles as a checklist and name the frame range and fix for each miss.
