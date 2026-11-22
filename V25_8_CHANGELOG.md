# Horizon v25.8 — Final Integration & Regression QA

## Purpose
This increment adds an offline integration/regression gate across the existing application data, EMASI framework, evidence traceability artifacts, and human-review workflow.

## Added
- `qa_v25_8.py`: 46 structural integration and regression checks.
- `QA_RESULTS_V25_8.txt`: captured results from the current package.
- `README_V25_8.md`: run instructions and scope.
- `RELEASE_READINESS_V25_8.md`: explicit readiness boundaries and remaining manual work.

## What the checks cover
- Root/data JSON registry synchronization.
- Presence and bilingual shape of 20 major profiles.
- 13 unique EMASI subject identifiers and bilingual names.
- Mapping protocol status and relationship-type integrity.
- Coverage and ID consistency across 260 matrix pairs and 186 source records.
- Review queues remain unreviewed by default; no missing evidence is fabricated.
- Python syntax and all historical offline QA scripts.

## Important limitations
Passing QA confirms structural consistency only. It does not validate the truth or current availability of external sources, confirm university curriculum claims, validate EMASI syllabus alignment, test browser/mobile behavior, or certify privacy/security. No live deployment was changed.
