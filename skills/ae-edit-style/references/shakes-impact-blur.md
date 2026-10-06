# Shakes, Impact Frames, and Blurs

Covers the camera-shake system (impact + ambient tiers, transition shakes), blur recipes (clip-start, full-clip, transition, build-up), and impact accents (one/two-framers, Levels flashes). Read this when you are adding punch to cuts, hits, or transitions, or when you are diagnosing an edit that feels static, muddy, or weak.

Sources: How To Get Started With Shakes (AE ESSENTIALS 2) https://youtu.be/EC9L53bIVkw · How To Easily Make Good Blurs In After Effects (AE ESSENTIALS 5) https://youtu.be/xBC0cB6jXJk · The Easiest Way To Add Impact (AE ESSENTIALS 6) https://youtu.be/qM11YaoLvZA · How To Learn The Most Important Thing In Editing (EDITING OUTLINES 1) https://youtu.be/cK_GkB3ORIM · Graphs Are Easier Than You Think To Master (EDITING OUTLINES 2) https://youtu.be/plIPW2NAcY8

## Conventions shared by every recipe

- Put every effect on its own trimmed **Adjustment Layer** (`Ctrl+Alt+Y` / `Cmd+Option+Y`) above the footage. Never apply to footage directly; separate layers keep timing tweaks and curve copying cheap.
- Name layers by role (`blur`, `levels`, `shake 1`, `shake 2`). Typical stack, top to bottom:
  ```
  shake 1   Adjustment  S_Shake     impact tier (short, violent)
  shake 2   Adjustment  S_Shake     ambient tier (full clip, gentle)
  levels    Adjustment  Levels      exposure flash / decay
  blur      Adjustment  Gaussian Blur
  clip pre-comps (Twixtor top layer / time-remapped bottom layer)
  ```
- Apply effects via Effects & Presets (`Ctrl+5`) or FX Console (Video Copilot, third-party, `Ctrl+Space`, type e.g. `s_shake`, `glow darks`).
- Step frames with `Ctrl+Left/Right Arrow` or `Page Up/Down`. Trim in/out to the playhead with `Alt+[` / `Alt+]`. Duplicate with `Ctrl+D`.
- Ease with **Flow** (aescripts, render.tom & Zack Lovatt, third-party) or the AE Graph Editor. Flow values below are cubic-bezier `[x1, y1, x2, y2]`. Copy a curve between clips: select source keyframes → Flow **Read Values** (arrow icon) → select target keyframes → **APPLY**. Reuse the shape as a starting point, then re-tune the handles per shot, because each shot's motion differs.
- Never leave keyframes on plain `F9` Easy Ease (33.33% influence). It lingers in the middle and reads as robotic.
- Align every peak (shake, blur, Levels) exactly on the audio transient / cut frame. Mark the beat with a timeline marker on the **first frame of the incoming clip** (numpad `*`).

Third-party plugins in this file: Boris FX Sapphire (`S_Shake`, `S_DissolveShake`, `S_GlowDarks`), Boris FX Continuum (`BCC Directional Blur`), OLM blurs (free alternatives), Flow, FX Console. Everything else is built in.

## Dual-shake system (canonical)

One shake reads as either an earthquake or a vibration, so run two `S_Shake` layers together. The **impact** tier gives the hit and the **ambient** tier keeps the frame from ever settling. Rule of thumb: high amplitude must resolve fast, and long-duration movement must stay low amplitude.

### Impact shake (`shake 1`)

1. Adjustment layer starting on the cut / hit frame. Apply Sapphire `S_Shake` (`Effect > Sapphire Stylize > S_Shake`).
2. `Wrap`: **Reflect**, which fills the edges pulled in by displacement [visual].
3. `Frequency`: high. **6.0–7.0** (Outlines 1, used 7.0). Outlines 2 showed ~**8–10** [visual] for a heavier hit.
4. `Amplitude`: Outlines 2 set **11.0** on the aggressive layer.
5. Keyframe the intensity: Outlines 2 keyframes `Dissolve %`, and Outlines 1's notes describe the same keyframes on amplitude. Peak **20–25** on the hit frame (Outlines 1 used 25, Outlines 2 used 21%), then **0** after **6–8 frames** (7 is the default choice).
6. Graph: stiff, with an instant peak on frame 1 and a rapid falloff. Flow value shown in Outlines 2: `[1.00, 0.00, 0.27, 1.00]` [visual]. Target the shape (max impulse immediately, then pull the bottom handle down a little so the shake stays visible before it dies). Keep it stiff: a stiff falloff also hides repeated/reflected edge tiles under motion.
7. Axes: open `X/Y/Z/Tilt Random Amp`, boost the axes that match the hit or transition direction, and lower the others (see the axis table below).
8. **Momentum carry (optional third keyframe):** if the impact dies in the first ~60% of the clip and the tail feels dead, add a keyframe of **4%** `Dissolve %` on the clip's last frame and graph that segment moderately stiff. Energy then ramps slightly into the cut. The general range for this residual is **1–4%**.

### Ambient shake (`shake 2`)

1. Separate adjustment layer spanning the **entire clip/scene**. `S_Shake`, `Wrap: Reflect`.
2. `Frequency`: low. **2.5–3.0** (Outlines 1, used 2.5). Outlines 2 showed ~1–3 [visual].
3. `Amplitude`: low, ~**1–3** (Outlines 2 [visual]).
4. `Tilt Shake`: small rotational sway, ~**8%** (Outlines 1 [visual]; entered as 0.08 or 8 depending on the field scale).
5. Keyframe the intensity: **~8** at the cut, easing to a **non-zero floor** at the clip end. Floors used: **1.5** (Outlines 1 tested 2.0, settled on 1.5) and **1.3%** (Outlines 2). Keep the floor between 1.3 and 2.0 so the camera keeps drifting right up to the next cut.
6. Graph: loose. Drag the top handle well down into the middle so the motion persists across the shot instead of dropping off early.

### Stiff vs. loose graphs

- **Stiff:** impacts on snares/kicks/gunshots, heavy shake amplitudes (to hide edge tiles), and keyframes that sit close together.
- **Loose:** ambient float, blurs, and exposure decays that must stay visible over several beats.
- A loose curve on a high-amplitude shake with widely spaced keyframes creates the "earthquake" error. Tighten the keyframe spacing or stiffen the graph.
- Also avoid shoving every handle into the corners (`0,0` / `1,1`). The effect then flashes for a frame and vanishes, leaving dead space. Keep handles in the middle ground: enough tension to punch, plus a tail that decays across the shot.

## Transition shake (S_DissolveShake, AE Essentials 2)

Use this on zoom/scale and slide/whip transitions, where the shake needs a build-up into the cut as well as a decay after it.

1. Adjustment layer covering the transition clip. Step back **8 frames** from the cut (`Ctrl+Left` ×8) and drag the in-point there. This gives an 8-frame build-up.
2. Apply Sapphire `S_DissolveShake`.
3. `Mo Blur`: **off**. The default smears line art.
4. `Frequency`: **5.0** baseline (lowered from default to remove buzzing jitter). For high-energy slides use **6.0** (possibly 6.5 [visual]).
5. `Amplitude`: default 1.0. Raise to **5.0** for aggressive slides.
6. Axes by transition type:

   | Transition | X Random / Wave | Y Random / Wave | Z Random / Wave | Tilt Random / Wave |
   |---|---|---|---|---|
   | Zoom / scale | 5 / 0 (default 192) | 5 / 0 (default 108) | **100 / 30** | **2.3 / 0.6** (tried 1.0/0 → 1.5/0.3 first) |
   | Horizontal slide / whip | **192 (default) / 60** | 3 (anything < 5) | default | 1.0 |
   | Vertical slide (extrapolated, not demoed) | low (3–5) | high random + wave | — | light |

   Keep suppressed axes at a small non-zero value (**3–5**) rather than 0. That keeps the camera from looking locked on rails while the dominant axis still leads. Only drive axes that match the transition's motion. A Y shake on a horizontal whip muddies it.
7. Keyframe `Dissolve %`: **0%** at the layer start (8 frames before the cut), **25%** exactly on the cut frame, **0%** at the layer end (the end of the incoming transition animation). Use 25% for every transition in the project so cuts feel consistent.
8. Graph in Flow: 0→25 is an aggressive ease-in (slow start, velocity spiking at the cut). 25→0 is the reverse (instant high-velocity drop into a gradual settle). If it wobbles too long after the cut ("jelly camera"), steepen the decay by pulling the upper-left handle up and inward.

### Fixing a bad shake hit (both systems)

Do these in order, and leave the keyframes alone:
1. Change `Seed`. It reshuffles the random path while keeping amplitude and frequency.
2. Nudge the whole adjustment layer **±1 frame** and keep whichever frame lands cleanest on the cut (Shea moved it 1 frame earlier).
3. Only then adjust curves or amplitudes.

## Blurs

Match the blur type to the motion vector: Gaussian for cut softening, Radial **Zoom** for scale transitions, Radial **Spin** for rotational spins/whip tilts, and Directional for slides. Keep intensity moderate. Values of 50–100+ turn the frame to mud.

### Clip-start softener (Gaussian, AE Essentials 5)

1. Adjustment layer trimmed exactly to the clip. `Effect > Blur & Sharpen > Gaussian Blur`. Use the modern effect, not **Gaussian Blur (Legacy)**.
2. `Blur Dimensions`: Horizontal and Vertical. `Repeat Edge Pixels`: **on**, to stop dark border fringing.
3. `Blurriness`: **15–16** on the clip's first frame, then **0** on frame **end − 1**. Go up to 18 only for noisy or high-contrast clips.
4. Select both keyframes → `F9`, then reshape into a front-loaded decay (fast drop right after the cut, gentle landing at zero). Flow ≈ `[0.15, 0.99, 0.27, 0.98]` [visual]. Copy it to the other clips with Flow Read Values.
5. Put one of these at the head of every major cut. It must not span the cut. Keep the zero keyframe inside the clip, never on the next clip's first frame.

### Full-clip lingering blur (Outlines 2 variant)

A heavier version that dissolves across the whole shot.
1. `blur` adjustment layer (Normal mode), Gaussian Blur, H+V, Repeat Edge Pixels on.
2. `Blurriness` **20–27** on the cut's first frame (23.3 seen on screen), then **0** on the clip's **last frame**, so the decay spans the full distance to the next cut.
3. Graph: pull the top (peak) handle **down** away from the top wall so the blur stays visibly thick through the middle frames. Pull the bottom (zero) handle slightly **out** into the graph instead of pinning it to the floor. The result is a delayed falloff that clearly dissipates across the clip.
4. Choose between the recipes: use 15–16 with a front-loaded curve for a clean, quick softener, and 20–27 with a middle-ground curve when the blur should read as part of the hit.

### Anticipatory build-up blur (before a transition / slow-mo onset)

1. On the lead-up, keyframe low/zero blur at the start of the pre-action and **peak** blur on the frame right before the action cut or Twixtor ramp.
2. Graph with a loose, gradual acceleration so the tension visibly builds.
3. On the incoming hit, start at maximum blur and decay across the scene with the lingering curve above.

### Scale / zoom transition blur (Radial Blur)

1. Adjustment layer exactly **4 frames**, centered on the cut: 2 frames on the outgoing tail, 2 frames on the incoming head.
2. `Effect > Blur & Sharpen > Radial Blur`. `Type`: **Zoom** (default is Spin). `Quality`: Draft for previews, Good for final [visual]. `Center`: the focal point (comp center `960,540` at 1080p by default [visual]).
3. `Amount` per frame: **8 → 16 → 16 → 8** (cut−2, cut−1, cut, cut+1). Linear/default interpolation is fine. It works as an instantaneous optical burst.
4. Use it only on scale moves (quick zooms into eyes, faces, wides), not on slides or pushes.

### Slide transition blur (Directional)

1. Same 4-frame layer centered on the cut.
2. `BCC Directional Blur` (Boris FX Continuum), or the free **OLM Directional Blur**. (OLM Radial Blur is the free option for zooms.)
3. `Angle` along the travel direction (0° horizontal / 90° vertical [visual]).
4. `Blur Amount`: **8 → 18 → 18 → 8**. Slides peak slightly stronger (17–18) than zooms (16).
5. Keep transition blurs to exactly 4 frames. Longer hides the choreography, and shorter doesn't register.

## Impact frames: one-framers and two-framers (AE Essentials 6)

A one/two-framer is an adjustment layer (or solid) lasting 1–2 frames that makes a hard luminance or color jump at the cut. Use them on almost every transition, hard cut, beat drop, and snare, even if subtle. How they are arranged and how much they contrast matters far more than which effect is on them. Spend most of the time on frame placement, not sliders.

### Build procedure

1. Put a marker on the first frame of the incoming clip (the beat).
2. Step back 1 frame (the last outgoing frame). `Ctrl+Alt+Y`, then trim to **1 frame** (`Alt+[`, advance 1 frame, `Alt+]`).
3. `Ctrl+D` twice to get three one-framers. **Spread them across adjacent frames** on both sides of the marker (an anticipation frame before, recoil frames on/after the cut). Never stack them on the same frame, because the color/exposure shifts compound uncontrollably.
4. Give each layer a look:
   - **Bright:** `Effect > Color Correction > Levels`, Channel RGB, `Input White` **255 → ~150**. Leave Input Black 0, Gamma 1.0, Output Black 0, Output White 255. No keyframes: the 1-frame layer boundary is the step.
   - **Dark:** `Effect > Color Correction > Curves`, RGB. Drag a lower-quadrant (shadow/midtone) point steeply down to crush the frame [visual].
   - **Dark chromatic glow:** Sapphire `S_GlowDarks` (`Effect > Sapphire Lighting`). Place and size its on-screen ellipse over the falloff area and push the sliders for deep saturated color. Then add `Exposure` (`Effect > Color Correction > Exposure`) **below it on the same layer** at about **−0.5 to −1.5** [visual]. That keeps the saturated glow while holding the frame dark.
   - **Classic flash:** `Layer > New > Solid` (`Ctrl+Y`), white `#FFFFFF`, comp size, 1 frame over the cut. It's the standard baseline, but prefer the custom adjustment stacks above for variety.
5. **Contrast rule:** alternate luminance. The strongest pattern sandwiches a bright frame between darks (**Dark → Bright → Dark**). Three brights or three darks in a row read as flat and muddy.
6. Play it back with audio, then rearrange:
   - Extend a frame to **2 frames** (a two-framer) when a dark dip or color shift has to register consciously, or when the frame vanishes during heavy motion. Keep 1 frame for subliminal ticks and high-frequency rhythm.
   - Stagger the bright frame by 1 frame to vary the cadence. The layout demoed: **2 frames dark → [cut/marker] → 1 frame gap → 1 frame bright → 1 frame dark glow** [visual].

### Levels exposure decay (Outlines 2)

This is the longer counterpart to the Levels one-framer and is paired with the full-clip blur.
1. `levels` adjustment layer directly above `blur`. Apply Levels and keyframe the brightness (`Input White` / RGB output [visual]) with its peak on the impact frame.
2. Start it on the same frame as the blur's peak keyframe and give it the **same curve shape** (top handle dipped, extended falloff) so flash and blur decay together.
3. Run it slightly longer than the blur if you want a lingering glow. Like the blur, let it decay across the shot rather than stopping mid-clip.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Frame freezes after the hit; shot dies mid-clip | Ambient shake floor 1.3–2.0. Add a 1–4% end keyframe on the impact shake. Drag the blur/Levels zero keyframe to the clip end. |
| Shake smears line art | `Mo Blur` off (S_DissolveShake). |
| Buzzing jitter | Lower `Frequency` (5 for transition shakes, 2.5–3 for ambient). |
| Long jelly wobble after the cut | Steepen the decay handle. Shorten the impact to 6–8 frames. |
| Earthquake feel | High amplitude + loose curve + far keyframes. Stiffen the curve or tighten the spacing. |
| Shake fights the transition | Suppress orthogonal axes to 3–5. Drive only the axes that match the motion. |
| Camera looks on rails | Don't zero the secondary axes. Keep them at 3–5. |
| Awkward displacement on the cut frame | `Seed`, then nudge the layer ±1 frame. |
| Empty/tiled edges show during shake | `Wrap: Reflect`, plus a stiff falloff. |
| Blur looks muddy | Stay at 15–18 (transitions 16–18). Use modern Gaussian Blur, not Legacy. |
| Dark fringe at frame borders | `Repeat Edge Pixels` on. |
| Motion on a slide looks disorganized | Use Directional blur along the slide angle, not Radial Zoom. |
| Impact accents feel flat | Alternate dark/bright. Unstack same-frame layers. Promote the weak frame to a two-framer. |

Scripting: see motion-and-timing.md §3f.
