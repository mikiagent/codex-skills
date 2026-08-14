# Prompt Enhancer Examples

These examples show how to extrapolate useful structure without inventing high-impact requirements.

## Example 1: vague coding request

### User prompt

```text
Fix the weird flashing thing when I click around the UI.
```

### Enhancement behavior

Inspect the repo before asking questions. Identify the affected UI stack, reproduce the issue if possible, inspect transitions/focus/active states/remount behavior, and only ask the user if multiple visually distinct symptoms remain ambiguous.

### Enhanced execution brief

```text
GOAL
Remove the visible UI flash that occurs during normal navigation/click interactions without changing intended animations.

CONTEXT
Inspect the current frontend implementation, global styles, route/layout transitions, focus/active states, loading boundaries, and components that remount on interaction.

CONSTRAINTS
- Preserve existing layout and functionality.
- Do not remove intentional transitions unless they are the cause.
- Prefer the smallest owning fix.
- Avoid masking the symptom with arbitrary delays.

WORKFLOW
1. Reproduce and isolate the flash.
2. Determine whether it is caused by CSS state, DOM remounting, loading fallback, browser default focus/tap behavior, or asset repaint.
3. Fix the owning layer.
4. Test the affected interactions and nearby UI states.

DONE WHEN
- the flash is no longer reproducible in the affected interactions;
- intended hover/focus/transition behavior remains;
- build/tests pass;
- the change is localized and explained.
```

## Example 2: vague game concept

### User prompt

```text
Make a cozy farm game with animals that makes passive income.
```

### High-value questions

If not already known:

1. Is the target primarily mobile/portrait, desktop, or both?
2. Should the core interaction be mostly passive collection/upgrades or active farming chores?
3. Do you want 2D sprites or procedural/voxel 3D for the first prototype?

Do not ask about names, exact currencies, button colors, or dozens of species yet.

### Enhanced brief after likely choices

```text
GOAL
Build a portrait mobile-friendly cozy animal-collecting farm prototype centered on passive income and upgrading animals.

CORE LOOP
Acquire animal → animal accumulates currency → collect → upgrade → unlock higher-value species.

FIRST PLAYABLE SCOPE
- one pasture;
- four animal species;
- individual and collect-all income;
- upgrades;
- simple unlock progression;
- local save;
- capped offline earnings.

ART DIRECTION
Stylized reconstruction-friendly voxel animals with large readable silhouettes and simple materials.

TECHNICAL CONSTRAINTS
- responsive portrait camera;
- clickable/tappable animals;
- reusable geometry/materials;
- no per-frame geometry allocation;
- runtime assets expose pivots/colliders where useful.

DONE WHEN
A fresh player can buy, collect, upgrade, leave/reload, and continue progression at phone aspect ratios.
```

## Example 3: vague image request

### User prompt

```text
Make this pirate look like he's attacking.
```

### High-value question

Ask only if missing:

```text
Should this remain the exact same canonical game character and camera framing, or is reinterpretation okay?
```

If the existing context clearly says it is a sprite identity anchor, do not ask.

### Enhanced prompt

```text
PURPOSE
Attack-pose source image for the existing 2D game character sprite pipeline.

CHANGE
Move the pirate into a strong sword-attack anticipation pose with the torso rotating into the strike and the sword arm drawn back.

PRESERVE
- exact face and eyepatch side;
- outfit and palette;
- sword in the same character hand;
- body proportions;
- facing direction;
- locked camera;
- subject scale;
- full-body framing;
- background.

PIPELINE CONSTRAINTS
Keep limbs and sword clearly separable from the torso, avoid cropping, preserve generous margin, and do not add motion blur or cast shadows that merge with the silhouette.

AVOID
No redesign, camera zoom, extra props, text, scenery, weapon swap, or mirrored identity traits.
```

## Example 4: multi-reference game asset

### User prompt

```text
Use these images to make the sprite more pixelated and use this pose.
```

### Enhanced prompt

```text
PURPOSE
Create a new pose for the canonical character that can later be normalized into the game sprite pipeline.

REFERENCE AUTHORITY
- Image 1: identity authority for face, outfit, palette, proportions, and handedness.
- Image 2: pose authority only.
- Image 3: pixel-grid/block-structure authority only.

Generate Image 1's character performing Image 2's pose while borrowing only the discrete block structure from Image 3.

PRESERVE
Identity, facing, palette, costume, asymmetrical traits, scale, and camera.

PIPELINE CONSTRAINTS
The result may be generated at high working resolution, but it will later be snapped to the canonical logical pixel grid. Do not invent tiny details that cannot survive the target sprite scale.
```

## Example 5: 3D reconstruction

### User prompt

```text
Turn this animal into a Three.js model.
```

### Enhanced prompt

```text
GOAL
Reconstruct the reference animal as an animation-ready procedural Three.js model for a mobile game.

REFERENCE USE
Treat the image as observed design evidence. Preserve visible silhouette, proportions, colors, and species-defining features. Mark unseen rear/underside geometry as inferred rather than exact.

RUNTIME CONTRACT
- +Y up;
- explicit local forward axis;
- feet grounded at minY = 0;
- named body/head/leg/tail hierarchy;
- pivots for moving parts;
- collider metadata;
- shared/reusable geometry and materials where practical;
- no unnecessary per-frame allocations.

WORKFLOW
Observation → component/spec contract → blockout → structure → form/materials → runtime pivots/colliders → controlled render comparison → optimization.

DONE WHEN
The model is recognizable at target camera distance, controlled views match the reference sufficiently, runtime hierarchy is usable, and hidden-surface uncertainty is documented.
```

## Example 6: short prompt that should NOT be expanded heavily

### User prompt

```text
Rename this variable from temp to frameCount.
```

### Correct behavior

Do not create a giant specification. Inspect scope and perform the straightforward rename safely.

The Skill exists to reduce expensive ambiguity, not to make simple tasks bureaucratic.
