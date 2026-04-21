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

        # === TEST 1: Entry screen ===
        print("=== TEST 1: ENTRY SCREEN ===")
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "t1_entry.png"), full_page=True)
        
        entry = page.evaluate("""() => {
            const cards = document.querySelectorAll('.entry-card');
            const fileInput = document.getElementById('file-input');
            const folderInput = document.getElementById('folder-input');
            return {
                card_count: cards.length,
                cards: Array.from(cards).map((c, i) => ({
                    i, text: c.innerText.substring(0, 40).replace(/\\n/g, ' '),
                    display: getComputedStyle(c).display,
                    opacity: getComputedStyle(c).opacity,
                    h: c.offsetHeight, w: c.offsetWidth,
                    clickable: c.onclick !== null || c.getAttribute('onclick')
                })),
                file_input_attrs: fileInput ? {
                    webkitdirectory: fileInput.webkitdirectory,
                    multiple: fileInput.multiple,
                    accept: fileInput.accept
                } : null,
                folder_input_attrs: folderInput ? {
                    webkitdirectory: folderInput.webkitdirectory,
                    multiple: folderInput.multiple,
                    accept: folderInput.accept
                } : null,
            };
        }""")
        print(f"  card_count: {entry['card_count']}")
        for c in entry['cards']:
            print(f"  card[{c['i']}]: text='{c['text']}' display={c['display']} opacity={c['opacity']} size={c['w']}x{c['h']} clickable={c['clickable']}")
        print(f"  file_input: {entry['file_input_attrs']}")
        print(f"  folder_input: {entry['folder_input_attrs']}")

        # === TEST 2: Text display ===
        print("\n=== TEST 2: TEXT DISPLAY ===")
        page.evaluate("""() => {
            document.getElementById('text-input').value = '春水初生，春林初盛。\\n\\n春风十里，不如你。\\n\\n愿你有诗有梦。';
            startDisplay();
        }""")
        time.sleep(3)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "t2_display.png"), full_page=True)

        display = page.evaluate("""() => {
            const el = document.querySelector('.sentence-text.active');
            const progress = document.getElementById('progress-val');
            return {
                text_visible: !!el,
                text: el ? el.innerText : null,
                opacity: el ? getComputedStyle(el).opacity : null,
                box: el ? el.getBoundingClientRect() : null,
                progress: progress ? progress.innerText : null,
                display_screen_opacity: getComputedStyle(document.getElementById('display-screen')).opacity,
                input_screen_display: getComputedStyle(document.getElementById('input-screen')).display,
            };
        }""")
        for k, v in display.items():
            print(f"  {k}: {v}")

        # === TEST 3: Next/Prev buttons ===
        print("\n=== TEST 3: NEXT/PREV BUTTONS ===")
        next_btn = page.query_selector("#next-btn")
        prev_btn = page.query_selector("#prev-btn")
        play_btn = page.query_selector("#bottom-play-btn")
        print(f"  next-btn exists: {next_btn is not None}")
        print(f"  prev-btn exists: {prev_btn is not None}")
        print(f"  play-btn exists: {play_btn is not None}")
        
        if next_btn:
            next_box = next_btn.bounding_box()
            print(f"  next-btn box: {next_box}")
            next_btn.click()
            time.sleep(1)
            after_next = page.evaluate("""() => {
                const el = document.querySelector('.sentence-text.active');
                return { text: el ? el.innerText : null, progress: document.getElementById('progress-val').innerText };
            }""")
            print(f"  after next: text='{after_next['text']}' progress={after_next['progress']}")
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "t3_after_next.png"), full_page=True)

        # === TEST 4: Settings panel ===
        print("\n=== TEST 4: SETTINGS PANEL ===")
        settings_btn = page.query_selector(".status-badge-setting")
        if settings_btn:
            settings_btn.click()
            time.sleep(1)
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "t4_settings.png"), full_page=True)

            settings = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                const themes = document.querySelectorAll('.theme-detail-item');
                const slider = document.getElementById('dpi-slider');
                return {
                    nb_display: getComputedStyle(nb).display,
                    nb_opacity: getComputedStyle(nb).opacity,
                    nb_zIndex: getComputedStyle(nb).zIndex,
                    nb_h: nb.offsetHeight,
                    ov_active: ov.classList.contains('active'),
                    ov_zIndex: getComputedStyle(ov).zIndex,
                    theme_count: themes.length,
                    theme0_h: themes[0] ? themes[0].offsetHeight : 0,
                    theme0_visible: themes[0] ? themes[0].offsetHeight > 0 : false,
                    slider_exists: !!slider,
                    slider_box: slider ? slider.getBoundingClientRect() : null,
                };
            }""")
            for k, v in settings.items():
                print(f"  {k}: {v}")

            # Try clicking slider
            if settings['slider_exists']:
                slider = page.query_selector("#dpi-slider")
                slider.click()
                time.sleep(0.5)
                after_slider = page.evaluate("""() => {
                    const nb = document.getElementById('nav-bar-luxury');
                    const ov = document.getElementById('settings-overlay');
                    return {
                        nb_still_visible: getComputedStyle(nb).opacity === '1',
                        ov_still_active: ov.classList.contains('active'),
                    };
                }""")
                print(f"  after slider click: {after_slider}")
                page.screenshot(path=os.path.join(SCREENSHOT_DIR, "t4_after_slider.png"), full_page=True)

            # Try clicking theme
            theme_item = page.query_selector(".theme-detail-item")
            if theme_item:
                try:
                    theme_item.click(timeout=3000)
                    time.sleep(0.5)
                    after_theme = page.evaluate("""() => {
                        const nb = document.getElementById('nav-bar-luxury');
                        const ov = document.getElementById('settings-overlay');
                        return {
                            nb_still_visible: getComputedStyle(nb).opacity === '1',
                            ov_still_active: ov.classList.contains('active'),
                        };
                    }""")
                    print(f"  after theme click: {after_theme}")
                    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "t4_after_theme.png"), full_page=True)
                except Exception as e:
                    print(f"  theme click failed: {str(e)[:100]}")

            # Click overlay to close
            overlay = page.query_selector("#settings-overlay")
            if overlay:
                overlay.click()
                time.sleep(0.5)
                after_close = page.evaluate("""() => {
                    const nb = document.getElementById('nav-bar-luxury');
                    const ov = document.getElementById('settings-overlay');
                    return {
                        nb_display: getComputedStyle(nb).display,
                        nb_opacity: getComputedStyle(nb).opacity,
                        ov_active: ov.classList.contains('active'),
                    };
                }""")
                print(f"  after overlay click: {after_close}")

        print("\n--- JS Errors ---")
        for err in js_errors:
            print(f"  {err}")

        browser.close()
        print("\nDone! Screenshots in:", SCREENSHOT_DIR)

if __name__ == "__main__":
    test()
