"""
XHS Pages Generator — Example
Reads a Markdown file and generates a multi-page HTML card for Xiaohongshu (小红书).

Usage:
  python xhs_pages.py              # Generate HTML only
  python xhs_pages.py --screenshot # Generate + Playwright screenshots
"""
import sys, re, argparse
from pathlib import Path

# ──────────────────── Config ────────────────────
# Modify these for your article:
SRC = Path(__file__).parent / "example_article.md"
OUT_HTML = Path(__file__).parent / "example_xhs_pages.html"
SCREENSHOT_DIR = Path(__file__).parent / "output"
AVATAR = "avatar.jpg"   # Replace with your avatar path
AUTHOR = "Your Name"
DATE = "2026年 04月 28日"
TITLE = "为什么你需要一个自己的排版系统"
FOOTER_LABEL = "XHS Card Generator"
TOTAL_PAGES = 4

# Page definitions: (start_line, end_line) — 1-indexed, inclusive
PAGES = [
    (1, 12),    # P1: Title + Hook
    (14, 26),   # P2: Code beats drag-and-drop
    (28, 42),   # P3: Comparison table
    (44, 60),   # P4: Get started
]

# ──────────────────── Markdown → HTML ────────────────────
def md_to_html(text):
    lines = text.split('\n')
    html_lines = []
    in_list = False
    in_code = False
    code_lines = []

    for line in lines:
        stripped = line.strip()

        # Code block toggle
        if stripped.startswith('```'):
            if in_code:
                html_lines.append('<pre><code>' + '\n'.join(code_lines) + '</code></pre>')
                code_lines = []
                in_code = False
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
            continue

        # H2
        if stripped.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            title = stripped[3:]
            html_lines.append(f'<h2>{title}</h2>')
            continue

        # H1 (skip — handled separately on page 1)
        if stripped.startswith('# '):
            continue

        # HR
        if stripped == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue

        # Table
        if '|' in stripped and stripped.startswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(set(c) <= set('- :') for c in cells):
                continue  # skip separator row
            if not any(c for c in cells):
                continue
            tag = 'th' if not html_lines or '</table>' in html_lines[-5:] else 'td'
            # Check if this looks like a header row (first table row)
            row = ''.join(f'<{tag}>{c}</{tag}>' for c in cells)
            html_lines.append(f'<tr>{row}</tr>')
            continue

        # Ordered list
        m = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if m:
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = inline_format(m.group(2))
            html_lines.append(f'<li>{content}</li>')
            continue

        # Unordered list
        if stripped.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = inline_format(stripped[2:])
            html_lines.append(f'<li>{content}</li>')
            continue

        # Regular paragraph
        if in_list:
            html_lines.append('</ul>')
            in_list = False
        content = inline_format(stripped)
        html_lines.append(f'<p>{content}</p>')

    if in_list:
        html_lines.append('</ul>')
    return '\n'.join(html_lines)


def inline_format(text):
    """Convert Markdown inline formatting to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

# ──────────────────── HTML Template ────────────────────
CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&family=Noto+Serif+SC:wght@400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
html, body {
  background: #F9F9F6;
  overflow: hidden;
  -ms-overflow-style: none;
  scrollbar-width: none;
  margin: 0; padding: 0;
}
html::-webkit-scrollbar, body::-webkit-scrollbar { display: none; }
* { margin: 0; padding: 0; box-sizing: border-box; }
.card {
  width: 1080px;
  background: #F9F9F6;
  padding: 90px;
  font-family: 'Noto Serif SC', serif;
  color: #1A1A1A;
  display: none;
  flex-direction: column;
}
.card.active { display: flex; }
h1 { font-size: 60px; font-weight: 700; line-height: 1.3; margin-bottom: 50px; color: #000; }
h2 { font-size: 44px; font-weight: 700; margin: 68px 0 34px; color: #000; }
p { font-size: 34px; font-weight: 400; line-height: 2; margin-bottom: 34px; color: #1A1A1A; }
strong { font-weight: 700; }
em { font-style: normal; color: #000; }
code { font-family: 'JetBrains Mono', monospace; font-size: 30px; background: #f5f5f5; padding: 2px 6px; border-radius: 4px; }
pre { background: #f5f5f5; padding: 20px; border-radius: 6px; margin: 18px 0; overflow-x: auto; }
pre code { font-size: 28px; background: none; padding: 0; }
ul { font-size: 34px; line-height: 2; padding-left: 34px; margin-bottom: 34px; }
li { margin-bottom: 8px; }
table { width: 100%; border-collapse: collapse; font-size: 28px; margin: 18px 0; }
th { background: #f0efe8; font-weight: 700; padding: 10px 12px; border-bottom: 2px solid #d0cec5; text-align: left; }
td { padding: 8px 12px; border-bottom: 1px solid #E8E6D9; line-height: 1.6; }
blockquote { border-left: 6px solid #4a9eff; padding-left: 34px; font-style: italic; margin: 34px 0; }
.author-area { display: flex; align-items: center; gap: 20px; margin-bottom: 50px; }
.author-area img { width: 80px; height: 80px; border-radius: 50%; border: 2px solid #E8E6D9; object-fit: cover; }
.author-info { display: flex; flex-direction: column; gap: 6px; }
.author-name { font-size: 30px; color: #333; font-weight: 400; line-height: 1.2; }
.author-date { font-size: 22px; color: #888; font-weight: 300; font-family: 'Inter', sans-serif; line-height: 1.3; }
.page-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 24px; border-top: 1px solid #E8E6D9; }
.footer-title { font-size: 20px; color: #aaa; font-family: 'Inter', sans-serif; font-weight: 300; }
.footer-page { font-size: 22px; color: #aaa; font-family: 'Inter', sans-serif; font-weight: 400; }
#navControls { position: fixed; bottom: 20px; right: 20px; z-index: 999; display: flex; gap: 10px; }
#navControls button { padding: 10px 20px; font-size: 16px; cursor: pointer; border: 1px solid #ccc; background: #fff; border-radius: 6px; }
"""

def build_html(pages_content):
    cards = []
    for i, content in enumerate(pages_content, 1):
        body_html = md_to_html(content)
        if i == 1:
            card_inner = f"""
      <h1>{TITLE}</h1>
      <div class="author-area">
        <img src="{AVATAR}" alt="avatar">
        <div class="author-info">
          <div class="author-name">{AUTHOR}</div>
          <div class="author-date">{DATE}</div>
        </div>
      </div>
      {body_html}
"""
        else:
            card_inner = body_html

        card_inner += f"""
      <div class="page-footer">
        <span class="footer-title">{FOOTER_LABEL}</span>
        <span class="footer-page">{i} / {TOTAL_PAGES}</span>
      </div>
"""
        cards.append(f'  <div class="card" data-page="{i}">\n{card_inner}\n  </div>')

    all_cards = '\n'.join(cards)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
{CSS}
</style>
</head>
<body>
{all_cards}
<div id="navControls">
  <button onclick="go(-1)">Prev</button>
  <button onclick="go(1)">Next</button>
</div>
<script>
let cur = parseInt(new URLSearchParams(location.search).get('page')) || 1;
function showPage(n) {{
  document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
  const el = document.querySelector('[data-page="'+n+'"]');
  if (el) el.classList.add('active');
  cur = n;
}}
function go(d) {{ cur = Math.max(1, Math.min({TOTAL_PAGES}, cur+d)); showPage(cur); }}
showPage(cur);
</script>
</body>
</html>"""

# ──────────────────── Main ────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--screenshot', action='store_true',
                        help='Generate HTML + take Playwright screenshots')
    args = parser.parse_args()

    # Read source
    src_lines = SRC.read_text(encoding='utf-8').split('\n')

    # Extract pages
    pages_content = []
    for start, end in PAGES:
        chunk = src_lines[start-1:end]
        pages_content.append('\n'.join(chunk))

    # Build HTML
    html = build_html(pages_content)
    OUT_HTML.write_text(html, encoding='utf-8')
    print(f"[OK] {OUT_HTML.name} generated ({TOTAL_PAGES} pages)")

    if args.screenshot:
        import asyncio
        asyncio.run(take_screenshots())

async def take_screenshots():
    from playwright.async_api import async_playwright
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in range(1, TOTAL_PAGES + 1):
            page = await browser.new_page(viewport={"width": 1080, "height": 1440})
            url = OUT_HTML.as_uri() + f"?page={i}"
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            # Clean up browser artifacts before screenshot
            await page.evaluate("""() => {
                document.getElementById('navControls').style.display = 'none';
                document.querySelectorAll('*').forEach(el => {
                    el.style.outline = 'none';
                    el.style.boxShadow = 'none';
                    el.style.filter = 'none';
                });
                document.querySelectorAll('body > :not(.card):not(script):not(#navControls)').forEach(el => el.remove());
                document.querySelectorAll('html *').forEach(el => {
                    if (el.shadowRoot) { el.shadowRoot.innerHTML = ''; }
                });
                document.documentElement.style.cssText = 'background:#F9F9F6!important;outline:none!important;box-shadow:none!important';
                document.body.style.cssText = 'background:#F9F9F6!important;padding:0!important;margin:0!important;overflow:hidden!important;outline:none!important;box-shadow:none!important';
            }""")
            await page.wait_for_timeout(500)
            card = await page.query_selector(f'[data-page="{i}"]')
            if card:
                out_path = SCREENSHOT_DIR / f"{str(i).zfill(2)}.png"
                await card.screenshot(path=str(out_path))
                print(f"[OK] {out_path.name}")
            await page.close()
        await browser.close()
    print(f"[OK] All {TOTAL_PAGES} pages saved to {SCREENSHOT_DIR.name}/")

if __name__ == "__main__":
    main()
