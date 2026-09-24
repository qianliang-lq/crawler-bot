---
name: export-query
description: "Use this when exposing the per-instance time-range query API (from/to → articles with content_md) and when exporting filtered articles from the local console/CLI. Downstream consumption is out of scope."
---

# export-query

## Purpose

本 skill = **对外时间窗接口**约定 + 控制台/CLI 导出。

- **默认对外出口**：本实例提供时间窗查询 API（因默认 SQLite，外部系统靠调此接口对接）。
- **保留**：控制台 / CLI 按筛选导出 CSV/JSON/JSONL。
- **边界**：只保证「按时间取出」；**下游消费出圈**（导入法规库、二次加工、推送编排均不属于本爬虫机器人）。

## 时间窗 API 约定

### 请求

| 项 | 约定 |
|----|------|
| 方法/路径 | `GET /api/articles?from=ISO8601&to=ISO8601`（亦可 `POST /api/articles` + JSON body：`{"from","to"}`） |
| 必选 | `from`、`to`（ISO8601，建议带时区或约定 Asia/Shanghai） |
| 区间 | **半开** `[from, to)`：含 `from`，不含 `to` |
| 过滤轴 | 默认 `published_at`；若按 `fetched_at` 过滤须在响应 `meta.filter_by` 标明 |
| 可选查询 | `source_id`、`site_id`、`limit` / `offset`（分页约定实现自定） |
| 鉴权 | 本机/内网默认；可挂 `Authorization: Bearer <token>`（只写约定） |

### 响应 schema（草案）

```json
{
  "meta": {
    "from": "2026-09-01T00:00:00+08:00",
    "to": "2026-09-24T00:00:00+08:00",
    "filter_by": "published_at",
    "count": 2
  },
  "articles": [
    {
      "title": "…",
      "published_at": "2026-09-10T10:00:00+08:00",
      "content_md": "…",
      "url": "https://…",
      "source_id": "csrc-szzyb-0599",
      "fetched_at": "2026-09-10T12:00:00+08:00"
    }
  ]
}
```

亦可直接返回数组（无 `meta` 包装）；元素字段要求不变。

| 级别 | 字段 |
|------|------|
| **必选** | `title`、`published_at`（或别名 `date`）、`content_md` |
| **建议** | `url`、`source_id`、`fetched_at` |
| **可选** | `site_id`、`intake_batch_id`、`attachments`、`content_hash`、`manuscript_id` / `penalty_doc_no` |

### 与 SQLite 字段映射

| API 字段 | 表 `crawl_article` 列 |
|----------|----------------------|
| `title` | `title` |
| `published_at` / `date` | `published_at` |
| `content_md` | `content_md` |
| `url` | `url` |
| `source_id` | `source_id` |
| `fetched_at` | `fetched_at` |
| `site_id` | `site_id` |
| `intake_batch_id` | `intake_batch_id` |
| `attachments` | `attachments`（JSON 字符串 → 解析为数组） |

查询示例（示意，非生产代码）：

```sql
SELECT title, published_at, content_md, url, source_id, fetched_at
FROM crawl_article
WHERE published_at >= :from AND published_at < :to
ORDER BY published_at ASC;
```

## 控制台 / CLI 导出（保留）

最小导出字段：  
`title, published_at, url, content_md, source_id, site_id, intake_batch_id, fetched_at, attachments`

绑定：`localhost:3000` 导出按钮 / `scripts/export.py`。

## 可选 MQ（定义位，不强迫实现）

消息体字段建议与 API 元素对齐（至少 `title` / `published_at` / `content_md` / `url` / `source_id`）。规约写清即可，M0 不强做。

## 禁止 / 出圈

- 不在本 skill 内实现下游法规库导入、摘要、对外再分发。
- 不默认把监管原文送到第三方 SaaS。
- 不把 MQ 当成 M0 必选项。

## Status

约定已加厚；实现落在项目骨架（web + sqlite），由 OpenClaw 机器人按方法论生成/演进。
