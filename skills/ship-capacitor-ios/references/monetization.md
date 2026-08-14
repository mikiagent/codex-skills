# Monetization choices

## Decision table

| Need | Preferred path | Tradeoff |
| --- | --- | --- |
| Subscriptions or cross-platform entitlements with minimal backend work | RevenueCat Capacitor SDK | Adds a SaaS account, SDK, data flow, and vendor configuration |
| Full ownership and iOS-only or custom backend | StoreKit 2 through maintained Capacitor plugin/custom bridge | More transaction, entitlement, server, and recovery work |
| Existing Cordova purchase implementation | `cordova-plugin-purchase` | Preserve only after current compatibility and migration risk are checked |
| Display ads | `@capacitor-community/admob` + Google UMP | Community plugin plus substantial privacy/consent obligations |

Verify current versions, supported Capacitor major, iOS minimum, and package-manager compatibility immediately before installation.

## In-app purchases

Use Apple's current StoreKit API for new native work. Digital features, levels, currency, subscriptions, and premium content generally require Apple's in-app purchase system unless a current rule or entitlement clearly applies.

### Required design work

1. Choose product types deliberately: consumable, non-consumable, non-renewing subscription, or auto-renewable subscription.
2. Freeze product IDs before creation; Apple product IDs cannot be reused after deletion.
3. Define entitlements independently from storefront product IDs.
4. Add clear price/period disclosures and Terms/Privacy links for subscriptions.
5. Provide a visible restore-purchases control for restorable purchases.
6. Handle success, cancellation, pending/Ask to Buy, network failure, duplicate taps, reinstall, account switching, refund/revocation, and expiration.
7. Grant durable access from verified transaction/customer information, not from a client-side boolean.
8. Do not log receipts, API secrets, personal purchase data, or full customer objects.

### RevenueCat path

```bash
npm install @revenuecat/purchases-capacitor
npx cap sync ios
```

Use the public iOS SDK key in the client, never a RevenueCat secret key. Configure products in App Store Connect, import/link them in RevenueCat, define entitlements and offerings, then configure the SDK once at app startup. Use stable app user IDs when accounts exist; understand anonymous-ID transfer behavior before launch.

Test offerings retrieval, purchase, entitlement refresh, restore, expiration, refund/revocation, and reinstall. Reconcile RevenueCat's disclosed data collection with the App Store privacy answers and privacy policy.

### App Store Connect product preparation

For each product, prepare reference name, immutable product ID, type, price/availability, tax category, at least one localization, review notes, and a review screenshot. Public promotional art has separate requirements.

The first product of a purchase type must be submitted with a new app version under Apple's current rules. Confirm the Paid Applications Agreement, banking, and tax setup before testing/sale. Use Sandbox Apple Accounts and then TestFlight.

## Ads

Capacitor's guide points to the actively maintained community AdMob plugin. Verify its current release instead of copying an old major-version install command.

### Safety sequence

1. Create the AdMob app and ad units, but use Google's sample/test IDs during development.
2. Add the AdMob app ID and the current Google-published `SKAdNetworkItems` list to `Info.plist`.
3. Configure Google UMP privacy messages.
4. Refresh consent information on launch and present required forms.
5. Load ads only when `canRequestAds` allows it.
6. Provide the required privacy-options entry point.
7. Request ATT only if the app actually tracks under Apple's definition; add an accurate `NSUserTrackingUsageDescription` first.
8. Ensure denial still leaves the app usable. Never incentivize or gate core functionality on ATT consent.
9. Verify child-directed/under-age settings, content rating, frequency caps, rewarded-ad grants, and failure behavior.
10. Replace test IDs with production IDs only in release configuration and verify no test-device UI appears in screenshots.

Ads change privacy declarations even when personalized tracking is disabled. Account for Google Mobile Ads, UMP, mediation partners, analytics, device identifiers, diagnostics, coarse location/IP processing, and tracking domains. The developer remains responsible for third-party SDK behavior.

### Product design checks

- Do not make the app predominantly an ad display.
- Keep banners outside touch controls and safe areas.
- Show interstitials only at natural breaks, never on launch or during critical input unless policy allows it.
- Grant rewarded items only after a verified reward callback; make the value clear beforehand.
- Pause/resume Three.js audio and rendering correctly around full-screen ads.
- Test no-fill, offline, consent denied, ATT denied, backgrounding, rotation, and repeated presentation.

## Manifest mapping

Record the selected model, provider, products, consent flow, tracking determination, and test status in `release/app-store.json`. Treat provider dashboard configuration as part of the release evidence, not as an invisible manual afterthought.
