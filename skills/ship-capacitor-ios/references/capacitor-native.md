# Capacitor and native iOS preparation

## Preflight

Require a Mac capable of the current Xcode, a paid Apple Developer Program membership for distribution, an unused reverse-DNS bundle ID, and access to App Store Connect. Confirm current Apple SDK minimums before building.

Inspect before changing:

```bash
npm pkg get scripts.build dependencies devDependencies
npm view @capacitor/core version
npm view @capacitor/cli version
npm view @capacitor/ios version
find ios -maxdepth 4 -type f | sort
```

If `ios/` exists, locate native changes and determine whether it uses CocoaPods or SPM. Never delete it as a shortcut.

## Add Capacitor to a web app

Use compatible versions on one Capacitor major:

```bash
npm install @capacitor/core @capacitor/ios
npm install --save-dev @capacitor/cli
npx cap init "APP_NAME" "BUNDLE_ID"
```

Set `webDir` to the actual build output, normally `dist` for Vite. Build before adding/syncing iOS:

```bash
npm run build
npx cap add ios --packagemanager SPM
npx cap sync ios
```

Use the SPM flag only after verifying every native plugin supports SPM. Otherwise omit it and use the CocoaPods project. For an existing native project, preserve its package manager.

Do not use a remote `server.url` in production to turn the app into a thin hosted website. Bundle the release web assets unless a deliberate, policy-compliant architecture requires otherwise.

## Three.js mobile checks

- Cap device pixel ratio, usually `Math.min(devicePixelRatio, 2)`.
- Recompute camera aspect/projection and renderer size on resize/orientation change.
- Set touch actions intentionally and test gestures against safe areas and browser scrolling.
- Pause or reduce rendering when backgrounded; recover WebGL and audio state when foregrounded.
- Avoid depending on desktop hover, right-click, keyboard, filesystem paths, or cross-origin assets without mobile alternatives.
- Test cold load, slow network, offline behavior, large textures, memory warnings, thermal load, and repeated scene transitions.
- Keep Vite asset URLs compatible with the bundled WKWebView origin.

## Xcode configuration checklist

- Bundle identifier matches Capacitor, signing, App Store Connect, and IAP product configuration.
- Marketing version and build number are explicit; every uploaded build number is unique.
- Automatic or managed signing is configured for the intended Apple team.
- Deployment target satisfies Capacitor and all plugins.
- `TARGETED_DEVICE_FAMILY` matches the screenshot plan. Do not claim iPad support accidentally.
- Orientations match the real UI and screenshot orientation.
- App icon includes the current App Store/marketing icon and has no accidental alpha.
- Launch screen, display name, status bar, and safe-area behavior are production quality.
- Permission purpose strings describe the actual user-facing reason.
- `ITSAppUsesNonExemptEncryption` is set only from a confirmed export-compliance determination.
- `PrivacyInfo.xcprivacy` and embedded SDK manifests are valid and consistent with actual use.
- Associated domains, push, Game Center, Sign in with Apple, and other capabilities are configured only when used.

Capacitor/SDK privacy manifests do not replace App Store privacy answers. Generate an Xcode privacy report and reconcile it with all first-party and third-party data flows.

## Native run loop

Use a clean, repeatable sequence:

```bash
npm run build
npx cap sync ios
npx cap run ios
```

After plugin or native dependency changes, sync again. Archive from Xcode once before relying on CI/Fastlane so signing and archive issues are visible.

## App Review risk for web wrappers

Apple requires more than a repackaged website. Document the durable entertainment or utility, touch-first experience, offline/error handling, platform integration, and complete mobile UI. A Three.js game or interactive experience can satisfy this, but a remote page with limited interaction is at higher risk under guideline 4.2.

Keep screenshots and metadata centered on the actual iOS experience. Remove debug controls, placeholder URLs, hidden features, and nonfunctional external links before review.
