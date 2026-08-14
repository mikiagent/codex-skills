#!/usr/bin/env python3
"""Validate App Store screenshot files against the release manifest."""

from __future__ import annotations

import argparse
import json
import struct
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


def orientations(values: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return values | {(height, width) for width, height in values}


FAMILY_SIZES = {
    "iphone-6.9": orientations({(1260, 2736), (1290, 2796), (1320, 2868)}),
    "iphone-6.5": orientations({(1284, 2778), (1242, 2688)}),
    "iphone-6.3": orientations({(1179, 2556), (1206, 2622)}),
    "iphone-6.1": orientations({(1170, 2532), (1125, 2436), (1080, 2340)}),
    "iphone-5.5": orientations({(1242, 2208)}),
    "iphone-4.7": orientations({(750, 1334)}),
    "ipad-13": orientations({(2064, 2752), (2048, 2732)}),
    "ipad-11": orientations({(1488, 2266), (1668, 2420), (1668, 2388), (1640, 2360)}),
    "ipad-10.5": orientations({(1668, 2224)}),
}


@dataclass
class Finding:
    severity: str
    path: str
    message: str


@dataclass
class ImageInfo:
    path: Path
    width: int
    height: int
    family: str | None
    has_alpha: bool


def read_png(path: Path) -> tuple[int, int, bool]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError("invalid PNG signature")
        length = struct.unpack(">I", handle.read(4))[0]
        chunk = handle.read(4)
        if chunk != b"IHDR" or length != 13:
            raise ValueError("missing PNG IHDR")
        payload = handle.read(13)
        width, height, _depth, color_type, _compression, _filter, _interlace = struct.unpack(">IIBBBBB", payload)
        handle.read(4)
        has_alpha = color_type in {4, 6}
        while True:
            raw_length = handle.read(4)
            if not raw_length:
                break
            chunk_length = struct.unpack(">I", raw_length)[0]
            chunk_type = handle.read(4)
            if chunk_type == b"tRNS":
                has_alpha = True
            handle.seek(chunk_length + 4, 1)
            if chunk_type == b"IEND":
                break
        return width, height, has_alpha


def read_jpeg(path: Path) -> tuple[int, int, bool]:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            raise ValueError("invalid JPEG signature")
        while True:
            marker_start = handle.read(1)
            if not marker_start:
                break
            if marker_start != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if not marker:
                break
            code = marker[0]
            if code in {0xD8, 0xD9} or 0xD0 <= code <= 0xD7:
                continue
            raw_length = handle.read(2)
            if len(raw_length) != 2:
                break
            segment_length = struct.unpack(">H", raw_length)[0]
            if segment_length < 2:
                raise ValueError("invalid JPEG segment")
            if code in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                data = handle.read(segment_length - 2)
                if len(data) < 5:
                    raise ValueError("truncated JPEG frame")
                height, width = struct.unpack(">HH", data[1:5])
                return width, height, False
            handle.seek(segment_length - 2, 1)
    raise ValueError("JPEG dimensions not found")


def image_info(path: Path) -> ImageInfo:
    suffix = path.suffix.casefold()
    if suffix == ".png":
        width, height, has_alpha = read_png(path)
    elif suffix in {".jpg", ".jpeg"}:
        width, height, has_alpha = read_jpeg(path)
    else:
        raise ValueError("unsupported file type")
    family = next((name for name, sizes in FAMILY_SIZES.items() if (width, height) in sizes), None)
    return ImageInfo(path, width, height, family, has_alpha)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--screenshots-root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.expanduser().resolve()
    root = args.screenshots_root.expanduser().resolve()
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: could not read config: {exc}", file=sys.stderr)
        return 2
    if not root.exists() or not root.is_dir():
        print(f"error: screenshot directory does not exist: {root}", file=sys.stderr)
        return 2

    screenshot_config = config.get("screenshots", {})
    locales = screenshot_config.get("locales", [])
    required_families = screenshot_config.get("deviceFamilies", [])
    states = screenshot_config.get("states", [])
    findings: list[Finding] = []
    images: list[ImageInfo] = []

    def add(severity: str, path: str, message: str) -> None:
        findings.append(Finding(severity, path, message))

    if not isinstance(locales, list) or not locales:
        add("error", "screenshots.locales", "manifest has no screenshot locales")
        locales = []
    if not isinstance(required_families, list) or not required_families:
        add("error", "screenshots.deviceFamilies", "manifest has no screenshot device families")
        required_families = []

    for locale in locales:
        locale_dir = root / locale
        if not locale_dir.is_dir():
            add("error", str(locale_dir), "missing locale screenshot directory")
            continue
        files = sorted(path for path in locale_dir.iterdir() if path.is_file() and path.suffix.casefold() in {".png", ".jpg", ".jpeg"})
        if not files:
            add("error", str(locale_dir), "contains no PNG or JPEG screenshots")
            continue
        locale_images: list[ImageInfo] = []
        for path in files:
            try:
                info = image_info(path)
            except (OSError, ValueError, struct.error) as exc:
                add("error", str(path), f"could not inspect image: {exc}")
                continue
            locale_images.append(info)
            images.append(info)
            if info.has_alpha:
                add("error", str(path), "screenshots cannot include alpha/transparency")
            if info.family is None:
                add("warning", str(path), f"unrecognized App Store dimensions: {info.width}x{info.height}; refresh Apple's specifications")

        for family in required_families:
            family_images = [info for info in locale_images if info.family == family]
            count = len(family_images)
            if count < 1:
                add("error", f"{locale}/{family}", "missing required screenshot family")
                continue
            if count > 10:
                add("error", f"{locale}/{family}", f"contains {count} screenshots; Apple allows at most 10")
            expected_states = [state.get("id") for state in states if isinstance(state, dict) and isinstance(state.get("id"), str)]
            if expected_states and count < len(expected_states):
                add("error", f"{locale}/{family}", f"contains {count} screenshots for {len(expected_states)} planned states")
            for state_id in expected_states:
                if not any(state_id.casefold() in info.path.name.casefold() for info in family_images):
                    add("warning", f"{locale}/{family}", f"no filename contains planned state id: {state_id}")

    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    if args.json:
        print(json.dumps({
            "screenshotsRoot": str(root),
            "valid": not errors,
            "errorCount": len(errors),
            "warningCount": len(warnings),
            "findings": [asdict(finding) for finding in findings],
            "images": [
                {
                    "path": str(info.path),
                    "width": info.width,
                    "height": info.height,
                    "family": info.family,
                    "hasAlpha": info.has_alpha,
                }
                for info in images
            ],
        }, indent=2))
    else:
        for finding in findings:
            print(f"{finding.severity.upper():7} {finding.path}: {finding.message}")
        print(f"\nScreenshots: {len(images)} image(s), {len(errors)} error(s), {len(warnings)} warning(s)")
        print("VALID" if not errors else "NOT READY")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
