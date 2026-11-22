# Horizon v25.2 — Evidence Transparency & Data Quality Update

Build date: 2026-11-22  
Base: Horizon v25.1 Consolidated Development  
Status: controlled development build; not cleared for broad public release.

## Implemented in v25.2

1. Added a per-major bilingual evidence-coverage indicator in the EMASI subject guidance section. It reports how many suggestions have attached curriculum references and how many still need claim-level sources.
2. Clarified in the UI that attached university references provide university-level curriculum context; they do not verify EMASI syllabus alignment or admission prerequisites.
3. Added bilingual evidence-scope text to all 109 subject-guidance records. For the 18 records that lacked scope text, the new text explicitly states that no claim-level source is attached and the suggestion remains exploratory.
4. Added `SOURCE_URL_INVENTORY_V25_2.csv`, consolidating 186 source occurrences into 86 distinct URLs, with occurrence counts, associated institutions, titles, majors and claim types.
5. Added stricter offline QA for all 109 guidance records, bilingual evidence status/scope, URL metadata, counts, mirrored JSON files and syntax.

## Current evidence coverage

- Canonical majors: 20
- EMASI subjects: 13
- Possible major-subject pairs: 260
- Existing subject-guidance records: 109
- Guidance records with attached claim-level references: 41
- Guidance records without attached claim-level references: 68
- Source occurrences in source-claim register: 186
- Distinct URLs in source-claim register: 86
- Formal programme-specific `emasi_subject_connections`: 0

The 18 previously missing bilingual evidence-scope descriptions were completed with explicit pending-source language. This does not add evidence or upgrade their status.

## What is still not verified

- The 86 distinct URLs have not all been opened and live-checked individually in this build.
- The 68 guidance records without claim-level sources remain pending.
- The 41 sourced guidance records have not all undergone a complete source-to-sentence verification in this build.
- Actual EMASI grade-level syllabi and learning outcomes for all 13 subjects have not been provided or reviewed.
- None of the 260 pairs is certified as an EMASI curriculum match or universal admissions prerequisite.
- Full browser-level, mobile, privacy/access-control and Vietnamese academic copy-editing remain outstanding.

## Release decision

Not cleared for broad public release. Do not replace v24 or the current Railway deployment. Use this build for controlled testing and continued evidence review only.
