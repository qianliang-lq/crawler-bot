---
name: ops-daily-status
description: "Use this when defining or emitting the daily pipeline status report (trigger mode, window, source counts, link/process/MQ stats, execution state) for a regulatory harvester instance."
---

# ops-daily-status

## Purpose

全流程**日报**字段、通知文案、execution 状态机。让运维看见「今日跑没跑、成败几何」，避免免调试只停在开发者本机。

## When to use

- 项目壳含定时全流程时，定日报 schema。
- Pipeline 结束（成功/部分失败/空跑）需可读摘要。
- 控制台看板「最近日报」入口。

## 日报字段（最小集）

| 字段 | 说明 |
|------|------|
| `triggered_by` | schedule / manual / api |
| `window` | 业务日或 `[from,to)` |
| `sources_total` / `sources_ok` / `sources_fail` | 源计数 |
| `links_valid` | 有效链 |
| `process_ok` / `process_anomaly` / `process_fail` | 预处理 |
| `mq_synced` / `mq_skipped` | 仅启用 MQ 时 |
| `status` | success / partial / failed / skipped_empty |
| `message` | 人话一句（无有效链 / MQ 未配置等不空转） |

## Steps

1. Pipeline 结束调用本约定生成 `daily_status` 对象。
2. 写 `ops_daily_status` 表或日志文件（SQLite / 本地 JSON，实现自定）。
3. 可选通知通道（邮件/群）只发摘要，**不默认外送正文**。
4. 看板展示最近 N 条；失败可一键跳任务详情。

## Outputs

- `daily_status` JSON + 可选纯文本通知稿

## Forbidden

- 无有效链仍假装 success 且无 `skipped_empty`。
- 日报里贴上全文 `content_md`。
- 未配置 MQ 时空转重试刷屏。

## Handoff

- 协作 `scheduler-incremental`（先打标再执行）；`console-ops-pages` 看板消费本字段。
