# Horizon v25.1 — Consolidated Improvement & Evidence Audit

Audit build: 2026-11-22
Base: v25 Major Intention + Visual Refinement development build.
This is a development/audit candidate, not a public-production certification.

## What was changed in this package

1. Preserved the 20-major canonical database and the 13-subject EMASI inventory.
2. Added current, claim-scoped official curriculum references for UC Irvine Cognitive Sciences/Psychology (2026–27), VinUniversity Psychology, UEH Computer Science, VNUHCM-US Computer Science, and VinUniversity's cohort-specific academic catalogue index.
3. Added an explicit bilingual clarification in the major profile: academic disciplines are university-level fields and are not the same as EMASI school subjects.
4. Added a full 13 × 20 audit matrix and source-to-claim inventory.
5. Kept `emasi_subject_connections` unchanged: no formal programme-specific EMASI connection is promoted without EMASI syllabus comparison.

## Database audit counts

- Majors: 20
- EMASI subjects: 13
- Possible major-subject pairs: 260
- Existing subject-guidance entries: 109
- Existing guidance entries with at least one attached reference: 41
- Formal `emasi_subject_connections` entries: 0
- Academic claim records: 65
- Source occurrences across claim records: 186
- Distinct URLs attached to current subject guidance: 35
- Guidance entries with no attached claim-level reference: 68

## Critical findings — what still needs improvement

### A. EMASI syllabus alignment is not yet verified
The package contains 13 subject names, but the actual grade-level EMASI syllabi and learning outcomes have not been supplied or reviewed in this audit. Therefore all existing subject guidance remains exploratory. Do not label any of the 260 pairs as a verified EMASI curriculum match or university admission prerequisite.

### B. Existing guidance is unevenly sourced
There are 109 guidance entries, but only 41 have one or more references attached at the entry level. The remaining 68 need claim-level evidence or should remain explicitly unsourced/pending.

### C. Major-level source references are not proof for every subject claim
A university programme page may support a major's overall curriculum or disciplinary context. It does not automatically support every subject recommendation in that profile. The `SOURCE_CLAIM_REGISTER.csv` keeps source references attached to their current claim records; further source-by-source review is still needed.

### D. University curriculum, EMASI alignment and admissions must stay separate
1. University Curriculum Evidence: what a named university programme teaches.
2. EMASI Syllabus Alignment: whether the current EMASI course content overlaps with those topics.
3. Admission Prerequisite Evidence: formal entry requirements for a named institution, programme and intake.
These are different claims and require different sources.

### E. Programme variability
Requirements differ by university, degree type, pathway and intake. For example, UC Irvine's 2026–27 comparison explicitly distinguishes its B.S. Cognitive Sciences and B.S. Psychology requirements; its specific comparison must not be generalized to all universities.

### F. Remaining product QA
- Browser-level testing of all pages in English and Vietnamese.
- Mobile and desktop visual testing, including dense multi-major networks.
- Reflection consistency and empty/edge-case input tests.
- Privacy/access-control review before sharing the public URL.
- Live validation of all source URLs and Vietnamese academic copy-editing.

## Evidence status policy

- Verified: the named source directly supports the exact claim within the stated institution/cohort scope.
- Supported: credible context exists, but exact claim scope or EMASI alignment remains incomplete.
- Pending Verification: source or syllabus evidence is missing.
- Rejected / Not Supported: reviewed evidence does not support the claim.

A Verified university course claim does not make an EMASI subject mapping Verified.

## Files in this package

- `EMASI_13x20_AUDIT_MATRIX.csv` — all 260 possible major-subject pairs, current guidance and limitations.
- `SOURCE_CLAIM_REGISTER.csv` — all existing source occurrences attached to claim records.
- `HORIZON_V25_1_AUDIT_REPORT.md` — this report.
- Updated `app.py`, `data/academic_sources.json`, and mirrored root data files.

## Release decision

**Not cleared for broad public release.** Keep the live Railway deployment and v24 unchanged. Use this package as the next controlled development/audit candidate. The next required input for a true EMASI mapping audit is the actual grade-level syllabus and learning outcomes for each of the 13 EMASI subjects.
