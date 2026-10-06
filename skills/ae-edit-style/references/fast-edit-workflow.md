# Fast Edit Workflow (Timed / Random-Constraint Edits)

How to plan and finish a complete edit under a hard time box (90 minutes) with randomized inputs: phase order, seed evaluation, triage rules, the recipes that pay off fastest, and the post-mortem loop. Read this when planning an edit end to end, when time or scope is limited, or when an edit is stalling.

Sources: MY FIRST TIME MAKING AN EDIT IN 90 MINUTES (Aimless Edits 1) https://youtu.be/BGRU99Qe-NY · ONE OF MY BEST EDITS IN JUST 90 MINUTES (Aimless Edits 2) https://youtu.be/9Zju4HcAvwM · SPINNING WHEELS TO MAKE A RANDOM EDIT (Aimless Edits 3) https://youtu.be/aUBkIJWSLbs

---

## 1. Challenge format (the constraint system)

- **Seed by randomizer.** Spin one web picker wheel for the anime (sometimes down to a specific episode) and a second for the song. Accept the result unless it fails the mockup test (§3).
- **Rerolls are scarce.** 3 rerolls for the *whole series* of challenges, not per edit. Scarcity forces you to commit to most seeds and spend a reroll only on a real dead end.
- **Hard clock.** 90 minutes total, tracked by a visible desktop countdown (Hourglass, third-party freeware). Stop when it rings; whatever is on the timeline is the edit.
- **Prep cap.** Downloading footage, pulling audio, and setting up the project get at most 25 minutes of the 90 (rule added in Edit 2).
- **Target length.** Aim for a short piece, about 30 seconds (Edit 3's final was ~30 s). Length is the main scope lever. Cut the song down to fit the clock rather than stretching the clock to fit the song.

For self-imposed practice, keep all four: random seed, limited rerolls, visible clock, prep cap. Dropping the visible clock is what lets perfectionism back in.

---

## 2. Phase order and time budget

Run the phases in this order. The minute budgets below are my own split, worked out from where each session ran long; the videos don't prescribe them.

| # | Phase | Budget | Output |
|---|-------|--------|--------|
| 0 | Spin seeds, run mockup test, reroll if needed | ~5 min | Locked anime + song |
| 1 | Prep: download 1–2 episodes, pull audio, set one design objective | ≤25 min (hard cap) | Project with footage + audio |
| 2 | Audio edit: cut the song to length | ~5 min | Final-length audio |
| 3 | Scrub and cull clips into a small pool | ~10 min | ~10–15 clips (Edit 2: exactly 11) |
| 4 | Rough-in: mark beats, place every cut on the timeline | ~15 min | Full-length rough cut, no effects |
| 5 | Section treatments: ramps, grades, text, graphics per section | ~25 min | Every section has its look |
| 6 | Texture/cleanup passes (flash frames, fills, re-record) | ~10 min | Problems fixed, grit added |
| 7 | Global polish on the master precomp (shake, drift) | last ~3–5 min | Final |

Phase rules:
- **Audio before picture.** Lock the audio length first (§4). Every later timing decision depends on it.
- **Rough-in everything before polishing anything.** Place all sequential cuts with baseline values first (e.g. shake Amp 1.0 / Freq 3.0), then come back to nuance. This rule came out of Edit 3, where looping one 2-second section to judge a shake ate the clock.
- **Global effects go last, on the master precomp.** Edit 3 added its position wiggle in the final seconds before the buzzer (§6.8). A last-pass global effect lifts the whole piece and costs almost nothing.
- **Checkpoint at the halfway mark.** If less than the full rough cut exists at ~45 min, freeze all new ideas and finish the rough cut. In Edit 1, having 25 minutes left while still on Roto Brush was the crisis point.
- **Preview at Quarter resolution** (Composition panel resolution dropdown) during phases 3–6 so scrubbing stays real-time on heavy stacks. Switch to Full only for the final watch.

---

## 3. Constraint-driven ideation

### Seed evaluation (mockup test)
1. On each spin, picture 2–3 concrete shots cut to the song's most distinctive moment.
2. If you can't picture any usable pairing, reroll immediately. Edit 2 burned a reroll on the first anime roll because it clashed with a high-energy glitch-pop song. Rerolling late wastes prep time.
3. Treat productive conflict as a pass. Edit 2 paired a colorful glitch/IDM track with a bleak grey cyberpunk anime. The friction read as editorial and fresh, and it became his favorite of the series.
4. Look for an **aesthetic bridge**, a trait the two seeds share or one can carry for the other. Edit 2's grey/black palette and flat vector-like art gave a neutral canvas for saturated glitch accents.

### Song suitability
- Prefer tracks with open rhythmic structure: clear accents, vocal chops, and tonal shifts you can map to visuals. Edit 1 wanted a song loose enough in vibe to take somewhere.
- Monotonous, dense tracks with no isolatable accents are the weak case. Plan around their few hits or spend a reroll.

### One design objective
- Before opening AE, write one sentence for the look (Edit 2: "experimental"; Edit 3: raw, intimate, mixed-media). Judge every later idea against it.

### Commit instantly
- Take the first idea that fits the objective and put it on the timeline now. Edit 2 worked because every idea stuck the moment he tried it. Keep A/B-ing only where it's cheap, like flash-frame color (§6.4).
- Cap effect browsing. Edit 3 tried CC Split, CC Color Offset, CC Tiler, and several BCC stylizers before landing on S_Threshold. Give one look about 2 minutes of browsing, then take the best candidate so far.

### Section-to-section contrast
- Plan the edit as a few sharply different sections, not one uniform grade and tempo. Edit 2 went from gritty monochrome character shots to a sterile white editorial card to a datamosh collapse to a dot-matrix screen.
- Hold the contrast together with **one persistent unifier**: a constant border frame (§6.2), a single hero hue (Edit 1's magenta), or a consistent texture (Edit 3's manga/threshold black-and-white).
- Mix media for grit: manga scans, marker-style handwriting, physical re-recording (§6.6). All-digital vector work reads sterile against raw, emotional songs.

---

## 4. Audio edit under a time cap

- If the song has a build longer than ~20 s, cut out the middle and butt-splice the intro straight into the emotional release or drop. In Edit 3 he cut the track roughly in half.
- Cut on a downbeat or phrase boundary so the splice sounds intentional. Add a short crossfade on the audio layer if the tails click.
- Mark beats with numpad `*`: with a layer selected it adds a layer marker, with nothing selected a comp marker. Tap along during RAM preview, then snap keyframes and cut points to the markers.

---

## 5. Triage: what to prioritize and what to skip

**Spend time on (highest impact per minute):**
1. Cut placement on transients: 1–2-frame cuts, flash frames, staggered cut rhythms.
2. Bold color decisions: a single hero hue, tints, threshold looks (one effect each, section-wide on an adjustment layer).
3. Framing devices: an iris mask, a constant border, a white negative-space card.
4. Speed ramps on a few expressive moments.
5. A single global pass on the master precomp.

**Skip or cap:**
- **Roto Brush on multi-second shots.** Limit roto to one high-impact frame or a ~0.5 s moment. Precompose first. In Edit 1, roto took far longer than expected.
- **Manual clone patches over lit backgrounds.** Go straight to Content-Aware Fill (§6.7). In Edit 3, a duplicated-wall patch plus Gaussian Blur still left hard edges and mismatched lighting.
- **Looping one short section** to fine-tune shake or ease. Set baseline values and move on.
- **Hoarding footage.** Download 1–2 episodes, not the series. Scrubbing is the biggest hidden time sink.
- **Full-resolution preview** before the final watch.

---

## 6. Recipes

### 6.1 Techniques covered elsewhere (one-line pointers)
- Hero-hue isolation (push one hue hard, keep the rest near monochrome): **color-light-blending.md**.
- Tritone + S-curve Curves candlelight grade (Tritone Blend With Original 0–50%): **color-light-blending.md**.
- S_Threshold two-tone silhouette at emotional peaks (Sapphire): **color-light-blending.md**.
- Starburst flare on the drop (Screen/Add solid, 1-frame attack, ~4–6-frame decay): **color-light-blending.md**.
- Halftone / dot-matrix screen and macro zoom into the dots: **color-light-blending.md**.
- Speed ramp via Time Remapping (`Ctrl+Alt+T`) or Twixtor with steep ease into slow motion (Flow ≈ `0.70, 0.05, 0.40, 0.95` [visual]): **motion-and-timing.md**.
- S_Shake tuning by vocal intensity (quiet: Amp 0–0.5, Freq 1–2; strained: Amp 0.8–1.1, Freq 2–3, extra X amplitude, Motion Blur on, shutter 180) [visual]: **shakes-impact-blur.md**.
- 3D text fly-through ("BECAUSE" on Z with slight Y rotation, motion blur on): **camera-text-shapes.md**.
- Trim Paths vector accent lines and the white editorial type card: **camera-text-shapes.md** (palette in §6.2).
- Datamosh burst (4–8 frames of rising macroblock tearing, then a hard cut) and Roto Brush subject isolation: **transitions-compositing.md**.

### 6.2 Persistent border frame (unifier for high-contrast sections)
1. Add a Shape Layer at the top of the master comp. Draw a rectangle at comp size (1920×1080).
2. Fill: None. Stroke: deep navy (≈`#0B0E2B` [visual]). Width ~12–16 px, inset at the canvas edge.
3. Leave it on for the whole edit, through transitions, so wild style shifts read as one piece.
4. Accent lines under the frame (Edit 2): salmon, light pink, and dark pink, plus yellow, mint, sky blue, and white [visual], in diagonal Bezier fans around the subject. Animate Trim Paths End 0→100% on glitch hits with a hard ease-out. Put bright accents only on monochrome footage or pure-white space.

### 6.3 Cut staggers
- **"Two, two, two… one at the end"** (Edit 2): swap clips or graphic elements every 2 frames for three swaps, then hold the last one to the end of the bar. Use it for fast micro-percussion without clutter.
- **Staccato intro** (Edit 1): 4 quick cuts on 4 snare hits against a flat hero-color solid before the drop.

### 6.4 1-framer / 2-framer flash solids
1. `Ctrl+Y` makes a solid: white `#FFFFFF` for bright/high-key targets, black `#000000` for dim/low-key targets.
2. Place it on the transient and trim it to 1 frame (`Alt+]` at the next frame).
3. RAM preview. Extend to 2 frames if the flash reads as subliminal, drops out of preview, or sits on a sustained crash rather than a dry snare. Keep it at 1 frame for a shutter-like subconscious flash.
4. Switch grade on the next clip (e.g. a hard Curves change) so the flash separates two looks.
- Edit 3: a white 1-framer between dark emotional shots washed out the mood. A black flash widened to 2 frames fixed it.

### 6.5 Circular iris montage on vocal chops (Edit 1)
1. Add a black solid (`#000000`) at the top. Draw a centered Ellipse mask and set it to **Subtract**, which leaves a round peephole.
2. Under it, cut 2–4-frame clips, each starting on the transient of one vocal repetition.
3. The static black surround anchors peripheral vision, so you can cut much faster inside the hole without disorienting the viewer.
4. To end: keyframe the mask to close (scale the mask or its layer from 100% to 0% with a snappy ease-in) to full black, then cut to the end card/logo.

### 6.6 Physical camcorder re-record (Edit 3, analog texture)
1. Finish the section in AE (e.g. the manga + handwriting card).
2. Play it full-screen on the monitor and film the screen with a handheld camcorder (he used a Sony Handycam). Let some natural hand sway and focus breathing through.
3. Copy the file off the card, import it, and lay it over the digital version at the same cut point, trimmed to the beat.
- This gives real moiré, sensor noise, and interlace artifacts that plugins only approximate. Use it on one or two intimate moments, not the whole edit.

### 6.7 Content-Aware Fill object removal (built-in)
1. Trim or precompose the clip down to the shot that needs the fix. Set the work area to it.
2. With the Pen tool (`G`), draw a closed mask tightly around the distraction (Edit 3: a ceiling lamp). Set Mask Mode to **Subtract**.
3. Open `Window > Content-Aware Fill`. Set Fill Method to **Surface** for static walls and flat or textured planes; use **Object** only for a moving foreground subject. Range: **Work Area**. Turn on Lighting Correction if the background luminance shifts.
4. Optional for hard cases: make a clean reference frame (he rendered a single frame out and re-imported it) to guide the fill.
5. Click **Generate Fill Layer**, then precompose the fill with the clip (`Ctrl+Shift+C`) and put it back in the master timeline.

### 6.8 Master-precomp drift (final-seconds global pass)
1. Precompose the finished section or the whole edit.
2. Apply `Animation > Presets > Transform > Wiggle - position`, or type "wiggle" in FX Console (`Ctrl+Space`).
3. Wiggle Speed ≈ 1.0/s (1.0–1.05 [visual]), Wiggle Amount 12 px. The result floats rather than shakes.
- Expression equivalent on Position: `wiggle(1, 12)`. Scale the layer up slightly (~102%) if the edges show.

### 6.9 Low-frame-rate impact (Posterize Time)
1. Enable Time Remapping on the clip and place beat markers on the drum hits.
2. Key Time Remap so the move (Edit 3: a character collapsing) fits exactly between markers.
3. Add `Effect > Time > Posterize Time` at 8–12 fps [visual] for choppy, cel-like violence.
- Posterize for erratic, distressed motion; smooth Twixtor interpolation for sustained cinematic moves. Timing detail: **motion-and-timing.md**.

### 6.10 Hand-lettered lyric card with manga stills (Edit 3)
1. White solid background. Set the lyric as a stacked block (`I LOVE(D)` / `EVERYTHING` / `ABOUT YOU`) in a rough marker/Sharpie font, black.
2. Recolor only the meaning-changing glyphs, e.g. the "(D)" in vivid red (≈`#ED1C24` [visual]), to mark the tense change.
3. Add black-and-white manga panels of the same characters and wrap the text around the figures.
4. Add a light S_Shake to match vocal strain (**shakes-impact-blur.md**), then consider the camcorder pass (§6.6).
- Clean sans-serif reads commercial against raw lyrics. Pick the messy font when the song is vulnerable.

---

## 7. Beat-to-treatment map (all three edits)

| Audio event | Treatment |
|---|---|
| Snare / rimshot clicks | Micro jump cuts, angle changes, scale pumps; staccato 4-cut runs |
| Bass drop / big downbeat | Full-frame flare, flash, inversion, chromatic split |
| Vocal-chop loops | Fast cuts confined inside a static frame (iris §6.5) |
| IDM hi-hats / glitch stutters | 2-frame staggers, Trim Paths line snaps, datamosh bursts |
| Long melodic or vocal phrase | Slow-motion ramp holds, negative-space type cards |
| Scream starts / heavy drum hits | 1–2-frame flash solids, then a grade change |
| Strained vocals | Higher-amplitude shake with horizontal bias |
| Build longer than ~20 s | Cut it (§4) |

---

## 8. Speed tooling

- **FX Console** (Video Copilot, free, third-party): `Ctrl+Space`, type a few letters ("POS" for Posterize Time). This replaces menu digging.
- **Flow** (third-party panel) docked for one-click bezier presets on ramps and graphics.
- Shortcuts used across the sessions: `Ctrl+Y` solid, `Ctrl+Alt+Y` adjustment layer, `Ctrl+Alt+T` time remap, `Ctrl+Shift+C` precompose ("Move all attributes into the new composition"), `Alt+]` trim out-point, `Alt+W` Roto Brush, `G` Pen, numpad `*` marker, `F9` Easy Ease.
- Optional prep utility: an external AI upscale/interpolation tool (2×, 60 fps) run on the few clips you'll ramp [visual]. It counts against the 25-minute prep cap.

---

## 9. Self-critique loop

Run this after each timed edit and carry the fixes into the next one:
1. **Where did the clock go?** Name the single biggest overrun (Edit 1: Roto Brush; Edit 3: re-looping shakes and the failed manual patch). Turn it into a rule for next time, like the roto cap and "rough-in first" in §5.
2. **Which ideas stuck on first try?** Edit 2 felt like his best because every idea landed immediately. Note what made that possible: few clips, clear objective, a strong aesthetic bridge.
3. **Did the contrast hold together?** Check that there's one persistent unifier across sections (§3).
4. **Flash and cut sanity:** at full-res playback, check every 1-framer registers and none blows out a dark scene.
5. **Watch the final once uninterrupted** before judging. Fix nothing after the buzzer. Log what you would fix instead.
