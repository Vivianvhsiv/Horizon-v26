# Horizon v25.6 — Evidence Traceability & Claim Verification Inventory

## Purpose
This release adds stable row IDs and a conservative traceability inventory to the existing evidence files. It is an offline documentation and data-integrity improvement, **not** a content verification or academic validation.

## What changed
- Every row in `SOURCE_CLAIM_REGISTER.csv` now has a stable `Source Row ID` in `SOURCE_TRACEABILITY_LEDGER_V25_6.csv`.
- The ledger preserves original claim fields and adds a conservative evidence-scope label and a plain-language use boundary.
- Every row in `EMASI_13x20_AUDIT_MATRIX.csv` now has a stable `Matrix Pair ID` in `MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv`.
- The crosswalk explicitly records whether the original matrix claim ID can be joined to a source-register row. No unsupported joins are guessed.

## Current inventory
- Source-register rows: 186
- Major–subject matrix pairs: 260
- Rows classified as programme availability only: 78
- Rows classified as curriculum context requiring page-level review: 60
- Rows classified as broad disciplinary context only: 3
- Rows classified as professional guidance context: 2
- Rows requiring other manual scope review: 43
- Missing URL fields: 0
- Non-HTTPS URL fields: 0

## Important traceability limitation
The supplied source register uses a `Claim Number` that repeats within majors, while the matrix uses a separate `Claim ID` format. The supplied files do not establish a reliable row-level foreign key between these records. Therefore v25.6 **does not claim that a particular source-register row supports a particular matrix pair**. The crosswalk preserves the original identifiers and marks the link unresolved until a human-reviewed mapping is supplied.

## Evidence boundaries
1. A programme listing does not establish curriculum content, subject prerequisites, or EMASI alignment.
2. A curriculum page may provide context, but its exact content must be reviewed against the wording of the claim.
3. A URL being present, reachable, or hosted by a university does not prove that it supports the claim.
4. Attached-reference counts and institution lists remain original bookkeeping fields; they are not independently validated by this release.
5. No EMASI grade-level syllabus or learning-outcome comparison is supplied in this dataset. No subject-major pair is upgraded to verified.

## Required next step
Create a human-reviewed source-to-claim crosswalk using the actual cited pages and exact claim wording. Then compare relevant claims with the official EMASI grade-level syllabus and learning outcomes. Keep uncertain relationships labelled exploratory.
