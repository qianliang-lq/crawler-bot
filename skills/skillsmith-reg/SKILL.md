---
name: skillsmith-reg
description: "Use this when a probe-site recon report is ready and you must write sites/<slug>/SKILL.yaml (list_rule api_path, detail→Markdown, rate_limit, url_pattern) for human review."
---

# skillsmith-reg

## Purpose
Turn a reconnaissance report into a reviewable **site skill contract** at `sites/<slug>/SKILL.yaml`. Skill describes *what* to collect; Adapter implements *how*.

## When to use
- After successful `probe-site`.
- When cloning a same-family channel (only swap `channelid` / prefix / slug).

## Inputs
- Recon report (+ fixtures)
- Suggested `site_id` / `slug` (e.g. `csrc-szzyb-0599`)
- `family` enum: `csrc_search_list` | `amac_penalty_pdf` | `amac_gov_rules` | `neris`

## Steps
1. Choose `slug` = `{org}-{channel_short}` (first 4 hex of channelid ok).
2. Fill YAML per v1.3 §5.4 (see template below).
3. For `csrc_search_list`:
   - `list_rule.api_path`: `/searchList/{channelid}` (document `/common/searchList/{channelid}` as alternate if observed).
   - `list_rule.query`: `_isJson=true`, `_pageSize`, `page`.
   - `url_pattern.detail_template`: `https://www.csrc.gov.cn/{org_prefix}/{column_code}/c{manuscriptId}/content.shtml`
   - `url_pattern.id_from_list`: `manuscriptId` (also normalize protocol-relative `//host/...` URLs from JSON).
4. Set `detail_rule.content_as: markdown` and point cleaning to **`detail-to-markdown`**.
5. Set `rate_limit.rps` in **0.2–0.5**.
6. Add `tests.golden_*` placeholders for `golden-test`.
7. Write `sites/<slug>/NOTES.md` with recon summary + human open questions.
8. Stop for **human Skill 定稿** before codegen.

## SKILL.yaml template (csrc_search_list)
```yaml
site_id: csrc-szzyb-0599
family: csrc_search_list
source_id: csrc-szzyb-0599
start_urls:
  - "https://www.csrc.gov.cn/szzyb/.../common_list.shtml?channelid=..."
compliance:
  robots: best_effort
  rate_limit_rps: 0.3
  notes: "保留来源 URL + 原文哈希 + 抓取时间；禁止打码农场"
runtime:
  preferred: http
  headed: optional
params:
  channelid: "..."
  org_prefix: "szzyb"
  column_code: "c101700"
  host: "www.csrc.gov.cn"
list_rule:
  api_path: "/searchList/{channelid}"
  api_path_alt: ["/common/searchList/{channelid}"]
  query: { _isAgg: false, _isJson: true, _pageSize: 20, _template: index, page: "{page}" }
  item_fields: [title, url, publishedTimeStr, manuscriptId, content, channelId]
  pagination:
    type: page_param
    param: page
    total_field: data.total
    max_pages_per_run: 20
detail_rule:
  content_type: html
  content_as: markdown
  title: meta[ArticleTitle] | h1 | list.title
  published_at: meta[PubDate] | list.publishedTimeStr   # Asia/Shanghai
  content: main article container → detail-to-markdown
  attachments: a[href$=.pdf], preview_resource.action
url_pattern:
  detail_template: "https://{host}/{org_prefix}/{column_code}/c{manuscriptId}/content.shtml"
  id_from_list: manuscriptId
  list_url_field: url   # may be protocol-relative
incremental:
  key: url
  watermark_field: published_at
  lookback_days: 3
parse_fields:
  required: [title, url, published_at, content_md]
  optional: [source_org, manuscript_id, tags]
rate_limit:
  rps: 0.3
  jitter_ms: [200, 800]
tests:
  golden_list_url: "..."
  golden_detail_urls: []
```

## Outputs
- `sites/<slug>/SKILL.yaml`
- `sites/<slug>/NOTES.md`

## Forbidden
- Shipping Skill that scrapes empty CSRC shell DOM as list source.
- rps > 0.5 without explicit human override recorded in NOTES.
- Auto-Live without golden-test.

## Handoff
Next: **`adapter-codegen`** (same family → parameterize; new family → new module).
