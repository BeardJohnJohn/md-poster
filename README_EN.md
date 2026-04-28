# 📸 MD Poster

**Turn Markdown articles into beautiful Xiaohongshu (小红书) image cards using HTML + CSS + Playwright.**

3 steps. 30 seconds. Battle-tested on **23+ published articles**.

[中文 README](README.md)

---

## What It Does

```
Markdown → Python script → HTML + CSS → Playwright screenshot → PNG images
```

| | Manual Tools (Canva/PS) | MD Poster |
|---|---|---|
| **Consistency** | Manual every time | CSS locks it in |
| **Speed** | 8 pages ≈ 2 hours | 8 pages ≈ 30 seconds |
| **Maintainability** | Redo all images for style change | Change 1 CSS line |
| **AI-friendly** | AI can't drag-and-drop | AI writes code natively |

---

## Quick Start

```bash
# 1. Install
pip install playwright && playwright install chromium

# 2. Generate HTML
cd examples/basic && python xhs_pages.py

# 3. Screenshot
python ../../scripts/screenshot.py --auto-height
```

Your image cards are in `output/` 🎉

---

## How It Works

1. **Write** your article in Markdown
2. **Configure** page splits in `xhs_pages.py` (line ranges for each page)
3. **Run** the script → generates multi-page HTML with embedded CSS design system
4. **Screenshot** → Playwright captures each page as a PNG at 1080px width

### Design System

| Parameter | Value |
|-----------|-------|
| Card width | 1080px (Xiaohongshu native) |
| Background | `#F9F9F6` (warm cream) |
| Body font | Noto Serif SC (Chinese serif) |
| Body size | 34px, line-height 2.0 |
| Headings | H1: 56px, H2: 44px |
| Padding | 90px |

### AI-Powered Workflow

You don't even need to write code. Send your Markdown + `SKILL.md` to any AI (ChatGPT/Claude/Gemini):

> "Based on this SKILL.md, generate a xhs_pages.py script to turn this article into Xiaohongshu image cards."

The AI will generate a complete working script. Just run it.

---

## Repository Structure

```
md-poster/
├── README.md / README_EN.md    # Documentation
├── SKILL.md                     # AI instruction manual
├── scripts/
│   ├── screenshot.py            # Universal screenshot script
│   └── setup.sh                 # One-click setup
├── templates/
│   └── xhs_card_template.html   # Editable HTML template
├── examples/
│   ├── basic/                   # Runnable example
│   └── real-output/             # Real production samples
└── docs/
    ├── design-system.md         # CSS system docs
    ├── methodology.md           # Why HTML > Canvas
    └── troubleshooting.md       # Gotchas & fixes
```

---

## Common Gotchas

| Issue | Fix |
|-------|-----|
| Blue border in screenshots | Use headless mode (default); JS cleanup is built-in |
| Fonts not loaded | First page waits 3s (handled in script) |
| Over 8 pages | Increase content per page, don't cut content |

---

## About

**Do A Bit 多少做点** — AI-augmented content creator

- 🐦 X: [@Bill_Do_A_Bit](https://x.com/Bill_Do_A_Bit)
- 📕 Xiaohongshu: Do A Bit 多少做点
- 💬 Signal: Billdoabit
- 📧 Email: bill.jjxu@gmail.com

MIT License © [Do A Bit 多少做点](https://github.com/BeardJohnJohn)
