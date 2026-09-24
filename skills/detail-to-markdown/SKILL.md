---
name: detail-to-markdown
description: "Use this when converting regulatory detail HTML or PDF-extracted text into cleaned Markdown for content_md storage in the per-instance SQLite."
---

# detail-to-markdown

## Purpose
Normalize detail page bodies (HTML or PDF text) into **Markdown** for `crawl_article.content_md`. Keep provenance; strip chrome.

## When to use
- Inside Adapter `fetch_detail` / PDF pipeline.
- Spot-fix golden fixtures.
- Console preview of article body.

## Inputs
| Field | Notes |
|-------|-------|
| `html` or `pdf_text` | Exactly one primary |
| `base_url` | For resolving relative links |
| `family` | Optional selector hints |

## HTML → Markdown steps (CSRC content.shtml)
1. Parse HTML (lxml/bs4). Prefer article root candidates in order:
   - `.detail-news` / `.content` / `#content` / `.article` / `div.TRS_Editor` / main section with PubDate sibling.
2. **Drop**: header/footer/nav/sidebar/share widgets/script/style/`#list`.
3. Read meta fallbacks: `ArticleTitle`, `PubDate`, `ContentSource`.
4. Convert body with a conservative HTML→MD library (e.g. `markdownify` / `html2text`):
   - Keep headings, paragraphs, lists, tables (simple), links.
   - Images → `![alt](abs_url)` but do not download unless attachment pipeline requests.
5. PDF / `preview_resource.action` links → record in `attachments[]`; in MD keep the link line.
6. Collapse ≥3 blank lines; trim; ensure UTF-8.
7. Compute `content_hash` = sha256(utf8 `content_md`).

## PDF text → Markdown
- Prefer `pdf-extract` output.
- Wrap as MD paragraphs; preserve 文号 lines as bold if detected (`^〔?\d{4}〕?` / `〔YYYY〕` patterns for AMAC).
- Do not OCR unless text layer empty (then flag `needs_ocr`).

## Outputs
- `content_md: str`
- `attachments: [{filename,url,content_type,path?,sha256?}]`
- `title`, `published_at` if extracted
- `warnings[]` (empty body, only nav left, etc.)

## Forbidden
- Sending原文 to third-party cloud summarizers by default.
- Stripping all links (lose legal source trail).
- Inventing missing titles/dates.

## Handoff
Caller Adapter writes SQLite `content_md` + hashes; then **`golden-test`** validates readability.
