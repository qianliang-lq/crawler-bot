---
name: intake-excel
description: "Use this when the user uploads an Excel of regulatory sources (URL / title / 备注) and you need to turn rows into source tickets with an intake_batch_id before probing."
---

# intake-excel

## Purpose
Read a user-uploaded Excel workbook of regulatory source rows and produce a batch of **source tickets** ready for `probe-site`. Aligns with proposal v1.3 Excel intake (not paste-only URL).

## When to use
- User uploads `.xlsx` / `.xls` / `.csv` with at least URL column.
- Re-intake of a new batch for the same employee instance.
- Console wizard step「上传 Excel」.

## Inputs
| Field | Required | Notes |
|-------|----------|-------|
| `excel_path` | yes | Absolute path inside Pod / workspace |
| `project_id` | yes | From employee config |
| `employee_id` | yes | Local self-description |
| `machine_id` | yes | Pod / machine id |
| Column map override | no | Default: URL / title / 备注 (flexible header match) |

### Column mapping heuristics
Accept Chinese/English headers (case-insensitive, strip spaces):
- URL: `url`, `链接`, `入口`, `start_url`, `网址`
- title: `title`, `标题`, `名称`, `栏目`
- note: `备注`, `note`, `notes`, `remark`, `说明`

If headers unknown: ask user once; do not invent columns.

## Steps
1. Open workbook (first non-empty sheet unless specified). Prefer `openpyxl` / `pandas`.
2. Generate `intake_batch_id` = `ib_{YYYYMMDD}_{HHmmss}_{short_uuid}` (Asia/Shanghai wall clock).
3. For each data row with a non-empty URL:
   - Normalize URL (trim; add `https://` only if scheme missing and host looks public).
   - Build ticket:
     ```json
     {
       "ticket_id": "t_{batch}_{row_no}",
       "intake_batch_id": "...",
       "excel_row_no": 2,
       "excel_title": "...",
       "excel_note": "...",
       "start_url": "https://...",
       "project_id": "...",
       "employee_id": "...",
       "machine_id": "...",
       "state": "Draft"
     }
     ```
4. Persist batch metadata for SQLite `intake_batch` + draft rows for `crawl_source` (state=Draft).
5. Emit human-readable summary: row_count, skipped blanks, duplicate URLs, suggested families if URL path already known (`csrc`/`amac`/`neris`).

## Outputs
- `intake_batch_id`
- `tickets[]` (JSON / YAML list)
- Optional: `intake_report.md` for console

## Forbidden
- Do not fetch remote URLs in this skill (that is `probe-site`).
- Do not invent missing URLs.
- Do not treat WeRead / 公众号 / RSS media lists as in-scope (out of product cut).
- Do not auto-mark Live.

## Handoff
Next skill: **`probe-site`** per ticket (or batched with rate limit).
