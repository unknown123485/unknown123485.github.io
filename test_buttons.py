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

        # Load text and start display
        page.evaluate("""() => {
            document.getElementById('text-input').value = '测试文字一。\\n\\n测试文字二。\\n\\n测试文字三。';
            startDisplay();
        }""")
        time.sleep(3)

        # Open settings panel
        page.evaluate("""() => { toggleNav(); }""")
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "func_settings_open.png"), full_page=True)

        # ===== TEST: 主题详情按钮 =====
        print("=== TEST: 主题详情按钮 ===")
        # Find the button and its position
        theme_btn_info = page.evaluate("""() => {
            const btn = document.querySelector('.themes-section .control-btn');
            if (!btn) return { exists: false };
            const rect = btn.getBoundingClientRect();
            const cs = getComputedStyle(btn);
            return {
                exists: true,
                text: btn.innerText,
                rect: rect,
                opacity: cs.opacity,
                pointerEvents: cs.pointerEvents,
                display: cs.display,
                parentPointerEvents: btn.parentElement ? getComputedStyle(btn.parentElement).pointerEvents : null,
                grandparentPointerEvents: btn.parentElement && btn.parentElement.parentElement ? getComputedStyle(btn.parentElement.parentElement).pointerEvents : null,
                controlGroupPointerEvents: (() => {
                    const cg = document.querySelector('.control-group');
                    return cg ? getComputedStyle(cg).pointerEvents : null;
                })(),
                controlGroupOpacity: (() => {
                    const cg = document.querySelector('.control-group');
                    return cg ? getComputedStyle(cg).opacity : null;
                })(),
            };
        }""")
        print(f"  Button info: {theme_btn_info}")

        # Try clicking the theme button via JS
        print("\n  --- JS click test ---")
        result_js = page.evaluate("""() => {
            const panel = document.getElementById('theme-detail-panel');
            const before = getComputedStyle(panel).display;
            openThemePanel();
            const after = getComputedStyle(panel).display;
            return { before, after, themePanelOpen };
        }""")
        print(f"  JS openThemePanel(): before={result_js['before']}, after={result_js['after']}, themePanelOpen={result_js['themePanelOpen']}")

        # Close theme panel
        page.evaluate("""() => { closeThemePanel(); }""")
        time.sleep(0.3)

        # Now try actual Playwright click on the button
        print("\n  --- Playwright click test ---")
        theme_btn = page.query_selector(".themes-section .control-btn")
        if theme_btn:
            try:
                theme_btn.click(timeout=5000)
                time.sleep(0.5)
                after_click = page.evaluate("""() => {
                    const panel = document.getElementById('theme-detail-panel');
                    return { display: getComputedStyle(panel).display, themePanelOpen };
                }""")
                print(f"  After Playwright click: display={after_click['display']}, themePanelOpen={after_click['themePanelOpen']}")
            except Exception as e:
                print(f"  Playwright click FAILED: {str(e)[:200]}")
                # Check what's intercepting
                intercept_info = page.evaluate("""() => {
                    const btn = document.querySelector('.themes-section .control-btn');
                    const rect = btn.getBoundingClientRect();
                    const cx = rect.x + rect.width / 2;
                    const cy = rect.y + rect.height / 2;
                    const topEl = document.elementFromPoint(cx, cy);
                    return {
                        btn_rect: rect,
                        center: {x: cx, y: cy},
                        top_element: topEl ? topEl.tagName + (topEl.id ? '#' + topEl.id : '') + (topEl.className ? '.' + topEl.className : '') : null,
                        top_element_parent: topEl && topEl.parentElement ? topEl.parentElement.tagName + (topEl.parentElement.id ? '#' + topEl.parentElement.id : '') : null,
                    };
                }""")
                print(f"  Intercept info: {intercept_info}")
        else:
            print("  Button not found!")

        # Close theme panel if open
        page.evaluate("""() => { closeThemePanel(); }""")
        time.sleep(0.3)

        # ===== TEST: 墨水屏模式按钮 =====
        print("\n=== TEST: 墨水屏模式按钮 ===")
        eink_info = page.evaluate("""() => {
            const toggle = document.getElementById('eink-toggle');
            if (!toggle) return { exists: false };
            const rect = toggle.getBoundingClientRect();
            const cs = getComputedStyle(toggle);
            const wrap = toggle.closest('.eink-toggle-wrap');
            const wrapCS = wrap ? getComputedStyle(wrap) : null;
            return {
                exists: true,
                rect: rect,
                opacity: cs.opacity,
                pointerEvents: cs.pointerEvents,
                display: cs.display,
                wrapOpacity: wrapCS ? wrapCS.opacity : null,
                wrapPointerEvents: wrapCS ? wrapCS.pointerEvents : null,
                einkMode_before: einkMode,
                active_before: toggle.classList.contains('active'),
            };
        }""")
        print(f"  Eink toggle info: {eink_info}")

        # Try JS click
        print("\n  --- JS click test ---")
        result_eink = page.evaluate("""() => {
            const before = einkMode;
            toggleEinkMode();
            const after = einkMode;
            const toggle = document.getElementById('eink-toggle');
            return { before, after, active: toggle.classList.contains('active') };
        }""")
        print(f"  JS toggleEinkMode(): before={result_eink['before']}, after={result_eink['after']}, active={result_eink['active']}")

        # Toggle back
        page.evaluate("""() => { toggleEinkMode(); }""")
        time.sleep(0.3)

        # Try Playwright click
        print("\n  --- Playwright click test ---")
        eink_toggle = page.query_selector("#eink-toggle")
        if eink_toggle:
            try:
                eink_toggle.click(timeout=5000)
                time.sleep(0.5)
                after_eink = page.evaluate("""() => {
                    return { einkMode, active: document.getElementById('eink-toggle').classList.contains('active') };
                }""")
                print(f"  After Playwright click: einkMode={after_eink['einkMode']}, active={after_eink['active']}")
                # Toggle back
                page.evaluate("""() => { if(einkMode) toggleEinkMode(); }""")
            except Exception as e:
                print(f"  Playwright click FAILED: {str(e)[:200]}")
                intercept_info = page.evaluate("""() => {
                    const toggle = document.getElementById('eink-toggle');
                    const rect = toggle.getBoundingClientRect();
                    const cx = rect.x + rect.width / 2;
                    const cy = rect.y + rect.height / 2;
                    const topEl = document.elementFromPoint(cx, cy);
                    return {
                        toggle_rect: rect,
                        center: {x: cx, y: cy},
                        top_element: topEl ? topEl.tagName + (topEl.id ? '#' + topEl.id : '') + (topEl.className ? '.' + topEl.className : '') : null,
                    };
                }""")
                print(f"  Intercept info: {intercept_info}")

        # ===== TEST: All interactive elements in nav-bar =====
        print("\n=== TEST: ALL NAV-BAR INTERACTIVE ELEMENTS ===")
        all_elements = page.evaluate("""() => {
            const navBar = document.getElementById('nav-bar-luxury');
            const interactives = navBar.querySelectorAll('button, [onclick], input, select, .eink-toggle');
            return Array.from(interactives).map(el => {
                const rect = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                const cx = rect.x + rect.width / 2;
                const cy = rect.y + rect.height / 2;
                const topEl = document.elementFromPoint(cx, cy);
                const isTop = topEl === el || el.contains(topEl);
                return {
                    tag: el.tagName,
                    id: el.id || '',
                    class: el.className ? el.className.substring(0, 60) : '',
                    onclick: el.getAttribute('onclick') || '',
                    rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)},
                    opacity: cs.opacity,
                    pointerEvents: cs.pointerEvents,
                    display: cs.display,
                    isTopElement: isTop,
                    topElement: topEl ? (topEl.tagName + (topEl.id ? '#'+topEl.id : '') + (topEl.className ? '.'+topEl.className.toString().substring(0,30) : '')) : null,
                    inViewport: rect.y >= 0 && rect.y <= 812,
                };
            });
        }""")
        for el in all_elements:
            status = "OK" if el['isTopElement'] and el['inViewport'] and el['pointerEvents'] != 'none' else "BLOCKED"
            if not el['inViewport']:
                status = "OFFSCREEN"
            print(f"  [{status}] {el['tag']}#{el['id']} onclick='{el['onclick'][:40]}' rect={el['rect']} pe={el['pointerEvents']} op={el['opacity']} top={el['isTopElement']} topEl={el['topElement']}")

        # ===== TEST: Scroll nav-bar and re-check =====
        print("\n=== TEST: SCROLL NAV-BAR AND RE-CHECK ===")
        page.evaluate("""() => {
            const navBar = document.getElementById('nav-bar-luxury');
            navBar.scrollTop = navBar.scrollHeight;
        }""")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "func_scrolled.png"), full_page=True)

        all_elements2 = page.evaluate("""() => {
            const navBar = document.getElementById('nav-bar-luxury');
            const interactives = navBar.querySelectorAll('button, [onclick], input, select, .eink-toggle');
            return Array.from(interactives).map(el => {
                const rect = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                const cx = rect.x + rect.width / 2;
                const cy = rect.y + rect.height / 2;
                const topEl = document.elementFromPoint(cx, cy);
                const isTop = topEl === el || el.contains(topEl);
                return {
                    tag: el.tagName,
                    id: el.id || '',
                    onclick: el.getAttribute('onclick') || '',
                    rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)},
                    pointerEvents: cs.pointerEvents,
                    isTopElement: isTop,
                    inViewport: rect.y >= 0 && rect.y <= 812,
                    topElement: topEl ? (topEl.tagName + (topEl.id ? '#'+topEl.id : '') + (topEl.className ? '.'+topEl.className.toString().substring(0,30) : '')) : null,
                };
            });
        }""")
        for el in all_elements2:
            status = "OK" if el['isTopElement'] and el['inViewport'] and el['pointerEvents'] != 'none' else "BLOCKED"
            if not el['inViewport']:
                status = "OFFSCREEN"
            print(f"  [{status}] {el['tag']}#{el['id']} onclick='{el['onclick'][:40]}' rect={el['rect']} pe={el['pointerEvents']} top={el['isTopElement']} topEl={el['topElement']}")

        print("\n--- JS Errors ---")
        for err in js_errors:
            print(f"  {err}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
