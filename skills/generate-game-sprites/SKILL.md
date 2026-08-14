---
name: generate-game-sprites
description: Create game-ready image assets from natural language prompts and optional reference images. Use when Codex needs to generate character, creature, base/building, item, prop, VFX, icon, tileset, UI pickup, projectile, parallax background, environment layer, or animation sprites such as idle, walk, run, attack, hurt, death, cast, interact, or loop animations, especially when the user asks for sprite sheets, transparent PNG frames, parallax layers, generated game art, consistent animation frames, or game asset metadata.
---

# Generate Game Sprites

## Overview

Create prompt-driven raster game assets with ImageGen, then package them into predictable PNG files, sprite sheets, parallax layers, and JSON metadata. Optimize for consistent silhouettes, readable gameplay scale, transparent backgrounds, seamless environment layers, and animation loops that an engine can consume directly.

## Workflow

1. Clarify only missing production-critical details: asset class, target subject, style, view angle, frame count, frame size, background requirements, parallax layer count, loop/seam rules, and whether references should be followed. If omitted, choose practical defaults: 4 or 6 frames, 128x128 cells, side or 3/4 side view for characters, transparent PNG for gameplay objects, 3 parallax layers for side-scrolling backgrounds.
2. If reference images or asset packs are provided, inspect representative files first. Preserve useful conventions: silhouette scale, frame padding, palette, outline weight, camera angle, animation row naming, black/transparent background assumptions, and icon readability. Do not copy protected characters or logos; use references for style/format guidance unless the user owns or supplied the assets for reuse.
3. Choose an output contract before generating:
   - **Characters/monsters**: one animation per sheet by default, especially for walk/run. Use a multi-row atlas only after the individual motion style is approved or when rough placeholder quality is acceptable.
   - **Bases/buildings/props/items/icons/projectiles/VFX**: transparent PNG frames or compact sprite sheet; no UI mockup framing.
   - **Backgrounds**: separate parallax layers as PNGs, ordered far-to-near, each horizontally tileable or wide enough for the camera path.
4. Use ImageGen for the source art. For objects and characters that will be extracted, prefer a solid chroma-key background color that is not used by the sprite, plus an explicit thin black outline around the full silhouette. The black outline is part of the asset contract: it helps the cropper preserve helmets, horns, feet, weapon tips, capes, tails, and fur edges during keyed-background removal. Use green (`#00ff00`) only for sprites that do not contain important greens; for forest creatures, grass, leaves, poison, emeralds, green clothing, or green VFX, choose magenta (`#ff00ff`), cyan (`#00e5ff`), or another absent high-contrast key color and pass that same key color to the trimming script. For parallax backgrounds ask for clean separated alpha layers or a stacked contact sheet with no labels, no borders, and clear layer separation.
5. Inspect generated results. Regenerate or repair if frames drift in identity, scale, orientation, lighting, or silhouette; if frame cells include neighboring art; if animation states are visually indistinguishable; if a death final frame is not suitable to linger; or if a parallax layer has visible seams.
6. Package accepted frames with `scripts/pack_sprite_sheet.py` or a task-local extractor. Produce PNGs plus sidecar JSON metadata with frame rectangles, animation fps, layer order, anchor/origin, and loop/seam assumptions.
7. Return final asset paths and metadata. Include concise notes about frame count, cell size, layer count, animation names, and any assumptions.

## Character Consistency Pipeline

For production character sprites, build identity before animation. Do not start by asking for idle, walk, attack, hurt, and death all at once. Use this sequence:

1. Create or inspect a neutral reference/model sheet first: same character in front, side, back, and 3/4 views, or a simple 360/turnaround sheet. Include a clean side-view grounded pose that shows how the feet, hooves, claws, or body rest on the battlefield baseline.
2. Extract or crop the approved side-view neutral pose. Treat it as the canonical animation reference for side-scrolling gameplay and save it as the source template in the codebase.
3. Generate each animation state separately from that same reference: walk, idle, attack, hurt, death, cast, and any special move. Repeat the exact outfit, silhouette, weapon, scale, camera angle, outline weight, cell size, key color, and ground anchor in every prompt.
4. After each state is generated, crop the useful sprite frames and, when sharper runtime art is needed, use those cropped frames as references for a final high-resolution cleanup/regeneration pass. Downsample the cleaned frames into the engine cell size. Prefer high-resolution raster cleanup for painterly sprites; vector conversion is only appropriate for simple flat icons/props, not detailed painterly characters.
5. Compare every generated state against the reference before packaging. Reject sheets where the attack sprite becomes a different creature/person, changes weapon side, shifts camera angle, changes armor, changes limb proportions, loses the approved silhouette, or has a frame that is nearly empty because the generated contact sheet was sliced incorrectly.

This reference-first flow matters most when walk and attack animations have been visually inconsistent. A single prompt should contain only one motion problem unless placeholder quality is acceptable.

## Template Reference Workflow

When a project needs many assets in one coherent art direction, create and store a template image before generating final sprites, backgrounds, props, or VFX:

1. Generate or choose a high-resolution master template that defines the camera angle, lighting, palette, brush style, outline weight, material rendering, and gameplay scale. For backgrounds, this can be a complete scene plate. For characters, it should be a neutral side-view or turnaround/model sheet. For UI objects, it can be a polished icon reference.
2. Save the original template source in the codebase near the derived assets, using a name such as `forest-master-cohesive-source.png`, `minotaur-reference-source.png`, or `coin-spin-source.png`. Do not only keep transient ImageGen paths.
3. Use that exact template as a reference for follow-up ImageGen calls. For parallax, derive far, hill, mid-tree, near-tree, foreground foliage, and ground layers from the same plate. For characters, derive each state from the same approved neutral pose. For pickups and spells, derive animation frames from the same HUD icon design.
4. Store the generated source sheet next to packaged frames, then package frames into engine-ready PNGs. Keep both the source sheet and the trimmed/cropped runtime frames so future regeneration can compare against the original style.
5. Record the relationship in a local README or manifest: template path, derived asset paths, frame count, key color or transparency method, crop/trim method, anchor assumptions, and any prompt constraints such as black outline or preserved aspect ratio.

This workflow prevents the common failure where parallax layers look like different scenes, animation states become different characters, or HUD pickups do not match their collection animation. Treat the template as the art director for the asset family.

## Parallax Background Pipeline

For production parallax, do not generate unrelated layers independently. Use this sequence:

1. Generate one high-resolution background template first. It should define the full scene, camera height, horizon line, palette, lighting, brush style, and intended playable ground. Store it in the codebase as a source template.
2. Feed that template back as the reference image for every parallax component. Derive these layers from the same template: far opaque sky/horizon, distant landforms, mid scenery, near trunks/rocks/large props, playable ground, and frontmost foliage.
3. For every cutout layer, prompt for a solid chroma-key background color that is distinct from all asset colors. For tropical/forest scenes, magenta (`#ff00ff`) is usually better than green or cyan. Also prompt for a thin black outline on every component so the cropper can preserve leaf tips, rocks, grass, roots, clouds, and silhouette edges.
4. Package cutouts by removing the chosen chroma key globally. If ImageGen ignores the requested chroma key and returns a white or checkerboard matte, remove only the border-connected matte color so internal highlights are preserved. Set transparent pixels to `(0,0,0,0)`.
5. Preserve the original aspect ratio for every layer in the renderer. Scale all layers from the same source width/height and change only their horizontal parallax speed. Do not assign each layer arbitrary independent heights, because that causes stretching, squashing, and mismatched perspective.
6. Use clear z-index bands: far/mid/near scenery behind gameplay, playable ground behind units, dead bodies behind living units, frontmost foliage in front of units when intentional, and projectiles/spell/drop feedback above the foliage.
7. Save a preview composite plus the source template, source layer sheets, runtime PNG layers, and notes describing key color, aspect ratio, layer order, and speed.

For new environment themes, the master template is the source of truth. The derived layers should look like pieces removed from that same painting, not separate paintings.

## Ground Anchor And Bounce Control

Every character animation needs a shared ground/contact anchor so frame crops do not create artificial bouncing:

- Prompt for the feet, claws, or body contact point to rest on the same invisible ground baseline in every frame.
- When a baseline reference helps extraction, ask for a thin temporary baseline in a key color not used by the sprite, placed just below the contact point and not touching the body. Remove this marker during cleanup after measuring it.
- Store anchor metadata when possible: `groundY`, `footAnchorX`, `cellSize`, `baselineRemoved`, and per-frame crop offsets.
- If no baseline marker exists, normalize frames by alpha bounding boxes: bottom-align all living frames to a shared `groundY`, bottom-align death frames to the resting contact edge, and center on the foot/contact anchor rather than the visual bbox center.
- Do not accept rows where the head/torso root moves up and down because the crop changed. The only vertical motion should be intentional animation bob inside a stable cell.

For walk cycles specifically, inspect the animation with a horizontal guide at the feet. Contact feet should appear planted on the guide while the body passes over them. If the whole sprite appears to hop, diagnose both the source frames and the runtime positioning before regenerating.

## Whitespace Trimming

Generated frames often include too much transparent/white padding. After extracting frames, trim them before engine import:

```bash
python scripts/trim_sprite_frames.py \
  --frames frame_001.png frame_002.png frame_003.png \
  --output-dir trimmed \
  --padding 2 \
  --fixed-cell 96x96
```

Use a fixed cell when animation playback needs stable anchors. The script bottom-centers trimmed art and writes `trim_metadata.json` with source crop boxes and offsets. For handoff to engines that support per-frame origins, omit `--fixed-cell` and use the metadata offsets. For animated characters, prefer a shared ground baseline/anchor over raw visual centering; otherwise crouch, attack, hurt, and death frames will appear to bounce or swim inside their cells.

When using chroma-key generation, remove the chosen key color by color distance and channel dominance rather than brightness. After keying, set fully transparent pixels to `(0,0,0,0)` so renderers that sample hidden RGB do not show fringes. Decontaminate edge pixels gently, but never key out low-saturation whites, silvers, golds, blues, or greens by brightness alone; that can punch holes in helmets, armor, crystals, leaves, and weapon highlights.

Avoid chroma-key color spill by cleaning both alpha and RGB:

- Transparent pixels must be saved as `(0,0,0,0)`, not as hidden pink/green/cyan RGB with alpha 0.
- Opaque or semi-opaque pixels that are still close to the key color should be replaced with a nearby outline/shadow color or a neighboring non-key sprite color. Do this only on near-key edge pixels, not by broad hue removal across the whole asset.
- For parallax foreground and ground layers, also remove leftover source-scene pixels that do not belong to the layer, such as ocean/sky matte colors in a foliage-only layer or water pixels underneath a playable ground shelf.
- After cleanup, scan the packaged PNGs for remaining key-like pixels and inspect a composite preview over a contrasting background. A clean alpha crop can still show a fringe if hidden RGB or antialiased edge pixels retain the matte color.

Pick the key color before prompting:

- Green-free sprites: green key (`#00ff00`) is acceptable.
- Green/forest/plant/poison sprites: use magenta (`#ff00ff`) or cyan (`#00e5ff`).
- Red/orange/fire/blood sprites: avoid magenta and pink keys; use green (`#00ff00`) or cyan (`#00e5ff`) if those colors are absent.
- Purple/magenta magic sprites: avoid magenta and use green, cyan, or orange only if absent from the asset.
- Blue/cyan ice or mana sprites: avoid cyan and use green or magenta only if absent from the asset.

Record the chosen key color in the generation notes and use `trim_sprite_frames.py --chroma-key-color '#rrggbb'` during cleanup. Keep `--chroma-key-green` only as a shorthand for legacy green-screen assets.

## Walking Animation Requirements

Do not accept a walking row where the character only bobs, hops, or slides with nearly fixed legs. For an 8-frame side-view walk cycle, require this exact pose sequence:

- frame 1, contact: front foot lands heel-first; rear foot touches the ground by the toe; arms swing opposite the legs.
- frame 2, down: body drops slightly as weight settles onto the front leg; rear heel lifts.
- frame 3, passing: rear leg moves forward and passes beneath the body; supporting leg is nearly straight.
- frame 4, up: body reaches its highest point; forward-moving knee lifts while the supporting foot pushes off.
- frame 5, opposite contact: the other foot lands heel-first; arm and leg positions reverse from frame 1.
- frame 6, opposite down: weight settles onto the new front leg; body lowers slightly and the trailing heel rises.
- frame 7, opposite passing: trailing leg passes underneath the body; torso remains balanced above the planted foot.
- frame 8, opposite up: body rises again as the planted foot pushes off and the opposite knee moves forward.

The animation must loop smoothly from frame 8 back to frame 1. The head and torso should gently bob downward during frames 2 and 6, and upward during frames 4 and 8. Keep the bob subtle; the body should not hop.

When walk quality is unreliable, generate or reason from a 4-key-pose scaffold first, then expand it into 8 frames:

- key pose A, legs apart/contact: front foot forward, rear foot back, wide readable stride.
- key pose B, legs together/passing: swing leg passes under the hips, knees close together, feet near the body centerline.
- key pose C, opposite legs apart/contact: the other foot forward, original foot back, wide readable stride reversed from A.
- key pose D, opposite legs together/passing: legs cross/pass near the body centerline again before looping.

The final 8-frame prompt should preserve those alternating silhouettes: frames 1 and 5 are legs-apart contact frames; frames 3 and 7 are legs-together passing frames; frames 2, 4, 6, and 8 are in-betweens for weight drop and push-off. Every walk cycle must have at least one unmistakable legs-together/passing frame where the moving leg is under the hips and the feet are close together. If no frame clearly shows legs together under the body, or no frame clearly shows legs apart in a stride, reject the walk sheet.

For heavy/tanky characters, a walk may be framed as a slow stomp. Keep the same 8-frame contact/down/passing/up structure, but exaggerate weight: contact frames show the foot/hoof planting hard with dust puffs, down frames show deeper knee compression and lowered shoulders, passing frames still show legs together under the hips, and push-off frames show the weapon/cloth lagging behind. Optional breath or snort effects should be sparse gray/white wisps near the mouth/nostrils, in a color distinct from the chroma-key background, and should not obscure the legs. Avoid constant steam. A good heavy loop can include a stomp, a brief planted pause with heavy breathing/shoulder rise, then another stomp.

Ask for visible shoulder and hip counter-rotation, knee bend, planted contact foot, arm sway opposite the legs, and the back foot swinging forward to become the dominant front foot. For weapon users, the weapon arm and free arm should visibly sway or lag with the shoulders unless the weapon is too heavy, in which case the shoulder roll and hand lag should still be readable. Require at least one clear push-off frame in each half-cycle: the support foot is near the middle under the body, its toe is pushing against the ground, and the opposite leg trails behind with the knee bent and foot hanging back before swinging through. The character's head/torso root should follow the contact/down/passing/up bob pattern without a bouncing or jumping body arc. The planted foot should appear to hold the ground while the body passes over it, like the reference `assets/references/141-Female_Walk_Dummy_Long.gif`.

Common failure diagnosis: walk cycles turn into hopping when too many animation rows are generated at once, robes/armor hide both feet, the prompt lacks explicit contact/down/passing/push-off poses, frame crops move the baseline between frames, or runtime code adds vertical bobbing during walk. Generate walk separately, make both feet visible in silhouette, require a shared baseline, and reject rows where the same foot stays forward throughout the loop.

Acceptance check before packaging:

- Scrub across the walk row: the forward foot must swap at least once.
- Contact frames must have one leg extended forward and the other extended back.
- Passing frames must include a clear legs-together silhouette, with the swing leg under the hips and feet near the body centerline.
- Passing frames must show the swing foot traveling under or in front of the body.
- Shoulders and arms must visibly sway or counter-rotate opposite the legs; a stiff upper body is not acceptable unless the unit is intentionally bracing a huge weapon, and even then shoulder roll must be visible.
- Push-off/up frames must show the support foot near the center under the body while the opposite leg hangs behind before swinging forward.
- The head height should remain nearly level; visible up/down hopping means regenerate.
- If feet remain in the same order, or the body just rises and falls, reject the sheet.

## Prompt Pattern

Use this structure for ImageGen prompts:

```text
Game sprite animation frames for {target}: {animation}.
Style: {pixel art / painterly / clean 2D / etc}; camera: {side / 3/4 / top-down}; frame count: {n}; output as {individual frames or contact sheet}.
Keep the same character identity, silhouette, outfit, palette, scale, camera angle, and anchor point in every frame.
If this is not the first state, follow the approved side-view reference sprite exactly: same character, same proportions, same weapon side, same outline weight, same scale, same ground contact anchor.
Pure green chroma-key background (#00ff00) or transparent background. Thin clean black outline around the entire silhouette, including feet, fingers, horns, helmet, weapon, cape, tail, and VFX edges. No text, labels, borders, grid lines, shadows, environment, UI, watermark, or extra characters.
Make the animation readable at {cell size}px and suitable for a seamless loop.

For walk animations, specify the full 8-frame sequence: contact, down, passing, up, opposite contact, opposite down, opposite passing, opposite up. Include subtle torso/head down bob on frames 2 and 6, subtle up bob on frames 4 and 8, no hopping, planted contact foot, alternating left/right heel-strike contacts, shoulder/hip counter-rotation, and the rear foot visibly swinging forward to become the front foot.
```

Replace the chroma-key sentence with the selected palette-safe key color when needed, for example: `solid magenta chroma-key background (#ff00ff), because the sprite contains green; no magenta reflections or rim light`.

For red/orange sprites, use a sentence like: `solid green chroma-key background (#00ff00), because the sprite is red/orange; no green reflections, green glow, grass, or green rim light`.

Read `references/prompt-recipes.md` when the user asks for a specific asset class, multiple animation states, pixel-art constraints, or engine handoff conventions.

## Packaging

Use the packaging script after generating or extracting frame PNGs:

```bash
python scripts/pack_sprite_sheet.py \
  --frames frame_001.png frame_002.png frame_003.png frame_004.png \
  --output hero_idle_sheet.png \
  --cell-size 128x128 \
  --columns 4 \
  --animation idle \
  --fps 8
```

The script preserves transparency, centers frames in fixed cells, writes `{output}.json`, and records frame rectangles for engine import.

## Quality Bar

- Keep each frame aligned to the same ground/contact point.
- Trim excess transparent/white padding after extraction. Use the smallest fixed cell that preserves weapons/VFX without clipping.
- Walking, attacking, hurting, and dying must be visually distinct. If generated frames look like repeated idle poses, regenerate or substitute a better reference-driven prompt.
- Death animations should include a final resting/corpse frame that can remain on screen for an extended linger.
- For ranged units, generate or include projectile frames separately from attack poses.
- Melee attack animations should usually include a lunge/pounce engage beat: anticipation, forward body travel, impact/strike, follow-through, and recovery. This lunge should read as the unit closing from just outside attack range into combat. For different body types, adapt the verb while preserving the timing: a small humanoid lunges, a heavy unit stomps/slams forward, and a multi-legged creature pounces or springs.
- Idle animations should always include both a subtle knee bounce/weight compression and at least one blink. Feet/contact points stay planted on the shared baseline; the knee bounce happens through slight knee bend, shoulder settle, and torso compression, not a hopping crop.
- Favor big readable pose changes over subtle motion for small sprites.
- Ensure weapons, tails, hair, capes, and held items remain attached and consistent.
- Avoid lighting or palette shifts between frames unless the animation is a VFX effect.
- For pixel art, request crisp hard-edged pixels and no anti-aliased painterly blending; do not upscale with smoothing.
- For multi-state sheets, keep the same cell size, columns, fps conventions, and origin across all states.
- For final character sprites, use one animation per generation and a consistent high-resolution source cell, such as 256x256 or 384x384 per frame, then downsample into the engine cell. Do less per prompt instead of asking for every state at once. Multi-row sheets are acceptable only for rough placeholders or after the walk style has already passed review. SVG conversion is only appropriate for flat icons or simple vector props; do not auto-vectorize painterly sprites or animated characters because it changes silhouettes and makes frame-to-frame motion less stable.
- For sharper painterly sprites, export retina-scale frames when the engine supports fixed display sizing: for example, store 192x192 or 256x256 PNG frames for a unit rendered at 96x96 or 128x128 CSS/layout pixels. This preserves more source detail on high-DPI screens without changing gameplay size. Use nearest-neighbor only for intentional pixel art; for painterly sprites use high-quality Lanczos downsampling and avoid excessive compression.
- For bases/buildings, render as transparent gameplay objects with intact silhouettes, readable damage/ownership variants if needed, and no baked-in health bars unless requested.
- For resource pickups, generate coin/gem/potion frames that read at HUD and ground scale, with transparent backgrounds and optional sparkle frames.
- For parallax backgrounds, generate separate far, mid, near, and foreground layers when possible. The far layer may be a full opaque sky/forest plate, but mid/near/foreground must be alpha cutouts: individual tree trunks, canopies, clouds, hanging vines, rocks, bushes, grass, and leaves on transparent or palette-safe chroma-key backgrounds. Do not use cropped full-scene rectangles for foreground parallax; rectangular strips create obvious sliding panels instead of depth. Each layer should tile horizontally or exceed the battlefield width; avoid baked-in UI, characters, or one-off focal objects that reveal repetition.
