#!/usr/bin/env python3
"""Build a structural inventory of a repository without reading file bodies.

This is intentionally simple and deterministic. It helps an agent learn the shape
of an unfamiliar workspace before deciding which files deserve semantic reading.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Iterable

DEFAULT_IGNORES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".cache",
    "__pycache__",
}


def iter_files(root: Path, ignores: set[str]) -> Iterable[Path]:
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in ignores)
        base = Path(current_root)
        for filename in sorted(filenames):
            path = base / filename
            try:
                if path.is_symlink() or not path.is_file():
                    continue
            except OSError:
                continue
            yield path


def safe_size(path: Path) -> int | None:
    try:
        return path.stat().st_size
    except OSError:
        return None


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def build_inventory(root: Path, ignores: set[str], largest_count: int) -> dict:
    extension_counts: Counter[str] = Counter()
    top_level_counts: Counter[str] = Counter()
    sized_files: list[tuple[int, Path]] = []
    total_bytes = 0
    file_count = 0

    for path in iter_files(root, ignores):
        size = safe_size(path)
        if size is None:
            continue

        file_count += 1
        total_bytes += size
        extension = path.suffix.lower() or "<no-extension>"
        extension_counts[extension] += 1

        rel = path.relative_to(root)
        owner = rel.parts[0] if len(rel.parts) > 1 else "<root>"
        top_level_counts[owner] += 1
        sized_files.append((size, path))

    sized_files.sort(key=lambda item: (-item[0], relative(item[1], root)))

    top_level_entries = []
    try:
        for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if child.name in ignores:
                continue
            top_level_entries.append(
                {
                    "name": child.name,
                    "type": "dir" if child.is_dir() else "file",
                }
            )
    except OSError:
        pass

    return {
        "root": str(root.resolve()),
        "file_count": file_count,
        "total_bytes": total_bytes,
        "ignored_names": sorted(ignores),
        "top_level_entries": top_level_entries,
        "top_level_file_counts": dict(top_level_counts.most_common()),
        "extension_counts": dict(extension_counts.most_common()),
        "largest_files": [
            {"path": relative(path, root), "bytes": size}
            for size, path in sized_files[:largest_count]
        ],
    }


def render_text(inventory: dict) -> str:
    lines = [
        f"Root: {inventory['root']}",
        f"Files: {inventory['file_count']}",
        f"Bytes: {inventory['total_bytes']}",
        "",
        "Top-level entries:",
    ]
    for item in inventory["top_level_entries"]:
        lines.append(f"- {item['type']}: {item['name']}")

    lines.extend(["", "Extension counts:"])
    for extension, count in inventory["extension_counts"].items():
        lines.append(f"- {extension}: {count}")

    lines.extend(["", "Largest files:"])
    for item in inventory["largest_files"]:
        lines.append(f"- {item['bytes']:>10}  {item['path']}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory repository structure without reading file contents."
    )
    parser.add_argument("root", nargs="?", default=".", help="Root directory to inspect")
    parser.add_argument(
        "--largest",
        type=int,
        default=25,
        help="Number of largest files to report (default: 25)",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Additional directory/file basename to ignore; may be repeated",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")
    if args.largest < 0:
        raise SystemExit("--largest must be >= 0")

    ignores = DEFAULT_IGNORES | set(args.ignore)
    inventory = build_inventory(root, ignores, args.largest)

    if args.json:
        print(json.dumps(inventory, indent=2, sort_keys=True))
    else:
        print(render_text(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
