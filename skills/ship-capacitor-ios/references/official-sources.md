# Official source index

Last researched: 2026-08-13. Requirements, SDK versions, prices, and review rules change. Re-open the relevant primary sources before a real upload or submission.

## Capacitor

- [Capacitor iOS getting started](https://capacitorjs.com/docs/ios)
- [Capacitor development workflow](https://capacitorjs.com/docs/basics/workflow)
- [Capacitor Swift Package Manager](https://capacitorjs.com/docs/ios/spm)
- [Capacitor iOS privacy manifest](https://capacitorjs.com/docs/ios/privacy-manifest)
- [Capacitor App Store deployment](https://capacitorjs.com/docs/ios/deploying-to-app-store)
- [Capacitor in-app purchases guide](https://capacitorjs.com/docs/guides/in-app-purchases)
- [Capacitor ads guide](https://capacitorjs.com/docs/guides/ads)

At the research date, Capacitor v8 documentation requires iOS 15+ and Xcode 26+, and supports either CocoaPods or opt-in SPM. Do not hardcode that baseline into a future project without checking again.

## Apple submission and policy

- [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/)
- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Submit an app](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app)
- [Required, localizable, and editable properties](https://developer.apple.com/help/app-store-connect/reference/app-information/required-localizable-and-editable-properties/)
- [App information limits](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information)
- [Platform version information and limits](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information)
- [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)
- [Upload screenshots and previews](https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots)
- [Manage app privacy](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy/)
- [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- [Set an app age rating](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/)
- [Accessibility Nutrition Labels overview](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/)
- [Manage Accessibility Nutrition Labels](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/manage-accessibility-nutrition-labels)
- [Export compliance overview](https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance)
- [App Store Connect roles](https://developer.apple.com/help/account/access/roles)

## App Store Connect automation

- [App Store Connect API overview](https://developer.apple.com/documentation/appstoreconnectapi/)
- [Create API keys](https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-api)
- [App Store version localizations](https://developer.apple.com/documentation/appstoreconnectapi/app-store-version-localizations)
- [App screenshots API](https://developer.apple.com/documentation/appstoreconnectapi/app-screenshots)
- [Review submissions API](https://developer.apple.com/documentation/appstoreconnectapi/review-submissions)
- [Configure accessibility declarations with the API](https://developer.apple.com/documentation/appstoreconnectapi/configuring-accessibility-declarations)
- [Builds API](https://developer.apple.com/documentation/appstoreconnectapi/builds)
- [Fastlane App Store Connect API keys](https://docs.fastlane.tools/app-store-connect-api/)
- [Fastlane deliver](https://docs.fastlane.tools/actions/deliver/)
- [Fastlane snapshot](https://docs.fastlane.tools/actions/snapshot/)
- [Fastlane pilot](https://docs.fastlane.tools/actions/pilot/)
- [Fastlane precheck](https://docs.fastlane.tools/actions/precheck/)

The API changes production App Store Connect data. Keep read-only discovery separate from write operations and obtain approval before writes.

## Purchases and subscriptions

- [Choosing a StoreKit API](https://developer.apple.com/documentation/storekit/choosing-a-storekit-api-for-in-app-purchases)
- [Configure in-app purchases](https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases/)
- [IAP metadata requirements](https://developer.apple.com/help/app-store-connect/reference/in-app-purchases-and-subscriptions/in-app-purchase-information)
- [Manage IAPs through the API](https://developer.apple.com/documentation/appstoreconnectapi/managing-in-app-purchases)
- [Submit an IAP](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase)
- [RevenueCat Capacitor SDK](https://www.revenuecat.com/docs/getting-started/installation/capacitor)
- [RevenueCat restore purchases](https://www.revenuecat.com/docs/getting-started/restoring-purchases)

## Ads, consent, and tracking

- [Capacitor Community AdMob repository](https://github.com/capacitor-community/admob)
- [Google Mobile Ads iOS quick start](https://developers.google.com/admob/ios/quick-start)
- [Google UMP consent setup](https://developers.google.com/admob/ios/privacy)
- [Google iOS privacy strategies](https://developers.google.com/admob/ios/privacy/strategies)
- [Apple App Tracking Transparency](https://developer.apple.com/documentation/apptrackingtransparency)
- [Apple user privacy and data use](https://developer.apple.com/app-store/user-privacy-and-data-use/)

Verify the community plugin's current Capacitor-major and SPM/CocoaPods compatibility from its release/package metadata before installation.
