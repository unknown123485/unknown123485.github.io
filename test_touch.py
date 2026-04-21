import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"d:\重要技术文件\项目\文本展示\pw-browsers"

from playwright.sync_api import sync_playwright
import time

MOBILE_VIEWPORT = {"width": 375, "height": 812}
MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

HTML_PATH = r"d:\重要技术文件\项目\文本展示\preview.html"
SCREENSHOT_DIR = r"d:\重要技术文件\项目\文本展示\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=MOBILE_VIEWPORT,
            user_agent=MOBILE_UA,
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
        )
        page = context.new_page()

        js_errors = []
        page.on("pageerror", lambda err: js_errors.append(str(err)))

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        time.sleep(1)

        # Load text
        page.evaluate("""() => {
            document.getElementById('text-input').value = '测试文字一。\\n\\n测试文字二。';
            startDisplay();
        }""")
        time.sleep(3)

        # Open settings with touch tap
        print("=== TOUCH TEST: SETTINGS ===")
        settings_btn = page.query_selector(".status-badge-setting")
        settings_btn.tap()
        time.sleep(1)
        
        settings_state = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            return {
                nb_open: nb.classList.contains('open'),
                nb_opacity: getComputedStyle(nb).opacity,
                ov_active: ov.classList.contains('active'),
            };
        }""")
        print(f"  After opening settings: {settings_state}")

        # Try tapping a slider inside nav-bar
        print("\n=== TOUCH TEST: TAP SLIDER ===")
        slider = page.query_selector("#dpi-slider")
        if slider:
            slider.tap()
            time.sleep(0.5)
            after_slider = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    nb_opacity: getComputedStyle(nb).opacity,
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            print(f"  After tapping slider: {after_slider}")

        # Try tapping a label inside nav-bar
        print("\n=== TOUCH TEST: TAP LABEL ===")
        label = page.query_selector(".slider-label")
        if label:
            label.tap()
            time.sleep(0.5)
            after_label = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    nb_opacity: getComputedStyle(nb).opacity,
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            print(f"  After tapping label: {after_label}")

        # Try tapping the overlay area (outside nav-bar)
        print("\n=== TOUCH TEST: TAP OVERLAY ===")
        overlay = page.query_selector("#settings-overlay")
        if overlay:
            try:
                overlay.tap(timeout=3000)
            except:
                pass
            time.sleep(0.5)
            after_overlay = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    nb_opacity: getComputedStyle(nb).opacity,
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            print(f"  After tapping overlay: {after_overlay}")

        # Re-open settings and try tapping inside nav-bar content area
        print("\n=== TOUCH TEST: TAP NAV-BAR CONTENT ===")
        page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            nb.classList.add('open');
            ov.classList.add('active');
        }""")
        time.sleep(0.5)

        # Tap on a control group
        control_group = page.query_selector(".control-group")
        if control_group:
            control_group.tap()
            time.sleep(0.5)
            after_cg = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    nb_opacity: getComputedStyle(nb).opacity,
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            print(f"  After tapping control-group: {after_cg}")

        # Check what happens when tapping the nav-bar itself (not a child)
        print("\n=== TOUCH TEST: TAP NAV-BAR DIRECTLY ===")
        navbar = page.query_selector("#nav-bar-luxury")
        if navbar:
            navbar.tap()
            time.sleep(0.5)
            after_nb = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    nb_opacity: getComputedStyle(nb).opacity,
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            print(f"  After tapping nav-bar: {after_nb}")

        # Check the closeSettingsFromOverlay function
        print("\n=== CHECK OVERLAY CLICK HANDLER ===")
        handler_info = page.evaluate("""() => {
            const ov = document.getElementById('settings-overlay');
            const nb = document.getElementById('nav-bar-luxury');
            return {
                ov_zIndex: getComputedStyle(ov).zIndex,
                nb_zIndex: getComputedStyle(nb).zIndex,
                nb_pointerEvents: getComputedStyle(nb).pointerEvents,
                ov_pointerEvents: getComputedStyle(ov).pointerEvents,
                nb_contains_ov: nb.contains(ov),
                ov_contains_nb: ov.contains(nb),
                nb_parent: nb.parentElement ? nb.parentElement.id : null,
                ov_parent: ov.parentElement ? ov.parentElement.id : null,
            };
        }""")
        for k, v in handler_info.items():
            print(f"  {k}: {v}")

        print("\n--- JS Errors ---")
        for err in js_errors:
            print(f"  {err}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
