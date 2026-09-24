# crawler-bot

监管源采集数字员工（M0）技能与站点配置仓库。

## 六层生命周期总表

| 层 | 名称 | Skills |
|----|------|--------|
| **L0** | 意图与产品闸门 | `product-brief-confirm` |
| **L1** | 接源与理解 | `intake-excel` → `probe-site` |
| **L2** | 站族规约 | `skillsmith-reg` + `harvest-parser-plugin` |
| **L3** | 采与洗 | `adapter-codegen` + `process-content-adapter` + `detail-to-markdown` + `pdf-extract` |
| **L4** | 完整项目壳 | `console-ops-pages` + `scheduler-incremental` + `export-query` + `outbound-mq-contract`(可选) + `ops-daily-status` |
| **L5** | 验收与上线 | `golden-test` → `pod-deploy` |

**16 skills**；按生命周期组织，非扁平并列。硬闸门：未确认 `product_brief.yaml` 前禁止生成整站、禁止 `pod-deploy`。默认出仓为时间窗 API；MQ 可选。

## 用户可见主链路

```text
批次 URL / Excel
  → product-brief-confirm（产品方案 + 配图 + Ask User → 冻结范围）
    → intake-excel → probe-site → skillsmith-reg
      → harvest-parser-plugin / adapter-codegen / process-content-adapter
        → detail-to-markdown（± pdf-extract）→ golden-test
          → 生成完整项目（console-ops-pages + scheduler + export-query + ops-daily-status）
            → 本地/试跑通过 → pod-deploy
              →（可选）outbound-mq-contract
```

**硬闸门**：`product-brief-confirm` 未确认前，**禁止**生成整站代码、**禁止** `pod-deploy`。

## 仓库结构

- **技能目录**：[`skills/`](./skills/) — 完整 16 技能详细说明
- **站点示例**：[`sites/`](./sites/) — CSRC 等站点配置示例
- **交接说明**：[`HANDOFF.md`](./HANDOFF.md) — 项目交接与约束
- **实验记录**：[`docs/experiments/`](./docs/experiments/) — CSRC 深圳/上海验证实验
- **MECE 认知**：[`docs/mece-cognition.md`](./docs/mece-cognition.md) — 六层完整认知体系

## 约束对齐

对齐方案 v1.3：Excel intake、详情 Markdown→每实例 SQLite、限速 0.2–0.5 rps、禁打码、禁默认外送原文。
