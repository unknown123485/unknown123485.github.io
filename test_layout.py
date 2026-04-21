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

        page.evaluate("""() => {
            document.getElementById('text-input').value = '测试文字。\\n\\n第二条。';
            startDisplay();
        }""")
        time.sleep(3)

        # Open settings
        page.evaluate("""() => { toggleNav(); }""")
        time.sleep(1)

        # Check nav-bar scroll state and content height
        info = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const dpiWrap = nb.querySelector('.dpi-content-wrap');
            return {
                nb_scrollHeight: nb.scrollHeight,
                nb_clientHeight: nb.clientHeight,
                nb_scrollTop: nb.scrollTop,
                nb_offsetHeight: nb.offsetHeight,
                nb_maxHeight: getComputedStyle(nb).maxHeight,
                nb_overflow: getComputedStyle(nb).overflow,
                nb_overflowY: getComputedStyle(nb).overflowY,
                dpiWrap_scrollHeight: dpiWrap ? dpiWrap.scrollHeight : 0,
                dpiWrap_offsetHeight: dpiWrap ? dpiWrap.offsetHeight : 0,
                dpiWrap_style: dpiWrap ? dpiWrap.style.cssText : '',
                dpiWrap_computed_maxHeight: dpiWrap ? getComputedStyle(dpiWrap).maxHeight : '',
                dpiWrap_computed_overflow: dpiWrap ? getComputedStyle(dpiWrap).overflow : '',
                dpiWrap_computed_overflowY: dpiWrap ? getComputedStyle(dpiWrap).overflowY : '',
                needs_scroll: nb.scrollHeight > nb.clientHeight,
            };
        }""")
        print("=== NAV-BAR SCROLL INFO ===")
        for k, v in info.items():
            print(f"  {k}: {v}")

        # Check if eink-toggle and theme button are visible without scrolling
        print("\n=== ELEMENT VISIBILITY WITHOUT SCROLL ===")
        vis = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const nbRect = nb.getBoundingClientRect();
            const themeBtn = nb.querySelector('.themes-section .control-btn');
            const einkToggle = document.getElementById('eink-toggle');
            const themeRect = themeBtn ? themeBtn.getBoundingClientRect() : null;
            const einkRect = einkToggle ? einkToggle.getBoundingClientRect() : null;
            return {
                nb_rect: {top: nbRect.top, bottom: nbRect.bottom, h: nbRect.height},
                theme_btn: themeRect ? {top: themeRect.top, bottom: themeRect.bottom, inView: themeRect.bottom <= nbRect.bottom} : null,
                eink_toggle: einkRect ? {top: einkRect.top, bottom: einkRect.bottom, inView: einkRect.bottom <= nbRect.bottom} : null,
            };
        }""")
        print(f"  {vis}")

        # Now scroll to bottom and check again
        page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            nb.scrollTop = nb.scrollHeight;
        }""")
        time.sleep(0.3)

        vis2 = page.evaluate("""() => {
            const nb = document.getElementById('nav-bar-luxury');
            const nbRect = nb.getBoundingClientRect();
            const themeBtn = nb.querySelector('.themes-section .control-btn');
            const einkToggle = document.getElementById('eink-toggle');
            const themeRect = themeBtn ? themeBtn.getBoundingClientRect() : null;
            const einkRect = einkToggle ? einkToggle.getBoundingClientRect() : null;
            return {
                nb_rect: {top: nbRect.top, bottom: nbRect.bottom, h: nbRect.height},
                theme_btn: themeRect ? {top: themeRect.top, bottom: themeRect.bottom, inView: themeRect.bottom <= nbRect.bottom} : null,
                eink_toggle: einkRect ? {top: einkRect.top, bottom: einkRect.bottom, inView: einkRect.bottom <= nbRect.bottom} : null,
            };
        }""")
        print(f"\n=== ELEMENT VISIBILITY AFTER SCROLL ===")
        print(f"  {vis2}")

        # Check the custom font select - it had rect 0,0,0,0
        print("\n=== FONT SELECT INFO ===")
        font_info = page.evaluate("""() => {
            const fs = document.getElementById('font-select');
            const cf = document.getElementById('custom-font-select');
            return {
                font_select: fs ? {
                    display: getComputedStyle(fs).display,
                    rect: fs.getBoundingClientRect(),
                    parent: fs.parentElement ? fs.parentElement.id : null,
                } : null,
                custom_font_select: cf ? {
                    display: getComputedStyle(cf).display,
                    rect: cf.getBoundingClientRect(),
                    opacity: getComputedStyle(cf).opacity,
                    pointerEvents: getComputedStyle(cf).pointerEvents,
                } : null,
            };
        }""")
        print(f"  {font_info}")

        # Check what the themes-section looks like
        print("\n=== THEMES SECTION ===")
        themes_info = page.evaluate("""() => {
            const section = document.querySelector('.themes-section');
            if (!section) return { exists: false };
            const rect = section.getBoundingClientRect();
            const cs = getComputedStyle(section);
            return {
                rect: {top: rect.top, bottom: rect.bottom, h: rect.height},
                overflow: cs.overflow,
                overflowY: cs.overflowY,
                maxHeight: cs.maxHeight,
                scrollHeight: section.scrollHeight,
                clientHeight: section.clientHeight,
            };
        }""")
        print(f"  {themes_info}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
