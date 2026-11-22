# Horizon v25.1 — Release Readiness

## Status: Development / controlled testing only

### Verified in this package
- 20 major profiles and 13 EMASI subject records are present.
- Major intention input supports up to three selections and the Undecided path.
- Major focus selector and bilingual UI code are present.
- 109 existing subject-guidance entries are retained.
- 260 major-subject combinations are listed in the audit matrix.
- Root and `data/` copies of `majors.json` and `academic_sources.json` are synchronized.
- `python -m py_compile app.py` passes.
- `python qa_check.py`: 574/574 passes.
- `python qa_v25.py`: 8/8 passes.
- `python qa_v25_1.py`: 12/12 passes.

### Not verified / must remain open
- Browser-level testing on current macOS/iOS/Android browsers.
- Full mobile/desktop layout and accessibility checks.
- All external URLs live and claim-by-claim content validation.
- Actual EMASI grade-level syllabi and learning outcomes for all 13 subjects.
- Final verification of all 109 subject guidance claims.
- Reflection behavior across every input combination.
- Privacy and access-control review before wider student access.

### Deployment protection
Do not overwrite v24 or the current Railway deployment with this package. Deploy only after the open checks are completed and the owner explicitly approves the release.
