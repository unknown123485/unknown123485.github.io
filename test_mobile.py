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

        # Collect console logs
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

        # Collect JS errors
        js_errors = []
        page.on("pageerror", lambda err: js_errors.append(str(err)))

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        print(f"Loading: {file_url}")
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Screenshot 1: Entry screen
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "01_entry_screen.png"), full_page=True)
        print("Screenshot 1: Entry screen saved")

        # Check entry card buttons
        buttons = page.query_selector_all(".btn-luxury")
        print(f"Found {len(buttons)} .btn-luxury buttons on entry screen")
        for i, btn in enumerate(buttons):
            text = btn.inner_text()
            box = btn.bounding_box()
            print(f"  Button {i}: text='{text.strip()}', box={box}")

        # Check file inputs
        file_input = page.query_selector("#file-input")
        folder_input = page.query_selector("#folder-input")
        if file_input:
            attrs = file_input.evaluate("el => ({webkitdirectory: el.webkitdirectory, multiple: el.multiple, accept: el.accept, directory: el.getAttribute('directory')})")
            print(f"  #file-input attrs: {attrs}")
        if folder_input:
            attrs = folder_input.evaluate("el => ({webkitdirectory: el.webkitdirectory, multiple: el.multiple, accept: el.accept, directory: el.getAttribute('directory')})")
            print(f"  #folder-input attrs: {attrs}")

        # Simulate file selection by setting text-input value and calling startDisplay
        print("\n--- Simulating file load via JS ---")
        page.evaluate("""
            () => {
                document.getElementById('text-input').value = '第一条测试文字\\n第二条测试文字\\n第三条测试文字';
                startDisplay();
            }
        """)
        time.sleep(3)

        # Screenshot 2: Display screen after loading text
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "02_display_screen.png"), full_page=True)
        print("Screenshot 2: Display screen saved")

        # Check if text is visible
        sentence_el = page.query_selector(".sentence-text")
        if sentence_el:
            text = sentence_el.inner_text()
            box = sentence_el.bounding_box()
            opacity = sentence_el.evaluate("el => getComputedStyle(el).opacity")
            color = sentence_el.evaluate("el => getComputedStyle(el).color")
            fontsize = sentence_el.evaluate("el => getComputedStyle(el).fontSize")
            display = sentence_el.evaluate("el => getComputedStyle(el).display")
            visibility = sentence_el.evaluate("el => getComputedStyle(el).visibility")
            has_active = sentence_el.evaluate("el => el.classList.contains('active')")
            print(f"  .sentence-text found: text='{text}', box={box}")
            print(f"  opacity={opacity}, color={color}, fontSize={fontsize}, display={display}, visibility={visibility}")
            print(f"  has .active class: {has_active}")
        else:
            print("  .sentence-text NOT FOUND!")

        # Check standard-area
        standard_area = page.query_selector("#standard-area")
        if standard_area:
            sa_box = standard_area.bounding_box()
            sa_opacity = standard_area.evaluate("el => getComputedStyle(el).opacity")
            sa_display = standard_area.evaluate("el => getComputedStyle(el).display")
            sa_overflow = standard_area.evaluate("el => getComputedStyle(el).overflow")
            print(f"  #standard-area: box={sa_box}, opacity={sa_opacity}, display={sa_display}, overflow={sa_overflow}")

        # Check display-screen
        ds = page.query_selector("#display-screen")
        if ds:
            ds_opacity = ds.evaluate("el => getComputedStyle(el).opacity")
            ds_display = ds.evaluate("el => getComputedStyle(el).display")
            ds_zindex = ds.evaluate("el => getComputedStyle(el).zIndex")
            print(f"  #display-screen: opacity={ds_opacity}, display={ds_display}, zIndex={ds_zindex}")

        # Check input-screen (should be hidden)
        is_el = page.query_selector("#input-screen")
        if is_el:
            is_display = is_el.evaluate("el => getComputedStyle(el).display")
            print(f"  #input-screen: display={is_display}")

        # Check progress
        progress = page.query_selector("#progress-val")
        if progress:
            print(f"  #progress-val: {progress.inner_text()}")

        # Screenshot 3: Click next button
        next_btn = page.query_selector("#bottom-next")
        if next_btn:
            next_box = next_btn.bounding_box()
            print(f"\n  #bottom-next: box={next_box}")
            next_btn.click()
            time.sleep(2)
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "03_after_next.png"), full_page=True)
            print("Screenshot 3: After clicking next saved")

            sentence_el2 = page.query_selector(".sentence-text")
            if sentence_el2:
                text2 = sentence_el2.inner_text()
                box2 = sentence_el2.bounding_box()
                opacity2 = sentence_el2.evaluate("el => getComputedStyle(el).opacity")
                has_active2 = sentence_el2.evaluate("el => el.classList.contains('active')")
                print(f"  After next: text='{text2}', box={box2}, opacity={opacity2}, active={has_active2}")
        else:
            print("  #bottom-next NOT FOUND!")

        # Screenshot 4: Open settings panel
        print("\n--- Testing settings panel ---")
        settings_btn = page.query_selector(".status-badge-setting")
        if settings_btn:
            settings_btn.click()
            time.sleep(1)
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "04_settings_open.png"), full_page=True)
            print("Screenshot 4: Settings panel open saved")

            # Check overlay
            overlay = page.query_selector("#settings-overlay")
            if overlay:
                overlay_active = overlay.evaluate("el => el.classList.contains('active')")
                overlay_display = overlay.evaluate("el => getComputedStyle(el).display")
                overlay_zindex = overlay.evaluate("el => getComputedStyle(el).zIndex")
                print(f"  #settings-overlay: active={overlay_active}, display={overlay_display}, zIndex={overlay_zindex}")

            # Check nav-bar
            navbar = page.query_selector("#nav-bar-luxury")
            if navbar:
                navbar_display = navbar.evaluate("el => getComputedStyle(el).display")
                navbar_zindex = navbar.evaluate("el => getComputedStyle(el).zIndex")
                navbar_opacity = navbar.evaluate("el => getComputedStyle(el).opacity")
                navbar_visibility = navbar.evaluate("el => getComputedStyle(el).visibility")
                print(f"  #nav-bar-luxury: display={navbar_display}, zIndex={navbar_zindex}, opacity={navbar_opacity}, visibility={navbar_visibility}")

            # Try clicking a slider inside nav-bar
            slider = page.query_selector("#dpi-slider")
            if slider:
                slider_box = slider.bounding_box()
                print(f"  #dpi-slider: box={slider_box}")
                # Try clicking the slider
                try:
                    slider.click()
                    time.sleep(0.5)
                    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "05_after_slider_click.png"), full_page=True)
                    print("Screenshot 5: After clicking slider saved")
                    # Check if settings panel is still open
                    navbar2 = page.query_selector("#nav-bar-luxury")
                    if navbar2:
                        navbar2_display = navbar2.evaluate("el => getComputedStyle(el).display")
                        navbar2_opacity = navbar2.evaluate("el => getComputedStyle(el).opacity")
                        print(f"  After slider click: nav-bar display={navbar2_display}, opacity={navbar2_opacity}")
                except Exception as e:
                    print(f"  Slider click failed: {e}")
            else:
                print("  #dpi-slider NOT FOUND!")

            # Try clicking a theme item
            theme_item = page.query_selector(".theme-detail-item")
            if theme_item:
                theme_box = theme_item.bounding_box()
                print(f"  .theme-detail-item: box={theme_box}")
                try:
                    theme_item.click()
                    time.sleep(1)
                    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "06_after_theme_click.png"), full_page=True)
                    print("Screenshot 6: After clicking theme saved")
                    navbar3 = page.query_selector("#nav-bar-luxury")
                    if navbar3:
                        navbar3_display = navbar3.evaluate("el => getComputedStyle(el).display")
                        navbar3_opacity = navbar3.evaluate("el => getComputedStyle(el).opacity")
                        print(f"  After theme click: nav-bar display={navbar3_display}, opacity={navbar3_opacity}")
                except Exception as e:
                    print(f"  Theme click failed: {e}")
            else:
                print("  .theme-detail-item NOT FOUND!")
        else:
            print("  .status-badge-setting NOT FOUND!")

        # Print all console logs and errors
        print("\n--- Console Logs ---")
        for log in console_logs:
            print(log)
        print("\n--- JS Errors ---")
        for err in js_errors:
            print(err)

        browser.close()
        print("\nDone! All screenshots saved to:", SCREENSHOT_DIR)

if __name__ == "__main__":
    test()
