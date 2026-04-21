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
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        page.goto(file_url, wait_until="networkidle", timeout=30000)
        time.sleep(1)

        # Test: manually call startDisplay step by step
        print("=== STEP BY STEP TEST ===")
        
        # Step 1: Set text
        page.evaluate("""() => {
            document.getElementById('text-input').value = '第一条测试文字。\\n\\n第二条测试文字。\\n\\n第三条测试文字。';
        }""")
        
        # Step 2: Check text was set
        text_val = page.evaluate("""() => document.getElementById('text-input').value""")
        print(f"  text-input value: '{text_val[:80]}'")
        
        # Step 3: Try parsing manually
        parse_result = page.evaluate("""() => {
            try {
                const text = document.getElementById('text-input').value;
                const parsed = text.split(/\\n\\n+/).flatMap(para => {
                    const result = [];
                    let cursor = 0;
                    while (cursor < para.length) {
                        let end = -1;
                        for (let i = cursor + 1; i < para.length; i++) {
                            const ch = para[i];
                            if (ch === '。' || ch === '！' || ch === '？' || ch === '?' || ch === '!') {
                                end = i;
                                break;
                            }
                            if (ch === '.') {
                                end = i;
                                break;
                            }
                        }
                        if (end === -1) {
                            const rest = para.substring(cursor).trim();
                            if (rest) result.push(rest);
                            break;
                        }
                        const sent = para.substring(cursor, end + 1).trim();
                        if (sent) result.push(sent);
                        cursor = end + 1;
                    }
                    return result.length > 0 ? result : [para.trim()];
                }).filter(s => s).map(text => ({ text }));
                return { success: true, count: parsed.length, texts: parsed.map(p => p.text) };
            } catch(e) {
                return { success: false, error: e.message };
            }
        }""")
        print(f"  Manual parse: {parse_result}")
        
        # Step 4: Call startDisplay with error catching
        print("\n=== CALL startDisplay ===")
        page.evaluate("""() => {
            try {
                window.__startDisplayError = null;
                startDisplay();
            } catch(e) {
                window.__startDisplayError = e.message + ' | stack: ' + e.stack;
            }
        }""")
        time.sleep(3)
        
        error_msg = page.evaluate("""() => window.__startDisplayError""")
        if error_msg:
            print(f"  startDisplay ERROR: {error_msg}")
        else:
            print(f"  startDisplay: no error thrown")
        
        # Check sentences
        sentences_info = page.evaluate("""() => {
            try {
                // Access sentences via closure - can't directly
                // Instead check DOM state
                const progressVal = document.getElementById('progress-val');
                const sentenceEl = document.querySelector('.sentence-text');
                const displayScreen = document.getElementById('display-screen');
                const inputScreen = document.getElementById('input-screen');
                return {
                    progress_text: progressVal ? progressVal.innerText : null,
                    sentence_exists: !!sentenceEl,
                    sentence_text: sentenceEl ? sentenceEl.innerText : null,
                    sentence_className: sentenceEl ? sentenceEl.className : null,
                    sentence_opacity: sentenceEl ? getComputedStyle(sentenceEl).opacity : null,
                    display_screen_display: displayScreen ? getComputedStyle(displayScreen).display : null,
                    display_screen_opacity: displayScreen ? getComputedStyle(displayScreen).opacity : null,
                    input_screen_display: inputScreen ? getComputedStyle(inputScreen).display : null,
                };
            } catch(e) {
                return { error: e.message };
            }
        }""")
        for k, v in sentences_info.items():
            print(f"  {k}: {v}")

        # Check entry-option and bottom controls
        print("\n=== DOM STRUCTURE ===")
        dom_info = page.evaluate("""() => {
            const entryOptions = document.querySelectorAll('.entry-option');
            const bottomPrev = document.getElementById('bottom-prev');
            const bottomNext = document.getElementById('bottom-next');
            const bottomPlay = document.getElementById('bottom-play');
            const controlBtns = document.querySelectorAll('.bottom-control-btn');
            const controlBtn = document.querySelectorAll('.control-btn');
            return {
                entry_option_count: entryOptions.length,
                bottom_prev_exists: !!bottomPrev,
                bottom_next_exists: !!bottomNext,
                bottom_play_exists: !!bottomPlay,
                bottom_control_btn_count: controlBtns.length,
                control_btn_count: controlBtn.length,
                control_btn_ids: Array.from(controlBtn).map(b => b.id || b.className.substring(0, 30)),
            };
        }""")
        for k, v in dom_info.items():
            print(f"  {k}: {v}")

        # Check the HTML structure of entry-card
        print("\n=== ENTRY CARD HTML ===")
        entry_html = page.evaluate("""() => {
            const card = document.querySelector('.entry-card');
            if (!card) return 'NO ENTRY CARD';
            return card.innerHTML.substring(0, 2000);
        }""")
        print(f"  {entry_html[:1500]}")

        # Check bottom-controls HTML
        print("\n=== BOTTOM CONTROLS HTML ===")
        bc_html = page.evaluate("""() => {
            const bc = document.getElementById('bottom-controls');
            if (!bc) return 'NO BOTTOM CONTROLS';
            return bc.innerHTML.substring(0, 1000);
        }""")
        print(f"  {bc_html[:800]}")

        print("\n--- JS Errors ---")
        for err in js_errors:
            print(f"  {err}")
        
        print("\n--- Console Logs ---")
        for log in console_logs[:20]:
            print(f"  {log}")

        browser.close()
        print("\nDone!")

if __name__ == "__main__":
    test()
