import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"d:\重要技术文件\项目\文本展示\pw-browsers"

from playwright.sync_api import sync_playwright
import time

MOBILE_VIEWPORT = {"width": 375, "height": 812}
MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

HTML_PATH = r"d:\重要技术文件\项目\文本展示\preview.html"
SCREENSHOT_DIR = r"d:\重要技术文件\项目\文本展示\screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

PASS = "✅ PASS"
FAIL = "❌ FAIL"

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

        results = []

        # === TEST 1: Entry screen - 3 cards visible ===
        print("=== TEST 1: ENTRY SCREEN ===")
        entry = page.evaluate("""() => {
            const cards = document.querySelectorAll('.entry-card');
            return {
                count: cards.length,
                all_visible: Array.from(cards).every(c => c.offsetHeight > 0 && getComputedStyle(c).opacity !== '0'),
            };
        }""")
        t1 = entry['count'] >= 3 and entry['all_visible']
        results.append(("3个入口卡片可见", t1))
        print(f"  {PASS if t1 else FAIL}: count={entry['count']}, all_visible={entry['all_visible']}")

        # === TEST 2: Text display ===
        print("\n=== TEST 2: TEXT DISPLAY ===")
        page.evaluate("""() => {
            document.getElementById('text-input').value = '春水初生，春林初盛。\\n\\n春风十里，不如你。\\n\\n愿你有诗有梦。';
            startDisplay();
        }""")
        time.sleep(3)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "regression_display.png"), full_page=True)

        display = page.evaluate("""() => {
            const el = document.querySelector('.sentence-text.active');
            return {
                visible: !!el,
                text: el ? el.innerText : null,
                opacity: el ? parseFloat(getComputedStyle(el).opacity) : 0,
                progress: document.getElementById('progress-val').innerText,
            };
        }""")
        t2 = display['visible'] and display['opacity'] > 0.3 and display['text']
        results.append(("文字正常显示", t2))
        print(f"  {PASS if t2 else FAIL}: visible={display['visible']}, opacity={display['opacity']:.2f}, text='{display['text']}', progress={display['progress']}")

        # === TEST 3: Next/Prev buttons ===
        print("\n=== TEST 3: NEXT/PREV BUTTONS ===")
        next_btn = page.query_selector("#next-btn")
        prev_btn = page.query_selector("#prev-btn")
        play_btn = page.query_selector("#bottom-play-btn")
        t3 = next_btn is not None and prev_btn is not None and play_btn is not None
        results.append(("底部按钮存在", t3))
        print(f"  {PASS if t3 else FAIL}: next={next_btn is not None}, prev={prev_btn is not None}, play={play_btn is not None}")

        if next_btn:
            next_btn.click()
            time.sleep(1)
            after_next = page.evaluate("""() => {
                const el = document.querySelector('.sentence-text.active');
                return { text: el ? el.innerText : null, progress: document.getElementById('progress-val').innerText };
            }""")
            t3b = after_next['text'] is not None
            results.append(("下一条按钮功能正常", t3b))
            print(f"  {PASS if t3b else FAIL}: after next: text='{after_next['text']}', progress={after_next['progress']}")

        # === TEST 4: Settings panel - open ===
        print("\n=== TEST 4: SETTINGS PANEL ===")
        settings_btn = page.query_selector(".status-badge-setting")
        if settings_btn:
            settings_btn.click()
            time.sleep(1)
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "regression_settings.png"), full_page=True)

            settings_open = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    ov_active: ov.classList.contains('active'),
                    nb_opacity: parseFloat(getComputedStyle(nb).opacity),
                };
            }""")
            t4 = settings_open['nb_open'] and settings_open['ov_active'] and settings_open['nb_opacity'] > 0.5
            results.append(("设置面板打开", t4))
            print(f"  {PASS if t4 else FAIL}: nb_open={settings_open['nb_open']}, ov_active={settings_open['ov_active']}, opacity={settings_open['nb_opacity']:.2f}")

        # === TEST 5: Settings panel - slider click keeps it open ===
        print("\n=== TEST 5: SLIDER CLICK KEEPS PANEL OPEN ===")
        slider = page.query_selector("#dpi-slider")
        if slider:
            slider.click()
            time.sleep(0.5)
            after_slider = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            t5 = after_slider['nb_open'] and after_slider['ov_active']
            results.append(("Slider点击后面板保持打开", t5))
            print(f"  {PASS if t5 else FAIL}: nb_open={after_slider['nb_open']}, ov_active={after_slider['ov_active']}")

        # === TEST 6: Label click keeps panel open ===
        print("\n=== TEST 6: LABEL CLICK KEEPS PANEL OPEN ===")
        label = page.query_selector(".slider-label")
        if label:
            label.click()
            time.sleep(0.5)
            after_label = page.evaluate("""() => {
                const nb = document.getElementById('nav-bar-luxury');
                const ov = document.getElementById('settings-overlay');
                return {
                    nb_open: nb.classList.contains('open'),
                    ov_active: ov.classList.contains('active'),
                };
            }""")
            t6 = after_label['nb_open'] and after_label['ov_active']
            results.append(("标签点击后面板保持打开", t6))
            print(f"  {PASS if t6 else FAIL}: nb_open={after_label['nb_open']}, ov_active={after_label['ov_active']}")

        # === TEST 7: Overlay click closes panel ===
        print("\n=== TEST 7: OVERLAY CLICK CLOSES PANEL ===")
        # Click at top of screen (overlay area, above nav-bar)
        page.mouse.click(187, 100)
        time.sleep(0.5)
        after_overlay_click = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            return {
                nb_open: nb.classList.contains('open'),
                ov_active: ov.classList.contains('active'),
            };
        }""")
        t7 = not after_overlay_click['nb_open'] and not after_overlay_click['ov_active']
        results.append(("Overlay点击关闭面板", t7))
        print(f"  {PASS if t7 else FAIL}: nb_open={after_overlay_click['nb_open']}, ov_active={after_overlay_click['ov_active']}")

        # === TEST 8: Theme panel opens ===
        print("\n=== TEST 8: THEME PANEL ===")
        # Re-open settings using toggleNav (which also hides bottom-controls)
        page.evaluate("""() => { toggleNav(); }""")
        time.sleep(0.5)
        
        # Click "主题详情" button
        theme_btn = page.query_selector(".themes-section .control-btn")
        if theme_btn:
            theme_btn.click()
            time.sleep(0.5)
            page.screenshot(path=os.path.join(SCREENSHOT_DIR, "regression_themes.png"), full_page=True)

            theme_panel = page.evaluate("""() => {
                const panel = document.getElementById('theme-detail-panel');
                const items = document.querySelectorAll('.theme-detail-item');
                return {
                    panel_display: getComputedStyle(panel).display,
                    item_count: items.length,
                    first_item_h: items[0] ? items[0].offsetHeight : 0,
                    first_item_visible: items[0] ? items[0].offsetHeight > 0 : false,
                };
            }""")
            t8 = theme_panel['panel_display'] != 'none' and theme_panel['first_item_visible']
            results.append(("主题面板打开且主题项可见", t8))
            print(f"  {PASS if t8 else FAIL}: display={theme_panel['panel_display']}, items={theme_panel['item_count']}, first_h={theme_panel['first_item_h']}")

        # === TEST 9: No JS errors ===
        print("\n=== TEST 9: JS ERRORS ===")
        t9 = len(js_errors) == 0
        results.append(("无JS错误", t9))
        if js_errors:
            for err in js_errors:
                print(f"  {FAIL}: {err[:100]}")
        else:
            print(f"  {PASS}: No JS errors")

        # === SUMMARY ===
        print("\n" + "=" * 50)
        print("REGRESSION TEST SUMMARY")
        print("=" * 50)
        passed = sum(1 for _, r in results if r)
        total = len(results)
        for name, result in results:
            print(f"  {PASS if result else FAIL} {name}")
        print(f"\n{passed}/{total} tests passed")
        print(f"Screenshots: {SCREENSHOT_DIR}")

        browser.close()

if __name__ == "__main__":
    test()
