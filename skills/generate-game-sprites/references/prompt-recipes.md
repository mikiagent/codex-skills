# Prompt Recipes

## Character Animation

Ask for a single target, one animation at a time, and a fixed frame count. Specify:

- Reference-first pipeline: create or inspect a neutral model/turnaround sheet before animation. Use the approved side-view pose as the reference for every animation state, so walk, attack, hurt, and death keep the same silhouette, weapon side, proportions, scale, camera, outline, and palette.
- View: side view for platformers, 3/4 side for action RPGs, top-down 3/4 for roguelikes.
- Anchor: feet, claws, or contact point planted on the same ground baseline, centered in every frame. If needed, prompt for a thin temporary baseline marker in a key color not used by the sprite, placed just below the contact point, then remove it after measuring `groundY`.
- Motion arc: beginning, anticipation, action, recovery, return-to-idle.
- Walk mechanics: alternating contact, down, and passing poses, not a hop or slide. Use `../assets/references/141-Female_Walk_Dummy_Long.gif` as the local reference for the stride structure.
- Extraction constraints: solid chroma-key background plus thick dark silhouette outline when transparent or white extraction has produced padding, holes, or halos. Pick a key color absent from the sprite. Use green (`#00ff00`) for non-green sprites; use magenta (`#ff00ff`) or cyan (`#00e5ff`) for forest, plant, poison, drake, grass, leaf, or green-clothed sprites. For red/orange/fire/blood sprites, avoid magenta/pink backgrounds and use green (`#00ff00`) or cyan (`#00e5ff`) when absent.
- Constraints: no shadows, no labels, no frame numbers.

Useful defaults:

- Idle: 4 or 8 frames at 6-8 fps, breathing/weight shift with a subtle knee bounce and at least one blink. Feet stay planted on the shared baseline; the bounce comes from knees bending and torso settling, not a moving crop.
- Walk: generate by itself as a single animation sheet. Use 8 frames at 10-12 fps: contact, down, passing, push-off/up, opposite contact, opposite down, opposite passing, opposite push-off/up. The back foot must visibly swing forward and become the front foot.

Walk prompt clause:

```text
Walking row must follow an 8-frame side-view walk-cycle reference: contact, down, passing, push-off/up, opposite contact, opposite down, opposite passing, opposite push-off/up. Frame 1: front foot lands heel-first and rear toe touches ground. Frame 2: body drops slightly, rear heel lifts. Frame 3: rear leg passes under the body. Frame 4: body reaches highest point; support foot is near the middle under the body and pushes off the ground while the opposite leg hangs behind with knee bent before swinging forward. Frame 5: opposite foot lands heel-first with arms and legs reversed from frame 1. Frame 6: body lowers onto new front leg, trailing heel rises. Frame 7: trailing leg passes under body. Frame 8: body rises as planted foot pushes off and the opposite knee moves forward, with the other leg hanging behind before the loop. Loop smoothly back to frame 1. Head and torso bob down on frames 2 and 6, up on frames 4 and 8. Keep the bob subtle, not a hop. Show one foot planted while the body passes over it; shoulders and hips counter-rotate. Reject static legs, bouncing in place, sliding, or same-foot-forward poses.
```

For difficult characters, scaffold the walk as 4 key poses before asking for the final 8 frames:

```text
First solve the walk as four readable silhouette poses: A legs apart/contact, B legs together/passing under the hips, C opposite legs apart/contact, D opposite legs together/passing under the hips. Then expand those into 8 frames with in-betweens. In the final row, frames 1 and 5 must be legs-apart contact silhouettes, and frames 3 and 7 must be legs-together passing silhouettes. If the sheet lacks both legs-apart and legs-together frames, it is not a valid walk cycle.
```

Generate walking separately from idle/attack/hurt/death when quality matters. If the output hops, diagnose these likely causes before regenerating: the prompt asked for too many states at once, both legs are hidden by a robe or cape, every frame was center-cropped to a different baseline, the runtime adds vertical walk bobbing, or the frames never reach opposite contact and push-off poses. A passing frame is not enough; the front foot must visibly change sides at least once, and one frame must show the supporting foot under the body while the opposite leg trails behind.
- Attack: 6 frames at 12 fps, anticipation, strike, follow-through, recover.
- Hurt: 3 or 4 frames at 10 fps, readable recoil.
- Death: 6 or 8 frames at 8 fps, final resting pose.

Reference handoff clause:

```text
Use the provided side-view reference sprite as the identity lock. This animation must keep the same character, proportions, armor/clothing, weapon side, silhouette, palette, outline thickness, camera angle, scale, and foot/contact anchor. Generate only this one animation state. Do not redesign the character between frames or between animation states.
```

Ground anchor clause:

```text
Keep the feet/contact point aligned to the same ground baseline in every frame. The body may squash, lean, recoil, or bob inside the animation, but the frame crop and contact baseline must stay stable so the sprite does not bounce during playback.
```

## Props, Items, and Icons

Generate one asset per prompt unless the user explicitly wants a sheet. Ask for orthographic or slight 3/4 view, strong silhouette, transparent background, and consistent lighting. For inventory icons, request a square composition with padding inside the target cell size.

For gameplay structures such as bases, towers, portals, barricades, and resource nodes, ask for transparent PNGs with no baked-in UI and no health bars. Request ownership/readability variants when useful:

```text
Game-ready transparent building sprites for {two opposing bases}.
Style: {style}; camera: side or slight 3/4; output as separate padded assets.
Each base should have a clear silhouette, faction color accents, readable scale, and no environment background.
No text, labels, UI, health bars, frame borders, grid lines, or watermark.
```

## VFX

Use frame-by-frame sheets for sparks, smoke, magic, explosions, projectiles, and impact bursts. Keep the effect centered, avoid background glow fills, and request alpha-friendly edges. For loops, require the last frame to transition cleanly back to the first.

For ranged units, generate projectile sprites separately from the attack animation. Include travel frames and impact frames when the engine will animate flight:

```text
Transparent projectile sprite frames for {arrow/fireball/etc.}; 4 frames.
Keep the projectile readable at {cell size}px, aligned horizontally, same scale, no background, no labels.
```

## Parallax Backgrounds

Ask for separated layers, not a finished screenshot, so the game can scroll them at different speeds:

```text
Game-ready parallax background layers for {environment}.
Style: {style}; camera: side-scrolling 2D; output as {3 or 4} wide horizontal strips stacked vertically with clean separation.
Layers: far silhouettes, mid trunks/structures, near foliage/rocks, foreground ground cover.
Each strip must be horizontally tileable or wide enough for the battlefield. No characters, buildings, UI, text, labels, borders, grid lines, or watermark.
```

After generation, split strips into `environment/{name}_far.png`, `environment/{name}_mid.png`, `environment/{name}_near.png`, and `environment/{name}_ground.png`. Store metadata with layer order, intended scroll factors, and whether the layer is tile-safe.

For lush forests or other color-dense scenes, ask for a two-part deliverable:

```text
1. One full opaque far background plate: sky, distant canopy, haze, and clouds.
2. Separate alpha/chroma-key cutout sheets for mid trees, near bushes/rocks, foreground grasses/leaves/vines, and optional clouds.
Use a chroma-key color absent from the foliage, such as magenta (#ff00ff) or cyan (#00e5ff), not green.
No rectangular scenic crop strips for moving layers; each moving layer must contain isolated trees, clouds, bushes, rocks, grass clumps, vines, or leaves with transparent space around them.
```

If ImageGen returns checkerboard backing instead of real alpha, remove only the connected checker/solid key background and inspect the layer over a dark and light fill before use.

## Full Game Asset Sets

For a feature pass that replaces drawn code with image assets, generate a compact object atlas for related assets, then extract individual PNGs:

```text
Game-ready transparent sprite atlas for {game scene}.
Include: bases/buildings, coins, mana potions, projectiles, spell cast frames, impact frames, and UI icons.
Keep every asset separated with generous padding, consistent style, no background, no text, no labels, no borders, no grid lines.
```

Inspect alpha carefully. If the generated image uses a checkerboard or white backing, remove only the connected background and verify each extracted PNG has transparent edges.

## Pixel Art

Request exact pixel-art constraints:

```text
Crisp pixel art sprite, hard-edged clusters, limited palette, no painterly blending, no anti-aliasing, no soft gradients, transparent background.
```

Package pixel-art frames with `--scale pixel`. Avoid resizing generated pixel art unless the frame is too large for the requested cell.

## Multi-Animation Handoff

For multiple states, create each animation separately from the same approved side-view reference, then pack each state into its own sheet unless the user needs an atlas. Use matching cell size, origin, camera, palette, scale, key color, and ground anchor across all states. Name outputs like:

- `{target}_idle_sheet.png`
- `{target}_walk_sheet.png`
- `{target}_attack_sheet.png`

The JSON sidecars generated by `pack_sprite_sheet.py` are suitable as import hints for engines or custom loaders.

For sharper painterly sprites, keep a retina export contract: source frames at 2x or 3x the layout size, such as 192x192 images displayed at 96x96, or 256x256 images displayed at 128x128. This usually improves browser/mobile sharpness more reliably than vectorizing generated art.

## Chroma-Key Extraction

Prefer chroma-key contact sheets when previous generations leave white/checkerboard padding or when important light parts, such as helmets, are being cut away. Prompt for a palette-safe key color:

```text
Solid {green/magenta/cyan} chroma-key background ({hex}), no transparency, thick black outline around the sprite, no key-color reflections on metal, foliage, crystals, weapons, or cloth.
```

During cleanup, key only pixels close to the chosen key color, decontaminate key-color spill at edges, and zero the RGB of fully transparent pixels. Do not remove pixels merely because they are bright or low-saturation; that causes holes in silver helmets, armor highlights, pale bones, magic glows, and pale leaves.
