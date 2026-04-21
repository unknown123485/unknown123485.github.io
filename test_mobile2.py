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

        # 1. Check entry screen
        print("=== ENTRY SCREEN ===")
        entry_info = page.evaluate("""() => {
            const btns = document.querySelectorAll('.btn-luxury');
            const opts = document.querySelectorAll('.entry-option');
            const card = document.querySelector('.entry-card');
            return {
                btn_count: btns.length,
                btn_texts: Array.from(btns).map(b => b.innerText.substring(0, 30)),
                opt_count: opts.length,
                opt_info: Array.from(opts).map((o, i) => ({
                    i, display: getComputedStyle(o).display, 
                    opacity: getComputedStyle(o).opacity,
                    h: o.offsetHeight, text: o.innerText.substring(0, 40)
                })),
                card_overflow: card ? getComputedStyle(card).overflow : null,
                card_h: card ? card.offsetHeight : 0,
                card_scrollH: card ? card.scrollHeight : 0
            };
        }""")
        print(f"  buttons: {entry_info['btn_count']} texts={entry_info['btn_texts']}")
        print(f"  options: {entry_info['opt_count']}")
        for o in entry_info['opt_info']:
            print(f"    opt[{o['i']}]: display={o['display']} opacity={o['opacity']} h={o['h']} text='{o['text']}'")
        print(f"  card: overflow={entry_info['card_overflow']} h={entry_info['card_h']} scrollH={entry_info['card_scrollH']}")

        # 2. Simulate text load
        print("\n=== AFTER TEXT LOAD ===")
        page.evaluate("""() => {
            document.getElementById('text-input').value = '第一条测试文字\\n第二条测试文字\\n第三条测试文字';
            startDisplay();
        }""")
        time.sleep(3)

        display_info = page.evaluate("""() => {
            const el = document.querySelector('.sentence-text');
            const sa = document.getElementById('standard-area');
            const da = document.querySelector('.display-area');
            return {
                sentences: window.sentences ? window.sentences.length : 0,
                sentence_texts: window.sentences ? window.sentences.map(s => s.text) : [],
                el_exists: !!el,
                el_text: el ? el.innerText : null,
                el_innerHTML: el ? el.innerHTML.substring(0, 100) : null,
                el_class: el ? el.className : null,
                el_opacity: el ? getComputedStyle(el).opacity : null,
                el_active: el ? el.classList.contains('active') : null,
                el_box: el ? el.getBoundingClientRect() : null,
                sa_h: sa ? sa.offsetHeight : 0,
                sa_children: sa ? sa.children.length : 0,
                sa_innerHTML_len: sa ? sa.innerHTML.length : 0,
                da_h: da ? da.offsetHeight : 0,
                currentTheme: window.currentTheme,
                einkMode: window.einkMode
            };
        }""")
        for k, v in display_info.items():
            print(f"  {k}: {v}")

        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "diag2_display.png"), full_page=True)

        # 3. Check bottom controls
        print("\n=== BOTTOM CONTROLS ===")
        bc_info = page.evaluate("""() => {
            const bc = document.getElementById('bottom-controls');
            const prev = document.getElementById('bottom-prev');
            const next = document.getElementById('bottom-next');
            return {
                bc_exists: !!bc,
                bc_display: bc ? getComputedStyle(bc).display : null,
                bc_opacity: bc ? getComputedStyle(bc).opacity : null,
                bc_visibility: bc ? getComputedStyle(bc).visibility : null,
                bc_hidden: bc ? bc.classList.contains('hidden') : null,
                prev_exists: !!prev,
                next_exists: !!next,
            };
        }""")
        for k, v in bc_info.items():
            print(f"  {k}: {v}")

        # 4. Check settings
        print("\n=== SETTINGS ===")
        page.evaluate("""() => {
            document.querySelector('.status-badge-setting').click();
        }""")
        time.sleep(1)

        settings_info = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            const themes = document.querySelectorAll('.theme-detail-item');
            return {
                nb_display: nb ? getComputedStyle(nb).display : null,
                nb_opacity: nb ? getComputedStyle(nb).opacity : null,
                nb_visibility: nb ? getComputedStyle(nb).visibility : null,
                nb_zIndex: nb ? getComputedStyle(nb).zIndex : null,
                nb_overflow: nb ? getComputedStyle(nb).overflow : null,
                nb_overflowY: nb ? getComputedStyle(nb).overflowY : null,
                nb_h: nb ? nb.offsetHeight : 0,
                nb_scrollH: nb ? nb.scrollHeight : 0,
                ov_active: ov ? ov.classList.contains('active') : null,
                ov_zIndex: ov ? getComputedStyle(ov).zIndex : null,
                theme_count: themes.length,
                theme0: themes[0] ? {
                    display: getComputedStyle(themes[0]).display,
                    opacity: getComputedStyle(themes[0]).opacity,
                    h: themes[0].offsetHeight,
                    text: themes[0].innerText.substring(0, 30)
                } : null
            };
        }""")
        for k, v in settings_info.items():
            print(f"  {k}: {v}")

        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "diag2_settings.png"), full_page=True)

        # 5. Try clicking inside nav-bar
        print("\n=== CLICK INSIDE NAV-BAR ===")
        click_result = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const slider = document.getElementById('dpi-slider');
            // Click slider
            if (slider) slider.click();
            // Check if nav-bar still visible
            return {
                after_click_nb_display: nb ? getComputedStyle(nb).display : null,
                after_click_nb_opacity: nb ? getComputedStyle(nb).opacity : null,
            };
        }""")
        for k, v in click_result.items():
            print(f"  {k}: {v}")

        time.sleep(0.5)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "diag2_after_slider.png"), full_page=True)

        # Check overlay click behavior
        print("\n=== OVERLAY CLICK BEHAVIOR ===")
        # Click on the overlay (not on nav-bar)
        overlay_click_result = page.evaluate("""() => {
            const ov = document.getElementById('settings-overlay');
            const nb = document.getElementById('nav-bar-luxury');
            // Simulate clicking overlay area (outside nav-bar)
            ov.click();
            return {
                after_overlay_click_nb_display: nb ? getComputedStyle(nb).display : null,
                after_overlay_click_nb_opacity: nb ? getComputedStyle(nb).opacity : null,
                after_overlay_click_ov_active: ov ? ov.classList.contains('active') : null,
            };
        }""")
        for k, v in overlay_click_result.items():
            print(f"  {k}: {v}")

        print("\n--- JS Errors ---")
        for err in js_errors:
            print(err)

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
