# App Store release automation

## What is and is not automated

Capacitor produces a normal native iOS project; it does not provide an Expo EAS-style end-to-end store listing workflow. Fastlane plus App Store Connect APIs cover local builds, TestFlight uploads, metadata, screenshots, and review submission. Ionic Appflow is the managed Capacitor alternative when a hosted service is desired.

Automation can draft and upload marketing text, screenshots, release notes, review notes, binaries, accessibility declarations, and many App Store fields. It must not guess legal/compliance declarations, accept agreements, or silently submit/release.

## App Store Connect prerequisites

- Active Apple Developer Program membership.
- App record and bundle ID, or approval to create them.
- Current agreements accepted by the Account Holder.
- App Manager/Admin-level operations for metadata, IAPs, and submissions as required.
- App Store Connect API key stored outside the repository.
- Signing certificate/profile or Xcode-managed signing.
- Support and privacy URLs that are public, stable, and accurate.

Generate the API key once, download the `.p8` once, and store it securely. Prefer an individual or role-scoped key with the least access needed.

## Metadata limits to validate

At the 2026-08-13 research date:

- app name: 2–30 characters;
- subtitle: at most 30 characters;
- promotional text: at most 170 characters;
- description: at most 4,000 characters, plain text;
- keywords: at most 100 UTF-8 bytes;
- What's New: at most 4,000 characters and required after the first version;
- review notes: at most 4,000 bytes.

Re-check Apple before submission. Keywords must be relevant, must not misuse competitor trademarks, and should not repeat the app/company name. Screenshots must show the app in use and accurately disclose paid features represented in them.

## Screenshot system

Use XCUITest with Fastlane snapshot for repeatability. Add a UI-test target and shared scheme, run `fastlane snapshot init`, add `SnapshotHelper.swift`, and adapt the bundled test template.

Make screenshot states deterministic through launch arguments or a test-only local route:

- seed fictional demo data;
- wait on a stable accessibility identifier exposed after WebGL/assets are ready;
- disable random events and long transitions;
- navigate by accessibility identifiers rather than coordinates;
- use one named snapshot per store story;
- capture every locale/device with the same content state.

Apple accepts one to ten screenshots per device family/localization. Current highest-resolution targets should be used so Apple can scale down when allowed. Screenshots cannot have alpha. If iPad is a supported device family, provide iPad screenshots.

Keep raw captures. If adding text overlays or device frames, generate a second derived set and visually compare it with the app. Do not include real personal data, non-iOS device imagery, prices that may vary, debug status, test ads, or unreviewable future features.

## Generated Fastlane lanes

The scaffold includes conservative lanes:

- `ios screenshots`: run snapshot only;
- `ios beta`: build/sync, archive, and upload to TestFlight;
- `ios listing`: upload metadata/screenshots with HTML preview and no binary/review submission;
- `ios candidate`: archive and upload the build plus listing, with review submission disabled;
- `ios submit_review`: submit the already prepared version only when `CONFIRM_APP_REVIEW_SUBMISSION=YES`.

Inspect and adapt the generated workspace, scheme, signing, export method, and screenshot scheme. Keep `force: false` for deliver so the HTML preview remains a human checkpoint.

## First release sequence

1. Validate the manifest and native project.
2. Create/verify the app record and bundle ID with approval.
3. Archive once locally in Xcode.
4. Capture and validate screenshots.
5. Upload a TestFlight build and wait for processing.
6. Test the exact processed build, including sandbox purchases and consent paths.
7. Upload listing/screenshots after preview approval.
8. Select/verify the build, IAPs, review details, privacy, accessibility, age rating, encryption, content rights, availability, and release mode.
9. Submit only after final explicit confirmation.

## Update sequence

1. Download current metadata/screenshots into a separate baseline folder.
2. Inspect code and UI changes since the last release/tag.
3. Create a new editable App Store version and unique build number.
4. Draft specific localized What's New text; generic text is acceptable only for genuinely minor fixes.
5. Reconcile new/removed SDKs, data flows, permissions, IAPs, ads, accessibility support, and age-rating descriptors.
6. Retake changed screenshots and keep unchanged ones only if still accurate.
7. Show a text diff, screenshot contact sheet, and manifest validation report.
8. Test via TestFlight, upload candidate, and use the final submission gate.

For phased release, confirm the choice explicitly. Apple's phased automatic update rollout spans seven days and can be paused, but a defective binary still requires a new fixed build.

## Fields that often remain manual or confirmation-bound

- agreements, banking, tax, and DSA trader status;
- privacy questionnaire publication when no reliable API workflow is available;
- accessibility claims until common tasks have been evaluated against Apple's criteria;
- exact age-rating answers without product-owner confirmation;
- export compliance determinations/documentation;
- availability, price, pre-order, and alternative distribution choices;
- first IAP-type submission association;
- final App Review submission and manual production release.

Browser automation may fill App Store Connect UI gaps in a signed-in session, but still requires the same factual evidence and external-write approvals.
