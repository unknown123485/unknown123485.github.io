import os
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"d:\重要技术文件\项目\文本展示\pw-browsers"
from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width":375,"height":812}, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)", is_mobile=True, has_touch=True)
    page = ctx.new_page()
    page.goto("file:///" + r"d:\重要技术文件\项目\文本展示\preview.html".replace("\\","/"), wait_until="networkidle", timeout=30000)
    time.sleep(1)
    page.evaluate("""() => { document.getElementById('text-input').value = '春水初生，春林初盛。\\n\\n春风十里，不如你。'; startDisplay(); }""")
    time.sleep(3)
    info = page.evaluate("""() => {
        const el = document.querySelector('#standard-area > .sentence-text');
        if (!el) return 'NOT FOUND';
        const cs = getComputedStyle(el);
        return {
            text: el.innerText,
            opacity: cs.opacity,
            filter: cs.filter,
            transform: cs.transform,
            display: cs.display,
            visibility: cs.visibility,
            color: cs.color,
            fontSize: cs.fontSize,
        };
    }""")
    print("Text in standard-area:", info)
    browser.close()
