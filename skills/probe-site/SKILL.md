---
name: probe-site
description: "Use this when you have a source ticket start_url and must classify page type (list/detail/other) and family (csrc_search_list / amac_penalty_pdf / amac_gov_rules / neris / unknown), including CSRC empty-shell + searchList API derivation."
---

# probe-site

## Purpose
Open one regulatory entry URL, decide what the page is for, which **family** it belongs to, and produce a **reconnaissance report** with candidate HTTP endpoints and URL-pattern hypotheses. Steady-state crawl should prefer HTTP/JSON/PDF after this skill succeeds.

## When to use
- After `intake-excel` tickets exist.
- When a Live source breaks and needs re-scout.
- M0 CSRC `common_list.shtml?channelid=…` entries.

## Inputs
| Field | Required |
|-------|----------|
| `start_url` / ticket | yes |
| `headed` | optional | Prefer headed/Xvfb when bare curl TLS/WAF fails |
| `rate_limit_rps` | yes | Cap **0.2–0.5**; default 0.3 |
| `save_dir` | yes | e.g. `briefs/reg-crawl-experiments/<date>/` |

## Steps
1. **Polite GET** of `start_url` (respect rate limit; jitter 200–800ms). Save status, content-type, body bytes, final URL.
2. **Page-type triage**
   - **list**: empty or populated index; pagination chrome; `channelid` query; `#list` / table of titles+dates.
   - **detail**: `ArticleTitle` / PubDate meta; single article body; `content.shtml`.
   - **other**: SPA shell only, login wall, error — mark `unknown` / human label; do not force list template.
3. **Family rules (M0 priority)**
   | Signal | Family |
   |--------|--------|
   | Host `www.csrc.gov.cn` + path `/*/common_list.shtml` + `channelid=` | `csrc_search_list` |
   | `amac.org.cn/.../jlcf/scfjg` or `scfry` + PDF links | `amac_penalty_pdf` |
   | `fg.amac.org.cn/.../zcgz_zlgz` | `amac_gov_rules` |
   | `neris.csrc.gov.cn` Vue shell | `neris` |
   | else | `unknown` |
4. **CSRC-specific (mandatory when family=csrc_search_list)**
   - Confirm shell `#list` (or list container) is **empty** in static HTML.
   - Parse `channelid` from query string.
   - Derive org prefix from path (`/szzyb/`, `/shzyb/`, …) and column code (`c101700`, …).
   - From page scripts / `common_list.js` pattern, hypothesize APIs:
     - `GET /searchList/{channelid}?_isAgg=false&_isJson=true&_pageSize={n}&_template=index&page={p}`
     - `GET /common/searchList/{channelid}?…` (seen in JSON `locationUrl`)
   - Sample one page JSON (`_pageSize` ≤ 5). Record top keys: `data.total`, `data.results[]` fields (`title`,`url`,`publishedTimeStr`,`manuscriptId`,`channelId`,…).
   - Click or open 1–2 detail URLs; record **URL pattern**.
5. If bare HTTP fails (TLS EOF / WAF `acw_tc` 302 to homepage): escalate to **headed** browser + network HAR; do **not** bypass captcha farms.
6. Write `recon_report.md` + raw fixtures under `save_dir`.

## Outputs (recon report checklist)
- `page_type`, `family`, `http_status` (shell + API)
- `shell_list_empty` (bool) for CSRC
- `channelid`, `org_prefix`, `column_code`
- `candidate_apis[]` with method/path/query
- `list_item_fields[]`
- `url_pattern.detail_template` hypothesis
- `risks` (TLS/WAF/SPA)
- Fixtures paths

## Forbidden
- Captcha solving / credential stuffing / high-frequency crawl.
- Claiming family without evidence.
- Treating shell DOM as list source when `#list` is empty.

## Handoff
Next: **`skillsmith-reg`** with this recon report.
