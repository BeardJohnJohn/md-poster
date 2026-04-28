# -*- coding: utf-8 -*-
"""
XHS Card Screenshot Generator V3
Automatically finds *_xhs_pages.html in the same directory and captures each page.

Supports two modes:
  python screenshot.py              # Fixed 1080x1440 (default)
  python screenshot.py --auto-height # Auto-height (fits content)

Requirements:
  pip install playwright && playwright install chromium
"""
import os, sys, re, glob, argparse

WIDTH = 1080
DEFAULT_HEIGHT = 1440

def find_html():
    """Auto-detect *_xhs_pages.html in the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(script_dir, "*_xhs_pages.html")
    matches = glob.glob(pattern)
    if not matches:
        print("❌ No *_xhs_pages.html found. Please generate the HTML first.")
        sys.exit(1)
    if len(matches) > 1:
        print(f"⚠️ Multiple HTML files found, using the most recent:")
        matches.sort(key=os.path.getmtime, reverse=True)
        for m in matches:
            print(f"  - {os.path.basename(m)}")
    return matches[0]

def count_pages(html_path):
    """Count total pages from data-page attributes in the HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    pages = re.findall(r'data-page="(\d+)"', content)
    if not pages:
        print("❌ No data-page attributes found in HTML. Check the template.")
        sys.exit(1)
    return max(int(p) for p in pages)

def main():
    parser = argparse.ArgumentParser(description="XHS Card Screenshot Generator")
    parser.add_argument("--auto-height", action="store_true",
                        help="Auto-height mode (captures at actual content height)")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright not installed. Run:")
        print("   pip install playwright && playwright install chromium")
        sys.exit(1)

    html_path = find_html()
    total = count_pages(html_path)
    output_dir = os.path.join(os.path.dirname(html_path), "output")
    os.makedirs(output_dir, exist_ok=True)

    file_url = "file:///" + html_path.replace("\\", "/")
    mode = "auto-height" if args.auto_height else f"fixed {DEFAULT_HEIGHT}px"
    print(f"📄 Source:  {os.path.basename(html_path)}")
    print(f"📐 Width:   {WIDTH}px | Height: {mode}")
    print(f"📑 Pages:   {total}")
    print(f"📁 Output:  {output_dir}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for n in range(1, total + 1):
            if args.auto_height:
                # Auto mode: use tall viewport first, then resize to actual height
                page = browser.new_page(viewport={"width": WIDTH, "height": 4000})
                page.goto(file_url)
                page.wait_for_timeout(3000 if n == 1 else 500)
                page.evaluate(f"showPage({n})")
                page.wait_for_timeout(300)
                # Get actual card height
                height = page.evaluate("document.querySelector('.card.active').scrollHeight")
                page.set_viewport_size({"width": WIDTH, "height": height})
                page.wait_for_timeout(200)
            else:
                # Fixed mode
                if n == 1:
                    page = browser.new_page(viewport={"width": WIDTH, "height": DEFAULT_HEIGHT})
                    page.goto(file_url)
                    page.wait_for_timeout(3000)
                page.evaluate(f"showPage({n})")
                page.wait_for_timeout(500)

            out = os.path.join(output_dir, f"{n:02d}.png")
            page.screenshot(path=out, full_page=True)
            print(f"  ✅ {n:02d}.png" + (f" ({height}px)" if args.auto_height else ""))

            if args.auto_height:
                page.close()

        browser.close()

    print(f"\n🎉 Done! {total} card images saved to output/")

if __name__ == "__main__":
    main()
