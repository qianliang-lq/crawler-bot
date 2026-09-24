---
name: console-ops-pages
description: "Use this when scaffolding or reviewing the six-page ops console information architecture (dashboard, tasks, history, articles, sources, config) and its API alignment for a full regulatory harvester project shell."
---

# console-ops-pages

## Purpose

**完整项目壳**的六页信息架构与 API 对齐清单。实现可为 Streamlit / 其他；本 skill 管「页有什么、调什么」，并与 `export-query` / `scheduler-incremental` / `ops-daily-status` 协作构成可运维壳。

## When to use

- `product-brief-confirm` 冻结后生成整站前端。
- 对照 KaaS 六页截图做监管源最小集。
- 验收「没有六页就不算免调试」。

## 六页最小集

| 页 | 职责 | 主要 API / 数据 |
|----|------|-----------------|
| 整体看板 | 磁盘/库占用、当前 run、pipeline 总览、最近日报 | storage stats、run 轮询、`ops-daily-status` |
| 任务管理 | 选源启动采集/全流程；增量跳过已知 URL | harvest/pipeline run |
| 任务详情 | 历史 execution、文档预览、批量删 | runs / docs preview |
| 文章明细 | 筛选、时间窗、质检状态、批量删 | 文章查询（可与时间窗 API 同源） |
| 数据源 | Excel 导入、按源/行改删、parser/族标签 | intake + sources CRUD |
| 配置 | API 基址、并发、**每日定时** CRUD、MQ 开关只读/可配 | schedules、runtime config |

## Steps

1. 按 `product_brief.yaml`.`features.console_pages` 生成/核对页面清单。
2. 每页列出只读 vs 写操作；写操作须二次确认（删源、批量删文）。
3. 对齐限速提示文案（0.2–0.5 rps）。
4. 配置页定时与 `scheduler-incremental`「先打标再执行」一致。
5. 文章/导出与 `export-query` 字段一致。

## Outputs

- 六页 IA checklist + API 对齐表（可进项目 README）

## Forbidden

- 缺页却宣称完整项目。
- 数据源删除默认级联清空历史 run（除非 brief 明示）。
- 在控制台暴露密钥明文。

## 主责 / 协作

| 本 skill | 协作 |
|----------|------|
| 六页 IA + API 对齐 | `export-query` 出口；`scheduler-incremental` 定时；`ops-daily-status` 日报；脚手架生成时可并入本 skill 清单 |
