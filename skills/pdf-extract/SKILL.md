---
name: pdf-extract
description: "Use this when an AMAC penalty/rules item is a PDF body and you need text extraction (pdfminer; OCR fallback) before detail-to-markdown (skeleton)."
---

# pdf-extract (skeleton)

## Purpose
Download PDF to local attachments volume; extract text with pdfminer; OCR only if empty text layer; hand text to `detail-to-markdown`.

## Notes
- Store path + sha256 in DB; never default-upload原文 to third-party SaaS.
- M0 primary consumer: `amac_penalty_pdf` family.

## Status
Skeleton; implement with AMAC scfjg/scfry Adapter.
