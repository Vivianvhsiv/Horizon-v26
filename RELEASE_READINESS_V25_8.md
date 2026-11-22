# Release Readiness — Horizon v25.8

## Status
**Development / controlled testing only. Not certified for public release.**

## Offline checks
- Integration QA: 46/46 passed.
- Historical offline QA chain: passed when invoked by `qa_v25_8.py`.
- Core data inventory: 20 majors, 13 EMASI subjects, 260 major-subject pairs, 186 source records.
- Root and `data/` JSON registries are synchronized.

## Still required before public release
1. Human review of each source page and the exact claim it supports.
2. Obtain and review the relevant official EMASI grade-level syllabi and learning outcomes.
3. Confirm source-to-matrix links manually; unresolved joins must remain unresolved until confirmed.
4. Browser and mobile testing of the actual deployed application, including bilingual UI review.
5. Privacy review of survey collection, storage, access, retention, and any public-facing data.
6. Deployment review and explicit approval before changing the live Railway service.

## Not claimed
This package does not claim live URL checks, academic claim validation, EMASI curriculum validation, end-to-end browser testing, privacy/security certification, or public-release readiness.
