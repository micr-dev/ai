# Motion and Timing

What this covers: making every frame move (dead-frame removal), splitting clips between Twixtor and manual time remap, the double pre-comp, graph/Flow curve rules, pacing against music, and Posterize Time. Read it before retiming footage, easing any keyframes, or laying out an edit's rhythm.

Sources: The Fundamentals of Movement in Editing (Editing Outlines 1) https://youtu.be/cK_GkB3ORIM · Graphs Are Easier Than You Think to Master (Editing Outlines 2) https://youtu.be/plIPW2NAcY8 · How to Correctly Pace Your Edits (Editing Outlines 3) https://youtu.be/jarphAPPnic · The Best And Easiest Effect In After Effects (AE Essentials 10) https://youtu.be/G9fcdItUNq4

Tool key: **[3P]** third-party, **[AE]** built-in.
- Twixtor / Twixtor Pro (RE:Vision Effects) [3P]: optical-flow retiming.
- Flow (renderTom & Zack Lovatt) [3P]: bezier preset panel with an **APPLY** button; its **Interpolate** toggle must be active (shows pink) [visual].
- FX Console (Video Copilot) [3P]: `Ctrl+Space` effect search launcher.
- Time Remapping `Ctrl+Alt+T` (Layer > Time > Enable Time Remapping), Pre-compose `Ctrl+Shift+C`, Split Layer `Ctrl+Shift+D`, Duplicate `Ctrl+D`, Easy Ease `F9`, Posterize Time (Effect > Time) [AE].

---

## 1. The movement rule: no dead frames

Anime is animated on twos or threes (12 or 8 drawings/sec in a 24 fps container), so raw clips contain held duplicates, called **dead frames**. On a fast edit they cause stutter, make overlays (shakes, glitches, CC) look pasted on over a frozen subject, and make Twixtor warp when it hits a held-then-jump.

Target: every frame on the timeline shows the **subject** in a new pose or position.
- Step one frame at a time (`Page Down`/`Page Up`, or `Ctrl+Right/Left` [visual]).
- A frame counts as movement only if the character's anatomy or position changes. A camera pan/truck over static lineart is still a dead frame. Cut or compress it out.
- Remove dead frames before applying any effect; effects over held frames look cheap.

## 2. Hybrid split: Twixtor vs manual time remap

Split each clip into two kinds of motion and route them to different layers.

| Motion | Tool | Examples |
|---|---|---|
| Smooth, linear, predictable; moderate continuous displacement | **Twixtor** (double pre-comped) | hand sliding across a surface, hair floating, slow torso/head turn, steady tracking |
| Sudden velocity change, big spatial jump, extreme foreshortening, single impact drawing that must read clearly | **Manual Time Remap** | punch, roundhouse kick, weapon swing, snap head-turn |

Also move a section to time remap when Twixtor produces warping, liquid anatomy, or background smear on it.

### 2a. Setup
1. Select the raw clip, `Ctrl+D`.
   - **Top copy**: Twixtor (smooth sub-action).
   - **Bottom copy**: time remap (impacts and discrete action).
2. On the top copy, step through, find where motion becomes consistent, and split (`Ctrl+Shift+D`) at its start and end. For a turn-into-snap shot, begin Twixtor on the subtle part of the turn and leave the violent snap frames for the bottom layer.

### 2b. Twixtor branch (with the double pre-comp)
1. Inside the isolated range, split at every repeated frame and delete the duplicates.
2. Slide the remaining unique frames flush against each other so there are no gaps or holds ("slim it down"). Any duplicate left inside means Twixtor sees zero motion and then jerks when motion resumes.
3. Select all the slices, `Ctrl+Shift+C`, choose **Move all attributes into the new composition** [visual], with duration matching the selection.
4. Apply **Twixtor** or **Twixtor Pro** to the pre-comp (FX Console or Effects & Presets). Twixtor Pro may show a GPU-acceleration warning dialog; dismiss it and continue.
5. **Pre-compose again** right away (`Ctrl+Shift+C`, Move all attributes). This second nest isolates Twixtor's frame buffer. Stretching, trimming, or time-remapping a single-nested Twixtor layer causes frame-sampling errors, cache mismatches, and tearing.
6. Drag the outer layer's edge across the whole span the retimed motion should fill.
7. Retime it (time remap keyframes on the outer layer, or `Speed %` keyframes on Twixtor), then ease it per §3.

### 2c. Manual time-remap branch
1. On the bottom copy, split out and delete the section directly under the Twixtor block so the two layers never render duplicate video/audio.
2. Select the remaining discrete pieces, `Ctrl+Alt+T`. AE adds time keyframes at the layer's start and end.
3. Step through. Wherever a held frame shows up, drag the **rightmost** Time Remap keyframe **left by 1–2 frames**. Check again; if a frame still repeats, pull it in 1 more frame. Stop when every frame shows a new drawing or position.
4. For a clip whose animation is simply too slow (a transition clip, for example), compress the end keyframe toward the start until the action plays in about **3–4 frames** as one burst.

### 2d. Legibility checks (both branches)
- **One-framer rule**: if an action jumps straight from windup to contact and can't be read (a kick that seems to teleport or disappear), go back to the discarded frames and re-insert one breakdown/extension frame between the start and the hit.
- **Harshness rule**: if an impact feels stroby or too jarring, add one extra frame before it to guide the eye to the focal point.
- **Snappiness rule**: if the motion after an impact drags, pull the end Time Remap keyframe **left 2–4 frames**, then re-apply the Flow curve.
- Review the whole assembled sequence at the end. Accidental repeats often slip back in after retiming.

---

## 3. Graph editor / Flow rules

Default `F9` Easy Ease (33.33% influence) looks robotic. Every keyframe pair gets a deliberate curve, applied through Flow (select keys, pick or shape a curve, **APPLY**) or the Graph Editor.

**Audit move**: to diagnose an edit, select all keys (`Ctrl+A`), press `F9`, and play it back. The robotic motion, dead frames, and abrupt stops show clearly. Then re-graph.

### 3a. Middle-ground handles (the default)
Most editors over-sharpen: they pin handles flat against the walls (`0,0` / `1,1` corners), so effects spike for 1–2 frames and leave dead static space after. Instead:
- **Top (peak) handle**: pull it **down**, away from the top wall, so the value holds and stays visible through the middle frames.
- **Bottom (zero) handle**: pull it **out** into the graph interior rather than pinning it to the floor.
- Result: a punch on the first frame, then a delayed exponential tail that lingers across the shot.
- Tune per shot. Even when the functional shape repeats (for example in-fast/out-fast for Twixtor), each shot's internal motion, subject scale, and framing need their own handle tweaks. Start from a preset and adjust it.

### 3b. Stiff vs loose
| Use **stiff/sharp** curves when | Use **loose/soft** curves when |
|---|---|
| an impact must land instantly on a snare, kick, or gunshot | secondary/ambient camera float |
| a heavy shake reveals Motion Tile seams or repeated edges; a steep falloff hides them in motion blur | blurs and exposure flashes that must stay visible over several beats |
| keyframes sit very close together | keyframes are far apart, **provided amplitude is low** |

**Earthquake error**: a loose curve across widely spaced keys on a high-amplitude property reads as a long, disorienting earthquake. Pair high amplitude with a quick resolve (tighter keys or a stiffer curve), and pair long durations with low amplitude.

### 3c. Non-zero floors and momentum into the cut
- Keep continuous effects above zero. On the ambient/soft shake layer, end on a floor: **1.3%** Dissolve (Outlines 2), or amplitude **1.5–2.0** (Outlines 1 tested 2.0 and settled on 1.5). The shot then keeps organic drift after the main keys finish.
- **Momentum keyframe**: when an aggressive shake dies within the first ~60% of the clip and the tail goes static, add a third key on the **last frame** of the clip at a small value (**4.0%** Dissolve) with a moderately stiff curve. Energy ramps slightly into the cut and carries into the next shot.
- General range: leave **1–4%** residual shake into the final frame of any shot that would otherwise freeze before the cut.
- Full shake parameters (S_Shake frequency/amplitude, Wrap Reflect, tilt, axis channels) are in `shakes-impact-blur.md`. This file owns only their curve shapes and floors.

### 3d. Recorded curve shapes
| Target | Keys | Curve | Flow values |
|---|---|---|---|
| Twixtor/outer time remap after dead-frame removal (Outlines 1) | start → end time remap | sharp, steep ease-out: fast initial acceleration settling into a smooth sustained tail (steep left bias) | sharp preset [visual] |
| Twixtor `Speed %` speed ramp (Outlines 2) | start of action, intermediate keys at peak movement, end at transition point | S-curve: steep in ("in fast"), flat plateau in the middle ("slow middle"), steep out ("out fast") | ≈ `0.25, 0.00, 0.25, 1.00` [visual], customized per shot |
| Aggressive impact shake Dissolve | peak → 0 over the burst | very stiff; top handle flush into the top-left corner for maximum impulse on frame 1; bottom handle pulled down a little so the shake stays visible before it dies | ≈ `1.00, 0.00, 0.27, 1.00` [visual] |
| Soft/ambient shake | peak → non-zero floor | relaxed; top handle dragged well down toward the center so motion persists through the shot | gentle ease |
| Full-clip Gaussian Blur | first frame of cut **20–27** (seen at 23.3) → **last frame** of clip **0** | middle ground: top handle down, bottom handle out, so the blur visibly dissipates across the whole clip | — |
| Levels exposure flash | start aligned with the blur's impact key | same shape as the blur so flash and blur decay together; run it slightly longer than the blur for extra lingering glow | — |
| Anticipatory blur build-up | ~0 at start of pre-action → peak just before the action cut / Twixtor ramp start | loose, gradual acceleration so tension visibly builds | — |
| Curves flash stack (under Posterize Time) | white-flash → deep dip → linear/slight S | asymmetrical S-curve preset, high entrance influence | preset [visual] |
| Audio Spectrum Start/End Point whip | across the clip | steep acceleration/deceleration | — |

Blur/Levels layer setup: adjustment layers named `blur` (Normal mode [visual]) then `levels` above it, both over the clip pre-comps. Gaussian Blur uses `Blur Dimensions: Horizontal and Vertical` and **Repeat Edge Pixels on**, which prevents dark borders. Levels keys `Input White` / `RGB Output White` [visual] on the impact frame. The build-up blur hands off to a follow-through: on the incoming impact, start at max blur and decay with the full-clip curve.

### 3e. Decay length
- Start every effect at its peak exactly on the audio transient: blur, shake dissolve, and Levels exposure.
- Run blur and exposure decay the full distance to the next cut. If an effect ends after 5 frames and leaves 20 static frames, drag the second key to the clip's last frame.

### 3f. Scripting equivalent (when Flow is unavailable)
[Not from the videos; standard AE ExtendScript facts. This is the one place the skill covers scripting; verify every scripted curve in the Graph Editor.]

**Flow bezier → AE temporal ease.** AE stores speed + influence per keyframe, not a cubic-bezier. For a 1D segment between key A (value vA, time tA) and key B (vB, tB), a Flow cubic-bezier `x1, y1, x2, y2` maps like this, with `avg = (vB − vA)/(tB − tA)`:
- A outgoing: `influence = x1·100`, `speed = (y1/x1)·avg` (0 when x1 = 0).
- B incoming: `influence = (1 − x2)·100`, `speed = ((1 − y2)/(1 − x2))·avg`.
- Apply on A with `prop.setTemporalEaseAtKey(kA, prop.keyInTemporalEase(kA), [new KeyframeEase(speed, influence)])`, and on B with `prop.setTemporalEaseAtKey(kB, [new KeyframeEase(speed, influence)], prop.keyOutTemporalEase(kB))`. Clamp influence to 0.1–100. Keys must use Bezier interpolation.
- Pass one `KeyframeEase` per dimension: one for 1D and spatial properties (Position), three for Scale.
- Shortcut when `y1 ≈ 0` and `y2 ≈ 1`: speed ≈ 0 at both keys, influence `x1·100` out and `(1 − x2)·100` in. Curves recorded in this skill: camera S `0.67, 0.04, 0.16, 0.99` → 67% / 84%; wipe `0.67, 0.04, 0.28, 0.99` → 67% / 72%; sharp shape morph `0.90, 0.00, 0.10, 1.00` → 90% / 90%.

**Layers, effects, blend modes.**
- Adjustment layer: `comp.layers.addSolid([1,1,1], "shake 1", comp.width, comp.height, comp.pixelAspect)`, then `.adjustmentLayer = true`.
- Timing: set `inPoint`/`outPoint` in seconds (`frame * comp.frameDuration`). A one-framer lasts exactly `comp.frameDuration`. For a one-framer or 1-frame mode swap cut from an existing clip, `layer.duplicate()` and trim the copy's in/out points.
- Effects: `layer.property("ADBE Effect Parade").addProperty(matchName)`. Built-in match names: Gaussian Blur `ADBE Gaussian Blur 2`, Radial Blur `ADBE Radial Blur`, Levels `ADBE Easy Levels2`, Levels (Individual Controls) `ADBE Pro Levels2`, Curves `ADBE CurvesCustom`, Exposure `ADBE Exposure2`, Fill `ADBE Fill`. For third-party effects (Sapphire, BCC, OLM), look up the installed match name in `app.effects`.
- The Curves curve and the Levels **Histogram** are custom-data properties that ExtendScript can't set. Script exposure flashes with Levels (Individual Controls), whose `Input White` is a plain 1D property. Build Curves looks by hand or load a saved `.ffx` preset.
- Blend mode: `layer.blendingMode = BlendingMode.CLASSIC_DIFFERENCE` (also `HARD_LIGHT`, `SOFT_LIGHT`, `SCREEN`, `SATURATION`).
- Shape Scale is always 3-valued: `layer.property("ADBE Transform Group").property("ADBE Scale").setValueAtTime(t, [x, y, 100])`.
- Hard one-frame swap (e.g. Fill color): two keys one frame apart, or `prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.HOLD)`.

**Chained-null camera rig** (camera-text-shapes.md).
- `comp.layers.addCamera("Camera 1", [comp.width/2, comp.height/2])` makes a two-node camera; confirm `camera.autoOrient == AutoOrientType.CAMERA_OR_POINT_OF_INTEREST`.
- `comp.layers.addNull()` once per move plus spares. Set `threeDLayer = true` on every null and every content layer, including the background solid.
- Parent bottom-up: `camera.parent = null1; null1.parent = null2; null2.parent = null3; null3.parent = null4`. Assigning `parent` keeps world position, so each child's Position is then in its parent's space: key moves as offsets from the null's current `value`, not as absolute comp coordinates.
- Keyframe each null's Position with `setValueAtTime` at `start` and `start + 15 * comp.frameDuration`, where each `start` is the previous null's end minus `5 * comp.frameDuration`. Then apply the camera S-curve above.

---

## 4. Pacing and music sync

Pacing is the rate at which the edit delivers information, and it sets tone and energy. The engine is contrast: **fast, slow, fast, slow**. Constant fast cutting tires the viewer and removes the baseline that makes fast cuts hit. Constant slowness goes flat.

### 4a. Prep
1. **Map the audio.** Put the track on the timeline (`audio 1`). Mark the macro structure (intro, main/impact block, outro). Put markers on major downbeats (numpad `*` [visual]). Add secondary markers on trailing accents right after downbeats (sub-bass rattles, vocal chops, snare snaps); these drive events inside clips.
2. **Over-harvest footage.** Scrub the source and split (`Ctrl+Shift+D`) every potentially useful shot. Collect **at least 2×** what you'll use (expect to use ≤50%). Sort into: atmospheric establishing shots, character introductions, fast directional combat fragments, and sustained anchor shots that have exit motion. Harvest before assembling, because hunting for footage mid-edit breaks timing flow.

### 4b. Intro structure
- Beat 1: an atmospheric/establishing shot, held for exactly one beat/bar.
- Beat 2: the character or antagonist introduction.
- Keep intro cuts on the primary beats for orientation before action starts.

### 4c. Fast sections: micro-flickers
- Place **2–3** clips of preparatory motion, strong directional silhouettes, or baked-in motion blur **directly before** a major impact beat. Skip static, low-motion frames.
- Trim them all to the **same length, 1–3 frames** (for example exactly 2 or exactly 3 each). Equal lengths give a crisp stroboscopic acceleration into the downbeat; irregular lengths blur the cadence.
- Also use fast passages over drum rolls, glitch noises, vocal stutters, rapid percussion, and scene bridges where motion continuity carries the cut.

### 4d. Slow sections: multi-beat anchors
- Land slow sections on heavy downbeats, bass impacts, drop arrivals, right after a flicker run, or wherever choreography and effects need screen time.
- An anchor clip needs clear entry motion and **unmistakable exit motion** (moving out of frame). Without exit motion, the jump into the next fast section feels disjointed.
- Pre-compose (`Ctrl+Shift+C`, Move all attributes), apply Twixtor Pro, and stretch the clip **across several beats** rather than cutting on the next one. Double pre-comp per §2b before stretching.
- Keep interest inside the hold with internal events on secondary markers: an angle switch/internal cut, a one-framer flash, a scale punch, a speed shift.

### 4e. Internal events (pacing without cutting)
Cutting on every beat is not pacing. Keeping one subject across several beats and firing events inside it feels more musical.
- **One-framer white flash + punch-in**: `Ctrl+Y`, solid at comp size (`1920×1080`), `#FFFFFF`, (`White Solid 1`). Trim it to **1 frame** (`Alt+]`) and place it directly above the clip on the cut/accent frame. On the clip, press `S` and raise Scale above 100% on that frame.
- **Speed burst**: time remap the clip and compress its end key to about 3–4 frames (§2c step 4).
- **Directional blur accent** [3P]: BCC Directional Blur (Boris FX Continuum; FX Console `bcc dir`; Effect > Boris FX Continuum > BCC Blur & Sharpen > BCC Directional Blur). Set Blur Amount and align Angle with the subject's motion.

### 4f. Directional continuity across cuts
- Read the exit vector of the outgoing shot. The next 1–3-frame clips must continue that direction (exits right, so the next clip enters moving right).
- If the footage lacks velocity, press `S`+`P`, scale in enough to hide borders, and keyframe Position over **3 frames** as a fast pan in the exit direction. Add a directional blur along the same angle.

### 4g. Cut placement
- Put impacts and peaks exactly on transients (§3e).
- End slow anchors on the **trailing** accent after the downbeat (release noise, sub drop, percussion echo) rather than on the downbeat itself. This reads more fluid and less robotic.

---

## 5. Posterize Time: stepped cadence as glue

Posterize Time [AE] quantizes all motion under it onto a low-frame-rate grid. The eye reads smooth motion as CG and 8–12 fps as hand-drawn, so posterizing unifies mismatched elements (shakes, blurs, harsh curves, spectrums, 2D/3D shapes over anime) into one crunchy anime cadence. It also hides interpolation flaws, so push the underlying effects harder than you would at full rate. Movement that looks ugly at 24/60 fps turns into stylized impact frames.

### 5a. Setup
1. Layer > New > Adjustment Layer (`Ctrl+Alt+Y` [visual]) above the target clip.
2. Effect > Time > **Posterize Time** (FX Console `pos`), then set `Frame Rate`.
3. Use **one adjustment layer per scene/cut**, not one global layer, so the rate can follow each shot's intensity (for example 12 → 8 at peak action).
4. When testing a risky or messy keyframe move, apply Posterize Time first to see whether the stepped cadence cleans it up.

### 5b. Frame-rate choice (prefer even numbers)
| fps | Use |
|---|---|
| **12** (on twos) | default: general action, character animation, stylized fast cuts, blur transitions, animated graphic overlays |
| **10** | transition moments, environment shots, slightly detached sequences |
| **8** (on threes) | extreme chaos: violent shakes, high wiggle amplitude, heavy blend-mode overlaps; turns continuous displacement into discrete impact poses |
| **6** | extreme lo-fi, slideshow, vintage stop-motion |
| **15** | exception: half of 30 fps, for 30 fps comps needing slight stepping with fast readability |

Demo assignment across four scenes: `12, 10, 12, 8`.

Skip Posterize Time for sleek UI/corporate/clean type work that needs liquid 60 fps, and for fast tracking shots or fluid pans where stepping strobes and hurts readability.

### 5c. Stacks that pair with it
- **Chaos flash (12 fps)**: S_Flicker [3P Sapphire] (`s_flic`) for luminance strobe. Add Gaussian Blur (`Repeat Edge Pixels` on, Horizontal and Vertical) with Blurriness spiking at the cut and easing quickly to 0. Add Curves (Effect > Color Correction > Curves) with three RGB keys: near-white overexposure → deep crushed dip → linear/slight S. Ease with an asymmetric S preset in Flow. Always keep Repeat Edge Pixels on when stacking heavy blurs at low fps; otherwise dark borders show during camera moves.
- **Subliminal color pop (10 fps)**: an adjustment layer trimmed to **1–2 frames** (`Alt+[` / `Alt+]`) above the cut with S_DuoTone [3P Sapphire] (`duot`), Color 1 and Color 2 set to saturated deep blue/purple [visual]. The posterized step holds the pop on screen as an impact accent.
- **Whip audio spectrum (12 fps)**: `Ctrl+Y` black solid (`Black Solid 1`, 1920×1080, `#000000`) directly above the footage. Put Effect > Generate > **Audio Spectrum** on the solid, not on an adjustment or footage layer. Set `Audio Layer` from None to the music layer (for example `4. audio`). Drag Start/End Point across the focal point. Raise `Maximum Height` well above default. Set `Display Options` to analog or digital lines with a high band count [visual], and `Inside/Outside Color` to pink/magenta + white [visual]. Keyframe Start/End Point so it whips across the frame, with steep Flow curves.
- **Violent wiggle (8 fps)**: Animation > Presets > Transform > **Wiggle - position** (`wigg`), with Wiggle Speed and Wiggle Amount far above subtle values. Add S_Flicker. Duplicate the clip (`Ctrl+D`), press `F4` for modes, and set the top copy to **Vivid Light** (or Hard Light / Overlay [visual]). The 8 fps step turns the jitter into combat impact frames without causing motion sickness.
- Before judging the result, RAM-preview at full resolution.
