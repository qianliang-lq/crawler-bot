# 监管源采集数字员工 · Skills 包（AI 主调用链）

> 落盘：`/workspace/briefs/reg-source-crawler-skills/`  
> 对齐方案：`/workspace/briefs/2026-09-24-reg-source-crawler-digital-employee-proposal.md` **v1.3**  
> 日期：2026-09-24（Asia/Shanghai）  
> 受众：OpenClaw/Agent 运行时 + 精细代码助手（仓内实现）

本目录是 **可交接的技能契约与步骤说明书**，不是完整员工仓库。仓库脚手架、Adapter 真代码、SQLite schema 由队友「精细代码助手」合入。

## 技能清单

### M0 主调用链（AI 优先）

| # | Skill 目录 | 一句话 |
|---|------------|--------|
| 1 | `intake-excel/` | Excel（URL/title/备注）→ source tickets + `intake_batch_id` |
| 2 | `probe-site/` | 打开入口，判页型/族；CSRC 空壳 + 推导 searchList；写侦察报告 |
| 3 | `skillsmith-reg/` | 侦察报告 → `sites/<slug>/SKILL.yaml` |
| 4 | `adapter-codegen/` | 生成/修改族 Adapter 的指导与伪代码（人审 diff） |
| 5 | `detail-to-markdown/` | 详情 HTML/PDF 文本 → `content_md` 清洗约定 |
| 6 | `golden-test/` | 金样试跑检查清单 |

### 次优先骨架

| Skill | 状态 |
|-------|------|
| `scheduler-incremental/` | 骨架 |
| `pdf-extract/` | 骨架（AMAC 处罚 M0 腿） |
| `export-query/` | 骨架 |

每个 skill 含 `SKILL.md`（YAML frontmatter: `name`, `description`「use this when…」+ 步骤/IO/禁止项）。

## 推荐调用顺序（与 v1.3 §3 旅程对齐）

```text
intake-excel
    → probe-site（逐 ticket；限速 0.2–0.5 rps）
        → skillsmith-reg（人确认 Skill 定稿）
            → adapter-codegen（人确认 diff）
                → detail-to-markdown（Adapter 内调用）
                    → golden-test
                        → scheduler-incremental（Canary 后）
```

控制台导出走 `export-query`；PDF 族详情走 `pdf-extract` → `detail-to-markdown`。

## 与 v1.3 方案对齐要点

- Intake：**Excel 为主**，不再默认粘贴裸 URL。
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
| `/workspace/briefs/2026-09-24-reg-source-crawler-digital-employee-proposal.md` | v1.3 方案 |
| `/workspace/briefs/reg-crawl-samples/` | 只读抽样 |
| `/workspace/briefs/reg-crawl-experiments/2026-09-24-m0-csrc/` | 本轮实验续写 |
