# 踩坑记录 & 常见问题

这些问题都是在实际生产 23+ 篇文章过程中遇到并解决的。

## 1. 截图出现蓝色边框/光晕

**症状**：Playwright 截图的图片四周有蓝紫色光晕或边框。

**原因**：Chromium 浏览器的 Shadow DOM（通常来自浏览器扩展）会在页面四周渲染覆盖层。

**解决方案**：截图前执行 JS 清理脚本（已内置在 `xhs_pages.py` 的截图流程中）：

```javascript
// 遍历所有元素，清除 outline/boxShadow
document.querySelectorAll('*').forEach(el => {
    el.style.outline = 'none';
    el.style.boxShadow = 'none';
    el.style.filter = 'none';
});
// 清空所有 Shadow DOM
document.querySelectorAll('html *').forEach(el => {
    if (el.shadowRoot) { el.shadowRoot.innerHTML = ''; }
});
```

**预防**：使用 `headless=True` 模式启动 Playwright（默认设置），headless 模式天生没有浏览器扩展覆盖层。

---

## 2. 滚动条出血

**症状**：截图边缘出现灰色滚动条轨道。

**原因**：某些 Chromium 版本即使设置了 `overflow: hidden` 仍会渲染滚动条。

**解决方案**：CSS 三重覆盖：

```css
html, body {
    overflow: hidden;
    -ms-overflow-style: none;        /* IE/Edge */
    scrollbar-width: none;           /* Firefox */
}
html::-webkit-scrollbar,
body::-webkit-scrollbar {
    display: none;                   /* Chrome/Safari */
}
```

---

## 3. 中文长文 Token 溢出

**症状**：让 AI 直接输出 5000+ 字的完整 HTML 时，输出被截断。

**原因**：中文字符的 token 成本约为英文的 2-3 倍，5000 字中文 HTML 可能超过 AI 的输出 token 上限 (16K)。

**解决方案**：不要让 AI 直接输出静态 HTML。让 AI 写一个 ~200 行的 Python 生成器脚本（`xhs_pages.py`），脚本读取源 Markdown → 按行号分页 → 输出完整 HTML。

---

## 4. 页脚被截断

**症状**：截图后页脚不可见或只显示一半。

**原因**：`.page-footer` 放在了 `.card` 的直接子元素位置，而非 `.content` 内部。

**解决方案**：确保 `.page-footer` 在 `.content` div **内部**，并加足够的底部内边距：

```css
.page-footer {
    margin-top: 50px;
    padding: 24px 0 50px 0;  /* 50px 底部内边距 */
}
```

---

## 5. Google Fonts 加载慢

**症状**：截图时字体还没加载完，显示为默认宋体/黑体。

**解决方案**：
- 第一页截图前等待 3000ms（`page.wait_for_timeout(3000)`）
- 后续页面等待 500ms 即可（字体已缓存）

---

## 6. 路径中含特殊字符（单引号/空格/中文）

**症状**：Windows PowerShell 中执行包含特殊字符（如 `O'Brien`、`My Docs`）路径的命令时，报错或路径被截断。

**解决方案**：
- ❌ 不要用 `python -c "..."` 内联命令
- ✅ 写成 `.py` 脚本文件，用 `pathlib.Path` 处理路径

---

## 7. 分页超过 8 页

**症状**：小红书图文上限 9 张图（1 封面 + 8 正文），文章太长放不下。

**解决方案**：
- ❌ 不要删减内容
- ✅ 增大每页的内容量（提高页面高度）
- 每页目标 700-800 字，页面高度约 2000px
- 如果仍超 8 页，继续增加每页字数
