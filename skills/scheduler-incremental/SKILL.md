---
name: scheduler-incremental
description: "Use this when a source passed golden-test and you need cron/watermark incremental pulls with enforced rate_limit and backoff (skeleton)."
---

# scheduler-incremental (skeleton)

## Purpose
Run Live incremental fetches by watermark (`published_at` / url set), enforcing Skill `rate_limit` and exponential backoff on errors.

## Steps (outline)
1. Load Live sources from registry + Skill digests.
2. For each source: `run_incremental(since=watermark-lookback)`.
3. Upsert articles; advance watermark only on success.
4. Emit `crawl_run` stats; alert on repeated failures.

## Forbidden
- Bursting above 0.5 rps/site.
- Silent digest overwrite.

## Status
Skeleton for M0; wire after first CSRC+AMAC Live.
