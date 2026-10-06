# Color, Light & Blending

This file covers color design across an edit (palette transitions, priming, palette abolition), lighting and exposure with native Curves and Levels, and blend-mode transitions. Read it when you plan an edit's color story, add a flash or contrast intro, or blend one clip into the next.

Sources: HOW TO MASTER CREATIVE COLORS IN EDITING (EDITING OUTLINES 4) https://youtu.be/UQvXFrlNeHI · Easy Lighting Effects In After Effects (AE ESSENTIALS 7) https://youtu.be/qHWL-F8kXEE · How To Make Every Scene Look Unique With Blending Modes (AE ESSENTIALS 9) https://youtu.be/iipcO2Y9MDo

Marking: **[built-in]** = native AE, **[3rd-party]** = plugin or extension. `[visual]` = the value was read off screen and may be inexact.

---

## 1. Color as part of the cut

- Build color shot by shot, into the cut, the layer stack, and the transitions. Shea rarely uses one global CC adjustment layer, and a single grade over the whole edit shouldn't be what defines the style.
- Change the color story from section to section as the song progresses. An edit graded one flat color (for example, every clip red) tires the eye.
- Put major palette shifts on structural music points: beat drops, verse→chorus, key changes. Put 1-frame color flashes on secondary accents (snares, percussion transients, footsteps).
- Sit every high-saturation hue against deep black, pure white, or neutral mid-gray.
- Show at most 1–2 vivid hues per beat or frame. Let variety come from how hues follow each other across cuts, not from packing them into one frame.

### Picking color values
- Sample from footage that's coming up (water, sky, jackets, grass) with the eyedropper, so graphics match the scene they lead into.
- Test saturated pairs that also contrast strongly in luminance: yellow + magenta, cyan + lime green, neon blue + lime green.
- Graphic backgrounds: pure black `#000000` or pure white `#FFFFFF`.

---

## 2. Grayscale buffer (palette reset transition)

Use this when a hard cut would jump between clashing palettes, such as red/orange → blue. Skip it when the adjacent scenes already share similar lighting.

1. **Strip natural color on the beat.** At the cut point or the climax of the outgoing scene, apply high-contrast mono: **Tint** or **Black & White** [built-in]. Keep one thematic accent (for example, crimson) plus black and white.
2. **Drop the accent.** Cut or fade the accent out, and hold pure grayscale for a few beats. This clears lingering color from the viewer's eye.
3. **Bring in the incoming hue as an accent only.** Keep the footage B&W. Add the next hue (for example, electric blue) through isolated strokes, subject outlines, or particles.
4. **Resolve.** Cut to the destination scene, whose natural lighting or wardrobe matches that accent (for example, a blue-lit night exterior). The hue was established before the cut, so the cut reads as continuous.

---

## 3. Subliminal priming (desaturation, subject tint, one-framers)

Use this to set up a big color shift several seconds ahead.

1. **Cool the lead-in shots.** In the shots before the shift, pull warmth down and push midtones toward a desaturated gray-blue.
2. **Tint focal subjects.** Mask key subjects with the **Pen Tool** (hands, a silhouette). Tint only the masked subject toward the target hue and keep the background neutral or desaturated.
3. **Insert one-framers.** These are cut-ins exactly **1 frame** long, placed on tight sync points (transients, drum hits, footsteps). Fill them with:
   - a solid, saturated silhouette fill in the target hue (for example, deep blue),
   - clean vector perspective or tracking lines `[visual]`,
   - high-contrast negative-space flashes.
   The viewer barely registers them, but they set up the dominant hue that follows.

---

## 4. Environmental palette extraction + graphic framing

Use this for subtle, live-action, or low-tempo edits where neon graphics would look out of place.

1. Find the dominant natural color in the footage (grass green, sky, pavement, wardrobe) and eyedropper it.
2. Build a minimal graphic comp of about **8–10 layers** `[visual]`, bottom to top:
   - a solid white plate `#FFFFFF`,
   - shape layers in the sampled color: repeating vertical pinstripes, rectangular blocks, bounding boxes,
   - the video duplicated, with the subject masked or rotoscoped, next to a mirrored or inverted copy of the same action.
3. Line up the subject's motion with the graphic borders so the footage and the design read as one image.

---

## 5. Palette abolition (duotone / invert remap)

Use this in fast "controlled chaos" edits (anime, hyperpop, phonk, intense action) where the footage's natural colors limit your palette.

1. Remove every natural hue (skin, clothing, background) with a stylized remap: **Sapphire S_Invert** [3rd-party, Boris FX], or native **Tint / Tritone / Duotone-style / Calculations** [built-in] `[visual]`.
2. Remap by luminance: shadows → a deep anchor (deep blue or black); highlights → a vivid complementary color (lime green, hot magenta).
3. The shot no longer carries realistic lighting, so the next cut can jump straight into another high-contrast palette (violet, pink, yellow) without a clash.
4. Overlaying saturated graphics on footage that has many competing natural colors looks muddy. Remove the native color first (duotone, invert, or grayscale), then add the graphics.

---

## 6. Monochrome anchoring for multi-hue sequences

Use this when an edit cycles through 10+ bright colors.

- Backgrounds: pure black or pure white.
- When fast colored graphics are on screen (dot arrays, sliding banners, neon boxes), render the character footage in high-contrast B&W.
- Keep the 1–2-hues-per-frame limit.

## 7. Cyclical palette loop

Use this for short-form showcase edits meant to loop.

1. Note the palette pair in the opening seconds (for example, neon blue + lime green).
2. Travel through contrasting themes across the body, for example blue/green → magenta/pink → solid crimson → stark white.
3. In the last **1–2 s**, flicker rapidly between frames in the opening hues. End on a transition that matches frame 1 so the loop is seamless.

---

## 8. Curves contrast intro (dark → normal reveal)

Open a shot crushed and contrasty, then ease it back to normal. Use it on an edit's opening shot or after a major transition, especially when the footage has a clear highlight (moon, neon, backlit hair, laser) against dark surroundings. It suits well-exposed footage with the detail you need above the lower midtones. Crushing already underexposed or heavily compressed footage causes banding, macroblocking, and noise.

1. `Ctrl+Alt+Y` / `Cmd+Opt+Y` makes a new Adjustment Layer. Put it directly above clip 1 and trim it to the clip's exact duration. Mode: Normal.
2. Apply **Curves** [built-in] (`Effect > Color Correction > Curves`, or search via FX Console). Channel: **RGB**.
3. The default curve is the diagonal (0,0)→(255,255). Add two points:
   - **Shadow point** (lower-left quadrant): drag it well down to crush shadows and darken the scene.
   - **Highlight point** (upper-right quadrant): drag it slightly up so light sources stay bright.
   This gives an aggressive S-curve.
4. Keyframes:
   - **KF1**: first frame of the layer. Click the stopwatch on **Curves**.
   - **KF2**: **one frame before the layer's end**. Click **Reset** on the Curves effect header to write the linear default.
5. Easing (Flow [3rd-party] or the Graph Editor): fast acceleration out of KF1 and a long, smooth deceleration into KF2. Pull the top-right handle down so the look carries further into the clip. Tune the bottom-left handle so the move starts fast without stalling. Click **Apply** in Flow.

---

## 9. Levels white-out flash (exposure transition across a cut)

A blown-out flash that hides a hard cut and carries energy between shots. Use it on high-tempo sections, drops, kick or snare hits, and fast action. Keep it off slow, atmospheric, or narrative sections, and save it for key hits rather than every cut in a fast run, because back-to-back white-outs tire the eye.

1. `Ctrl+Alt+Y` makes an Adjustment Layer. Snap it to clip 2's start, then drag its in-point **back exactly 4 frames** into clip 1. It now spans the cut: 4 frames before it and several frames after. Mode: Normal `[visual]`.
2. Apply **Levels** [built-in] (`Effect > Color Correction > Levels`). Channel: **RGB**.
3. Standard Levels has no separate stopwatch for Input White. Input Black, Input White, and Gamma all keyframe together under the **Histogram** property, so click the stopwatch there. (**Levels (Individual Controls)** exposes Input White as its own property.)
4. Keyframes:
   - **KF1**: layer start, 4 f before the cut. Input White = **255.0**.
   - **KF2**: exactly on the cut frame. Input White ≈ **30–60** `[visual]` for an extreme blowout.
   - **KF3**: **one frame before the layer's end**. Input White = **255.0**.
5. Asymmetric easing:
   - **Attack (KF1→KF2)**: sharp exponential ease-in. It starts slow and snaps into the peak on the cut.
   - **Decay (KF2→KF3)**: soft, extended ease-out, so the flash lingers briefly and fades over clip 2.
   - Then steepen the tail handle a little so the glow doesn't obscure clip 2's action.
6. Timing rules:
   - The peak (KF2) sits on the cut frame **and** the audio transient.
   - Attack is 3–5 f max (4 f is the demo standard), short enough that the viewer can't anticipate the cut.
   - Decay is 2–3× the attack.
   - Linear or symmetric flashes feel robotic. Always snap in and ease out.

### Landing-hit variant (from the blend-modes video)
Apply Levels to the landing clip itself instead of a spanning adjustment layer. On its **first frame**, keyframe Input White (or the Histogram) well below 255 `[visual]`. A few frames later, return it to **255**. Ease with a sharp decay: steep drop-off, then a smooth level-out. It reads as optical exposure bloom on arrival and pairs with §13.

### Keyframe hygiene (both lighting techniques)
- Put end keyframes **one frame before** the adjustment layer's out-point, not on its edge. A key on the edge can go unevaluated or cause a 1-frame color pop into the next shot.
- Native Curves and Levels are all these looks need. They render fast and work on any AE install. Sapphire and Universe lighting suites aren't required.

---

## 10. Blend-mode fundamentals

- A blend mode combines a layer with the layers **below** it, so the incoming clip must sit on a higher track and **overlap in time** with the outgoing clip. Clips placed end to end on one track can't blend.
- **Place beat markers on the audio cues first** (`*` on the numeric keypad `[visual]`), then extend in-points. The markers are hard anchors for cuts and keyframes once layers overlap.
- Show the Mode column: **Toggle Switches / Modes** at the bottom of the timeline, or `F4` `[visual]`.
- Pick modes by trial: cycle through the dropdown against the real footage. Results depend on each clip's palette and dynamic range, so the math only tells you where to start.

### Mode selection
| Footage | Try first | Result |
|---|---|---|
| High-key light sources (headlights, lamps, neon) | `Screen`, `Hard Light`, `Soft Light` | Brights bloom through, darks drop out |
| Flat or inverted contrast | `Classic Difference` | Edge-detect / silhouette artifacts |
| Unknown | `Hard Light` (default first trial) | Keeps contrast, blends midtones |
| Also auditioned | `Saturation` | Transfers the top layer's color intensity |

---

## 11. Ramped-opacity blend transition (slow/melodic)

1. Clip 1 on the lower layer, incoming clip 2 on the layer above. Drag clip 2's in-point back so the overlap runs up to the beat marker (it can span several beats).
2. Set clip 2's mode. The demo auditioned Classic Difference, Saturation, and Hard Light, and picked **Classic Difference**.
3. `T` `[visual]` shows Opacity. **0%** at the overlap start, **100%** on the beat marker.
4. Select both keys. In **Flow** [3rd-party], apply an aggressive exponential ease-in, cubic-bezier **[0.75, 0.05, 0.90, 0.98]** `[visual]`, then **APPLY**. Opacity stays near 0 for most of the overlap and spikes to 100 on the beat.
5. Always use this ease-in rather than linear interpolation. A linear ramp leaves a muddy half-transparent double exposure through the middle of the transition.

## 12. Rapid overlap + duplicate stacking (fast/aggressive)

1. Drag the incoming clip's in-point back only **4–5 frames** before the beat marker. Hard-cut the outgoing clip on the marker. Add no opacity keys.
2. Mode: **Hard Light**.
3. If the blend is too weak, **duplicate** the incoming layer (`Ctrl+D` / `Cmd+D` `[visual]`) and keep the copy directly on top with the same Hard Light mode for the same 4–5 f. Stacking applies the blend twice, which adds contrast and punch.
4. To strengthen a washed-out blend, duplicate the layer. Leave clip brightness and curves alone.

## 13. Ramped blend + 1-frame Screen hit + Levels landing

Use this to soften the seam of a ramped blend when the incoming clip has strong light sources (the demo used headlights).

1. Overlap incoming clip 4 over clip 3. Mode: **Soft Light**. Opacity **0% → 100%** at the beat marker, eased with the same Flow curve **[0.75, 0.05, 0.90, 0.98]** `[visual]`.
2. **1-frame mode swap.** Split the layer so the **single frame before the full cut** uses **Screen**. The scene's own lights produce a natural white hit just before the shot lands.
3. **Landing exposure hit.** On clip 4's landing, apply the Levels landing-hit variant (§9): Input White low on frame 1, back to 255 a few frames later, sharp ease-out.

## 14. Master texture for cohesion

At the top of the comp, put an Adjustment Layer spanning the whole edit (`Ctrl+Alt+Y`). Apply **S_Flicker** [3rd-party, Boris FX Sapphire] via FX Console, at default or lightly calibrated frequency and amplitude. The small luminance flicker across all footage masks color differences between clips and ties different blend styles together.

---

## 15. Tools referenced

- **[built-in]**
  - Adjustment Layer (`Layer > New > Adjustment Layer`, `Ctrl+Alt+Y`)
  - Curves, Levels, Levels (Individual Controls), Tint, Tritone, Black & White, Calculations
  - Pen Tool masks, shape layers, track/alpha mattes (silhouette cutouts, geometric reveals) `[visual]`
  - Blend modes, Graph Editor, beat markers
- **[3rd-party]**
  - **Flow** (RenderTom & Zack Lovatt): bezier easing panel
  - **FX Console** (Video Copilot): hotkey effect search
  - **Sapphire S_Invert** and **S_Flicker** (Boris FX)
  - **Topaz Video AI** `[visual]` (upscale / frame interpolation; seen docked in the workspace)

Scripting: see motion-and-timing.md §3f.
