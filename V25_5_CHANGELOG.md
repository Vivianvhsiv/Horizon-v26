# Horizon v25.5 — Evidence Coverage Inventory

## Added
- `build_evidence_coverage_report.py` generates a reproducible per-major inventory from the source-claim register and 13×20 EMASI audit matrix.
- `EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv` provides machine-readable counts by major.
- `EVIDENCE_COVERAGE_REPORT_V25_5.md` explains totals, interpretation, and evidence boundaries.
- `qa_v25_5.py` checks the generated report against its source datasets.

## Verified dataset facts
- 20 majors, 13 subjects per major, 260 audit pairs.
- 186 source-claim rows and 86 distinct URLs.
- 78 programme-availability rows are counted separately from curriculum context.
- 109 pairs have current exploratory guidance; 151 have no current guidance entry.
- No pair is currently labelled as verified against the EMASI syllabus in the audit matrix.

## Limitations
This release does not validate the truth or relevance of individual academic claims, inspect source-page contents, test URL reachability, or compare actual EMASI syllabi. Counts are coverage indicators only. It does not modify `app.py`, the v24 baseline, or the live Railway deployment.
