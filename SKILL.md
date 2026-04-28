---
name: md-poster
description: |
  将 Markdown 文章自动排版成小红书/社交媒体图文卡片。
  输入 Markdown 正文 → 自动分页 → 生成 HTML → Playwright 截图 → 输出 PNG 图片。
  触发词：「排版成图文」「生成小红书卡片」「做图文切割」「XHS card」「生成 xhs_pages」。
---

> 「排版不应该比写作更难。」—— 这套系统让你 30 秒出 8 张卡片。

## 核心能力

将 Markdown 文本自动转换为精美的小红书图文卡片，具体包括：
- **Markdown 解析**：H1/H2/段落/加粗/列表/表格/代码块 → HTML
- **分页引擎**：按行号区间自动切分为多页卡片
- **CSS 设计系统**：米白底 + 思源宋体 + 1080px 宽度，开箱即用
- **截图自动化**：Playwright 无头浏览器逐页截图为 PNG

## 工作流

### Phase 0: 需求确认

收到用户请求后，确认以下信息：

| 信息 | 说明 | 默认值 |
|------|------|--------|
| 源文件 | Markdown 正文路径 | 当前目录下的 .md 文件 |
| 文章标题 | 卡片第 1 页显示的大标题 | 从 Markdown H1 提取 |
| 作者名 | 作者区域显示名 | 用户自定义 |
| 日期 | 发布日期 | 今天 |
| 总页数 | 计划分几页 | 根据字数估算（每页 700-800 字） |
| 头像路径 | 作者头像图片路径 | `avatar.jpg` |

### Phase 1: 分页规划

**规则**：
- 每页目标 **700-800 字**，页面高度约 2000px
- 最多 **8 页正文**（小红书上限 9 张图 = 1 封面 + 8 正文）
- 在**自然断点**处分页（段落之间、章节标题前）
- 第 1 页必须包含：标题 + 作者区域 + 开头 Hook
- 最后一页可以稍短

**操作**：
1. 读取源 Markdown 文件
2. 确定每页的行号范围 `(start_line, end_line)`
3. 记录到 `PAGES` 配置数组

### Phase 2: 生成 HTML

生成 `xhs_pages.py` 脚本，该脚本：
1. 读取源 Markdown 文件
2. 按 `PAGES` 配置提取每页内容
3. 将 Markdown 转换为 HTML（`md_to_html()` 函数）
4. 套用 CSS 设计系统模板
5. 输出完整的多页 HTML 文件

**CSS 设计系统核心参数**：

| 参数 | 值 |
|------|------|
| 卡片宽度 | `1080px` |
| 背景色 | `#F9F9F6`（米白） |
| 正文字体 | `Noto Serif SC`（思源宋体） |
| 正文字号 | `34px`，行高 `2.0` |
| H1 标题 | `56-60px`，`font-weight: 700` |
| H2 标题 | `44px`，`font-weight: 700` |
| 内边距 | `90px` |
| 分割线色 | `#E8E6D9` |

**Markdown → HTML 支持的元素**：
- `# H1` → `<h1>`（仅第 1 页）
- `## H2` → `<h2>`
- 段落 → `<p>`
- `**加粗**` → `<strong>`
- `*斜体*` → `<em>`
- `` `代码` `` → `<code>`
- `- 无序列表` → `<ul><li>`
- `1. 有序列表` → `<ul><li>`
- 表格 → `<table>`
- ` ``` 代码块 ``` ` → `<pre><code>`

### Phase 3: 截图

运行 `scripts/screenshot.py` 自动截图：

```bash
# 固定高度 1080×1440（3:4 比例）
python scripts/screenshot.py

# 自适应高度（按内容实际高度）
python scripts/screenshot.py --auto-height
```

**截图脚本自动处理**：
- 自动查找 `*_xhs_pages.html` 文件
- 等待 Google Fonts 加载（首页 3 秒）
- 清除浏览器扩展覆盖层（蓝色边框）
- 逐页截图输出到 `output/` 目录

---

## 踩坑铁律

> 以下是 23+ 篇文章生产中积累的血泪教训。

| # | 铁律 | 原因 |
|---|------|------|
| 1 | **使用 headless 模式** | 非 headless 模式会渲染浏览器扩展的蓝色边框 |
| 2 | **首页等 3 秒** | Google Fonts（思源宋体）需要加载时间 |
| 3 | **不要用 `python -c` 内联命令** | Windows 路径含单引号会被 PowerShell 吞掉 |
| 4 | **页脚放在 `.content` 内部** | 放在外面会被截图裁切 |
| 5 | **隐藏所有滚动条** | 需要 CSS 三重覆盖（`overflow:hidden` + `-ms-overflow-style:none` + `::-webkit-scrollbar`） |
| 6 | **不要让 AI 直接输出 HTML** | 中文 token 约为英文 2-3 倍，5000 字正文 HTML 会被截断。让 AI 写 Python 生成器脚本 |
| 7 | **超 8 页时增大每页字数** | 不要删内容，增加页面高度 |

---

## 文件引用

| 文件 | 用途 |
|------|------|
| `templates/xhs_card_template.html` | 手动编辑时使用的 HTML 模板 |
| `scripts/screenshot.py` | 通用截图脚本 |
| `examples/basic/xhs_pages.py` | 生成器脚本参考实现 |
| `docs/design-system.md` | CSS 设计系统详细文档 |
| `docs/troubleshooting.md` | 完整踩坑记录 |

---

## 诚实边界

- 本系统**不会**帮你写文章内容——它只管排版
- 本系统**不会**自动分页——你需要手动指定每页的行号范围
- 本系统**不会**处理图片插入——卡片目前为纯文字排版
- CSS 样式针对中文优化——英文排版可能需要微调字号和行高
- 需要本地安装 Python + Playwright，非零门槛

---

> 本 Skill 由 [多少做点 BILL DO A BIT](https://x.com/BillDoABit) 创建
> 基于 23+ 篇正式文章的生产经验迭代
