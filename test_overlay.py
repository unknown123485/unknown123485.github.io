import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"d:\重要技术文件\项目\文本展示\pw-browsers"

from playwright.sync_api import sync_playwright
import time

MOBILE_VIEWPORT = {"width": 375, "height": 812}
MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

HTML_PATH = r"d:\重要技术文件\项目\文本展示\preview.html"

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

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        time.sleep(1)

        # Load text
        page.evaluate("""() => {
            document.getElementById('text-input').value = '测试文字。\\n\\n第二条文字。';
            startDisplay();
        }""")
        time.sleep(3)

        # Open settings
        page.evaluate("""() => {
            document.getElementById('nav-bar-luxury').classList.add('open');
            document.getElementById('settings-overlay').classList.add('active');
        }""")
        time.sleep(0.5)

        # Check nav-bar position
        nb_box = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            return {
                nb_rect: nb.getBoundingClientRect(),
                ov_rect: ov.getBoundingClientRect(),
            };
        }""")
        print(f"  nav-bar rect: {nb_box['nb_rect']}")
        print(f"  overlay rect: {nb_box['ov_rect']}")

        # Try tapping at the top of the screen (should be overlay area, not nav-bar)
        print("\n=== TAP AT TOP (overlay area) ===")
        page.mouse.click(187, 100)  # Top center
        time.sleep(0.5)
        after_top = page.evaluate("""() => ({
            nb_open: document.getElementById('nav-bar-luxury').classList.contains('open'),
            ov_active: document.getElementById('settings-overlay').classList.contains('active'),
        })""")
        print(f"  Result: {after_top}")

        if after_top['nb_open']:
            # Re-open and try tapping at a different position
            page.evaluate("""() => {
                document.getElementById('nav-bar-luxury').classList.add('open');
                document.getElementById('settings-overlay').classList.add('active');
            }""")
            time.sleep(0.5)

            # Try clicking overlay via JS
            print("\n=== JS CLICK ON OVERLAY ===")
            page.evaluate("""() => {
                document.getElementById('settings-overlay').click();
            }""")
            time.sleep(0.5)
            after_js = page.evaluate("""() => ({
                nb_open: document.getElementById('nav-bar-luxury').classList.contains('open'),
                ov_active: document.getElementById('settings-overlay').classList.contains('active'),
            })""")
            print(f"  Result: {after_js}")

        # Now test the REAL problem: does clicking inside nav-bar close it?
        # Re-open
        page.evaluate("""() => {
            document.getElementById('nav-bar-luxury').classList.add('open');
            document.getElementById('settings-overlay').classList.add('active');
        }""")
        time.sleep(0.5)

        # Use JS to simulate touchstart + touchend on a slider
        print("\n=== SIMULATE TOUCH ON SLIDER ===")
        result = page.evaluate("""() => {
            const slider = document.getElementById('dpi-slider');
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            
            // Simulate touch
            const touch = new Touch({
                identifier: 0,
                target: slider,
                clientX: slider.getBoundingClientRect().x + 50,
                clientY: slider.getBoundingClientRect().y + 4,
            });
            const touchStart = new TouchEvent('touchstart', {
                touches: [touch],
                changedTouches: [touch],
                bubbles: true,
            });
            const touchEnd = new TouchEvent('touchend', {
                touches: [],
                changedTouches: [touch],
                bubbles: true,
            });
            slider.dispatchEvent(touchStart);
            slider.dispatchEvent(touchEnd);
            
            return {
                nb_open: nb.classList.contains('open'),
                ov_active: ov.classList.contains('active'),
            };
        }""")
        print(f"  After touch on slider: {result}")

        # Check if there's a document-level touch handler that closes the panel
        print("\n=== CHECK DOCUMENT EVENT HANDLERS ===")
        handlers = page.evaluate("""() => {
            // Check if there's a click handler on document that might close the panel
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            
            // Simulate a click on the document body
            const event = new MouseEvent('click', { bubbles: true });
            document.body.dispatchEvent(event);
            
            return {
                nb_open: nb.classList.contains('open'),
                ov_active: ov.classList.contains('active'),
            };
        }""")
        print(f"  After document body click: {handlers}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
