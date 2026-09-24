# 交接给「精细代码助手」

> 发件：Skills / 实验执行子代理  
> 收件：精细代码助手（仓库写入）  
> 日期：2026-09-24（Asia/Shanghai）  
> **不要**从本交接 git clone 用户仓；由你在既定仓内拷贝/落地。

## 你该拷进仓的东西

| 源（绝对路径） | 建议仓内路径 | 说明 |
|----------------|--------------|------|
| `/workspace/briefs/reg-source-crawler-skills/intake-excel/` | `skills/intake-excel/` | 含 `SKILL.md` |
| `…/probe-site/` | `skills/probe-site/` | |
| `…/skillsmith-reg/` | `skills/skillsmith-reg/` | |
| `…/adapter-codegen/` | `skills/adapter-codegen/` | 伪代码/接口约定，非整仓实现 |
| `…/detail-to-markdown/` | `skills/detail-to-markdown/` | |
| `…/golden-test/` | `skills/golden-test/` | |
| `…/scheduler-incremental/` | `skills/scheduler-incremental/` | 骨架可先拷 |
| `…/pdf-extract/` | `skills/pdf-extract/` | 骨架 |
| `…/export-query/` | `skills/export-query/` | 骨架 |
| `…/examples/sites/csrc-szzyb-0599/` | `sites/csrc-szzyb-0599/` | `SKILL.yaml` + `NOTES.md` |
| `…/examples/sites/csrc-shzyb-3fde/` | `sites/csrc-shzyb-3fde/` | 同上 |
| `…/README.md` | `skills/README.md` 或仓根 `docs/skills.md` | 调用顺序 |
| `…/EXPERIMENT-csrc-sz-sh.md` | `docs/experiments/2026-09-24-csrc-sz-sh.md` | 证据 |

可选 fixtures（只读对照，可放 `tests/fixtures/csrc-szzyb-0599/`）：

- `/workspace/briefs/reg-crawl-samples/csrc_searchList_sample.json`
- `/workspace/briefs/reg-crawl-samples/csrc_sz.html`
- `/workspace/briefs/reg-crawl-samples/csrc_sh.html`
- `/workspace/briefs/reg-crawl-samples/common_list.js`
- `/workspace/briefs/reg-crawl-samples/csrc_detail_sample.html`

## 请你实现的代码侧（本包未提供整文件实现）

1. `adapters/base.py` — `fetch_list` / `fetch_detail` / `run_incremental`
2. `adapters/families/csrc_search_list.py` — **`CsrcSearchListAdapter`**（伪代码见 `skills/adapter-codegen/SKILL.md`）
3. 注册两源到 `config/sources.registry.yaml`，指向上述 `sites/*/SKILL.yaml`
4. SQLite schema 按 v1.3（`content_md`, `intake_batch_id`, …）
5. Runner **强制** `rate_limit` 0.2–0.5 rps；URL 协议相对路径规范化
6. 金样测试：离线优先吃 `csrc_searchList_sample.json`；在线需稳定出口（本 box 今日 WAF/TLS 不稳）

## 不要做的事

- 不要为沪办再 fork 一套 Adapter 类。
- 不要把壳页 DOM 当列表源。
- 不要绕 WAF/打码；失败升 headed 或换执行面。
- 不要改本 briefs 目录作为「正本仓」——正本在你管理的 git 仓。

## 验收目光检

- [ ] 六主 skill 的 `SKILL.md` 在仓内可被 Agent 发现  
- [ ] 两份 site `SKILL.yaml` 人可读；`family` 均为 `csrc_search_list`  
- [ ] Adapter 单测：同一类加载两套 params 能构建正确 API URL  
- [ ] 实验文档已链到 PR / docs  

## 方案锚点

`/workspace/briefs/2026-09-24-reg-source-crawler-digital-employee-proposal.md`（v1.3）
