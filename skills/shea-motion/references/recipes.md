# Recipes

Tool-agnostic recipes for the `shea-motion` principles. Frames at 30 fps; values are starting points. Curves refer to the table in `SKILL.md`. Each recipe lists what to animate; the §Tool mapping at the end says where that lives in common tools.

## Motion

### Chained camera glide (subject to subject)
One continuous camera travels from subject to subject: logo → feature 1 → feature 2 → CTA.
1. Lay subjects out in one space (a large 2D canvas or 3D scene), not as separate screens.
2. Drive the camera through a chain of parents (one transform per move), each child nested in the previous. One move per transform keeps paths and speed graphs clean.
3. Move 1: push in ~15 f onto the first subject, camera S-curve.
4. Moves 2…N: start each 5 f before the previous one lands; 15 f each; same curve. Land each arrival on a beat.
5. Orbits: one parent with rotation instead of a chain.

### Impact + ambient shake
- **Hit:** high frequency (~6–7 Hz-like jitter), amplitude peak on the beat (in px, ≈1–2% of frame width), decaying to 0 over 6–8 f, stiff curve. Weight the axis matching the move (horizontal slide → X, zoom → scale/Z).
- **Ambient:** low frequency (~2.5–3), small amplitude, slight rotation (~0.08°–1°), spanning the scene, decaying to a floor of ~20% of its start. Never zero.
- **Momentum carry:** if the hit dies early and the tail goes still, add a small rise (~1–4% of peak) on the last frame into the cut.
- Fill edges the shake exposes by mirroring/scaling up ~3–5%.
- Product/UI videos: halve the amplitudes; readability of UI text wins.

### Speed ramps and dead-frame removal
- Screen recordings and product footage hold still between actions: cut the holds, or ramp speed fast–slow–fast (speed-ramp curve) so only the key moment plays slow.
- Compress an action into a 3–4 f burst for punch; restore one in-between frame if the move becomes unreadable ("one-framer rule"); add one frame before a hit if it feels stroby.

### Stepped frame rate
Hold frames to 12 fps (10, 8 for rougher; 15 for subtle) on selected scenes for a snappy, hand-made feel. Apply per scene, not globally; keep it off smooth camera glides and UI scrolling.

### Background drift
The last global pass: a slow wiggle over the whole piece (≈1 cycle/s, ≈12 px at 1080p) so nothing ever sits perfectly still.

## Type and shapes

### Typewriter with hold
Reveal characters over ~10–15 f, hold fully visible long enough to read, then remove (reverse or cut on a beat). Randomized character order turns it into a decode/glitch reveal.

### Per-character jitter
Offset each character's Y by a random 0–7 px, re-randomized every 2–3 f (stepped, not smooth): stop-motion boil that keeps held text alive.

### Text on a circle
Repeat a word 8–10× along a circular path and rotate slowly: badges, orbits, frames around a product shot.

### Shape morph sequence on beats
One rectangle carries a whole sequence: slit (scale X 2% → 100% over 14–16 f) → bar → square on beat 4 (morph curve) → one-frame color swap on beat 5 (hold interpolation) → collapse → stroke "portal" outro. Put the secondary deformation on a parent so each property has one motion phase.

### Line draw-ons with flicker heads
Draw stroke paths 0→100% with the line curve; the frame the stroke finishes, flicker the arrow/tip opacity 100↔0 over 2–4 f. For thick filled arrows, reveal with a directional wipe whose angle follows the arrow's bends instead of stroke trimming.

## Color and texture

- **Build color per scene**, changing the color story by section; one flat global grade tires the eye.
- **Grayscale buffer:** between clashing palettes, pass through a desaturated scene or frames.
- **Priming:** a 1-frame flash of the next section's hue several seconds before the shift.
- **Palette remap:** duotone/gradient-map footage to the brand palette for "controlled chaos" sections.
- **Monochrome anchor:** in sections cycling many hues, keep one neutral element constant.
- **Contrast intro:** open a scene crushed/dark and ease to normal over ~15–30 f (glide curve); best when there is a clear highlight (screen glow, logo light).
- **Exposure flash across a cut:** brighten to near-white starting ~4 f before the cut, peak on it, decay 2–3× longer than the attack. Reserve for key hits.
- **Texture glue:** grain (visible, not subtle, on flat vector type), a fine dot/LED grid masked to highlights, animated "boiling" noise on shapes, posterized tones, paper/film textures in soft-light/screen/overlay. Subtle 4-point gradients inside a single hue keep fills from looking flat.
- **Master flicker:** a faint global luminance flicker ties differently styled scenes together.

### Blend-mode transitions
The incoming scene overlaps the outgoing one on a layer above.
- **Slow/melodic:** overlap several beats, opacity 0→100% with the crossfade curve, mode difference/hard-light/soft-light.
- **Fast:** overlap only 4–5 f before the beat, hard light, duplicated for density; hard-cut the outgoing.
- **Light hit:** one frame in screen mode right before the full cut, then an exposure landing on frame 1.
Screen/add for light sources, multiply for dark textures, overlay/soft light for texture.

## Transitions and impact

### One-framers (every cut)
1–2 frame accents at cuts, drops, snares. The arrangement and contrast matter more than the effect:
- Bright: white or accent-color solid, or exposure up.
- Dark: crushed contrast frame.
- Pattern: dark → bright → dark around the cut. Use 2 f if 1 f vanishes in playback or sits on a sustained sound.
- White flashes over bright scenes, black over dark ones.
- Pair a flash with a scale punch-in (~105–110%) on the same frame.

### Cut blurs
- **Clip-start softener:** blur ~15 px at the first frame after a cut → 0 by the end, post-cut decay curve.
- **Zoom transitions:** radial/zoom blur over 4 f centered on the cut, 8 / 16 / 16 / 8.
- **Slides:** directional blur over 4 f in the slide direction, 8 / 18 / 18 / 8.
- **Build-up:** blur rising into a big transition, then decaying from peak after it.
- Keep blur moderate; heavy values turn frames to mud.

### Wipe reveals (collage, stickers, feature cards)
- Direction is physically motivated: grounded objects reveal from the floor up; hanging ones top down; tilted assets at their tilt.
- Bracket the beat: start 3–6 f before, end 2–4 f after, so peak velocity hits the transient. Wipe curve.
- Stagger elements; wiggle or drift them after landing so the layout never freezes.
- Pixel/dot-matrix wipes for digital looks; step the frame rate to 12 fps for a cutout feel.

### Physical re-record
Play the finished section full-screen and film it with a handheld camera, flicking the wrist toward the subject. Real motion blur and lens artifacts unify everything.

## Compositing checklist

Work in order per scene: **Assets** (few, clean) → **Colors** (sampled palette) → **Textures** → **Effects** (one global force) → **Assessment** (pacing, readability, spelling/kerning, one-framers placed).

## Time-boxed

- Commit to one sentence of design intent before starting; judge every idea against it.
- Take the first idea that fits; cap effect browsing at ~2 minutes per look.
- Shorten the track: cut long builds and splice into the release on a downbeat.
- Spend time on: cut placement on transients, flash frames, stagger rhythms (2-2-2-hold), camera movement. Skip: fine grading of short scenes, perfect cleanup no one sees at speed.
- Hold section contrast together with one persistent unifier (border frame, hero hue, or texture).
- Afterward, list what took longest and what landed best; carry both into the next piece.

## Tool mapping

| Concept | After Effects | Remotion / React | Motion Canvas | CSS / Web Animations | Rive / Figma / Jitter | NLE (Premiere/Resolve) |
|---|---|---|---|---|---|---|
| Custom curve | Graph Editor / Flow | `Easing.bezier(...)` in `interpolate` | `easeInOutCubic` or custom timing fn | `cubic-bezier(...)` | Custom bezier on keyframe | Bezier keyframe handles |
| Camera chain | 3D camera parented to nulls | nested transform `<div>`s / R3F camera | nested `Node` transforms | nested wrappers with transforms | nested groups | nested sequences + transform |
| Shake | S_Shake / wiggle expression | `noise2D` from `@remotion/noise` × decay | `noise` signals | JS noise → transform | noise modifier / manual keys | transform keys or shake plugin |
| One-framer | 1-frame adjustment layer / solid | `<Sequence durationInFrames={1}>` | 1-frame `waitFor` + fill | step keyframe | hold keyframe | 1-frame clip |
| Stepped fps | Posterize Time | `Math.floor(frame / 2.5) * 2.5` (30→12) | stepped time | `steps()` | frame-rate setting | frame-hold / optical-flow off |
| Blur | Gaussian / Radial / Directional | CSS `filter: blur()` / canvas | `filters.blur` | `filter: blur()` | blur effect | Gaussian/directional blur |
| Blend modes | layer modes | `mix-blend-mode` | `compositeOperation` | `mix-blend-mode` | layer blend | composite mode |
| Grain / texture | Add Grain, Noise | SVG `feTurbulence` / video overlay | noise shader | SVG filter / overlay | image overlay | film grain / overlay clip |

Sources: Shea5Editing *Editing Outlines* 1–5, *AE Essentials* 1–10, *Aimless Edits* 1–3 (https://www.youtube.com/@Shea5Editing). AE-specific depth: the `ae-edit-style` skill.
