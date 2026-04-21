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
            document.getElementById('text-input').value = '测试文字一。\\n\\n测试文字二。';
            startDisplay();
        }""")
        time.sleep(5)

        # Deep CSS investigation
        info = page.evaluate("""() => {
            const el = document.querySelector('.sentence-text.active');
            if (!el) return { error: 'no .sentence-text.active found' };
            
            const cs = getComputedStyle(el);
            const allRules = [];
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules) {
                        if (rule.selectorText && el.matches(rule.selectorText)) {
                            allRules.push({
                                selector: rule.selectorText,
                                opacity: rule.style.opacity || 'not set',
                                transform: rule.style.transform || 'not set',
                                href: sheet.href ? sheet.href.substring(sheet.href.length - 30) : 'inline'
                            });
                        }
                    }
                } catch(e) {}
            }
            
            return {
                className: el.className,
                innerText: el.innerText,
                inline_opacity: el.style.opacity,
                inline_transform: el.style.transform,
                inline_color: el.style.color,
                computed_opacity: cs.opacity,
                computed_transform: cs.transform,
                computed_transition: cs.transition,
                computed_display: cs.display,
                computed_visibility: cs.visibility,
                computed_position: cs.position,
                computed_zIndex: cs.zIndex,
                computed_width: cs.width,
                computed_height: cs.height,
                computed_fontSize: cs.fontSize,
                computed_color: cs.color,
                offsetWidth: el.offsetWidth,
                offsetHeight: el.offsetHeight,
                boundingRect: el.getBoundingClientRect(),
                parent_id: el.parentElement ? el.parentElement.id : null,
                parent_computed_display: el.parentElement ? getComputedStyle(el.parentElement).display : null,
                parent_computed_opacity: el.parentElement ? getComputedStyle(el.parentElement).opacity : null,
                matching_rules: allRules
            };
        }""")
        
        for k, v in info.items():
            if k == 'matching_rules':
                print(f"  matching_rules ({len(v)} rules):")
                for r in v:
                    print(f"    {r}")
            elif k == 'boundingRect':
                print(f"  {k}: x={v['x']:.1f} y={v['y']:.1f} w={v['width']:.1f} h={v['height']:.1f}")
            else:
                print(f"  {k}: {v}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
