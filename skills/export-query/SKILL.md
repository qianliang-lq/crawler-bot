---
name: export-query
description: "Use this when exporting filtered articles from the local console/CLI (CSV/JSON including content_md) from the per-instance SQLite (skeleton)."
---

# export-query (skeleton)

## Purpose
Query local SQLite and export CSV/JSON/JSONL for console or external pullers. Default downstream = leave-in-DB.

## Minimum export fields
`title, published_at, url, content_md, source_id, site_id, intake_batch_id, fetched_at, attachments`

## Status
Skeleton; bind to `localhost:3000` export endpoint.
