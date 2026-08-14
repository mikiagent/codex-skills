#!/usr/bin/env python3
"""Scaffold a conservative Capacitor iOS release configuration."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read JSON from {path}: {exc}") from exc


def detect_capacitor_values(project: Path) -> tuple[str | None, str | None]:
    for name in ("capacitor.config.ts", "capacitor.config.js", "capacitor.config.json"):
        path = project / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        app_id = re.search(r"\bappId\s*[:=]\s*['\"]([^'\"]+)['\"]", text)
        app_name = re.search(r"\bappName\s*[:=]\s*['\"]([^'\"]+)['\"]", text)
        return (
            app_id.group(1) if app_id else None,
            app_name.group(1) if app_name else None,
        )
    return None, None


def detect_package_values(project: Path) -> tuple[str | None, str | None]:
    package_path = project / "package.json"
    if not package_path.exists():
        return None, None
    package = load_json(package_path)
    raw_name = package.get("displayName") or package.get("name")
    version = package.get("version")
    if isinstance(raw_name, str):
        raw_name = re.sub(r"[-_]+", " ", raw_name).strip().title()
    return raw_name if isinstance(raw_name, str) else None, version if isinstance(version, str) else None


def safe_copy(source: Path, destination: Path, force: bool, created: list[Path]) -> None:
    if destination.exists() and not force:
        raise RuntimeError(f"Refusing to overwrite existing file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    created.append(destination)


def write_manifest(
    destination: Path,
    app_name: str,
    bundle_id: str,
    version: str,
    force: bool,
    created: list[Path],
) -> None:
    if destination.exists() and not force:
        raise RuntimeError(f"Refusing to overwrite existing file: {destination}")
    manifest = load_json(ASSETS_DIR / "release-config.example.json")
    manifest["app"]["name"] = app_name
    manifest["app"]["bundleId"] = bundle_id
    manifest["app"]["sku"] = f"{bundle_id}-ios"
    manifest["app"]["copyright"] = f"{dt.date.today().year} TODO"
    manifest["version"]["marketingVersion"] = version
    manifest["localizations"]["en-US"]["name"] = app_name[:30]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    created.append(destination)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--app-name", help="Public app name; detected when possible")
    parser.add_argument("--bundle-id", help="Reverse-DNS bundle identifier; detected when possible")
    parser.add_argument("--version", help="Marketing version; defaults to package.json or 1.0.0")
    parser.add_argument("--force", action="store_true", help="Replace only the files scaffolded by this script")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = args.project.expanduser().resolve()
    if not project.exists() or not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2

    cap_id, cap_name = detect_capacitor_values(project)
    package_name, package_version = detect_package_values(project)
    app_name = args.app_name or cap_name or package_name or "TODO"
    bundle_id = args.bundle_id or cap_id or "com.example.app"
    version = args.version or package_version or "1.0.0"

    targets = [
        project / "release" / "app-store.json",
        project / "Gemfile",
        project / "fastlane" / "Appfile",
        project / "fastlane" / "Fastfile",
        project / "fastlane" / "Snapfile",
        project / "release" / "templates" / "StoreScreenshotUITests.swift",
    ]
    conflicts = [path for path in targets if path.exists()]
    if conflicts and not args.force:
        print("error: refusing to overwrite existing release files:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        print("Merge the templates manually, or use --force only after reviewing every target.", file=sys.stderr)
        return 1

    created: list[Path] = []
    try:
        write_manifest(
            project / "release" / "app-store.json",
            app_name,
            bundle_id,
            version,
            args.force,
            created,
        )
        safe_copy(ASSETS_DIR / "fastlane" / "Gemfile", project / "Gemfile", args.force, created)
        for filename in ("Appfile", "Fastfile", "Snapfile"):
            safe_copy(
                ASSETS_DIR / "fastlane" / filename,
                project / "fastlane" / filename,
                args.force,
                created,
            )
        safe_copy(
            ASSETS_DIR / "screenshot-tests" / "StoreScreenshotUITests.swift",
            project / "release" / "templates" / "StoreScreenshotUITests.swift",
            args.force,
            created,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if created:
            print("Files created before the conflict (preserved):", file=sys.stderr)
            for path in created:
                print(f"  {path}", file=sys.stderr)
        return 1

    print(f"Scaffolded release workflow in {project}")
    for path in created:
        print(f"  {path.relative_to(project)}")
    if "TODO" in app_name or bundle_id == "com.example.app":
        print("warning: replace placeholder app identity before continuing")
    print("Next: complete release/app-store.json, then run validate_release.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
