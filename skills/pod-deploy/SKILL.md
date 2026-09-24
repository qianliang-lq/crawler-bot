---
name: pod-deploy
description: "Use this when a generated crawler site has passed local/canary golden-test and you must deploy it to an OpenClaw Pod with image/volume/SQLite/secrets/health-check/rollback checklist—after product_brief.yaml is confirmed."
---

# pod-deploy

## Purpose

L5 上线：把已金样通过的完整采集项目部署到 **OpenClaw Pod**。本 skill 写**约定 checklist**，不实现具体生产 Dockerfile 细节。

**前置硬闸门**：`product_brief.yaml` 已 `confirmed`；`golden-test` 相关项全绿（或 Canary 明确豁免并记录）。

## When to use

- 本地 / 试跑通过，用户要求上线。
- 变更 Adapter / 壳之后的滚动发布。
- 回滚到上一镜像版本。

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| `product_brief_path` | yes | 须 `status: confirmed` |
| `artifact_ref` | yes | 镜像 tag / 构建产物路径 |
| `env_label` | yes | 与 brief.`deploy.env_label` 一致 |
| `secrets_plan` | yes | Key 挂载清单（模型 Key、可选 MQ 凭据等） |

## Checklist（约定）

### 1. 镜像与构建

- [ ] 镜像标签可读：`reg-source-<instance>-<gitsha|date>`
- [ ] 构建上下文不含本机绝对密钥文件
- [ ] 运行用户非 root（若平台允许）

### 2. 卷与 SQLite

- [ ] SQLite 目录持久卷挂载（例：`/data/sqlite`）；**一 Pod 一库**
- [ ] 库文件路径与配置一致（`SQLITE_PATH`）
- [ ] 备份策略一句：卷快照或定时 `sqlite3 .backup`（实现自定）

### 3. 密钥挂载（Key）

- [ ] 模型 / OpenClaw **BYO Key** 以 Secret 挂载，不进镜像层
- [ ] 可选 MQ 凭据仅当 `outbound_mq: true` 时挂载
- [ ] 环境变量名写入实例 README；值不进 git

### 4. 健康检查

- [ ] HTTP readiness：例 `GET /health` 或时间窗 API `GET /api/articles?from=&to=` 空窗 200
- [ ] 存活探针与就绪探针分离（平台能力允许时）
- [ ] 失败阈值与启动宽限期符合冷启动 SQLite 迁移

### 5. 网络与限速

- [ ] 出站限速配置与 brief.`rate_limit_rps` 一致
- [ ] 时间窗 API 仅内网 / 鉴权策略与 `export-query` 约定一致

### 6. 回滚（一句）

- [ ] **回滚 = 切回上一镜像 tag + 保留 SQLite 卷**（schema 不向前破坏时）；破坏性迁移须先备份卷再发布

### 7. 发布后冒烟

- [ ] 看板可打开；任选 1 源 dry_run；日报字段可生成
- [ ] `product_brief.yaml` 与部署 env 归档进实例配置

## Outputs

- `deploy_record.md`：镜像、卷、健康检查 URL、回滚点、时间（Asia/Shanghai）
- 实例状态：`Live` / `RolledBack`

## Forbidden

- `product_brief` 未确认就部署。
- 把密钥写进 Dockerfile / 日志。
- 多实例共用同一 SQLite 文件。
- 未备份卷做破坏性 schema 迁移。
- 实现或粘贴完整生产 Dockerfile 机密细节（本 skill 只 checklist）。

## Handoff

- 可选启用 → **`outbound-mq-contract`**（若 brief 打开 MQ）。
- 日常 → **`ops-daily-status`** 观察。
