---
name: harvest-parser-plugin
description: "Use this when defining or reviewing the list-level site parser plugin contract (matches / build_request / parse, router order, Generic fallback) for a regulatory harvest family—before or alongside adapter-codegen."
---

# harvest-parser-plugin

## Purpose

**列表级**站点插件契约：注册顺序、`matches` / `build_request` / `parse`、特化优先、**Generic 兜底**。主责「契约长什么样」；怎么写实现指导归协作方 `adapter-codegen`。

## When to use

- 新站族或新 parser 注册前，冻结插件接口。
- 对照 KaaS ParserRouter 思路迁到监管源族枚举。
- `adapter-codegen` 前先对齐 Runner/插件字段。

## Contract（草案）

```text
matches(source) -> bool
build_request(source) -> RequestSpec   # 可选；可吃备注 curl
parse(fetch_result) -> ExtractedLink[]
```

| 规则 | 说明 |
|------|------|
| 路由顺序 | 特化 parser 在前，**Generic 必须最后** |
| 同族 | 只换 channel / 路径前缀 / Skill 参数，不复制类 |
| ExtractedLink | 至少 `title`、`url`（绝对化）、`published_at?`、`raw?` |
| 备注 curl | 可还原 method/headers/cookies/body，避免站内写死鉴权头 |

## Steps

1. 确认 `family` 枚举或新建族名（与 `skillsmith-reg` 对齐）。
2. 写 `matches` 信号（域、路径、源名、栏目）。
3. 定 `parse` 字段映射与日期推断策略。
4. 声明是否需要 `build_request`（备注含 curl 时建议要）。
5. 登记路由器插入位置（不得压过更特化项；不得去掉 Generic）。
6. Handoff：`adapter-codegen` 按本契约出 diff；金样断言「命中预期 parser 名」。

## Outputs

- 插件契约段落（可写入族知识 / Skill）
- 路由器登记项 checklist

## Forbidden

- 在列表 parser 内硬爬 SPA 详情（改走 `process-content-adapter`）。
- 无 Generic 兜底或把 Generic 插到特化之前。
- 把 MySQL 卷模型写进插件契约。

## 主责 / 协作

| 本 skill | `adapter-codegen` |
|----------|-------------------|
| 契约与路由 | 实现指导与人审 diff |
