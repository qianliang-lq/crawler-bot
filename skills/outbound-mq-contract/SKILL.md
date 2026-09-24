---
name: outbound-mq-contract
description: "Use this when optionally enabling outbound MQ insert for harvested articles: freeze payload shape, validation, truncation, and one-message-one-article rules. Default implementation is off; time-range API remains the primary export."
---

# outbound-mq-contract

## Purpose

**可选出仓**：MQ insert 的形状、校验、截断、一消息一文。监管源**默认关闭实现**；契约保留。默认对外出口仍是 `export-query` 时间窗 API。

## When to use

- `product_brief.yaml` 中 `outbound_mq: true`。
- 对接方要求推送而非只拉 API。
- 评审 MQ 字段是否与 API 元素对齐。

## Contract（草案）

| 规则 | 约定 |
|------|------|
| 粒度 | **一消息一文**；`externalData` 长度恒为 **1** |
| 发送前 | `validate_*_payload` 失败 → 跳过并计数（可观测），默认不阻断整批（策略可在 brief 改） |
| 正文 | 过短拒绝；超限**截断**并打标 |
| 时间 | `infoDt` / 发布时刻格式写死（与实例时区一致） |
| 与 API | 字段应对齐 `title` / url / published_at / `content_md`（MQ 侧可换名，映射表必写） |

顶层示意（名称可按对接方改，**校验规则不能糊**）：

```text
kbId, tenantId, opType, externalData[1], batchNo
行内: title, media, originlUrl, infoDt, content, ext…
```

## Steps

1. 确认 brief 启用 MQ；否则本 skill 只文档、不接线。
2. 冻结字段映射表与校验清单。
3. 金样：故意过短 / 超长 / externalData≠1 → 可观测失败。
4. `ops-daily-status` 计入 `mq_synced` / `mq_skipped`。

## Outputs

- MQ 契约文档段落 + 校验 checklist

## Forbidden

- 未确认 brief 就实现并默认开启。
- 一条消息塞多文。
- 用 MQ **替换**时间窗 API 作为唯一出口（API 须保留为默认）。

## 主责 / 协作

| `export-query`（主） | 本 skill（次） |
|----------------------|----------------|
| 时间窗 API + 控制台导出 | 可选 MQ |
