---
name: process-content-adapter
description: "Use this when a detail page is SPA or API-backed and you must adapt download to HTML that the shared HTML→Markdown path can consume—without polluting list parsers."
---

# process-content-adapter

## Purpose

**详情下载适配**：当普通 GET HTML 不够（SPA / 接口详情）时，在**下载层** `matches(url) → fetch_html`，产出可进通用 `detail-to-markdown` 的 HTML。不污染列表 parser。

## When to use

- 侦察显示详情为前端路由壳、正文在 JSON API。
- 金样失败原因是「导航壳 / 空正文」且根因是未打对详情 API。
- 与 `pdf-extract` 并列：本 skill 管 HTML 腿；PDF 附件另腿。

## Contract（草案）

```text
matches(url) -> bool
fetch_html(url, ctx) -> html_str   # 可先打 JSON 再包成 HTML
```

- 输出 HTML 须含可抽取主标题与正文容器，供 `detail-to-markdown` 质量门。
- 站点特例（缺标题策略）写在 Adapter/Skill 备注，不改通用转换默认。

## Steps

1. 确认列表 parser 只产出详情 URL，不内嵌详情爬取。
2. 定 API 形状与包 HTML 模板（最小：`<article><h1>…</h1><div class="body">…</div></article>`）。
3. 编码兜底与限速沿用实例配置。
4. 交 `detail-to-markdown` → 质量门（空 / 登录墙 / 过短 / 导航壳）。
5. 金样：SPA 站必须命中本 adapter 名，而非 generic GET。

## Outputs

- content_adapter 契约段落 + 样例 URL→HTML 说明（无生产长代码）

## Forbidden

- 在 `harvest-parser-plugin` / 列表 Adapter 里拧详情 JSON。
- 绕过质量门直接标 success。
- 默认外送原文到第三方 SaaS。

## 主责 / 协作

| 本 skill | `detail-to-markdown` | `pdf-extract` |
|----------|----------------------|---------------|
| 如何拿到可转 HTML | HTML/文本→`content_md` | 附件→文本再进 MD |
