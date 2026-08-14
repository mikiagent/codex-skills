#!/usr/bin/env python3
"""Pack transparent frame PNGs into a fixed-cell sprite sheet plus JSON metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from PIL import Image


def parse_cell_size(value: str) -> tuple[int, int]:
    parts = value.lower().replace(",", "x").split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("cell size must look like 128x128")
    try:
        width, height = int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("cell size must contain integers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("cell size must be positive")
    return width, height


def load_frame(path: Path, cell_size: tuple[int, int], scale: str) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    cell_w, cell_h = cell_size
    if image.width > cell_w or image.height > cell_h:
        if scale == "none":
            raise ValueError(f"{path} is {image.width}x{image.height}, larger than cell {cell_w}x{cell_h}")
        resampling = Image.Resampling.NEAREST if scale == "pixel" else Image.Resampling.LANCZOS
        image.thumbnail((cell_w, cell_h), resampling)

    cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    x = (cell_w - image.width) // 2
    y = cell_h - image.height
    cell.alpha_composite(image, (x, y))
    return cell


def sorted_pngs(directory: Path) -> list[Path]:
    return sorted(p for p in directory.iterdir() if p.suffix.lower() == ".png")


def resolve_frames(frame_args: Iterable[str], directory: str | None) -> list[Path]:
    frames = [Path(p).expanduser() for p in frame_args]
    if directory:
        frames.extend(sorted_pngs(Path(directory).expanduser()))
    frames = [p.resolve() for p in frames]
    missing = [str(p) for p in frames if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing frame file(s): " + ", ".join(missing))
    if not frames:
        raise ValueError("Provide --frames or --frame-dir")
    return frames


def pack(args: argparse.Namespace) -> dict:
    frames = resolve_frames(args.frames, args.frame_dir)
    cell_w, cell_h = args.cell_size
    columns = args.columns or len(frames)
    rows = (len(frames) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, rows * cell_h), (0, 0, 0, 0))
    metadata_frames = []

    for index, frame_path in enumerate(frames):
        cell = load_frame(frame_path, args.cell_size, args.scale)
        col = index % columns
        row = index // columns
        x = col * cell_w
        y = row * cell_h
        sheet.alpha_composite(cell, (x, y))
        metadata_frames.append(
            {
                "index": index,
                "source": str(frame_path),
                "x": x,
                "y": y,
                "w": cell_w,
                "h": cell_h,
                "duration_ms": round(1000 / args.fps),
            }
        )

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)

    metadata = {
        "image": str(output),
        "animation": args.animation,
        "fps": args.fps,
        "frame_count": len(frames),
        "cell": {"w": cell_w, "h": cell_h},
        "columns": columns,
        "rows": rows,
        "origin": {"x": cell_w // 2, "y": cell_h},
        "frames": metadata_frames,
    }
    metadata_path = output.with_suffix(output.suffix + ".json")
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
    return {"sheet": str(output), "metadata": str(metadata_path), "frame_count": len(frames)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", nargs="*", default=[], help="Frame PNG files in animation order")
    parser.add_argument("--frame-dir", help="Directory of PNG frames sorted by filename")
    parser.add_argument("--output", required=True, help="Output sprite sheet PNG")
    parser.add_argument("--cell-size", type=parse_cell_size, default=(128, 128), help="Cell size, e.g. 128x128")
    parser.add_argument("--columns", type=int, help="Sheet columns; defaults to one row")
    parser.add_argument("--animation", default="idle", help="Animation name for metadata")
    parser.add_argument("--fps", type=float, default=8, help="Playback frames per second")
    parser.add_argument("--scale", choices=["smooth", "pixel", "none"], default="pixel", help="How to shrink oversized frames")
    args = parser.parse_args()
    if args.columns is not None and args.columns <= 0:
        raise SystemExit("--columns must be positive")
    if args.fps <= 0:
        raise SystemExit("--fps must be positive")
    print(json.dumps(pack(args), indent=2))


if __name__ == "__main__":
    main()
