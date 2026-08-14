---
name: game-asset-router
description: Route 2D game asset requests to the appropriate installed image, sprite, video-to-sprite, map, and validation skills.
---

# Game Asset Router

Use this skill whenever the user asks Codex to create or modify visual assets for a 2D game.

## Goal

Do not treat game art as a single image-generation request. Treat it as an asset-production pipeline.

## Routing

### Static game object
Examples: platform, coin, leaf, button, prop, pickup.

1. Generate or edit with the installed image generation skill.
2. Produce transparent PNG whenever the asset is meant to float over a scene.
3. Remove unrelated text/backgrounds.
4. Normalize dimensions and padding.
5. Run `$asset-validator`.

### Character sprite
Use `$generate2dsprite`.

Preserve:
- canonical character identity
- silhouette
- palette
- proportions
- outfit
- camera angle
- ground contact

### Animation from a still character
Prefer `$video2dsprite` for motion that benefits from temporal continuity:
- walk
- run
- breathing idle
- cloth/hair motion
- expressive loops

For simple sprite-sheet generation, use `$generate2dsprite`.

### Map / level art
Use `$generate2dmap`.

### Pixel art
If a pixel-snap workflow exists in the project/reference repos:
- restore a consistent pixel grid
- nearest-neighbor scale only
- avoid antialiased mixed pixel sizes

## Character consistency rule

Before generating multiple animations, establish one canonical anchor image.

Every later generation must reference the canonical anchor.

## Animation production rule

For every animation:
1. lock ground/foot baseline
2. avoid camera motion
3. avoid zoom
4. keep framing constant
5. loop cleanly
6. extract frames
7. remove backgrounds
8. normalize size
9. align feet/center
10. export preview GIF/WebM and runtime sheet

## Output organization

Use:

assets/
  characters/
  platforms/
  collectibles/
  ui/
  backgrounds/
  fx/
  manifests/

Never overwrite source/reference art. Put generated intermediates in `assets/_work/`.
