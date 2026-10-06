# 3D Camera, Text, and Shape Layers

Covers the chained-null 3D camera rig, three text treatments (typewriter, per-character stop-motion wiggle, circular path text), and beat-synced shape-layer graphics. Read when planning camera movement across subjects, adding kinetic type, or building shape accents, wipes, and outros.

Sources: How To Use The 3D Camera For All Your Movement (AE ESSENTIALS 1) https://youtu.be/VKgYqel1tn8 · 3 Of The Easiest Ways To Use Text In After Effects (AE ESSENTIALS 3) https://youtu.be/lfChY_rIQg8 · How To Start Using Shape Layers In Your Edits (AE ESSENTIALS 4) https://youtu.be/vS51L2K9ob4

Tool marking: **[3P]** = third-party, everything else is built-in AE. Demo host: AE 2024, 1920×1080, 30 fps.

## Shared conventions

- **One motion phase per layer.** Put each camera move on its own null; put a shape's secondary deformation on a parent null. Stacking a second move's keyframes on a property that's already animated tangles the spatial paths and speed graphs.
- **Every move gets an S-curve** (slow out, fast middle, slow in). Apply it with **Flow [3P]** (RenderTom & Zack Lovatt; select keyframes → pick/edit curve → APPLY), or with the native Graph Editor in Edit Speed Graph mode. Linear or one-sided curves read as stiff.
- **Flow bezier values seen** (`x1, y1, x2, y2`):
  | Use | Curve | Character |
  |---|---|---|
  | 3D camera null moves | `0.67, 0.04, 0.16, 0.99` [visual] | balanced S, long glide in |
  | Shape scale morphs | `0.85, 0.00, 0.15, 1.00` → steepened to `≈0.90, 0.00, 0.10, 1.00` [visual] | sharp: explosive burst, snappy stop |
  | Visible in Flow during the text video (not tied to a step) | `0.69, 0.13, 0.28, 0.83` [visual] | softer S |
- Scripting: see motion-and-timing.md §3f.
- **Beat sync:** land the arrival keyframe on the beat marker. Eased moves decelerate into the target, so if the hit looks late, select both keyframes and shift them 1 frame earlier.
- Null shortcut: `Ctrl+Alt+Shift+Y` (Win) / `Cmd+Opt+Shift+Y` (Mac), i.e. Layer > New > Null Object. Duplicate: `Ctrl+D`. Reveal keyframed properties: `U`.

## 3D camera: chained-null rig

Shea drives all scene movement with this rig: push into one subject, then glide from subject to subject. Keyframing the camera's own Position and Point of Interest across several targets causes gimbal lock, erratic arcs, conflicting spatial interpolation, and errors that compound when you edit an earlier key. Give each move its own null instead. Each null carries exactly one move, so retiming or reframing one move leaves the others intact, and each inherits the world position of the moves before it.

### Build the rig
1. **Make every layer 3D.** Show the switches column (`Toggle Switches / Modes`, bottom left, if hidden) and drag down the **3D Layer** switch (cube) across every content layer *and* the background. Demo stack, bottom to top [visual]: `White Solid 1` (grid background), `Pokemon-Logo.png`, `Pikachu.png`, `Espeon.png`, `Snorlax.png`, all in `Normal` mode.
2. **Camera.** Timeline right-click > **New > Camera…** (`Ctrl+Alt+Shift+C` / `Cmd+Opt+Shift+C`). Camera Settings: **Type = Two-Node Camera**. This is the one setting that matters: a One-Node camera binds position to orientation and rotates unexpectedly when the rig translates it. Demo values [visual]: Name `Camera 1`, Preset `50mm`, Zoom `1422.2 px`, Comp Size `1920 × 1080`, Focus Distance `1422.2 px`, Enable Depth of Field off, Units `Millimeters`, Measure Film Size `Horizontally`. OK. Place it directly above the content layers.
3. **Nulls.** Create a null (`Ctrl+Alt+Shift+Y`), then `Ctrl+D` until you have one null per planned move plus spares (demo: `Null 1`–`Null 4`; make 4–5). Stack them above the camera with `Null 1` lowest: `Null 4`, `Null 3`, `Null 2`, `Null 1`, `Camera 1`, then content. Make surplus nulls now: unused nulls at the end of the chain can stay unkeyed or be deleted later without affecting active moves, but inserting a null mid-chain shifts spatial origins and breaks the existing offsets.
4. Turn on the **3D Layer** switch for all four nulls.
5. **Chain the parents** with the pick whip (spiral) in the Parent & Link column. Whip each layer to the one directly above it: `Camera 1 → Null 1`, `Null 1 → Null 2`, `Null 2 → Null 3`, `Null 3 → Null 4`. Hierarchy: `Camera 1 → Null 1 → Null 2 → Null 3 → Null 4`.

### Animate move 1 (Z push-in)
1. Select `Null 1`, press `P`, and stopwatch Position at frame `0` (default `[960.0, 540.0, 0.0]` [visual]).
2. Go +15 frames (`00:15`) and add a keyframe with the keyframe diamond.
3. Push Z forward (demo ≈ `+1150 px` [visual]) until the first subject fills the camera view (demo: the logo).
4. Select both keyframes and, in Flow, apply the camera S-curve `0.67, 0.04, 0.16, 0.99` [visual].

### Animate moves 2…N (overlapping hand-offs)
For each next null:
1. Put the playhead on the previous null's **landing** keyframe, then step **5 frames back**.
2. On the next null, press `P` and stopwatch Position there.
3. Go **+15 frames** and add a keyframe.
4. Frame the next subject. In the Composition viewer (Active Camera), drag the null's center square handle onto it. For strict single-axis travel (pure X or pure Y pan) or exact alignment, scrub the Position values instead.
5. Select both keyframes and apply the **same** S-curve in Flow.

Demo schedule at 15f/5f: Null 1 `0–15` (push to the logo), Null 2 `10–25` (pan up-right to Pikachu), Null 3 `20–35` (cross-screen to Espeon, upper left), Null 4 `30–45` (down to Snorlax, bottom center). Real cameras rarely stop before the next pan or push. The overlap blends the departing move's deceleration with the incoming move's acceleration, so the camera rounds corners and carries momentum instead of halting at each subject.

### Decision rules and pitfalls
- **Use it for** multi-subject showcases (title cards, collage assets, UI layouts, anime clips, stickers), typography and lyric edits that travel from word to word across a 3D canvas, and parallax scenes that need depth in front of and behind the focal plane.
- **Skip it for** pure 2D moves, where flat scale/position on one pre-comp is enough, and for continuous orbits around one object, where a single 3D null with Y Rotation keyframes fits better.
- **Timing:** 15 frames per move (0.5 s at 30 fps), overlap 5 frames (one-third of the move). That blends the moves without muddying the framing. Keep the interval, overlap, and curve identical across standard moves so the rhythm stays even.
- **Beat sync:** put each arrival keyframe on a beat marker. Start each move 15 frames before it, so the 5-frame overlap straddles the beat hand-offs.
- **Stiff curve:** linear interpolation or extreme one-sided eases (e.g. the sharp ease-out `0.85, 0.04, 0.84, 0.16`) jerk the camera. Use the balanced S `0.67, 0.04, 0.16, 0.99`: smooth acceleration into the move, soft landing.
- **Stop-and-go:** starting a move only after the last one finishes makes the camera dead-stop at every subject. Always step 5 frames back from the previous landing keyframe.
- **Missing 3D switch:** a 2D layer ignores camera depth, and a 2D null breaks the parenting chain. Check the cube on every content layer, solid, and null before keyframing.
- **One-Node camera:** unexpected rotation during translation. Check Camera Settings for `Two-Node Camera`.
- **Null inserted mid-chain:** broken offsets. Make spares up front.

## Text

Text is a focal visual in edits, not a label. Demo type: font `Uniwash` Bold, yellow fill (`#FFFF00` range) with a thin black stroke, on a magenta solid (`#E01B84` range) with grain [visual]. Type Tool: `Ctrl+T`.

### Typewriter reveal: hold, then type out
1. Effects & Presets (`Ctrl+5`) > **Animation Presets > Presets > Text > Animate In > Typewriter**. Drag it onto the text layer. It creates `Animator 1 > Range Selector 1` with **Start** keyframes.
2. Press `U`. Keyframe 1 is Start `0%`, keyframe 2 is Start `100%`.
3. **Hold:** copy the 100% keyframe (`Ctrl+C`), move the playhead forward, and paste (`Ctrl+V`). The text stays fully visible between keyframes 2 and 3.
4. **Type out:** further on, add keyframe 4 at Start `0%`. The text un-types in reverse.
5. Hold on 100% for at least 0.5–1.5 s, or long enough for a viewer to read it about 1.5 times.
6. Sync: put the first Start keyframe on a downbeat or the start of a vocal phrase. Put the 100% keyframe on the end of a vocal bar or a snare hit.

### Randomized (decode/glitch) typewriter
- Text > Animator 1 > Range Selector 1 > **Advanced > Randomize Order = On**. Characters then appear in random order instead of left to right.
- **Random Seed** (default `0`): set it to any integer to change the order.
- Leave the other Advanced defaults [visual]: Units `Percentage`, Based On `Characters`, Mode `Add`, Amount `100%`, Shape `Square`, Smoothness `0%`, Ease High `0%`, Ease Low `0%`.
- Choose sequential for narrative, subtitle, or retro-terminal typing. Choose randomized for sci-fi decoding, glitch or cyber looks, and frantic intros.

### Per-character wiggle with stop-motion boil
1. Twirl open the text layer. Next to **Text**, click **Animate: > Position**. This creates `Animator 1` with `Range Selector 1` and `Position`.
2. On the `Animator 1` row, click **Add: > Selector > Wiggly**. This adds `Wiggly Selector 1`.
3. Animator **Position = `0.0, 7.0`**. X stays 0 so the text doesn't drift sideways, and Y gives a subtle vertical jitter.
4. Wiggly Selector 1:
   - **Wiggles/Second: `2.0` → `6.0`**
   - **Correlation: `50%` → `0%`**, so each glyph moves independently instead of in unison
   - Leave at defaults [visual]: Mode `Add`, Max Amount `100%`, Min Amount `-100%`, Based On `Characters`, Temporal Phase `0x +0.0°`, Spatial Phase `0x +0.0°`, Lock Dimensions `Off`, Random Seed `0`.
5. Apply **Effect > Time > Posterize Time** to the text layer and set **Frame Rate: `30` → `8.0`**. The smooth 30 fps sliding becomes stepped, hand-drawn boil.

Tuning ranges:
- Displacement Y: 5–10 px (demo 7). Past about 15–20 px legibility drops, so use that only for a deliberate impact shake. Stay Y-only unless you want horizontal jitter as a style.
- Wiggles/Second: 5–8 for energetic type. Below 3 feels lethargic.
- Correlation: 0% for organic chaos. Use >50% only when you want a unified wave ripple.
- Posterize Time: 8–12 fps. Below 6 is too choppy, and above 15 turns smooth and digital again.
- Use this for playful, scrapbook, grunge, or indie styles where static text looks dead and full keyframing would distract.

Pitfalls:
- If the whole word bobs as one card, the wiggle is at layer level (Transform or a `wiggle()` expression). Move it into a text animator with a Wiggly Selector and check that Correlation is 0%.
- If the motion looks floaty or jelly-like, Posterize Time is missing. The expression equivalent on a property is `posterizeTime(8); …`.

### Circular path text (badges, orbits, frames)
1. Type the word or phrase with a trailing space, then paste it repeatedly on one line about 8–10 times (`mask path mask path …`).
2. With the text layer selected, press `Q` to cycle to the **Ellipse Tool**. **Shift-drag** from near the comp center to draw a true circle as a mask on the text layer (`Mask 1`; Mode `Add`, Inverted off [visual]).
3. Text > **Path Options > Path: `None` → `Mask 1`**. The baseline wraps the circle.
4. **Force Alignment = On** spreads the characters evenly around the whole loop, so there's no clump with an empty arc.
5. **Reverse Path**: toggle it if the text sits inside or upside down, or runs the wrong way (clockwise vs counter-clockwise).
6. Defaults [visual]: Perpendicular To Path `On`, First Margin `0.0`, Last Margin `0.0`.
7. To spin: animate **First Margin** with linear keyframes, or an expression like `time * speed` with the speed tied to the track's BPM.
- Use it for stamps and rotating badges, for framing a centered subject (icon, star, portrait), and for looping decorative borders.

### Third-party text tools (seen, not used)
BCC Type On Text **[3P]** (Boris FX Continuum, under `BCC 3D Objects`); uni.Type Cast and uni.Type On **[3P]** (Red Giant Universe, `RG Universe Text`). All techniques above use built-in features only.

## Shape layers: beat-synced morph sequence

A single rectangle plus one parent null carries a full sequence: slit → bar → square → color pop → collapse → stroke "portal" outro. Use shape layers for high-contrast frames, wipes, expanding-line transitions, audio-synced pulses, and graphic accents.

### 1. Draw the base shape
1. Press `Q` to cycle to the **Rectangle Tool**. Drag a horizontal bar in the viewer (no layer selected, so it becomes a new shape layer).
2. In the tool options bar, **Alt+click the Fill label** to cycle None → Solid → Linear → Radial, and stop on **Solid Color** (demo magenta `#E82276` [visual]). **Alt+click Stroke** until it's **None** (red slash). This beats opening the pickers.
3. Center before keyframing anything. Right-click > **Transform > Center Anchor Point in Layer Content** (`Ctrl+Alt+Home` / `Cmd+Opt+Home`). Then open **Window > Align**, set Align Layers to `Composition`, and click the 2nd icon (Horizontal Center) and the 5th icon (Vertical Center).

### 2. Slit → bar (non-uniform scale on the shape)
1. Press `S` and click the chain icon to unlink Scale.
2. Frame 0: **Scale `[2.0, 100.0]%`**, a razor-thin vertical line. Use 2%, not 0%, so the line is visible before it opens.
3. +16 frames: **Scale `[100.0, 100.0]%`**. Opening moves take 14–16 frames.
4. Apply the sharp S-curve (`0.85,0,0.15,1` → `≈0.90,0,0.10,1`), with near-vertical tangents so it bursts out and stops hard. If it feels sluggish, tighten the keyframe gap by 1 frame.

### 3. Bar → square on a beat (on a parent null)
1. Create `Null 1` above the shape. Pick-whip `Shape Layer 1`'s parent to `Null 1` (or choose `1. Null 1` in the dropdown).
2. On `Null 1`, press `S` and unlink Scale. Just before **Beat 4**, add a hold keyframe at `[100, 100]%`. **On Beat 4**, set X down until width equals height (demo `≈[26.0, 100.0]%` [visual]; match it by eye).
3. Apply an S-curve. If the arrival lags the hit, shift both keyframes 1 frame earlier.
- Keep secondary squash and rotation off a layer that already has unlinked non-uniform scale keys. Route them through the parent null.

### 4. One-frame color pop (Fill effect)
1. Apply **Effect > Generate > Fill** to `Shape Layer 1` (Effects & Presets, or **FX Console [3P]** by Video Copilot, `Ctrl+Space`). This puts Color at the top level of Effect Controls instead of deep in `Contents > Rectangle 1 > Fill 1 > Color`.
2. Set Color to the shape's color (`#E82276`) and keyframe it **1 frame before Beat 5**.
3. Step +1 frame onto **Beat 5** and set Color to dark teal (`#1B6E60` [visual]). That gives a hard swap in one frame: old color on beat−1, new color on the beat.

### 5. Collapse to a point, then cut
1. Select the **shape layer**, not the null. Press `S` and **re-link** Scale for a uniform scale.
2. Keyframe `100%` 1 frame before Beat 5. Land **`6.0%`** at Beat 6, or 1–2 frames before it for snappier pacing.
3. Use ~6% as the floor, not 0% or 2%. Near zero, the shape fades into sub-pixel anti-aliasing before the cut. At 6% it's still a crisp point the eye can register.
4. Apply a steep deceleration curve. Put the playhead just after the last keyframe and trim the out-point (`Alt+]` / `Opt+]`), so it disappears on a hard cut.
- If the collapse moves the wrong thing, you keyed the null. Re-select the shape layer.

### 6. Cascading stroke "portal" shockwave outro
1. Rectangle Tool: draw a square about the size of the final square. **Alt+click Fill → None**, **Alt+click Stroke → Solid**, white `#FFFFFF`, Stroke Width about **8–10 px** [visual].
2. Center Anchor Point in Layer Content, then comp-center it with Align.
3. Trim the layer to exactly **2 frames**.
4. `Ctrl+D` ×3 for 4 layers total. Stagger them in sequence by 1–2 frames each.
5. Scale each one up progressively [visual]: `~100%`, `~160%`, `~230%`, `~320%`. The last one exceeds the canvas.
- Two-frame steps read as a percussive burst outward. Longer layers read as static boxes.

### Shape checklist
- Anchor centered and comp-aligned before the first keyframe.
- Transform arrivals on beat markers, color swaps in one frame, outro steps 2 frames each.
- Morph floor is 2% (entry slit), collapse floor is ~6% (exit).
- Nudge a late-landing keyframe pair 1 frame earlier.
