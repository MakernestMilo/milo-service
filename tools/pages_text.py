import json
from playwright.sync_api import sync_playwright
SRC = "/mnt/user-data/outputs/The Maker's Book of Origins - A5 complete.html"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.route("http*://**", lambda r: r.abort())
    pg.goto("file://" + SRC); pg.wait_for_timeout(3000)
    pages = pg.evaluate("""[...document.querySelectorAll('section.page')].map(s=>({id:s.id, text:s.querySelector('.c')?s.querySelector('.c').innerText:s.innerText}))""")
    b.close()
json.dump(pages, open("/tmp/claude-0/-home-claude/3631de14-c379-5cf7-8bb1-7c3db6aef04f/scratchpad/milo_build/pages.json", "w"), indent=1, ensure_ascii=False)
print(len(pages))
