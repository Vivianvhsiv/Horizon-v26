# Horizon v25.6 — Evidence Traceability Development

This package adds row-level IDs and conservative source-scope inventory files. It does not alter the app's matching logic, public deployment, or the protected v24 baseline.

## New files
- `SOURCE_TRACEABILITY_LEDGER_V25_6.csv` — stable IDs and scope boundaries for source-register rows.
- `MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv` — stable IDs for matrix pairs and explicit unresolved source-row linkage.
- `EVIDENCE_TRACEABILITY_REPORT_V25_6.md` — limitations and next validation steps.
- `build_claim_traceability_v25_6.py` — reproducible generator.
- `qa_v25_6.py` — offline QA.

Run: `python build_claim_traceability_v25_6.py && python qa_v25_6.py`

No live URL check, source-page content review, EMASI syllabus validation, browser test, or privacy review is claimed.
