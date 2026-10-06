# Transitions & Compositing

Covers wipe-based reveals for collage/sticker scenes (Linear Wipe, Sapphire pixel/dot wipes) and the five-pillar compositing checklist (assets, colors, textures, effects, final assessment) that makes layered elements read as one image. Read when animating PNG/graphic entrances or when a scene looks like "stuff stacked on footage".

Sources: How To Use The Best Wipe Effects In After Effects (AE Essentials 8) — https://youtu.be/FaVcflIKs5M · Compositing Is Easier Than You Think (Editing Outlines 5) — https://youtu.be/bnkgyFRVjTU

Marking: **[built-in]** = native AE; **[3P]** = third-party plugin/extension. Effects in both videos are applied through FX Console (`Ctrl+Space`, type a fragment like `linear`, `s_wipe`, `wipepi`, `posterize`, `gaus`) [3P, Video Copilot]; the menu paths below work without it.

---

## Part 1 — Wipe reveals

### Shared wipe rules (apply to every wipe below)

- **Match the wipe direction to the asset.** Direction must be physically motivated:
  - Grounded character standing on a baseline → reveal upward from the floor (Linear Wipe `Wipe Angle 180°`).
  - Overhead / floating graphic → reveal downward from the top (Sapphire `Angle 270°`).
  - Tilted graphic → set the angle parallel to the asset's tilt (e.g. `10°` for a slightly counter-clockwise-tilted window). Eyeball or read the layer's Rotation; test a rough value (≈30°) then refine.
  - Circular/rotating graphic → horizontal sweep from one side is fine (demo: right→left).
- **Keyframe only the visible range of completion.** Scrub the completion slider until the art is *just* fully hidden and keyframe that value (demo: `76%`, not 100%). The revealed keyframe is the value where the art is *just* fully visible (demo: `10–13%`, or `0%` depending on orientation). Every percent beyond those bounds is dead frames where the effect runs on nothing.
- **Bracket the beat.** Start keyframe 3–6 frames *before* the beat marker, end keyframe 2–4 frames *after*, so the curve's peak velocity lands on the transient. Never start the wipe on the beat.
- **Ease hard.** Linear keyframes read robotic. Flow [3P, Zack Lovatt & render.tom, v1.4.2] curve for wipes: `cubic-bezier(0.67, 0.04, 0.28, 0.99)` [visual] — aggressive ease-in/ease-out that snaps into place on the hit. Select keyframes → set curve in Flow → **Apply**.
  - Scripting: see motion-and-timing.md §3f.
- **Anti-uniformity.** Never reveal several graphics on the same frame, and never paste identical spacing + identical curves onto every layer — cloned graphs look stiff and "flavorless".
  - Copy the keyframes/curve from the hero layer, then shift each secondary layer's start a few frames later so they cascade across beats and in-between frames.
  - Nudge the bezier tension per layer so arrival speeds differ slightly.
- **Choosing the wipe type:**
  | Wipe | Use on |
  | --- | --- |
  | Linear Wipe [built-in] | Characters, grounding elements, solid dividers, chunky shapes — clean directional slice |
  | S_WipePointalize [3P, Sapphire] | Circular / tech / retro-pop-art elements (CDs, vinyl, round icons) — halftone dot edge |
  | S_WipePixelate [3P, Sapphire] | Retro OS windows, digital icons, game items, 8/16-bit UI — pixel-block disintegration |

### Linear Wipe reveal — main subject [built-in]

`Effect > Transition > Linear Wipe`, on the character cutout PNG.

1. `Wipe Angle`: default `+90°` [visual] → `180°` (subject rises from the bottom as completion decreases).
2. `Feather`: leave `0.0` for a crisp edge.
3. `Transition Completion`: drag up until the subject is just fully hidden (`76%`), keyframe it a few frames before the beat.
4. Move past the beat, lower completion until fully revealed (`10–13%`) — second keyframe.
5. Apply the Flow wipe curve `0.67, 0.04, 0.28, 0.99`.

### Linear Wipe with keyframed angle — chunky filled arrows [built-in]

Use when a shape is a thick, closed, filled path (wide stem + angled head). Trim Paths trims the *outline* of a closed shape instead of growing it along the stem, so it fails here.

1. Apply `Linear Wipe` to the arrow shape layer.
2. Keyframe `Transition Completion` `100%` (hidden) → `0%` (revealed).
3. At each bend in the arrow, add `Wipe Angle` keyframes (e.g. horizontal `90°` → vertical or diagonal) so the wipe direction follows the arrow's turns.

### S_WipePointalize — dot-matrix wipe on a circular graphic [3P, Sapphire]

`Effect > Sapphire Transitions > S_WipePointalize` (may appear under Sapphire Stylize).

1. **Edge Width → minimum (≈0)** immediately. The default draws wide orange guide bounds and scatters dots across the whole frame, so the viewer can't tell where the element emerges. Pull it down until the orange guide lines collapse together into a tight, localized edge. Widen it only when a foggy, ambient dissolve is explicitly wanted.
2. Orient: drag the on-screen crosshair/target widget [visual] (or set `Angle`) to the far right of the asset so dots advance right→left.
3. Keyframe `Wipe %`: start high enough that the asset is fully concealed; end where it is 100% revealed.
4. Apply the Flow wipe curve.
5. Rotating layers: the wipe gizmo lives in layer space, so on a continuously rotating layer (the spinning CD) the wipe direction rotates with it. Shea keeps this as a free dynamic touch. Precompose first only if you need the wipe direction locked to screen space.

### S_WipePixelate — pixel-block wipe [3P, Sapphire]

Same procedure as Pointalize: apply → `Edge Width` to minimum → set `Angle` → keyframe `Wipe %` concealed→revealed → Flow curve.

- **Tilted asset** (retro "Loading..." dialog): `Angle 10°` to match the box's tilt (tested ≈30° first, refined down).
- **Top-down accessory cascade** (stars, floppy disk, envelope): `Angle 270°` so the reveal comes down from above. Copy spacing + curve from an earlier layer, then offset each layer's start several frames later so they cascade.

### Keep revealed elements alive — Wiggle - position [built-in]

After the wipe lands, static stickers freeze into a dead layout.

1. Apply `Animation > Presets > Transform > Wiggle - position` to one floating PNG.
2. Copy the preset's effect/expression controls from Effect Controls and paste onto every other floating PNG (CD, stars, floppy, envelope, dialog box). Result: a gentle drift in place.

### Stop-motion crunch — Posterize Time on an adjustment layer [built-in]

Smooth high-frame-rate wipes and wiggles look plastic next to pixel/halftone/cutout aesthetics.

1. New adjustment layer spanning the whole comp, above all PNG layers (below a final camera if any) [visual].
2. `Effect > Time > Posterize Time`, `Frame Rate` → `12.0` (from the 24/30/60 comp rate).
3. Result: wipe edges and wiggle drift step at 12 fps — snappy, hand-made, paper-cutout feel.

---

## Part 2 — Compositing: the five-pillar checklist

Compositing = assembling cutouts, graphics, type, textures, and lighting so the scene reads as one image. Layers read as one space when they share (a) one global optical force (camera move, shake, blur, lens), (b) one continuous surface texture, (c) one sampled palette. Work the pillars in order: **1 Assets → 2 Colors → 3 Textures → 4 Effects → 5 Final assessment.**

### Scale the checklist to scene length

- **Very short scenes (~10–15 frames):** keep it readable in one glance. Two or three assets max (subject, simple text, one secondary graphic). Skip stacked blurs, intense shakes, and geometric clutter; get impact from one-framers instead.
- **Extended scenes (several seconds):** layer all five pillars — unified camera move, continuous shake, subtle global blur, textured/masked passes, secondary graphic flourishes.

### Pillar 1 — Assets

- Pick or design clean, minimal focal assets: shape graphics, text, icons, a freeze-framed subject. No clutter.
- Freeze-frame the footage on static, high-impact moments to avoid tracking work.
- Design flourishes from references (e.g. Y2K / 2000s vector arrows from Pinterest). Draw with the Pen tool (`G`) on a new Shape Layer, no fill, solid stroke, snaking multi-segment angled paths.
- Stylized display type (demo font: Usao [visual]) set via the Character panel.

### Pillar 2 — Colors

- **Lock a palette sampled from the hero asset.** Eyedrop colors from a prominent existing element (demo: hot pink from the vinyl record player). Introduce no arbitrary colors.
- **Desaturate competing backgrounds** into a stylized black-and-white so vivid foreground color pops (demo: B&W moon asset behind colored arrows).
- **Vary distribution within the palette** ("controlled chaos"). Across multiple vector shapes, mix dual-color lines (red + blue), solid-color lines, white lines with color accents, and alternate arrowhead tip colors (white, blue, pink). Avoid coloring every element identically (e.g. all red stems with pink tips).

### Pillar 3 — Textures

Goal: break flat vector perfection so graphics glue to footage.

#### Depth-masked micro-LED grid on the subject [3P, Boris FX Continuum 2026]

Confines the LED texture to highlights/character surfaces instead of flooding the canvas. Stack on the character layer (inside its precomp), in this order:

1. `BCC Depth Map` — raise depth bias/contrast until rim light and silhouette separate strongly from the background [visual].
2. `Linear Color Key` [built-in] — eyedrop `Key Color` on the dark/background tone of the depth map to remove it, leaving only lit depth planes.
3. `BCC LED` (or `BCC LED OBSOLETE`) — set dot/element size **small and dense** (fine, high-res grid, never chunky circles); eyedrop the dot color from the hero asset (hot pink from the record).

#### Multi-pass typography texture

1. `Effect > Noise & Grain > Add Grain` [built-in]: `Viewing Mode` `Preview` → **`Final Output`** (otherwise grain shows only in a preview box); `Intensity ≈ 5.0` so grain clearly registers on flat fills.
2. Duplicate the text layer (or stack an instance above) and put `BCC LED` [3P] on the upper copy for a halftone dot pass over the grain.
3. `Effect > Generate > 4-Color Gradient` [built-in]: four close shades of one family (deep violet, mid-purple, magenta, bright pink). Text still reads as one hue but shifts subtly across letterforms instead of a dry solid fill.

#### Boiling noise on shapes [built-in]

For moving vector shapes (arrows); use Add Grain for text, animated Noise for shapes.

1. Apply the Noise & Grain effect that has a `Noise Phase` parameter — in stock AE that is `Effect > Noise & Grain > Noise HLS` (the video calls it "Noise"; plain `Noise` has no phase control). Raise the noise amount until grain is visible but edges stay clean.
2. Animate `Noise Phase` across the shape's on-screen time — keyframes, or expression `time * 500` [visual] — so granules boil continuously.

#### Tonal stepping — Posterize adjustment layer [built-in]

1. `Ctrl+Alt+Y` → adjustment layer over the scene.
2. `Effect > Color Correction > Posterize`, `Level ≈ 11` [visual] at peak moments (can be modulated over time).
3. Bands smooth depth-map lighting and highlights into distinct steps; combined with grain on text it gives a rough, print-like finish.

#### External textures

Paper/film textures from the web on top, blend mode `Soft Light`, `Screen`, or `Overlay` (demo settled on Soft Light).

### Pillar 4 — Effects (global unification)

**Rule:** if any element looks disconnected, move *everything* together — camera zoom, directional pan, or subtle shake — via an adjustment layer or a 3D Camera parented to a Null. Motion shared by all layers erases layer boundaries.

- **Unified camera move:** 3D Camera + parent Null; demo uses a pull-back-then-push move with camera shake on top.
- **Global blur:** subtle `Gaussian Blur` [built-in] on an adjustment layer.
- **Text entrance:** Typewriter preset / text animator Range Selector on opacity [built-in].

#### Practical camcorder re-record (wrist flick)

Real momentum, shake, and optical motion blur that presets don't reproduce.

1. Play or freeze the rendered comp full-screen on the monitor.
2. Film the screen with a camcorder or phone; flick the wrist to pan fast across the screen toward the subject.
3. Import the recording, place it above the base scene, and sync the flick to transition into the frame. Every element moves together with shared organic aberration.

#### Vector line draw-on with flickering arrowheads [built-in]

For open stroke paths (thin lines). Use the Linear Wipe method above for chunky filled arrows.

1. Shape layer → `Add:` → `Trim Paths`.
2. Keyframe `End` `0%` → `100%`.
3. Ease with Flow `cubic-bezier(0.25, 0.08, 0.26, 0.94)` [visual] (or Graph Editor). Softer than the wipe curve.
4. Arrowheads: separate triangle shapes at the stroke's end points. On the exact frame the stroke finishes, keyframe the triangle's Opacity rapidly between `100%` and `0%` over 2–4 frames for a sharp digital flicker.

(An anchor-point script [3P, visual] was used to snap anchors to corners/centers before animating.)

### Pillar 5 — Final assessment & details

#### One-framers (single-frame accents at cuts/hits)

1. **Flash frame:** Solid (`Ctrl+Y`) in the scene's dominant saturated accent (hot pink), trimmed to exactly **1 frame** (`Alt+[` / `Alt+]`) on the transition point.
2. **Contrast dip:** 1-frame adjustment layer right next to it with `Effect > Color Correction > Curves` pulled down to crush blacks — a brief dark hit before the scene resolves.

#### Audit pass

- Re-watch for motion rhythm, shake quality, and whether every animation completes.
- On short scenes, confirm the subject reads instantly at the scene's real length (the 10-frame check).
- Proof all text: spelling, apostrophes, kerning, layout. (Shea caught a mis-set apostrophe in "I'M SO" at this stage.)
