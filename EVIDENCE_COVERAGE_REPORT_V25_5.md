# Horizon v25.5 — Evidence Coverage Inventory

## Purpose and interpretation
This report describes the contents and status labels in the current source register and EMASI audit matrix. It is a coverage inventory, not an academic validation. Counts do not establish source quality, claim accuracy, causal relevance, or universal degree requirements.

## Dataset totals
- Major profiles: 20
- EMASI subjects per profile: 13
- Major–subject audit pairs: 260
- Source-claim register rows: 186
- Distinct URLs in source register: 86
- Programme availability rows: 78 (these establish only the listed programme availability/label, not EMASI subject alignment).
- Pairs with an existing guidance role: 109
- Pairs with no current guidance entry: 151
- Pairs explicitly labelled exploratory / not verified against EMASI syllabus: 109
- Pairs labelled as EMASI-syllabus-verified in the matrix: 0

## Evidence boundaries
1. Programme availability is not curriculum evidence and is not a subject prerequisite.
2. University curriculum references can provide exploratory disciplinary context, but do not prove equivalence to EMASI grade-level learning outcomes.
3. An attached reference count is a register/matrix bookkeeping field; it does not prove that every cited page supports the specific subject-to-major suggestion.
4. No EMASI syllabus-verified pair is currently labelled in the matrix. Do not describe any mapping as formally verified until the relevant EMASI syllabus and learning outcomes are reviewed pair by pair.
5. This report does not assess URL reachability. Run audit_source_urls.py separately; reachability is not content validation.

## Per-major inventory
| Major | Claims | URLs | Programme availability | Curriculum context | Guidance pairs | No guidance | Exploratory / not EMASI-verified |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cognitive Science | 12 | 11 | 2 | 7 | 6 | 7 | 6 |
| Psychology | 13 | 13 | 5 | 6 | 5 | 8 | 5 |
| Computer Science | 14 | 14 | 6 | 8 | 4 | 9 | 4 |
| Data Science | 17 | 17 | 5 | 12 | 11 | 2 | 11 |
| Economics | 7 | 7 | 3 | 4 | 6 | 7 | 6 |
| Biology | 9 | 9 | 5 | 4 | 5 | 8 | 5 |
| Mechanical Engineering | 9 | 9 | 4 | 5 | 4 | 9 | 4 |
| Finance | 7 | 7 | 3 | 4 | 4 | 9 | 4 |
| Chemistry | 10 | 10 | 5 | 5 | 4 | 9 | 4 |
| Physics | 9 | 9 | 4 | 5 | 4 | 9 | 4 |
| Environmental Science | 8 | 8 | 4 | 4 | 6 | 7 | 6 |
| Architecture | 7 | 7 | 3 | 4 | 7 | 6 | 7 |
| Electrical Engineering | 12 | 12 | 6 | 6 | 4 | 9 | 4 |
| Civil Engineering | 11 | 11 | 6 | 5 | 5 | 8 | 5 |
| Political Science | 7 | 7 | 3 | 4 | 6 | 7 | 6 |
| Sociology | 6 | 6 | 2 | 4 | 6 | 7 | 6 |
| Linguistics | 6 | 6 | 2 | 4 | 5 | 8 | 5 |
| Education | 7 | 6 | 3 | 4 | 6 | 7 | 6 |
| Accounting | 7 | 7 | 3 | 4 | 4 | 9 | 4 |
| Communication & Media Studies | 8 | 8 | 4 | 4 | 7 | 6 | 7 |

## Files
- `EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv`: machine-readable per-major counts.
- `SOURCE_CLAIM_REGISTER.csv`: underlying source/claim records.
- `EMASI_13x20_AUDIT_MATRIX.csv`: underlying subject-pair status records.
