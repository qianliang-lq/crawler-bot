# 交接给「精细代码助手」

> 发件：Skills / 实验执行子代理  
> 收件：精细代码助手（仓库写入）  
> 日期：2026-09-24（Asia/Shanghai）  
> **不要**从本交接 git clone 用户仓；由你在既定仓内拷贝/落地。

## 技能包总览

**16 skills / 六层生命周期**：L0 意图闸门 → L1 接源理解 → L2 站族规约 → L3 采洗 → L4 完整项目壳 → L5 验收上线。

详见 [`skills/README.md`](./skills/README.md) 和 [`docs/mece-cognition.md`](./docs/mece-cognition.md)。

**硬闸门**：未确认 `product_brief.yaml`（L0 `product-brief-confirm`）前，**禁止**生成整站代码、**禁止** `pod-deploy`。

## 仓库已落地内容

### 全部 16 技能（已完成）

| 层 | Skills | 说明 |
|----|--------|------|
| **L0** | `product-brief-confirm/` | 产品方案 + 配图确认闸门 |
| **L1** | `intake-excel/`, `probe-site/` | 接源与侦察 |
| **L2** | `skillsmith-reg/`, `harvest-parser-plugin/` | 站族规约与插件契约 |
| **L3** | `adapter-codegen/`, `process-content-adapter/`, `detail-to-markdown/`, `pdf-extract/` | 采集与清洗 |
| **L4** | `console-ops-pages/`, `scheduler-incremental/`, `export-query/`, `outbound-mq-contract/`, `ops-daily-status/` | 完整项目壳、出仓 API、运维 |
| **L5** | `golden-test/`, `pod-deploy/` | 验收与部署 |

每个 skill 含 `SKILL.md`（YAML frontmatter + 步骤/IO/禁止项）。

### 站点示例

- `sites/csrc-szzyb-0599/` — 深圳证监局通知公告（`SKILL.yaml` + `NOTES.md`）
- `sites/csrc-shzyb-3fde/` — 上海证监局通知公告

实验证明两者同属 `csrc_search_list` 族：见 [`docs/experiments/2026-09-24-csrc-sz-sh.md`](./docs/experiments/)。

### 文档

- [`docs/mece-cognition.md`](./docs/mece-cognition.md) — MECE + 六层完整认知体系
- [`docs/experiments/`](./docs/experiments/) — CSRC 深圳/上海验证实验

## 请你实现的代码侧（本包未提供整文件实现）

1. **Adapter 基类** — `adapters/base.py`：`fetch_list` / `fetch_detail` / `run_incremental`
2. **族 Adapter** — `adapters/families/csrc_search_list.py`：`CsrcSearchListAdapter`（伪代码见 `adapter-codegen/SKILL.md`）
3. **源注册** — `config/sources.registry.yaml`：注册两源到 `sites/*/SKILL.yaml`
4. **SQLite schema** — 按 v1.3（`content_md`, `intake_batch_id`, `source_id`, `discovered_at`, …）
5. **Runner** — 强制 `rate_limit` 0.2–0.5 rps；URL 协议相对路径规范化；增量打标
6. **金样测试** — 离线优先读 fixtures；在线需稳定出口

**注意**：本仓库**不包含**生产 Adapter 完整实现、SQLite runner、或生产爬虫代码，仅提供技能契约与伪代码指导。

## 不要做的事

- **不要**为沪办再 fork 一套 Adapter 类（同族只换 params）。
- **不要**把壳页 DOM 当列表源（CSRC 空列表是设计）。
- **不要**绕 WAF/打码农场（见方案 v1.3 合规约束）。
- **不要**在未确认 `product_brief.yaml` 前生成整站或部署。
- **不要**改本交接目录作为「正本仓」（正本在你管理的 git 仓）。

## 验收目光检

- [ ] 所有 16 技能的 `SKILL.md` 在 `skills/` 目录下可被 Agent 发现
- [ ] 两份 site `SKILL.yaml` 人可读；`family` 均为 `csrc_search_list`
- [ ] Adapter 单测：同一类加载两套 params 能构建正确 API URL
- [ ] 实验文档已链到 PR / docs
- [ ] 根 README 展示六层生命周期表和主链路

## 方案锚点与约束

- **六层生命周期** — 16 skills 按 L0–L5 组织，非扁平并列
- **硬闸门** — `product-brief-confirm` 必须在整站生成 / 部署前完成
- **对齐方案 v1.3** — Excel intake、详情 Markdown→SQLite `content_md`、限速 0.2–0.5 rps、禁打码、禁默认外送原文
- **默认出仓** — 时间窗 API (`export-query`)；MQ (`outbound-mq-contract`) 可选

---

完整技能清单与调用链见 [`skills/README.md`](./skills/README.md)。
