---
name: asset-validator
description: Validate generated 2D game assets and sprite animations before they are used at runtime.
---

# Asset Validator

Run after creating or modifying game assets.

## Static asset checks

- PNG has expected transparency.
- No accidental background rectangle.
- No watermark.
- No unwanted text.
- No clipped edges.
- Padding is reasonable.
- Asset scale matches related assets.
- Pivot recommendation is documented.

## Sprite animation checks

- Every frame has the same canvas size.
- Character does not drift horizontally without intent.
- Foot/ground baseline remains locked.
- No sudden scale changes.
- No camera motion baked into frames.
- Character identity stays consistent.
- First/last pose transition loops cleanly.
- Blink does not create extra eyes or facial artifacts.
- Transparent edges do not have obvious matte halos.
- Runtime frame order is explicit.

## Export expectations

Prefer:
- transparent PNG frames
- horizontal or atlas spritesheet
- JSON manifest with frame order and duration
- GIF/WebM preview

If validation fails, fix deterministic layout/alignment problems with code before regenerating artwork.
