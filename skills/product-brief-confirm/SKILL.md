---
name: product-brief-confirm
description: "Use this when the user wants to crawl a batch of regulatory URLs (or uploads Excel) and you must produce a product brief with feature list + wireframe image tasks, Ask User questions, and freeze scope into product_brief.yaml before generating the full site or deploying."
---

# product-brief-confirm

## Purpose

批次级**产品闸门**：用户说要爬某一批 URL / 上传 Excel 后，Agent **先**出产品方案与配图任务 → **Ask User Question** 确认 → 冻结范围写入 `product_brief.yaml`，供后续 skills 消费。

**未确认前禁止**：生成整站代码、调用 `pod-deploy`。

## When to use

- 用户给出一批 URL，或上传监管源 Excel。
- 新批次 / 新 OpenClaw 实例立项。
- 用户说「帮我做这个采集站 / 整站」但尚未确认功能范围。

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| `batch_hint` | yes | URL 列表摘要，或 Excel 路径 / 行数 / 机构域 |
| `user_constraints` | no | 口头约束（只要 API、不要 MQ、部署环境等） |
| `prior_product_brief` | no | 同实例修订时的旧 `product_brief.yaml` |

## Steps

1. **摘要批次**：机构数 / URL 数 / 已知站族线索 / 备注里的禁爬范围（只读，不抓站）。
2. **写产品方案**（功能清单，映射六页 + 壳能力）：
   - 六页控制台：整体看板、任务管理、任务详情、文章明细、数据源、配置
   - 定时增量、本机 SQLite（一实例一库）、时间窗 API（默认出仓）
   - 可选 MQ、日报（`ops-daily-status`）
   - **明确出圈**：下游法规库/知识库消费不属于本站
3. **配图任务卡**（至少 3 张；本 skill **规定画什么**，图由草图 skill/设计师生成）：
   - 整体看板
   - 任务管理
   - 文章明细（或数据源）
   - 详见 MECE 文 §7；向用户展示草图或线框说明，勿空等真图阻塞确认
4. **Ask User Question**（必问项）：
   - [ ] 是否启用 MQ？（默认否）
   - [ ] 定时时刻 `time_of_day`（及时区 Asia/Shanghai）
   - [ ] 限速（建议 0.2–0.5 rps）是否接受
   - [ ] 是否只要时间窗 API（控制台导出是否保留）
   - [ ] 备注约束是否已理解（禁爬栏目 / 文号去重 / 附件形态等）
   - [ ] 部署目标 Pod 环境（标签 / 命名空间约定）
5. **闸门**：用户微调确认前 → 停；确认后 → 写 `product_brief.yaml`。
6. **Handoff**：下一步 `intake-excel`（若尚未 tickets）或按冻结范围继续 L1–L5。

## Outputs

### `product_brief.yaml` 字段草案

```yaml
brief_id: pb_YYYYMMDD_HHmmss_short
intake_batch_id: null          # intake-excel 后回填
created_at: ISO8601+08:00
status: confirmed             # draft | confirmed | superseded
batch_summary:
  url_or_row_count: 0
  org_domains: []             # 财富 / 支付 / …
  known_families: []          # csrc_search_list / …
features:
  console_pages: [dashboard, tasks, history, articles, sources, config]
  scheduler_incremental: true
  sqlite_local: true
  export_time_range_api: true   # 默认出仓
  console_export: true
  outbound_mq: false            # 用户确认
  ops_daily_status: true
out_of_scope:
  - downstream_kb_ingest
  - third_party_saas_repost
runtime:
  rate_limit_rps: 0.3
  schedule_time_of_day: "02:00"
  timezone: Asia/Shanghai
deploy:
  target: openclaw_pod
  env_label: ""                 # 用户填写
wireframes:
  - id: dashboard
    status: tasked              # tasked | ready | skipped
  - id: tasks
    status: tasked
  - id: articles
    status: tasked
user_answers: {}                # Ask User 原始答复
frozen_at: ISO8601+08:00
```

## Forbidden

- 未 `status: confirmed` 前生成整站脚手架 / Adapter 生产代码 / `pod-deploy`。
- 把下游知识库入库画进功能清单。
- 静默默认开启 MQ。
- 忽略 Excel 备注禁爬范围。

## Handoff

- 确认后 → **`intake-excel`**（或已有 tickets 则 `probe-site`）。
- 协作：`skillsmith-reg` 只定单站采什么；本 skill 定整站产品与 UI。
- 对照：`/workspace/briefs/2026-09-24-reg-source-skills-mece-cognition.md`
