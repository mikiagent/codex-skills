import XCTest

final class StoreScreenshotUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    @MainActor
    func testStoreScreenshots() throws {
        capture(state: "home", snapshotName: "01-home")
        capture(state: "gameplay", snapshotName: "02-gameplay")
        capture(state: "progress", snapshotName: "03-progress")
    }

    @MainActor
    private func capture(state: String, snapshotName: String) {
        app = XCUIApplication()
        setupSnapshot(app)
        app.launchArguments += [
            "-store-screenshot-mode", "YES",
            "-store-screenshot-state", state
        ]
        app.launch()

        // Adapt the app so each deterministic state exposes this identifier only
        // after the WebGL scene, fonts, textures, and seeded demo data are ready.
        let ready = app.otherElements["store-screenshot-ready-\(state)"]
        XCTAssertTrue(ready.waitForExistence(timeout: 30), "Screenshot state did not become ready: \(state)")
        snapshot(snapshotName)
        app.terminate()
    }
}
