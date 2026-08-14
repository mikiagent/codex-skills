#!/usr/bin/env python3
"""Audit a web/Capacitor project for iOS release readiness without modifying it."""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


@dataclass
class Finding:
    severity: str
    area: str
    message: str


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_semver_major(value: Any) -> int | None:
    if not isinstance(value, str):
        return None
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else None


def command_version(command: list[str]) -> str | None:
    if not shutil.which(command[0]):
        return None
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    output = (result.stdout or result.stderr).strip()
    return output.splitlines()[0] if output else None


def find_capacitor_config(project: Path) -> tuple[Path | None, dict[str, str]]:
    for name in ("capacitor.config.ts", "capacitor.config.js", "capacitor.config.json"):
        path = project / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        values: dict[str, str] = {}
        for key in ("appId", "appName", "webDir"):
            match = re.search(rf"\b{key}\s*[:=]\s*['\"]([^'\"]+)['\"]", text)
            if match:
                values[key] = match.group(1)
        return path, values
    return None, {}


def find_info_plist(project: Path) -> Path | None:
    candidates = (
        project / "ios" / "App" / "App" / "Info.plist",
        project / "ios" / "App" / "App" / "info.plist",
    )
    for path in candidates:
        if path.exists():
            return path
    matches = [path for path in (project / "ios").glob("**/[Ii]nfo.plist") if "Pods" not in path.parts]
    return matches[0] if matches else None


def read_plist(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("rb") as handle:
            data = plistlib.load(handle)
        return data if isinstance(data, dict) else None
    except (OSError, plistlib.InvalidFileException):
        return None


def pbx_values(text: str, key: str) -> list[str]:
    pattern = re.compile(rf"\b{re.escape(key)}\s*=\s*([^;]+);")
    return sorted({match.group(1).strip().strip('"') for match in pattern.finditer(text)})


def inspect_app_icon(project: Path) -> tuple[bool, str]:
    content_files = [
        path for path in (project / "ios").glob("**/AppIcon.appiconset/Contents.json")
        if "Pods" not in path.parts
    ]
    if not content_files:
        return False, "AppIcon.appiconset/Contents.json was not found"
    for contents_path in content_files:
        try:
            data = read_json(contents_path)
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("images", []):
            if not isinstance(item, dict):
                continue
            if item.get("idiom") == "ios-marketing" and item.get("size") == "1024x1024":
                filename = item.get("filename")
                if filename and (contents_path.parent / filename).exists():
                    return True, str(contents_path.parent / filename)
                return False, "1024x1024 iOS marketing icon entry has no existing file"
    return False, "1024x1024 iOS marketing icon entry was not found"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true", help="Treat missing release prerequisites as errors")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = args.project.expanduser().resolve()
    findings: list[Finding] = []
    facts: dict[str, Any] = {"project": str(project)}

    def add(severity: str, area: str, message: str) -> None:
        findings.append(Finding(severity, area, message))

    def release_issue(area: str, message: str) -> None:
        add("error" if args.strict else "warning", area, message)

    if not project.is_dir():
        print(f"error: project directory does not exist: {project}", file=sys.stderr)
        return 2

    package_path = project / "package.json"
    package: dict[str, Any] = {}
    if not package_path.exists():
        add("error", "web", "package.json was not found")
    else:
        try:
            package = read_json(package_path)
        except (OSError, json.JSONDecodeError) as exc:
            add("error", "web", f"package.json could not be read: {exc}")

    scripts = package.get("scripts", {}) if isinstance(package.get("scripts"), dict) else {}
    dependencies: dict[str, str] = {}
    for section in ("dependencies", "devDependencies"):
        values = package.get(section, {})
        if isinstance(values, dict):
            dependencies.update({str(key): str(value) for key, value in values.items()})
    facts["packageName"] = package.get("name")
    facts["packageVersion"] = package.get("version")
    facts["buildScript"] = scripts.get("build")
    if "build" not in scripts:
        add("error", "web", "package.json has no build script")
    if "three" not in dependencies:
        add("warning", "web", "Three.js dependency was not detected; confirm this is the intended project")

    cap_packages = {name: value for name, value in dependencies.items() if name.startswith("@capacitor/")}
    cap_majors = {name: parse_semver_major(value) for name, value in cap_packages.items()}
    facts["capacitorPackages"] = cap_packages
    known_majors = {major for major in cap_majors.values() if major is not None}
    if len(known_majors) > 1:
        add("error", "capacitor", f"@capacitor packages use mixed major versions: {cap_majors}")
    for required in ("@capacitor/core", "@capacitor/cli", "@capacitor/ios"):
        if required not in cap_packages:
            release_issue("capacitor", f"missing package: {required}")

    cap_path, cap_values = find_capacitor_config(project)
    facts["capacitorConfig"] = str(cap_path) if cap_path else None
    facts.update({f"capacitor{key[0].upper()}{key[1:]}": value for key, value in cap_values.items()})
    if not cap_path:
        release_issue("capacitor", "capacitor.config.* was not found")
    else:
        for key in ("appId", "appName", "webDir"):
            if not cap_values.get(key):
                add("error", "capacitor", f"Capacitor config does not expose a string {key}")
        web_dir = cap_values.get("webDir")
        if web_dir and not (project / web_dir).is_dir():
            release_issue("capacitor", f"built webDir does not exist yet: {web_dir}; run the web build")

    ios_dir = project / "ios"
    if not ios_dir.is_dir():
        release_issue("ios", "ios/ platform directory was not found")
    project_files = list(ios_dir.glob("**/*.xcodeproj/project.pbxproj")) if ios_dir.exists() else []
    workspaces = list(ios_dir.glob("**/*.xcworkspace")) if ios_dir.exists() else []
    uses_pods = (ios_dir / "App" / "Podfile").exists() or any(ios_dir.glob("**/Podfile")) if ios_dir.exists() else False
    uses_spm = any(ios_dir.glob("**/CapApp-SPM/Package.swift")) if ios_dir.exists() else False
    facts["iosPackageManager"] = "spm" if uses_spm else "cocoapods" if uses_pods else "unknown"
    facts["xcodeProjects"] = [str(path.parent) for path in project_files]
    facts["xcodeWorkspaces"] = [str(path) for path in workspaces]
    if ios_dir.exists() and not project_files:
        add("error", "ios", "Xcode project.pbxproj was not found")
    if uses_spm and workspaces:
        add("warning", "ios", "both SPM evidence and workspaces exist; confirm which project Fastlane should build")
    if uses_spm:
        add("info", "fastlane", "set IOS_PROJECT for SPM projects unless an intentional workspace is used")
    elif uses_pods and not workspaces:
        release_issue("ios", "CocoaPods project has no .xcworkspace")

    pbx_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in project_files)
    for key in (
        "PRODUCT_BUNDLE_IDENTIFIER",
        "MARKETING_VERSION",
        "CURRENT_PROJECT_VERSION",
        "IPHONEOS_DEPLOYMENT_TARGET",
        "TARGETED_DEVICE_FAMILY",
        "DEVELOPMENT_TEAM",
        "CODE_SIGN_STYLE",
    ):
        values = pbx_values(pbx_text, key) if pbx_text else []
        facts[key] = values
        if key in {"PRODUCT_BUNDLE_IDENTIFIER", "MARKETING_VERSION", "CURRENT_PROJECT_VERSION", "IPHONEOS_DEPLOYMENT_TARGET"} and not values and ios_dir.exists():
            release_issue("xcode", f"{key} was not found in project settings")
    bundle_values = [value for value in facts.get("PRODUCT_BUNDLE_IDENTIFIER", []) if "$" not in value]
    if cap_values.get("appId") and bundle_values and cap_values["appId"] not in bundle_values:
        add("error", "identity", f"Capacitor appId {cap_values['appId']} does not match Xcode bundle identifiers {bundle_values}")

    cap_major = cap_majors.get("@capacitor/core")
    targets = []
    for value in facts.get("IPHONEOS_DEPLOYMENT_TARGET", []):
        try:
            targets.append(float(value))
        except ValueError:
            pass
    if cap_major is not None and cap_major >= 8 and targets and min(targets) < 15:
        add("error", "xcode", "Capacitor 8 requires an iOS 15+ deployment target")

    plist_path = find_info_plist(project) if ios_dir.exists() else None
    plist = read_plist(plist_path) if plist_path else None
    facts["infoPlist"] = str(plist_path) if plist_path else None
    if ios_dir.exists() and not plist_path:
        add("error", "ios", "application Info.plist was not found")
    elif plist_path and plist is None:
        add("error", "ios", f"Info.plist could not be parsed: {plist_path}")

    native_plugins = sorted(
        name for name in dependencies
        if name.startswith("@capacitor/") or "capacitor" in name or name.startswith("cordova-plugin-")
    )
    facts["nativePlugins"] = native_plugins
    risk_tokens = ("admob", "analytics", "firebase", "sentry", "revenuecat", "purchases", "facebook", "adjust", "appsflyer")
    risk_dependencies = sorted(name for name in dependencies if any(token in name.casefold() for token in risk_tokens))
    facts["privacySensitiveDependencies"] = risk_dependencies
    if risk_dependencies:
        release_issue("privacy", f"reconcile third-party SDK data flows and manifests: {', '.join(risk_dependencies)}")

    privacy_manifests = [
        path for path in ios_dir.glob("**/PrivacyInfo.xcprivacy")
        if "Pods" not in path.parts and "DerivedData" not in path.parts
    ] if ios_dir.exists() else []
    facts["privacyManifests"] = [str(path) for path in privacy_manifests]
    if ios_dir.exists() and native_plugins and not privacy_manifests:
        release_issue("privacy", "no app PrivacyInfo.xcprivacy was found; determine required-reason API and data declarations")

    if plist is not None:
        if "@capacitor-community/admob" in dependencies:
            for key in ("GADApplicationIdentifier", "SKAdNetworkItems"):
                if not plist.get(key):
                    add("error", "ads", f"Info.plist is missing {key}")
            if not plist.get("NSUserTrackingUsageDescription"):
                add("warning", "ads", "NSUserTrackingUsageDescription is absent; this is correct only if ATT is not requested")
        if "ITSAppUsesNonExemptEncryption" not in plist:
            release_issue("compliance", "ITSAppUsesNonExemptEncryption is not explicit; complete export-compliance determination")

    has_icon, icon_message = inspect_app_icon(project) if ios_dir.exists() else (False, "iOS project not present")
    facts["appStoreIcon"] = icon_message if has_icon else None
    if ios_dir.exists() and not has_icon:
        release_issue("assets", icon_message)

    tools = {
        "node": command_version(["node", "--version"]),
        "npm": command_version(["npm", "--version"]),
        "xcodebuild": command_version(["xcodebuild", "-version"]),
        "ruby": command_version(["ruby", "--version"]),
        "bundle": command_version(["bundle", "--version"]),
        "fastlane": command_version(["fastlane", "--version"]),
    }
    facts["tools"] = tools
    for tool in ("node", "npm", "xcodebuild", "bundle"):
        if not tools[tool]:
            release_issue("tools", f"required release tool is unavailable: {tool}")
    if not tools["fastlane"]:
        release_issue("tools", "fastlane is unavailable; install through the project's Bundler workflow")

    for relative in ("Gemfile", "fastlane/Fastfile", "fastlane/Appfile", "fastlane/Snapfile"):
        if not (project / relative).exists():
            release_issue("fastlane", f"missing release automation file: {relative}")

    secret_candidates = []
    for base in (project, project / "release", project / "fastlane", project / "ios"):
        if base.is_dir():
            secret_candidates.extend(path for path in base.glob("*.p8") if path.is_file())
    for path in sorted(set(secret_candidates)):
        add("error", "secrets", f"App Store Connect private key is inside the project: {path}")

    release_config = project / "release" / "app-store.json"
    facts["releaseConfig"] = str(release_config) if release_config.exists() else None
    if not release_config.exists():
        release_issue("manifest", "release/app-store.json was not found")
    else:
        try:
            manifest_data = read_json(release_config)
        except (OSError, json.JSONDecodeError) as exc:
            manifest_data = {}
            add("error", "manifest", f"release/app-store.json could not be read: {exc}")
        manifest_app = manifest_data.get("app", {}) if isinstance(manifest_data.get("app"), dict) else {}
        manifest_version = manifest_data.get("version", {}) if isinstance(manifest_data.get("version"), dict) else {}
        manifest_bundle = manifest_app.get("bundleId")
        if manifest_bundle and cap_values.get("appId") and manifest_bundle != cap_values["appId"]:
            add("error", "identity", f"manifest bundleId {manifest_bundle} does not match Capacitor appId {cap_values['appId']}")
        if manifest_bundle and bundle_values and manifest_bundle not in bundle_values:
            add("error", "identity", f"manifest bundleId {manifest_bundle} does not match Xcode bundle identifiers {bundle_values}")
        native_versions = [value for value in facts.get("MARKETING_VERSION", []) if "$" not in value]
        if manifest_version.get("marketingVersion") and native_versions and manifest_version["marketingVersion"] not in native_versions:
            add("error", "version", f"manifest marketingVersion {manifest_version['marketingVersion']} does not match Xcode values {native_versions}")
        native_builds = [value for value in facts.get("CURRENT_PROJECT_VERSION", []) if "$" not in value]
        if manifest_version.get("buildNumber") and native_builds and manifest_version["buildNumber"] not in native_builds:
            add("error", "version", f"manifest buildNumber {manifest_version['buildNumber']} does not match Xcode values {native_builds}")
        command = [sys.executable, str(SCRIPT_DIR / "validate_release.py"), "--config", str(release_config), "--json"]
        if args.strict:
            command.append("--strict")
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        try:
            validation = json.loads(result.stdout)
            for finding in validation.get("findings", []):
                severity = finding.get("severity", "warning")
                add(severity, f"manifest:{finding.get('path', '$')}", finding.get("message", "validation finding"))
        except json.JSONDecodeError:
            add("error", "manifest", "release validator did not return readable JSON")

    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    release_ready = args.strict and not errors
    if args.json:
        print(json.dumps({
            "project": str(project),
            "strict": args.strict,
            "ready": release_ready,
            "errorCount": len(errors),
            "warningCount": len(warnings),
            "facts": facts,
            "findings": [asdict(finding) for finding in findings],
        }, indent=2))
    else:
        for finding in findings:
            print(f"{finding.severity.upper():7} {finding.area}: {finding.message}")
        print(f"\nAudit: {len(errors)} error(s), {len(warnings)} warning(s)")
        if not args.strict:
            print("AUDIT COMPLETE — run with --strict for a release gate")
        else:
            print("RELEASE READY" if release_ready else "NOT RELEASE READY")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
