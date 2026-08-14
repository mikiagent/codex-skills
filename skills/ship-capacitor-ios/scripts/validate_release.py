#!/usr/bin/env python3
"""Validate the ship-capacitor-ios release manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


APP_STORE_LOCALES = {
    "ar-SA", "bn-BD", "ca", "cs", "da", "de-DE", "el", "en-AU", "en-CA",
    "en-GB", "en-US", "es-ES", "es-MX", "fi", "fr-CA", "fr-FR", "gu-IN",
    "he", "hi", "hr", "hu", "id", "it", "ja", "kn-IN", "ko", "ml-IN",
    "mr-IN", "ms", "nl-NL", "no", "or-IN", "pa-IN", "pl", "pt-BR", "pt-PT",
    "ro", "ru", "sk", "sl-SI", "sv", "ta-IN", "te-IN", "th", "tr", "uk",
    "ur-PK", "vi", "zh-Hans", "zh-Hant",
}

CATEGORIES = {
    "BOOKS", "BUSINESS", "DEVELOPER_TOOLS", "EDUCATION", "ENTERTAINMENT",
    "FINANCE", "FOOD_AND_DRINK", "GAMES", "GRAPHICS_AND_DESIGN",
    "HEALTH_AND_FITNESS", "LIFESTYLE", "MAGAZINES_AND_NEWSPAPERS", "MEDICAL",
    "MUSIC", "NAVIGATION", "NEWS", "PHOTO_AND_VIDEO", "PRODUCTIVITY",
    "REFERENCE", "SHOPPING", "SOCIAL_NETWORKING", "SPORTS", "STICKERS",
    "TRAVEL", "UTILITIES", "WEATHER",
}

PRODUCT_TYPES = {
    "consumable", "non-consumable", "non-renewing-subscription",
    "auto-renewable-subscription",
}

MONETIZATION_MODELS = {"none", "iap", "subscriptions", "ads", "hybrid"}
IAP_PROVIDERS = {"none", "revenuecat", "storekit", "cordova-plugin-purchase", "other"}
AD_PROVIDERS = {"none", "admob", "other"}
SCREENSHOT_FAMILIES = {"iphone-6.9", "iphone-6.5", "ipad-13"}
ACCESSIBILITY_FEATURES = {
    "voiceover", "voice-control", "larger-text", "dark-interface",
    "differentiate-without-color", "sufficient-contrast", "reduced-motion",
    "captions", "audio-descriptions",
}


@dataclass
class Finding:
    severity: str
    path: str
    message: str


class Validator:
    def __init__(self, config_path: Path, strict: bool) -> None:
        self.config_path = config_path
        self.project_root = config_path.parent.parent
        self.strict = strict
        self.findings: list[Finding] = []

    def error(self, path: str, message: str) -> None:
        self.findings.append(Finding("error", path, message))

    def warning(self, path: str, message: str) -> None:
        self.findings.append(Finding("warning", path, message))

    def release_fact(self, condition: bool, path: str, message: str) -> None:
        if condition:
            return
        (self.error if self.strict else self.warning)(path, message)

    def required_string(self, value: Any, path: str, *, allow_placeholder: bool = False) -> str:
        if not isinstance(value, str) or not value.strip():
            self.error(path, "must be a non-empty string")
            return ""
        text = value.strip()
        if not allow_placeholder and is_placeholder(text):
            self.release_fact(False, path, "contains a placeholder")
        return text

    def optional_string(self, value: Any, path: str) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            self.error(path, "must be a string")
            return ""
        return value.strip()

    def validate_url(self, value: Any, path: str, *, required: bool) -> None:
        text = self.required_string(value, path) if required else self.optional_string(value, path)
        if not text:
            return
        parsed = urlparse(text)
        if parsed.scheme != "https" or not parsed.netloc:
            self.error(path, "must be a complete public HTTPS URL")
        if parsed.hostname in {"localhost", "127.0.0.1"} or parsed.hostname is None:
            self.error(path, "must not use a local host")
        if is_placeholder(text):
            self.release_fact(False, path, "uses a placeholder URL")

    def validate(self, data: Any) -> None:
        if not isinstance(data, dict):
            self.error("$", "root must be an object")
            return
        if data.get("schemaVersion") != 1:
            self.error("schemaVersion", "must equal 1")

        app = require_object(data, "app", self)
        version = require_object(data, "version", self)
        localizations = require_object(data, "localizations", self)
        review = require_object(data, "review", self)
        compliance = require_object(data, "compliance", self)
        accessibility = require_object(data, "accessibility", self)
        monetization = require_object(data, "monetization", self)
        screenshots = require_object(data, "screenshots", self)

        self.validate_app(app)
        self.validate_version(version)
        self.validate_localizations(localizations, version)
        self.validate_review(review)
        self.validate_compliance(compliance, version)
        self.validate_accessibility(accessibility, app)
        self.validate_monetization(monetization, compliance)
        self.validate_screenshots(screenshots, app, localizations)

    def validate_app(self, app: dict[str, Any]) -> None:
        name = self.required_string(app.get("name"), "app.name")
        if name and not 2 <= len(name) <= 30:
            self.error("app.name", "must be 2–30 characters")

        bundle_id = self.required_string(app.get("bundleId"), "app.bundleId")
        if bundle_id and not re.fullmatch(r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", bundle_id):
            self.error("app.bundleId", "must be a reverse-DNS identifier")

        self.required_string(app.get("sku"), "app.sku")
        self.required_string(app.get("copyright"), "app.copyright")

        primary = self.required_string(app.get("primaryCategory"), "app.primaryCategory", allow_placeholder=True)
        if primary and primary not in CATEGORIES:
            self.error("app.primaryCategory", f"unsupported category: {primary}")
        secondary = self.optional_string(app.get("secondaryCategory"), "app.secondaryCategory")
        if secondary and secondary not in CATEGORIES:
            self.error("app.secondaryCategory", f"unsupported category: {secondary}")
        if primary and secondary and primary == secondary:
            self.warning("app.secondaryCategory", "duplicates the primary category")

        families = app.get("deviceFamilies")
        if not isinstance(families, list) or not families:
            self.error("app.deviceFamilies", "must contain iphone and optionally ipad")
        else:
            unknown = sorted(set(families) - {"iphone", "ipad"})
            if unknown:
                self.error("app.deviceFamilies", f"unsupported values: {', '.join(unknown)}")
            if "iphone" not in families:
                self.warning("app.deviceFamilies", "an iOS release normally includes iphone")

    def validate_version(self, version: dict[str, Any]) -> None:
        marketing = self.required_string(version.get("marketingVersion"), "version.marketingVersion", allow_placeholder=True)
        if marketing and not re.fullmatch(r"\d+(?:\.\d+){0,2}", marketing):
            self.error("version.marketingVersion", "must contain one to three numeric components")
        build = self.required_string(version.get("buildNumber"), "version.buildNumber", allow_placeholder=True)
        if build and (not build.isdigit() or int(build) < 1):
            self.error("version.buildNumber", "must be a positive integer string")
        if not isinstance(version.get("isFirstRelease"), bool):
            self.error("version.isFirstRelease", "must be true or false")
        mode = version.get("releaseMode")
        if mode not in {"manual", "automatic"}:
            self.error("version.releaseMode", "must be manual or automatic")
        if not isinstance(version.get("phasedRelease"), bool):
            self.error("version.phasedRelease", "must be true or false")
        if version.get("isFirstRelease") and version.get("phasedRelease"):
            self.error("version.phasedRelease", "phased release applies to updates, not a first release")
        if version.get("phasedRelease") and mode != "automatic":
            self.warning("version.phasedRelease", "confirm phased release behavior with the selected release mode")
        self.release_fact(
            version.get("testFlightVerified") is True,
            "version.testFlightVerified",
            "the processed TestFlight build has not been confirmed as tested",
        )

    def validate_localizations(self, localizations: dict[str, Any], version: dict[str, Any]) -> None:
        if not localizations:
            self.error("localizations", "must contain at least one locale")
            return
        for locale, raw in localizations.items():
            base = f"localizations.{locale}"
            if locale not in APP_STORE_LOCALES:
                self.error(base, "is not a supported App Store locale code")
            if not isinstance(raw, dict):
                self.error(base, "must be an object")
                continue
            name = self.required_string(raw.get("name"), f"{base}.name")
            if name and not 2 <= len(name) <= 30:
                self.error(f"{base}.name", "must be 2–30 characters")
            subtitle = self.optional_string(raw.get("subtitle"), f"{base}.subtitle")
            if len(subtitle) > 30:
                self.error(f"{base}.subtitle", "must be at most 30 characters")
            if subtitle and is_placeholder(subtitle):
                self.release_fact(False, f"{base}.subtitle", "contains a placeholder")
            description = self.required_string(raw.get("description"), f"{base}.description")
            if len(description) > 4000:
                self.error(f"{base}.description", "must be at most 4,000 characters")
            keywords = self.required_string(raw.get("keywords"), f"{base}.keywords")
            if len(keywords.encode("utf-8")) > 100:
                self.error(f"{base}.keywords", "must be at most 100 UTF-8 bytes")
            for item in [part.strip() for part in keywords.split(",") if part.strip()]:
                if len(item) <= 2:
                    self.warning(f"{base}.keywords", f"keyword is too short: {item!r}")
            promo = self.optional_string(raw.get("promotionalText"), f"{base}.promotionalText")
            if len(promo) > 170:
                self.error(f"{base}.promotionalText", "must be at most 170 characters")
            whats_new = self.optional_string(raw.get("whatsNew"), f"{base}.whatsNew")
            if len(whats_new) > 4000:
                self.error(f"{base}.whatsNew", "must be at most 4,000 characters")
            if version.get("isFirstRelease") is False:
                self.release_fact(bool(whats_new) and not is_placeholder(whats_new), f"{base}.whatsNew", "is required for an update")
            elif whats_new:
                self.warning(f"{base}.whatsNew", "Apple does not expose What's New for the first version")
            self.validate_url(raw.get("supportUrl"), f"{base}.supportUrl", required=True)
            self.validate_url(raw.get("privacyUrl"), f"{base}.privacyUrl", required=True)
            self.validate_url(raw.get("marketingUrl"), f"{base}.marketingUrl", required=False)

    def validate_review(self, review: dict[str, Any]) -> None:
        contact = require_object(review, "contact", self, prefix="review")
        self.required_string(contact.get("firstName"), "review.contact.firstName")
        self.required_string(contact.get("lastName"), "review.contact.lastName")
        email = self.required_string(contact.get("email"), "review.contact.email")
        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            self.error("review.contact.email", "must be a valid email address")
        self.required_string(contact.get("phone"), "review.contact.phone")
        notes = self.required_string(review.get("notes"), "review.notes")
        if len(notes.encode("utf-8")) > 4000:
            self.error("review.notes", "must be at most 4,000 UTF-8 bytes")
        requires_login = review.get("requiresLogin")
        if not isinstance(requires_login, bool):
            self.error("review.requiresLogin", "must be true or false")
        if requires_login:
            for key in ("demoUserEnv", "demoPasswordEnv"):
                env_name = self.required_string(review.get(key), f"review.{key}", allow_placeholder=True)
                if env_name and not re.fullmatch(r"[A-Z][A-Z0-9_]*", env_name):
                    self.error(f"review.{key}", "must name an uppercase environment variable")

    def validate_compliance(self, compliance: dict[str, Any], version: dict[str, Any]) -> None:
        confirmations = (
            "contentRightsConfirmed",
            "privacyAnswersConfirmed",
            "ageRatingConfirmed",
            "exportComplianceConfirmed",
            "thirdPartySdksReviewed",
            "agreementsConfirmed",
        )
        for key in confirmations:
            self.release_fact(compliance.get(key) is True, f"compliance.{key}", "must be explicitly confirmed for this release")
        self.release_fact(isinstance(compliance.get("usesTracking"), bool), "compliance.usesTracking", "must be determined as true or false")

        privacy = require_object(compliance, "privacy", self, prefix="compliance")
        collects_data = privacy.get("collectsData")
        self.release_fact(isinstance(collects_data, bool), "compliance.privacy.collectsData", "must be determined as true or false")
        data_types = privacy.get("dataTypes")
        if not isinstance(data_types, list):
            self.error("compliance.privacy.dataTypes", "must be an array")
        else:
            if any(not isinstance(item, str) or not item.strip() for item in data_types):
                self.error("compliance.privacy.dataTypes", "must contain non-empty string identifiers")
            if collects_data is True:
                self.release_fact(bool(data_types), "compliance.privacy.dataTypes", "record every collected App Store data type")
            if collects_data is False and data_types:
                self.error("compliance.privacy.dataTypes", "must be empty when collectsData is false")

        age_rating = require_object(compliance, "ageRating", self, prefix="compliance")
        answers = age_rating.get("answers")
        if not isinstance(answers, dict):
            self.error("compliance.ageRating.answers", "must be an object mirroring the current questionnaire")
        else:
            self.release_fact(bool(answers), "compliance.ageRating.answers", "record the current questionnaire answers")

        export = require_object(compliance, "exportCompliance", self, prefix="compliance")
        self.release_fact(isinstance(export.get("usesEncryption"), bool), "compliance.exportCompliance.usesEncryption", "must be determined as true or false")
        self.release_fact(isinstance(export.get("usesNonExemptEncryption"), bool), "compliance.exportCompliance.usesNonExemptEncryption", "must be determined as true or false")
        status = self.optional_string(export.get("documentationStatus"), "compliance.exportCompliance.documentationStatus")
        self.release_fact(bool(status) and status != "unconfirmed", "compliance.exportCompliance.documentationStatus", "record the resulting documentation status")

    def validate_accessibility(self, accessibility: dict[str, Any], app: dict[str, Any]) -> None:
        self.release_fact(accessibility.get("reviewed") is True, "accessibility.reviewed", "evaluate common tasks for Accessibility Nutrition Labels")
        self.validate_url(accessibility.get("url"), "accessibility.url", required=False)
        devices = accessibility.get("devices")
        if not isinstance(devices, dict):
            self.error("accessibility.devices", "must be an object keyed by supported device family")
            return
        app_families = app.get("deviceFamilies") if isinstance(app.get("deviceFamilies"), list) else []
        for family in app_families:
            path = f"accessibility.devices.{family}"
            device = devices.get(family)
            if not isinstance(device, dict):
                self.release_fact(False, path, "record an accessibility declaration for this supported device")
                continue
            supports_any = device.get("supportsAny")
            self.release_fact(isinstance(supports_any, bool), f"{path}.supportsAny", "must be determined as true or false")
            features = device.get("features")
            if not isinstance(features, list):
                self.error(f"{path}.features", "must be an array")
                continue
            unknown = sorted(set(features) - ACCESSIBILITY_FEATURES) if all(isinstance(item, str) for item in features) else []
            if any(not isinstance(item, str) for item in features):
                self.error(f"{path}.features", "must contain string identifiers")
            if unknown:
                self.error(f"{path}.features", f"unsupported identifiers: {', '.join(unknown)}")
            if supports_any is True and not features:
                self.error(f"{path}.features", "must list at least one evaluated feature when supportsAny is true")
            if supports_any is False and features:
                self.error(f"{path}.features", "must be empty when supportsAny is false")

    def validate_monetization(self, monetization: dict[str, Any], compliance: dict[str, Any]) -> None:
        model = monetization.get("model")
        if model not in MONETIZATION_MODELS:
            self.error("monetization.model", f"must be one of: {', '.join(sorted(MONETIZATION_MODELS))}")
            return
        iap_provider = monetization.get("iapProvider")
        if iap_provider not in IAP_PROVIDERS:
            self.error("monetization.iapProvider", f"must be one of: {', '.join(sorted(IAP_PROVIDERS))}")
        products = monetization.get("products")
        if not isinstance(products, list):
            self.error("monetization.products", "must be an array")
            products = []

        needs_iap = model in {"iap", "subscriptions", "hybrid"}
        if needs_iap:
            self.release_fact(iap_provider not in {None, "none"}, "monetization.iapProvider", "an IAP provider is required")
            self.release_fact(bool(products), "monetization.products", "at least one product is required")
            self.release_fact(compliance.get("agreementsConfirmed") is True, "compliance.agreementsConfirmed", "paid-app agreements must be active")
        elif products:
            self.warning("monetization.products", "products exist while the monetization model does not include IAP")

        seen_ids: set[str] = set()
        for index, product in enumerate(products):
            base = f"monetization.products[{index}]"
            if not isinstance(product, dict):
                self.error(base, "must be an object")
                continue
            product_id = self.required_string(product.get("id"), f"{base}.id")
            if product_id and not re.fullmatch(r"[A-Za-z0-9._-]{1,100}", product_id):
                self.error(f"{base}.id", "contains unsupported characters or exceeds 100 characters")
            if product_id in seen_ids:
                self.error(f"{base}.id", "duplicates another product ID")
            seen_ids.add(product_id)
            if product.get("type") not in PRODUCT_TYPES:
                self.error(f"{base}.type", f"must be one of: {', '.join(sorted(PRODUCT_TYPES))}")
            reference = self.required_string(product.get("referenceName"), f"{base}.referenceName")
            if len(reference) > 64:
                self.error(f"{base}.referenceName", "must be at most 64 characters")
            self.release_fact(bool(self.optional_string(product.get("priceReference"), f"{base}.priceReference")), f"{base}.priceReference", "record the intended reference price")
            localizations = product.get("localizations")
            if not isinstance(localizations, dict) or not localizations:
                self.error(f"{base}.localizations", "must contain at least one localization")
            else:
                for locale, localized in localizations.items():
                    path = f"{base}.localizations.{locale}"
                    if locale not in APP_STORE_LOCALES:
                        self.error(path, "uses an unsupported locale")
                    if not isinstance(localized, dict):
                        self.error(path, "must be an object")
                        continue
                    display = self.required_string(localized.get("displayName"), f"{path}.displayName")
                    if display and not 2 <= len(display) <= 30:
                        self.error(f"{path}.displayName", "must be 2–30 characters")
                    description = self.required_string(localized.get("description"), f"{path}.description")
                    if len(description) > 45:
                        self.error(f"{path}.description", "must be at most 45 characters")
            screenshot = self.optional_string(product.get("reviewScreenshot"), f"{base}.reviewScreenshot")
            self.release_fact(bool(screenshot), f"{base}.reviewScreenshot", "an App Review screenshot path is required")
            if screenshot and not (self.project_root / screenshot).exists():
                self.release_fact(False, f"{base}.reviewScreenshot", f"file does not exist: {screenshot}")

        ads = require_object(monetization, "ads", self, prefix="monetization")
        provider = ads.get("provider")
        if provider not in AD_PROVIDERS:
            self.error("monetization.ads.provider", f"must be one of: {', '.join(sorted(AD_PROVIDERS))}")
        needs_ads = model in {"ads", "hybrid"}
        if needs_ads:
            self.release_fact(provider not in {None, "none"}, "monetization.ads.provider", "an ad provider is required")
            self.release_fact(ads.get("consentFlow") == "ump" if provider == "admob" else bool(ads.get("consentFlow")), "monetization.ads.consentFlow", "a verified consent flow is required")
            self.release_fact(ads.get("testModeVerified") is True, "monetization.ads.testModeVerified", "ad test mode and production-ID separation must be verified")
            self.release_fact(isinstance(compliance.get("usesTracking"), bool), "compliance.usesTracking", "tracking must be determined before ads ship")
        elif provider not in {None, "none"}:
            self.warning("monetization.ads.provider", "an ad provider is set while the model does not include ads")
        if ads.get("personalized") is True and compliance.get("usesTracking") is False:
            self.warning("monetization.ads.personalized", "reconcile personalized ad behavior with the no-tracking determination")

    def validate_screenshots(self, screenshots: dict[str, Any], app: dict[str, Any], localizations: dict[str, Any]) -> None:
        if screenshots.get("strategy") not in {"fastlane-snapshot", "manual", "other"}:
            self.error("screenshots.strategy", "must be fastlane-snapshot, manual, or other")
        locales = screenshots.get("locales")
        if not isinstance(locales, list) or not locales:
            self.error("screenshots.locales", "must contain at least one locale")
            locales = []
        for locale in locales:
            if locale not in localizations:
                self.error("screenshots.locales", f"locale has no metadata localization: {locale}")
        families = screenshots.get("deviceFamilies")
        if not isinstance(families, list) or not families:
            self.error("screenshots.deviceFamilies", "must contain at least one device family")
            families = []
        unknown = sorted(set(families) - SCREENSHOT_FAMILIES)
        if unknown:
            self.error("screenshots.deviceFamilies", f"unsupported values: {', '.join(unknown)}")
        app_families = app.get("deviceFamilies") if isinstance(app.get("deviceFamilies"), list) else []
        if "iphone" in app_families and not ({"iphone-6.9", "iphone-6.5"} & set(families)):
            self.error("screenshots.deviceFamilies", "iPhone support requires iphone-6.9 or Apple's current fallback family")
        if "ipad" in app_families and "ipad-13" not in families:
            self.error("screenshots.deviceFamilies", "iPad support requires ipad-13 screenshots")
        states = screenshots.get("states")
        if not isinstance(states, list) or not states:
            self.error("screenshots.states", "must contain one to ten screenshot states")
            return
        if len(states) > 10:
            self.error("screenshots.states", "Apple permits at most ten screenshots per set")
        seen: set[str] = set()
        for index, state in enumerate(states):
            base = f"screenshots.states[{index}]"
            if not isinstance(state, dict):
                self.error(base, "must be an object")
                continue
            state_id = self.required_string(state.get("id"), f"{base}.id")
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", state_id):
                self.error(f"{base}.id", "must use lowercase letters, digits, and hyphens")
            if state_id in seen:
                self.error(f"{base}.id", "duplicates another screenshot state")
            seen.add(state_id)
            self.required_string(state.get("description"), f"{base}.description")


def is_placeholder(text: str) -> bool:
    lowered = text.casefold()
    return any(token in lowered for token in ("todo", "example.com", "com.example", "<app", "replace me", "your-"))


def require_object(data: dict[str, Any], key: str, validator: Validator, prefix: str = "") -> dict[str, Any]:
    path = f"{prefix}.{key}" if prefix else key
    value = data.get(key)
    if not isinstance(value, dict):
        validator.error(path, "must be an object")
        return {}
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="Path to release/app-store.json")
    parser.add_argument("--strict", action="store_true", help="Treat unresolved release facts as errors")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = args.config.expanduser().resolve()
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: config does not exist: {config_path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {config_path}: {exc}", file=sys.stderr)
        return 2

    validator = Validator(config_path, args.strict)
    validator.validate(data)
    errors = [finding for finding in validator.findings if finding.severity == "error"]
    warnings = [finding for finding in validator.findings if finding.severity == "warning"]

    if args.json:
        print(json.dumps({
            "config": str(config_path),
            "strict": args.strict,
            "valid": not errors,
            "errorCount": len(errors),
            "warningCount": len(warnings),
            "findings": [asdict(finding) for finding in validator.findings],
        }, indent=2))
    else:
        for finding in validator.findings:
            print(f"{finding.severity.upper():7} {finding.path}: {finding.message}")
        print(f"\nRelease manifest: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("VALID" if not errors else "NOT READY")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
