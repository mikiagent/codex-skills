---
name: ship-capacitor-ios
description: Turn an existing Three.js, Vite, or other web project into a Capacitor iOS app and prepare, test, update, and publish it through TestFlight and the Apple App Store. Use for Capacitor setup, Xcode signing readiness, App Store metadata and screenshots, Fastlane/App Store Connect automation, release notes and version updates, privacy and review preparation, StoreKit or RevenueCat in-app purchases, and AdMob ads with consent and ATT handling.
---

# Ship Capacitor iOS

Build a reproducible release pipeline around an evidence-backed `release/app-store.json` manifest. Treat the web app, native wrapper, store listing, monetization, and compliance declarations as one release.

## Non-negotiable rules

- Inspect the app and its dependencies before drafting store claims or compliance answers.
- Refresh temporally unstable requirements and package compatibility from official sources before a real submission. Read [references/official-sources.md](references/official-sources.md).
- Never invent privacy, age-rating, encryption, content-rights, pricing, tax, banking, legal, or review-account facts.
- Never store App Store Connect `.p8` keys, Apple passwords, or review demo passwords in the repository.
- Use test ad unit IDs and sandbox/TestFlight purchases until production readiness is explicitly verified.
- Prepare and validate locally without approval. Ask before creating or changing App Store Connect records, uploading metadata/screenshots/builds, distributing TestFlight builds, or submitting to App Review.
- Require a separate, explicit confirmation immediately before App Review submission. Do not accept agreements, release a pending version, or enable a phased release implicitly.
- Preserve existing iOS native changes. Do not recreate or migrate the `ios/` project unless it is disposable or the user explicitly approves.

## Resource routing

- Read [references/capacitor-native.md](references/capacitor-native.md) when adding or repairing Capacitor/iOS, signing, icons, or privacy manifests.
- Read [references/monetization.md](references/monetization.md) when adding purchases, subscriptions, or ads.
- Read [references/app-store-release.md](references/app-store-release.md) when creating metadata, screenshots, TestFlight builds, or submissions.
- Read [references/release-manifest.md](references/release-manifest.md) when creating or editing `release/app-store.json`.

Use the bundled scripts from this skill directory:

```text
scripts/audit_ios_release.py
scripts/scaffold_release.py
scripts/validate_release.py
scripts/render_fastlane_metadata.py
scripts/validate_screenshots.py
```

## End-to-end workflow

### 1. Inventory the project

Identify:

- package manager, build command, web output directory, framework, and Three.js entry points;
- existing Capacitor versions/configuration and iOS package manager;
- bundle ID, app name, version/build number, deployment target, device families, orientations, signing team, and native edits;
- plugins/SDKs that collect data, use required-reason APIs, serve ads, or process purchases;
- login, network, user-generated content, account deletion, support, and review-only requirements;
- current store state for updates: live version, editable version, build numbers, listing, screenshots, accessibility declarations, IAPs, and unresolved review issues.

Run the audit first:

```bash
python3 <skill-dir>/scripts/audit_ios_release.py --project <project-root>
```

Use `--strict` only as a release gate. The audit is diagnostic; do not mutate the project merely to silence a warning that does not apply.

### 2. Choose the release path

Prefer the local, inspectable path:

- Capacitor for the native shell;
- Xcode for signing/archive configuration;
- Fastlane `snapshot`, `gym`, `pilot`, and `deliver` for screenshots, builds, TestFlight, and listing uploads;
- App Store Connect API keys for non-interactive authentication.

Offer Ionic Appflow only if the user wants managed cloud builds/deployments and accepts its account and pricing. Do not move a working Three.js app to Expo solely for submission automation.

For native dependencies, prefer SPM only when every selected plugin supports the project's Capacitor major and SPM. Otherwise keep CocoaPods. Never mix assumptions.

### 3. Create or repair the Capacitor app

Follow [references/capacitor-native.md](references/capacitor-native.md). Keep all `@capacitor/*` packages on the same major. Verify current versions before installing.

Maintain this loop:

```bash
npm run build
npx cap sync ios
npx cap run ios
```

Test on at least one current simulator and one physical iPhone before release. Verify touch controls, safe areas, rotation policy, audio interruption, background/foreground behavior, offline/error states, performance, memory pressure, and cold launch.

### 4. Add monetization deliberately

Read [references/monetization.md](references/monetization.md) and choose one purchase path:

- RevenueCat Capacitor SDK for the lowest operational burden and cross-platform entitlements;
- a maintained StoreKit 2 Capacitor plugin or custom native bridge when avoiding a SaaS dependency;
- `cordova-plugin-purchase` only after verifying current compatibility and accepting its API model.

For ads, verify the current `@capacitor-community/admob` release supports the project's Capacitor major and chosen iOS package manager. Implement UMP consent and load ads only when consent state permits. Request ATT only when the actual data flow meets Apple's tracking definition.

Always expose purchase restoration, handle pending/cancelled purchases, derive entitlements from verified transactions, and test interruption/reinstall/account-change paths. Do not unlock paid digital features with an external payment mechanism unless a current policy exception clearly applies.

### 5. Create the release manifest

Scaffold without overwriting existing files:

```bash
python3 <skill-dir>/scripts/scaffold_release.py \
  --project <project-root> \
  --app-name "<App Name>" \
  --bundle-id "com.example.app"
```

Then populate `release/app-store.json` from project evidence and user-confirmed facts. Draft marketing copy from functionality that is present and reviewable. Mark unresolved facts as `null` or `TODO`; never resolve them by inference.

Render deterministic Fastlane metadata:

```bash
python3 <skill-dir>/scripts/render_fastlane_metadata.py \
  --config <project-root>/release/app-store.json \
  --output <project-root>/fastlane/metadata
```

### 6. Build the screenshot system

Create a deterministic screenshot mode reachable through UI-test launch arguments. It may seed local demo data, disable nondeterministic animation, wait for WebGL/assets, and navigate to named states. Ensure it is unavailable in production interaction paths.

Use XCUITest plus Fastlane `snapshot`; adapt `assets/screenshot-tests/StoreScreenshotUITests.swift` instead of relying on timed manual taps. Capture actual in-app UI. Text overlays may clarify features but must not obscure or misrepresent the experience.

Target Apple's current highest-resolution required families and validate exact dimensions, file counts, and alpha:

```bash
python3 <skill-dir>/scripts/validate_screenshots.py \
  --config <project-root>/release/app-store.json \
  --screenshots-root <project-root>/fastlane/screenshots
```

Inspect every screenshot visually for loading indicators, test ads, real personal data, debug UI, permission prompts, misleading purchase state, and incorrect device chrome.

### 7. Validate the release candidate

Run:

```bash
python3 <skill-dir>/scripts/validate_release.py \
  --config <project-root>/release/app-store.json \
  --strict

python3 <skill-dir>/scripts/audit_ios_release.py \
  --project <project-root> \
  --strict
```

Also run web tests, native build/tests, purchase sandbox tests, ad consent scenarios, and a clean-install device smoke test. Reconcile App Store privacy answers with the binary's SDK privacy manifests and the app's actual data flows.

### 8. Prepare credentials without leaking them

Use an App Store Connect API key with the least role needed. Keep its `.p8` file outside the repository and pass only environment variables at runtime:

```text
ASC_KEY_ID
ASC_ISSUER_ID
ASC_KEY_PATH
APP_IDENTIFIER
APPLE_TEAM_ID
APP_REVIEW_DEMO_USER       # only when login is required
APP_REVIEW_DEMO_PASSWORD   # only when login is required
```

Do not print these values. Confirm the Account Holder has accepted current agreements and the Paid Applications Agreement is active before IAP testing or sale.

### 9. TestFlight before production

Use the generated Fastlane setup. First create the archive and upload to TestFlight without App Review submission:

```bash
bundle install
bundle exec fastlane ios beta
```

Wait for processing, inspect Apple warnings, distribute only to the intended group, and test the processed TestFlight build. First IAPs of a purchase type may need to accompany a new app version; follow current App Store Connect rules.

### 10. Preview, diff, and upload listing changes

For an update, download the live metadata into a separate baseline directory, render the candidate metadata, and show a file diff plus screenshot contact sheet. Explain which fields are editable live versus version-bound.

Fastlane `deliver` generates an HTML preview when `force` is false. Keep this confirmation step. After user approval, upload the candidate metadata/screenshots without submitting the app for review:

```bash
bundle exec fastlane ios listing
bundle exec fastlane ios candidate
```

The `candidate` lane uploads a build and listing but leaves `submit_for_review` false.

### 11. Submit only at the final gate

Immediately before submission, summarize:

- app/version/build and selected binary;
- locales and screenshot families;
- monetization products included in the review;
- privacy, accessibility, age-rating, encryption, content-rights, and ad declarations;
- review credentials/notes and release mode;
- known warnings and TestFlight evidence.

Ask for explicit confirmation. Only then run:

```bash
CONFIRM_APP_REVIEW_SUBMISSION=YES bundle exec fastlane ios submit_review
```

After submission, report the App Store Connect status and do not release an approved manual-release build without separate approval.

## Update workflow

For every update:

1. Fetch current store state and preserve a baseline.
2. Inspect code changes since the last release and draft specific `whatsNew` text.
3. Increment marketing version intentionally and choose a unique build number.
4. Re-run privacy, accessibility, age-rating, SDK, and monetization reconciliation; do not assume prior answers still apply.
5. Retake screenshots when the represented UI or claims changed.
6. Test via TestFlight, preview the store diff, upload the candidate, and use the same final submission gate.

Prefer a phased release for higher-risk updates only when the user selects it. Keep rollback planning focused on shipping a fixed build; App Store binaries cannot be replaced in place.

## Completion criteria

Call the work complete only when the requested stage is achieved: native app runs, TestFlight build is processed, listing is uploaded, or review submission is accepted by App Store Connect. State which stage was reached and list any remaining Apple-side, legal, financial, or reviewer prerequisites.
