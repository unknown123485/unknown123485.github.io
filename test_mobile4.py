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

        js_errors = []
        page.on("pageerror", lambda err: js_errors.append(str(err)))

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        time.sleep(1)

        page.evaluate("""() => {
            document.getElementById('text-input').value = '第一条测试文字。\\n\\n第二条测试文字。\\n\\n第三条测试文字。';
            startDisplay();
        }""")
        time.sleep(5)

        info = page.evaluate("""() => {
            const allST = document.querySelectorAll('.sentence-text');
            const result = [];
            for (let i = 0; i < allST.length; i++) {
                const el = allST[i];
                const cs = getComputedStyle(el);
                result.push({
                    i: i,
                    text: el.innerText,
                    html: el.innerHTML.substring(0, 100),
                    cls: el.className,
                    opacity: cs.opacity,
                    transform: cs.transform,
                    display: cs.display,
                    color: cs.color,
                    fontSize: cs.fontSize,
                    w: el.offsetWidth,
                    h: el.offsetHeight,
                    active: el.classList.contains('active'),
                    parent: el.parentElement ? el.parentElement.id : null,
                });
            }
            const sa = document.getElementById('standard-area');
            const da = document.querySelector('.display-area');
            return {
                sentences: result,
                sa_html_len: sa ? sa.innerHTML.length : 0,
                sa_child_count: sa ? sa.children.length : 0,
                da_h: da ? da.offsetHeight : 0,
                progress: document.getElementById('progress-val') ? document.getElementById('progress-val').innerText : null,
            };
        }""")

        print("=== ALL .sentence-text ELEMENTS ===")
        for s in info['sentences']:
            print(f"  [{s['i']}] text='{s['text'][:50]}' cls='{s['cls']}' opacity={s['opacity']} transform={s['transform']} display={s['display']} color={s['color']} fontSize={s['fontSize']} w={s['w']} h={s['h']} active={s['active']} parent={s['parent']}")
        print(f"  sa_html_len={info['sa_html_len']} sa_child_count={info['sa_child_count']} da_h={info['da_h']} progress={info['progress']}")

        # Check what's in standard-area innerHTML
        sa_html = page.evaluate("""() => document.getElementById('standard-area').innerHTML.substring(0, 500)""")
        print(f"\n  standard-area innerHTML: {sa_html}")

        # Check if there's a .typewriter-display inside standard-area
        tw_display = page.evaluate("""() => {
            const tw = document.querySelector('.typewriter-display');
            return tw ? { exists: true, display: getComputedStyle(tw).display, h: tw.offsetHeight, opacity: getComputedStyle(tw).opacity } : { exists: false };
        }""")
        print(f"\n  .typewriter-display: {tw_display}")

        print("\n--- JS Errors ---")
        for err in js_errors:
            print(f"  {err}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
