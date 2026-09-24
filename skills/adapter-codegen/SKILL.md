---
name: adapter-codegen
description: "Use this when a sites/<slug>/SKILL.yaml is drafted and you must generate or patch a family Adapter (e.g. CsrcSearchListAdapter), emphasizing human-reviewed diffs—not a full-repo dump."
---

# adapter-codegen

## Purpose
Guide AI to **generate or modify** Python Adapter code under `adapters/families/` (and thin site overrides). Output is a **diff for human confirmation**, not silent merge.

## When to use
- After `skillsmith-reg` Skill 定稿.
- Same-family new channel: usually **no new family class**—only Skill params + maybe thin override.
- New family: scaffold new module + first Adapter.

## Inputs
- Approved `sites/<slug>/SKILL.yaml`
- Existing `adapters/base.py` Runner interface
- Optional prior family code

## Runner interface (contract)
```python
class BaseAdapter(Protocol):
    def fetch_list(self, *, page: int, page_size: int, watermark: str | None) -> ListPage: ...
    def fetch_detail(self, item: ListItem) -> DetailDoc: ...
    def run_incremental(self, *, since: str | None) -> RunStats: ...
```

`ListItem` must carry at least: `title`, `url`, `published_at`, `manuscript_id` (optional), `raw` (JSON snippet).  
`DetailDoc` must carry: `title`, `url`, `published_at`, `content_md`, `content_html?`, `attachments[]`, `raw_hash`.

## CsrcSearchListAdapter — pseudo-code / conventions
```python
# adapters/families/csrc_search_list.py
class CsrcSearchListAdapter(BaseAdapter):
    """One Adapter for all CSRC common_list/searchList channels.
    Site differences = Skill params: channelid, org_prefix, column_code, host.
    """

    def __init__(self, skill: SiteSkill, http: HttpClient, md: MarkdownCleaner):
        self.skill = skill
        self.http = http          # enforces skill.rate_limit
        self.md = md              # detail-to-markdown

    def _api_url(self, page: int, page_size: int) -> str:
        path = self.skill.list_rule.api_path.format(channelid=self.skill.params.channelid)
        # Prefer https://{host}{path}; try api_path_alt on 404/empty
        ...

    def fetch_list(self, *, page, page_size, watermark=None) -> ListPage:
        data = self.http.get_json(self._api_url(page, page_size))
        total = dig(data, "data.total")
        items = []
        for row in dig(data, "data.results") or []:
            url = normalize_url(row.get("url"))  # //host → https://host
            items.append(ListItem(
                title=row["title"],
                url=url,
                published_at=row.get("publishedTimeStr"),
                manuscript_id=str(row.get("manuscriptId") or ""),
                raw=row,
            ))
        return ListPage(items=items, total=total, page=page)

    def fetch_detail(self, item: ListItem) -> DetailDoc:
        # Prefer item.url; fallback skill.url_pattern.detail_template
        html = self.http.get_text(item.url)
        title, published_at, body_html, atts = extract_csrc_detail(html)
        content_md = self.md.html_to_markdown(body_html)
        return DetailDoc(...)
```

### Same Adapter, two M0 sites
| site_id | channelid | org_prefix | column_code |
|---------|-----------|------------|-------------|
| csrc-szzyb-0599 | 059986f6… | szzyb | c101700 |
| csrc-shzyb-3fde | 3fdeb6b6… | shzyb | c101682 |

**Do not** fork a second family class for SH vs SZ.

## Steps for AI
1. Read Skill; decide *reuse family* vs *new family*.
2. Produce unified diff only under:
   - `adapters/families/<family>.py`
   - `adapters/<site_id>/` override (rare)
   - `tests/fixtures/<site_id>/`
   - `tests/test_<site_id>.py`
3. List new dependencies / outbound hosts explicitly.
4. Present diff to human; wait for confirm before applying to Live digest.

## Outputs
- Proposed file diffs + dependency note
- Suggested commit message
- Checklist: rate_limit wired? URL normalize? Markdown path? Golden hooks?

## Forbidden
- Whole-repo rewrite or unrelated refactors.
- Auto-merge to Live; changing auth, DB path, or volume mounts without human.
- Introducing unapproved outbound domains or captcha services.
- Implementing “config-only forever” claims.

## Handoff
Next: **`golden-test`** then optional **`scheduler-incremental`**.
