# 监管源 Skills · MECE 检视 + 完整爬虫站认知体系

> 日期：2026-09-24（Asia/Shanghai）  
> 对照：存量 9 skills + KaaS 蒸馏建议新建 5 + 用户拍板确认闸门 / Pod 部署  
> 边界：只写认知与契约骨架；不写生产 Adapter；不改 github。

---

## 1. MECE 一句话结论

**存量 9 + KaaS 5 不完全穷尽、不完全独立**：缺「批次产品方案 + 配图确认闸门」「Pod 部署/上线」两块独立认知（项目脚手架可并入 `console-ops-pages` + `export-query`）；若干 skill 有职责重叠，须用「主责 / 协作」划清而非硬删。**合起来可构成「完整做爬虫网站」认知**，但须重组为**六层生命周期**，不是扁平 14 并列。最终建议 **16 skills**（原 9 + KaaS 5 + `product-brief-confirm` + `pod-deploy`）。

---

## 2. MECE 检视表

### 2.1 缺口（不完全穷尽）

| 缺口 | 是否并入已有 | 裁决 |
|------|--------------|------|
| 批次产品方案 + 配图 + Ask User 确认闸门 | 否；`skillsmith-reg` 只管单站采什么 | **独立新建** `product-brief-confirm` |
| 项目脚手架（六页 + 定时 + SQLite + API） | 可并入 | **主责** `console-ops-pages`；`export-query` / `scheduler-incremental` / `ops-daily-status` **协作**出约定 |
| Pod 部署 / 上线 / 回滚 | 否 | **独立新建** `pod-deploy` |

### 2.2 重叠（不完全独立 → 主责 / 协作）

| 重叠对 | 主责 | 协作 | 划界句 |
|--------|------|------|--------|
| `adapter-codegen` ↔ `harvest-parser-plugin` | `harvest-parser-plugin`：列表插件契约（`matches`/`build_request`/`parse`、路由顺序） | `adapter-codegen`：按契约生成/改族 Adapter 的指导与人审 diff | 契约归插件 skill；怎么写实现归 codegen |
| `detail-to-markdown` ↔ `process-content-adapter` ↔ `pdf-extract` | `detail-to-markdown`：HTML/文本→`content_md` + 质量门 | `process-content-adapter`：详情如何拿到可转 HTML（SPA/API→HTML）；`pdf-extract`：附件腿→文本再进 MD | 下载适配 / 附件 / 清洗三腿，出口统一 `content_md` |
| `export-query` ↔ `outbound-mq-contract` | `export-query`：**默认出仓**（时间窗 API + 控制台导出） | `outbound-mq-contract`：**可选** MQ 形状/校验；默认关闭实现 | 同属出仓；主次写死：API 默认、MQ 可选 |
| `skillsmith-reg` ↔ `product-brief-confirm` | `product-brief-confirm`：批次级「整站产品功能与 UI 长什么样」 | `skillsmith-reg`：单站点「采什么」规约 | 产品闸门在前；站族规约在后 |

### 2.3 存量 9 各自仍独立吗？

| Skill | 裁决 |
|-------|------|
| `intake-excel` / `probe-site` / `golden-test` / `scheduler-incremental` | 独立；职责清晰 |
| `skillsmith-reg` / `adapter-codegen` / `detail-to-markdown` / `pdf-extract` / `export-query` | 独立但须与上表协作方写清边界 |

---

## 3. 六层完整认知体系（定稿）

| 层 | 名称 | Skills |
|----|------|--------|
| **L0** | 意图与产品闸门 | `product-brief-confirm`（新建） |
| **L1** | 接源与理解 | `intake-excel` → `probe-site` |
| **L2** | 站族规约 | `skillsmith-reg` + `harvest-parser-plugin` |
| **L3** | 采与洗 | `adapter-codegen` + `process-content-adapter` + `detail-to-markdown` + `pdf-extract` |
| **L4** | 完整项目壳 | `console-ops-pages` + `scheduler-incremental` + `export-query` + `outbound-mq-contract`(可选) + `ops-daily-status` |
| **L5** | 验收与上线 | `golden-test` → `pod-deploy`（新建） |

说明：`golden-test` 在主链路上于「采与洗」之后、整站生成之前就要跑通；分层上归 L5「验收」，与主链路时序不矛盾——可在 codegen 后先金样，整站壳就绪后再做一次端到端金样。

---

## 4. 用户可见主链路（含确认闸门）

```text
批次 URL / Excel
  → product-brief-confirm（产品方案 + 配图 + Ask User → 冻结范围 → product_brief.yaml）
    → intake-excel → probe-site → skillsmith-reg
      → harvest-parser-plugin / adapter-codegen / process-content-adapter
        → detail-to-markdown（± pdf-extract）→ golden-test
          → 生成完整项目（对齐 console-ops-pages + scheduler-incremental
             + export-query + ops-daily-status）
            → 本地 / 试跑通过 → pod-deploy
              → （可选）outbound-mq-contract
```

**硬闸门**：`product-brief-confirm` 未确认前，**禁止**生成整站代码、**禁止** `pod-deploy`。

---

## 5. 最终 skill 清单（16）

| # | Skill | 层 | 主责一句话 | 状态 |
|---|-------|----|------------|------|
| 1 | `product-brief-confirm` | L0 | 批次产品方案 + 配图任务卡 + Ask User 确认 → 冻结 `product_brief.yaml` | **新建骨架** |
| 2 | `intake-excel` | L1 | Excel → source tickets + `intake_batch_id` | 已有 |
| 3 | `probe-site` | L1 | 打开入口，判页型/族，写侦察报告 | 已有 |
| 4 | `skillsmith-reg` | L2 | 侦察报告 → `sites/<slug>/SKILL.yaml` | 已有 |
| 5 | `harvest-parser-plugin` | L2 | 列表插件契约：注册顺序、`matches`/`build_request`/`parse`、Generic 兜底 | **新建骨架** |
| 6 | `adapter-codegen` | L3 | 按契约生成/改族 Adapter 指导与人审 diff | 已有 |
| 7 | `process-content-adapter` | L3 | 详情下载适配：SPA/API→可转 MD 的 HTML | **新建骨架** |
| 8 | `detail-to-markdown` | L3 | HTML/文本 → `content_md` + 质量门 | 已有 |
| 9 | `pdf-extract` | L3 | 附件 PDF/WPS 等 → 文本腿，再进 MD | 已有（骨架） |
| 10 | `console-ops-pages` | L4 | 六页信息架构与 API 对齐清单 | **新建骨架** |
| 11 | `scheduler-incremental` | L4 | 日触发打标、已知 URL 跳过、限速 | 已有（骨架） |
| 12 | `export-query` | L4 | **默认出仓**：时间窗 API + 控制台导出 | 已有（骨架） |
| 13 | `outbound-mq-contract` | L4 | 可选 MQ insert 形状/校验（默认关实现） | **新建骨架** |
| 14 | `ops-daily-status` | L4 | 全流程日报字段、通知文案、execution 状态 | **新建骨架** |
| 15 | `golden-test` | L5 | 金样试跑检查清单 | 已有 |
| 16 | `pod-deploy` | L5 | OpenClaw Pod 部署 checklist：镜像/卷/密钥/健康检查/回滚 | **新建骨架** |

---

## 6. 与「免调试批量出站」的关系

免调试宣称须**同时**满足（对齐 KaaS 蒸馏 §4）：

| 条件 | 对应层 / Skill |
|------|----------------|
| 批次功能范围已冻结 | L0 `product-brief-confirm` → `product_brief.yaml` |
| 族已登记 + Skill 参数齐全 | L2 `skillsmith-reg` + `harvest-parser-plugin` |
| 插件契约稳定 + 质量门明确 | L3 四 skill |
| 出仓 schema 冻结 | L4 `export-query`（± MQ） |
| 六页壳可运维 | L4 `console-ops-pages` + `ops-daily-status` |
| 金样全绿 | L5 `golden-test` |
| 部署约定可执行 | L5 `pod-deploy` |

**无 L0 闸门** →「免调试」只是开发者本机幻觉（用户未确认功能与 UI）。  
**无 L5 部署** → 站生成了但不上线，不算完整爬虫站认知闭环。  
同族只换 channel / 路径前缀时，L2–L3 可跳过新契约编写，仍须过 L0 确认与 L5 金样/部署。

---

## 7. 配图任务卡（给产品草图设计师）

> 由草图 skill / 设计师出图；本体系只规定「画什么」。至少 **3** 张线框。

| # | 画什么 | 须可见元素 | 用途 |
|---|--------|------------|------|
| 1 | **整体看板** | 磁盘/库占用、当前 run 进度、今日成功/失败源数、最近日报摘要入口 | 用户理解「跑起来后长什么样」 |
| 2 | **任务管理** | 源多选、启动采集/全流程、增量开关、限速提示、执行中状态 | 对齐「怎么触发一批」 |
| 3 | **文章明细**（或数据源管理） | 时间窗筛选、标题/来源/质检状态、预览 `content_md`、批量删除；若画数据源则：Excel 导入、按行改删、parser/族标签 | 对齐「最终产物里的数据长什么样」 |

可选第四张：配置页（定时 `time_of_day`、是否启用 MQ、Pod 环境标签）——Ask User 项可视化时用。

---

## 8. 相关路径

| 路径 | 用途 |
|------|------|
| `/workspace/briefs/reg-source-crawler-skills/` | Skills 包（含新建骨架） |
| `/workspace/briefs/2026-09-24-reg-source-agent-methodology.md` | 方法论（已嵌入确认环与部署） |
| `/workspace/briefs/2026-09-24-kaas-harvester-skills-distill.md` | KaaS 五 skill 蒸馏来源 |
