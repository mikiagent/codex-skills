#!/usr/bin/env python3
"""Structural validator for raid design Markdown artifacts.

This validator checks whether a design document contains the major contracts
required by the raid-encounter-designer Skill. It does not judge whether the
encounter is fun, fair, balanced, or actually works in play.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


REQUIRED_SECTIONS = {
    "fantasy": [r"fantasy", r"emotional target"],
    "player_count": [r"player count", r"fireteam"],
    "mechanic_vocabulary": [r"mechanic vocabulary", r"mechanic language"],
    "pacing": [r"pacing"],
    "encounters": [r"encounter"],
    "information_graph": [r"information graph"],
    "role_graph": [r"role graph"],
    "state_machine": [r"state machine"],
    "pressure": [r"pressure"],
    "combat_integration": [r"combat integration"],
    "feedback": [r"feedback"],
    "failure_recovery": [r"failure", r"recovery"],
    "accessibility": [r"accessibility", r"callout"],
    "blind_solve": [r"blind", r"solve|playtest"],
    "repeat_clear": [r"repeat", r"clear|validation"],
    "technical_reliability": [r"technical reliability", r"reliability matrix"],
    "challenge_variant": [r"challenge", r"mastery variant|variant"],
    "implementation_handoff": [r"implementation handoff"],
}

WARNING_PATTERNS = {
    "no_visible_wipe_reason": (
        [r"wipe"],
        [r"visible cause", r"feedback", r"reason"],
        "Wipes are mentioned but no obvious visible-cause/feedback contract was found.",
    ),
    "no_role_transfer": (
        [r"role"],
        [r"transfer", r"handoff", r"swap"],
        "Roles are present but no transfer/handoff language was found. Fixed roles may be intentional; verify recovery/adaptation.",
    ),
    "no_boss_dps_decision": (
        [r"boss"],
        [r"active dps", r"damage phase", r"dps behavior", r"vulnerability"],
        "A boss is mentioned but no explicit vulnerability/DPS behavior contract was found.",
    ),
    "no_callout_collision": (
        [r"callout"],
        [r"collision", r"simultaneous"],
        "Callouts are present but simultaneous-callout/collision analysis was not found.",
    ),
    "no_blind_feedback": (
        [r"blind"],
        [r"hypothesis", r"feedback", r"breakthrough"],
        "Blind play is mentioned but the hypothesis/feedback loop may be underspecified.",
    ),
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def contains_all(text: str, patterns: list[str]) -> bool:
    return all(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def find_sections(text: str) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    normalized = normalize(text)

    for name, patterns in REQUIRED_SECTIONS.items():
        if contains_all(normalized, patterns):
            present.append(name)
        else:
            missing.append(name)
    return present, missing


def find_warnings(text: str) -> list[dict[str, str]]:
    normalized = normalize(text)
    warnings: list[dict[str, str]] = []

    for code, (trigger_patterns, expected_patterns, message) in WARNING_PATTERNS.items():
        if any(re.search(p, normalized) for p in trigger_patterns) and not any(
            re.search(p, normalized) for p in expected_patterns
        ):
            warnings.append({"code": code, "message": message})

    encounter_count = len(re.findall(r"^##+\s+Encounter\b", text, flags=re.IGNORECASE | re.MULTILINE))
    if encounter_count == 0:
        warnings.append(
            {
                "code": "no_encounter_cards",
                "message": "No headings beginning with 'Encounter' were found; verify this is a raid-level design rather than only a concept note.",
            }
        )

    if "<" in text and ">" in text:
        template_tokens = re.findall(r"<[^>\n]+>", text)
        if template_tokens:
            warnings.append(
                {
                    "code": "template_tokens_remaining",
                    "message": f"Template placeholders appear to remain ({len(template_tokens)} found).",
                }
            )

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a raid design Markdown artifact.")
    parser.add_argument("path", type=Path, help="Path to raid design Markdown file")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2

    text = args.path.read_text(encoding="utf-8")
    present, missing = find_sections(text)
    warnings = find_warnings(text)

    result = {
        "path": str(args.path),
        "structurally_complete": not missing,
        "present_sections": present,
        "missing_sections": missing,
        "warnings": warnings,
        "note": "Structural completeness does not prove encounter quality; blind/repeat playtests are still required.",
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Raid design: {args.path}")
        print(f"Structural sections present: {len(present)}/{len(REQUIRED_SECTIONS)}")
        if missing:
            print("Missing required contracts:")
            for item in missing:
                print(f"  - {item}")
        else:
            print("All required structural contracts were detected.")

        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"  - [{warning['code']}] {warning['message']}")

        print("NOTE: structural validation is not a playtest.")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
