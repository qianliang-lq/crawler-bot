# 监管源采集数字员工 · Skills 包（AI 主调用链）

> 来源：监管源采集数字员工 Skills 包  
> MECE / 六层认知：[`../docs/mece-cognition.md`](../docs/mece-cognition.md)  
> 日期：2026-09-24（Asia/Shanghai）  
> 受众：OpenClaw/Agent 运行时 + 精细代码助手（仓内实现）

本目录是 **可交接的技能契约与步骤说明书**，不是完整员工仓库。仓库脚手架、Adapter 真代码、SQLite schema 由队友「精细代码助手」合入。

**最终 skill 数：16**（原 9 + KaaS 蒸馏 5 + `product-brief-confirm` + `pod-deploy`）。按**六层生命周期**组织，非扁平并列。


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

## 六层技能清单

### L0 意图与产品闸门

| Skill | 一句话 | 状态 |
|-------|--------|------|
| `product-brief-confirm/` | 批次产品方案 + 配图任务 + Ask User → 冻结 `product_brief.yaml`；未确认禁止整站 / 部署 | **骨架待写→已落骨架** |

### L1 接源与理解

| Skill | 一句话 | 状态 |
|-------|--------|------|
| `intake-excel/` | Excel（URL/title/备注）→ source tickets + `intake_batch_id` | 已有 |
| `probe-site/` | 打开入口，判页型/族；CSRC 空壳 + 推导 searchList；写侦察报告 | 已有 |

### L2 站族规约

| Skill | 一句话 | 状态 |
|-------|--------|------|
| `skillsmith-reg/` | 侦察报告 → `sites/<slug>/SKILL.yaml` | 已有 |
| `harvest-parser-plugin/` | 列表插件契约：`matches`/`build_request`/`parse`、路由顺序、Generic 兜底 | **骨架（新建）** |

### L3 采与洗

| Skill | 一句话 | 状态 |
|-------|--------|------|
| `adapter-codegen/` | 生成/修改族 Adapter 的指导与伪代码（人审 diff） | 已有 |
| `process-content-adapter/` | 详情下载适配：SPA/API→可转 MD 的 HTML | **骨架（新建）** |
| `detail-to-markdown/` | 详情 HTML/PDF 文本 → `content_md` 清洗约定 | 已有 |
| `pdf-extract/` | 附件腿（AMAC 处罚等）→ 文本再进 MD | 骨架 |

### L4 完整项目壳

| Skill | 一句话 | 状态 |
|-------|--------|------|
| `console-ops-pages/` | 六页 IA 与 API 对齐清单 | **骨架（新建）** |
| `scheduler-incremental/` | 日触发打标、已知 URL 跳过、限速 | 骨架 |
| `export-query/` | **默认出仓**：时间窗 API + 控制台导出 | 骨架 |
| `outbound-mq-contract/` | 可选 MQ 契约（默认关实现） | **骨架（新建）** |
| `ops-daily-status/` | 全流程日报字段与通知文案 | **骨架（新建）** |

### L5 验收与上线

| Skill | 一句话 | 状态 |
|-------|--------|------|
| `golden-test/` | 金样试跑检查清单 | 已有 |
| `pod-deploy/` | OpenClaw Pod：镜像/卷/密钥/健康检查/回滚 checklist | **骨架（新建）** |

每个 skill 含 `SKILL.md`（YAML frontmatter: `name`, `description`「use this when…」+ 步骤/IO/禁止项）。

## 用户可见主链路（含确认闸门）

```text
批次 URL / Excel
  → product-brief-confirm（产品方案 + 配图 + Ask User → 冻结范围）
    → intake-excel → probe-site → skillsmith-reg
      → harvest-parser-plugin / adapter-codegen / process-content-adapter
        → detail-to-markdown（± pdf-extract）→ golden-test
          → 生成完整项目（console-ops-pages + scheduler + export-query + ops-daily-status）
            → 本地/试跑通过 → pod-deploy
              → （可选）outbound-mq-contract
```

硬闸门：未确认 `product_brief.yaml` 前，禁止生成整站代码、禁止 `pod-deploy`。

`export-query` = **对外时间窗接口**（`from`/`to` → 文章含 `content_md`）+ 控制台导出；PDF 族详情走 `pdf-extract` → `detail-to-markdown`。

## 与 v1.3 方案对齐要点

- Intake：**Excel 为主**，不再默认粘贴裸 URL；**先产品方案确认**。
- 族分类：`csrc_search_list` / `amac_penalty_pdf` / `amac_gov_rules` / `neris` / `unknown`。
- CSRC：`common_list` 壳页空列表；稳态 **`CsrcSearchListAdapter` + HTTP JSON**；同 Adapter 只换 `channelid` + 路径前缀。
- 详情正文主格式：**Markdown → SQLite `content_md`**；一 Pod 一库。
- 合规：限速约 **0.2–0.5 rps**；禁止打码农场；不默认外送原文到第三方 SaaS。

## 示例站点 Skills

- `examples/sites/csrc-szzyb-0599/SKILL.yaml` — 深专员办通知公告  
- `examples/sites/csrc-shzyb-3fde/SKILL.yaml` — 沪专员办通知公告  

实验证明两者同属 `csrc_search_list`：见 `EXPERIMENT-csrc-sz-sh.md`。

## 仓内建议路径（拷贝时）

见 `HANDOFF-to-code-assistant.md`：流程 Skills → 员工仓 `skills/`；示例站点 → `sites/`。

## 相关路径

| 路径 | 用途 |
|------|------|
| [`../docs/mece-cognition.md`](../docs/mece-cognition.md) | MECE + 六层定稿 |
| [`../sites/`](../sites/) | 站点示例配置 |
| [`../HANDOFF.md`](../HANDOFF.md) | 项目交接说明 |
