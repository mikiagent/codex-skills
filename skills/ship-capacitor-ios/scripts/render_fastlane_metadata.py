#!/usr/bin/env python3
"""Render Fastlane deliver metadata from release/app-store.json."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


MARKER = ".generated-by-ship-capacitor-ios"


def write_text(path: Path, value: Any, *, private: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "" if value is None else str(value).strip()
    path.write_text(text + "\n", encoding="utf-8")
    if private:
        os.chmod(path, 0o600)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="Allow rendering into a non-empty unmarked directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.expanduser().resolve()
    output = args.output.expanduser().resolve()
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: config does not exist: {config_path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {config_path}: {exc}", file=sys.stderr)
        return 2

    if output.exists() and any(output.iterdir()) and not (output / MARKER).exists() and not args.force:
        print(
            f"error: refusing to write into non-empty unmarked directory: {output}\n"
            "Use --force only after reviewing the existing metadata.",
            file=sys.stderr,
        )
        return 1
    output.mkdir(parents=True, exist_ok=True)

    app = config.get("app", {})
    version = config.get("version", {})
    localizations = config.get("localizations", {})
    review = config.get("review", {})
    contact = review.get("contact", {})

    if not isinstance(localizations, dict) or not localizations:
        print("error: localizations must contain at least one locale", file=sys.stderr)
        return 1

    rendered: list[Path] = []

    def render(relative: str, value: Any, *, private: bool = False) -> None:
        path = output / relative
        write_text(path, value, private=private)
        rendered.append(path)

    render("copyright.txt", app.get("copyright", ""))
    render("primary_category.txt", app.get("primaryCategory", ""))
    if app.get("secondaryCategory"):
        render("secondary_category.txt", app.get("secondaryCategory"))

    field_files = {
        "name": "name.txt",
        "subtitle": "subtitle.txt",
        "description": "description.txt",
        "keywords": "keywords.txt",
        "promotionalText": "promotional_text.txt",
        "supportUrl": "support_url.txt",
        "marketingUrl": "marketing_url.txt",
        "privacyUrl": "privacy_url.txt",
    }
    for locale, localized in sorted(localizations.items()):
        if not isinstance(localized, dict):
            print(f"error: localization {locale} must be an object", file=sys.stderr)
            return 1
        for field, filename in field_files.items():
            render(f"{locale}/{filename}", localized.get(field, ""))
        if not version.get("isFirstRelease", False):
            render(f"{locale}/release_notes.txt", localized.get("whatsNew", ""))

    review_fields = {
        "first_name.txt": contact.get("firstName", ""),
        "last_name.txt": contact.get("lastName", ""),
        "phone_number.txt": contact.get("phone", ""),
        "email_address.txt": contact.get("email", ""),
        "notes.txt": review.get("notes", ""),
    }
    for filename, value in review_fields.items():
        render(f"review_information/{filename}", value, private=True)

    marker = output / MARKER
    marker.write_text(
        "Generated from release/app-store.json. Review diffs before upload.\n"
        "Demo credentials are intentionally supplied through environment variables.\n",
        encoding="utf-8",
    )
    rendered.append(marker)

    print(f"Rendered {len(rendered)} metadata files in {output}")
    print("Review demo credentials were not written to disk.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
