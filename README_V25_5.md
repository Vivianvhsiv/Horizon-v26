# Horizon v25.5 — Evidence Coverage Inventory

This is a development/audit package. It adds a reproducible evidence-coverage report without changing the Streamlit application or live deployment.

## Run
```bash
python build_evidence_coverage_report.py
python qa_v25_5.py
```

## Main outputs
- `EVIDENCE_COVERAGE_REPORT_V25_5.md`
- `EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv`

The report distinguishes programme-availability records from curriculum-context records and from EMASI subject-pair status. It is not academic validation. Actual EMASI grade-level syllabus comparison and claim-by-claim source review remain outstanding.
