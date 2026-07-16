import os
from rustwright.sync_api import sync_playwright

def run_validation_test():
    print("[INFO] Starting Rustwright engine...")
    with sync_playwright() as p:
        # Launch Chromium (Rustwright is currently Chromium-only)
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        print("[INFO] Navigating to login page...")
        page.goto("https://the-internet.herokuapp.com/login")

        # Fill inputs using native CDP events
        page.locator("input#username").fill("tomsmith")
        page.locator("input#password").fill("SuperSecretPassword!")
        
        print("[INFO] Submitting form...")
        page.locator("button[type='submit']").click()

        # Wait for the success banner
        page.wait_for_selector(".flash.success")
        
        # Verify the element is visible
        is_logged_in = page.locator(".flash.success").is_visible()
        print(f"[RESULT] Login successful: {is_logged_in}")

        # Capture a screenshot to verify rendering
        page.screenshot(path="rustwright_test.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    run_validation_test()