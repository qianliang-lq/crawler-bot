---
name: golden-test
description: "Use this when a site Skill + Adapter are ready and you must run a small golden sample (3–5 items) to verify list fields, detail Markdown, and dry_run DB writes before Live."
---

# golden-test

## Purpose
Checklist-driven canary for one `site_id`: sample list + details, assert required fields, confirm Markdown quality, optionally write Testing/dry_run rows without moving Live watermark.

## When to use
- After `adapter-codegen` human-approved diff applied in sandbox.
- After Skill parameter change on existing family.
- Regression when site layout drifts.

## Inputs
- `sites/<slug>/SKILL.yaml` (`tests.golden_*`)
- Adapter instance / try_run script
- Fixture dir `tests/fixtures/<site_id>/` (optional offline mode)

## Checklist
### A. List
- [ ] API/list HTTP 200 (or fixture load) within rate_limit
- [ ] `data.total` (or equivalent) > 0 for known live channels
- [ ] First N≤5 items have non-empty `title`, absolute `url`, parseable `published_at`
- [ ] CSRC: `manuscriptId` present; URL matches `url_pattern` or normalizes from JSON `url`
- [ ] Protocol-relative URLs fixed to `https://`

### B. Detail
- [ ] Fetch 2–3 golden detail URLs
- [ ] `content_md` length ≥ threshold (e.g. 80 chars) **or** explicit attachment-only page documented
- [ ] No header/footer junk dominating MD (spot check)
- [ ] `content_hash` / `raw_hash` computed
- [ ] Timezone labels Asia/Shanghai for displayed times

### C. DB dry_run
- [ ] Rows land with `state` Testing or `dry_run` flag
- [ ] `intake_batch_id` / `source_id` / `site_id` set
- [ ] UNIQUE(`url_hash`) does not explode on re-run
- [ ] Live watermark **unchanged**

### D. Report
Write `golden_report_<site_id>.md` with pass/fail table + sample MD excerpt (≤40 lines).

## Outputs
- Pass/fail boolean per site
- Report path + fixture updates if AI captured new goldens (human must accept)

## Forbidden
- Promoting to Live automatically.
- Disabling rate_limit for “faster tests”.
- Overwriting production DB file.

## Handoff
On pass → human Canary → **`scheduler-incremental`**. On fail → back to probe/skillsmith/adapter.
