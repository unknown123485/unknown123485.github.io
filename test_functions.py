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

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        time.sleep(1)

        page.evaluate("""() => {
            document.getElementById('text-input').value = '测试文字。\\n\\n第二条。';
            startDisplay();
        }""")
        time.sleep(3)

        # Open settings
        page.evaluate("""() => { toggleNav(); }""")
        time.sleep(1)

        # Test each button by clicking and verifying the function was actually called
        tests = []

        # 1. openThemePanel button
        print("=== 1. 主题详情按钮 ===")
        result = page.evaluate("""() => {
            const btn = document.querySelector('.themes-section .control-btn');
            const panel = document.getElementById('theme-detail-panel');
            const before = panel.style.display;
            btn.click();
            const after = panel.style.display;
            const items = document.querySelectorAll('.theme-detail-item');
            const firstVisible = items[0] ? items[0].offsetHeight > 0 : false;
            return { before, after, items: items.length, firstVisible, themePanelOpen };
        }""")
        ok = result['after'] == 'flex' and result['themePanelOpen'] and result['firstVisible']
        tests.append(("主题详情按钮", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: before={result['before']}, after={result['after']}, items={result['items']}, firstVisible={result['firstVisible']}, themePanelOpen={result['themePanelOpen']}")

        # Close theme panel
        page.evaluate("""() => { closeThemePanel(); }""")
        time.sleep(0.3)

        # 2. eink toggle
        print("\n=== 2. 墨水屏模式按钮 ===")
        result = page.evaluate("""() => {
            const toggle = document.getElementById('eink-toggle');
            const before = einkMode;
            toggle.click();
            const after = einkMode;
            const active = toggle.classList.contains('active');
            return { before, after, active };
        }""")
        ok = result['after'] == True and result['active'] == True
        tests.append(("墨水屏模式按钮", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: before={result['before']}, after={result['after']}, active={result['active']}")

        # Toggle back
        page.evaluate("""() => { if(einkMode) toggleEinkMode(); }""")
        time.sleep(0.3)

        # 3. mode toggle
        print("\n=== 3. 模式切换按钮 ===")
        result = page.evaluate("""() => {
            const btn = document.getElementById('mode-btn');
            const before = displayMode;
            btn.click();
            const after = displayMode;
            return { before, after };
        }""")
        ok = result['before'] != result['after']
        tests.append(("模式切换按钮", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: before={result['before']}, after={result['after']}")

        # Toggle back
        page.evaluate("""() => { toggleMode(); }""")
        time.sleep(0.3)

        # 4. custom font select
        print("\n=== 4. 字体选择器 ===")
        result = page.evaluate("""() => {
            const header = document.getElementById('custom-font-select-header');
            const dropdown = document.getElementById('custom-font-select-dropdown');
            const select = document.getElementById('custom-font-select');
            const before = dropdown.style.display;
            header.click();
            const after = dropdown.style.display;
            return {
                before, after,
                header_rect: header.getBoundingClientRect(),
                dropdown_rect: dropdown.getBoundingClientRect(),
                select_display: getComputedStyle(select).display,
            };
        }""")
        ok = result['after'] == 'block'
        tests.append(("字体选择器", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: before={result['before']}, after={result['after']}, select_display={result['select_display']}")

        # Close dropdown
        page.evaluate("""() => {
            const dropdown = document.getElementById('custom-font-select-dropdown');
            const customFontSelect = document.getElementById('custom-font-select');
            dropdown.style.display = 'none';
            customFontSelect.classList.remove('open');
        }""")
        time.sleep(0.3)

        # 5. anim select
        print("\n=== 5. 动画选择器 ===")
        result = page.evaluate("""() => {
            const select = document.getElementById('anim-select');
            const before = select.value;
            select.value = 'slide';
            select.dispatchEvent(new Event('change'));
            const after = select.value;
            const savedAnim = localStorage.getItem('animType');
            return { before, after, savedAnim };
        }""")
        ok = result['after'] == 'slide'
        tests.append(("动画选择器", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: before={result['before']}, after={result['after']}, savedAnim={result['savedAnim']}")

        # Reset
        page.evaluate("""() => {
            const select = document.getElementById('anim-select');
            select.value = 'fade';
            select.dispatchEvent(new Event('change'));
        }""")
        time.sleep(0.3)

        # 6. Theme item click
        print("\n=== 6. 主题项点击 ===")
        # First open theme panel
        page.evaluate("""() => { openThemePanel(); }""")
        time.sleep(0.3)
        result = page.evaluate("""() => {
            const items = document.querySelectorAll('.theme-detail-item');
            const cyberItem = Array.from(items).find(i => i.getAttribute('data-theme') === 'cyber');
            if (!cyberItem) return { found: false };
            const before = currentTheme;
            cyberItem.click();
            const after = currentTheme;
            return { found: true, before, after };
        }""")
        ok = result.get('found') and result.get('after') == 'cyber'
        tests.append(("主题项点击", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: {result}")

        # Reset theme
        page.evaluate("""() => {
            closeThemePanel();
            setTheme('dark');
        }""")
        time.sleep(0.3)

        # 7. Check if clicking inside nav-bar closes the panel (should NOT)
        print("\n=== 7. 点击nav-bar内部不应关闭面板 ===")
        result = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const ov = document.getElementById('settings-overlay');
            const slider = document.getElementById('dwell-slider');
            slider.click();
            return {
                nb_open: nb.classList.contains('open'),
                ov_active: ov.classList.contains('active'),
            };
        }""")
        ok = result['nb_open'] and result['ov_active']
        tests.append(("点击nav-bar内部不关闭面板", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: {result}")

        # 8. Check if clicking overlay closes panel
        print("\n=== 8. 点击overlay关闭面板 ===")
        page.mouse.click(187, 100)
        time.sleep(0.5)
        result = page.evaluate("""() => ({
            nb_open: document.getElementById('nav-bar-luxury').classList.contains('open'),
            ov_active: document.getElementById('settings-overlay').classList.contains('active'),
        })""")
        ok = not result['nb_open'] and not result['ov_active']
        tests.append(("点击overlay关闭面板", ok))
        print(f"  {'PASS' if ok else 'FAIL'}: {result}")

        # Summary
        print("\n" + "=" * 50)
        print("FUNCTION TEST SUMMARY")
        print("=" * 50)
        passed = sum(1 for _, r in tests if r)
        for name, result in tests:
            print(f"  {'✅' if result else '❌'} {name}")
        print(f"\n{passed}/{len(tests)} tests passed")

        browser.close()

if __name__ == "__main__":
    test()
