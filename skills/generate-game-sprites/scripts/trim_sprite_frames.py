#!/usr/bin/env python3
"""Trim transparent or chroma-key padding from sprite frames.

Outputs tight PNG frames and metadata with the original bounding boxes so an
engine can restore anchors if it needs fixed-cell playback.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image


def alpha_bbox(image: Image.Image, threshold: int) -> tuple[int, int, int, int] | None:
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value > threshold else 0)
    return mask.getbbox()


def parse_rgb(value: str) -> tuple[int, int, int]:
    raw = value.strip().lower()
    if raw.startswith("#"):
        raw = raw[1:]
    if "," in raw:
        parts = [int(part.strip()) for part in raw.split(",")]
        if len(parts) != 3:
            raise argparse.ArgumentTypeError("RGB colors must have three channels")
        red, green, blue = parts
    elif len(raw) == 6:
        red, green, blue = int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)
    else:
        raise argparse.ArgumentTypeError("Use #rrggbb, rrggbb, or r,g,b")
    if not all(0 <= channel <= 255 for channel in (red, green, blue)):
        raise argparse.ArgumentTypeError("RGB channels must be between 0 and 255")
    return red, green, blue


def key_color(image: Image.Image, key: tuple[int, int, int], tolerance: int) -> Image.Image:
    """Remove a palette-safe chroma key while preserving non-key highlights."""
    keyed = image.convert("RGBA")
    key_red, key_green_value, key_blue = key
    key_max_channel = max(range(3), key=lambda channel: key[channel])
    key_min_channel = min(range(3), key=lambda channel: key[channel])
    pixels = []
    for red, green, blue, alpha in keyed.getdata():
        channels = (red, green, blue)
        distance = math.sqrt((red - key_red) ** 2 + (green - key_green_value) ** 2 + (blue - key_blue) ** 2)
        dominant_match = (
            channels[key_max_channel] > 70
            and channels[key_max_channel] > channels[(key_max_channel + 1) % 3] * 1.08
            and channels[key_max_channel] > channels[(key_max_channel + 2) % 3] * 1.08
            and channels[key_max_channel] - channels[key_min_channel] > 28
            and distance < tolerance * 1.8
        )
        if distance <= tolerance or dominant_match:
            pixels.append((0, 0, 0, 0))
        elif distance <= tolerance * 1.65:
            cleaned = list(channels)
            cleaned[key_max_channel] = max(min(channels), int(cleaned[key_max_channel] * 0.5))
            pixels.append((cleaned[0], cleaned[1], cleaned[2], alpha))
        elif alpha == 0:
            pixels.append((0, 0, 0, 0))
        else:
            pixels.append((red, green, blue, alpha))
    keyed.putdata(pixels)
    return keyed


def key_green(image: Image.Image) -> Image.Image:
    """Backward-compatible shorthand for legacy green-screen assets."""
    return key_color(image, (0, 255, 0), 76)


def clear_hidden_rgb(image: Image.Image) -> Image.Image:
    clean = image.convert("RGBA")
    clean.putdata([(0, 0, 0, 0) if alpha == 0 else (red, green, blue, alpha) for red, green, blue, alpha in clean.getdata()])
    return clean


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--alpha-threshold", type=int, default=8)
    parser.add_argument("--chroma-key-green", action="store_true", help="Legacy shorthand for --chroma-key-color #00ff00")
    parser.add_argument("--chroma-key-color", type=parse_rgb, help="Remove this chroma key before trimming, e.g. #ff00ff, 00e5ff, or 0,255,0")
    parser.add_argument("--key-tolerance", type=int, default=76, help="RGB distance tolerance for --chroma-key-color")
    parser.add_argument("--padding", type=int, default=2)
    parser.add_argument("--fixed-cell", help="Optional WxH canvas to bottom-center frames after trimming, e.g. 96x96")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fixed_cell: tuple[int, int] | None = None
    if args.fixed_cell:
        width, height = args.fixed_cell.lower().split("x", 1)
        fixed_cell = (int(width), int(height))

    metadata = {"frames": []}
    for index, frame_path in enumerate(args.frames):
        source_path = Path(frame_path)
        image = Image.open(source_path).convert("RGBA")
        if args.chroma_key_green:
            image = key_green(image)
        if args.chroma_key_color:
            image = key_color(image, args.chroma_key_color, args.key_tolerance)
        bbox = alpha_bbox(image, args.alpha_threshold)
        if bbox is None:
            trimmed = Image.new("RGBA", fixed_cell or image.size, (0, 0, 0, 0))
            crop_box = [0, 0, 0, 0]
            offset = [0, 0]
        else:
            left = max(0, bbox[0] - args.padding)
            top = max(0, bbox[1] - args.padding)
            right = min(image.width, bbox[2] + args.padding)
            bottom = min(image.height, bbox[3] + args.padding)
            crop_box = [left, top, right, bottom]
            cropped = image.crop((left, top, right, bottom))
            if fixed_cell:
                trimmed = Image.new("RGBA", fixed_cell, (0, 0, 0, 0))
                x = (fixed_cell[0] - cropped.width) // 2
                y = fixed_cell[1] - cropped.height
                trimmed.alpha_composite(cropped, (x, y))
                offset = [x - left, y - top]
            else:
                trimmed = cropped
                offset = [-left, -top]

        output_path = out_dir / f"{source_path.stem}_trimmed.png"
        trimmed = clear_hidden_rgb(trimmed)
        trimmed.save(output_path)
        metadata["frames"].append(
            {
                "index": index,
                "source": str(source_path),
                "output": str(output_path),
                "sourceSize": [image.width, image.height],
                "cropBox": crop_box,
                "outputSize": [trimmed.width, trimmed.height],
                "offset": offset,
            }
        )

    (out_dir / "trim_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
