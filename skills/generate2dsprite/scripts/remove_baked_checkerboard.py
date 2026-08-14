#!/usr/bin/env python3
"""Remove a light neutral checkerboard that was baked into an otherwise opaque PNG."""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


def remove_checkerboard(
    image: Image.Image,
    *,
    min_channel: int = 225,
    max_channel_spread: int = 14,
) -> Image.Image:
    rgba = np.asarray(image.convert("RGBA")).copy()
    rgb = rgba[:, :, :3].astype(np.int16)
    alpha = rgba[:, :, 3]
    light = rgb.min(axis=2) >= min_channel
    neutral = (rgb.max(axis=2) - rgb.min(axis=2)) <= max_channel_spread
    candidate = (light & neutral) | (alpha == 0)

    height, width = candidate.shape
    connected = np.zeros((height, width), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        if candidate[0, x]:
            queue.append((0, x))
        if candidate[height - 1, x]:
            queue.append((height - 1, x))
    for y in range(height):
        if candidate[y, 0]:
            queue.append((y, 0))
        if candidate[y, width - 1]:
            queue.append((y, width - 1))

    while queue:
        y, x = queue.popleft()
        if connected[y, x] or not candidate[y, x]:
            continue
        connected[y, x] = True
        if x > 0:
            queue.append((y, x - 1))
        if x + 1 < width:
            queue.append((y, x + 1))
        if y > 0:
            queue.append((y - 1, x))
        if y + 1 < height:
            queue.append((y + 1, x))

    rgba[connected] = (0, 0, 0, 0)
    return Image.fromarray(rgba, mode="RGBA")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-channel", type=int, default=225)
    parser.add_argument("--max-channel-spread", type=int, default=14)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = remove_checkerboard(
        Image.open(args.input),
        min_channel=args.min_channel,
        max_channel_spread=args.max_channel_spread,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output)
    alpha = np.asarray(output.getchannel("A"))
    transparent = int(np.count_nonzero(alpha == 0))
    visible = int(np.count_nonzero(alpha > 0))
    if transparent == 0 or visible == 0:
        raise SystemExit("checkerboard cleanup failed alpha coverage validation")
    print(args.output)


if __name__ == "__main__":
    main()
