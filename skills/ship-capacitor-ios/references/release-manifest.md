# Release manifest contract

`release/app-store.json` is the reviewable source of truth for one App Store candidate. The scaffold copies `assets/release-config.example.json` and fills discoverable project identifiers.

## Main sections

- `app`: stable identity, categories, copyright, device families.
- `version`: marketing/build version, first-release flag, release mode, phased release.
- `localizations`: store copy and public URLs by App Store locale.
- `review`: contact, notes, login requirement, and environment-variable names for demo credentials.
- `compliance`: explicit privacy, age-rating, export, rights, SDK, agreement, and tracking evidence.
- `accessibility`: per-device Accessibility Nutrition Label evaluation without inferred claims.
- `monetization`: model, provider, products, ads, and test evidence.
- `screenshots`: capture strategy, locales, device families, and named states.

## Drafting rules

- Use the app's real UI and source as evidence for feature claims.
- Use `TODO` or `null` for missing information.
- Do not put passwords, API keys, receipts, banking data, or tax data in the manifest.
- Keep `demoUserEnv` and `demoPasswordEnv` as environment-variable names.
- Keep product IDs stable once created in App Store Connect.
- Use Apple locale codes supported by App Store Connect.
- Express keywords as one comma-separated string; the validator measures UTF-8 bytes.
- Set `isFirstRelease` accurately because What's New is unavailable for the first version and required for updates.

## Confirmation meanings

Set confirmation fields to `true` only after the named fact has been checked for this binary and release:

- `contentRightsConfirmed`: the developer has rights to all included/marketed content.
- `privacyAnswersConfirmed`: App Store answers cover the app and third-party SDKs.
- `ageRatingConfirmed`: the current questionnaire reflects content and capabilities.
- `exportComplianceConfirmed`: encryption use and documentation were determined.
- `thirdPartySdksReviewed`: included SDK privacy manifests/data behavior were reviewed.
- `agreementsConfirmed`: required Apple agreements are active.
- `testFlightVerified`: the processed TestFlight build passed the release smoke test.

`usesTracking` must be `true` or `false` from an actual data-flow determination, never from whether ATT code happens to be present.

Also record the underlying declarations, not just confirmations:

- `compliance.privacy.collectsData` and `dataTypes` from the app and every third-party SDK;
- `compliance.ageRating.answers` using the current App Store Connect/API questionnaire keys;
- `compliance.exportCompliance` with encryption and non-exempt-encryption determinations;
- `accessibility.devices` after evaluating every common task on each supported device. Set `supportsAny` to false rather than claiming features that were not fully evaluated.

## Monetization products

Each product includes:

```json
{
  "id": "com.example.app.premium",
  "type": "non-consumable",
  "referenceName": "Premium Unlock",
  "priceReference": "USD 4.99",
  "localizations": {
    "en-US": {
      "displayName": "Premium",
      "description": "Unlock every level"
    }
  },
  "reviewScreenshot": "release/iap/premium-review.png"
}
```

`priceReference` is a requested/reference price for review. App Store price points and storefront equalization remain the source of truth.

## Screenshot families

Use logical family names in the manifest:

- `iphone-6.9` for the current highest-resolution iPhone family;
- `iphone-6.5` only as Apple's allowed fallback when current rules permit;
- `ipad-13` when iPad is supported.

The screenshot validator recognizes the current accepted pixel dimensions embedded in the script. Refresh those values from Apple if specifications change.

## Validation modes

Draft mode checks shape, limits, identifiers, URLs, and internal consistency while reporting placeholders as warnings:

```bash
python3 <skill-dir>/scripts/validate_release.py --config release/app-store.json
```

Strict mode treats placeholders, missing confirmations, missing update notes, and unverified monetization as release-blocking:

```bash
python3 <skill-dir>/scripts/validate_release.py --config release/app-store.json --strict
```

Use `--json` to feed the validation result into CI or another tool.
