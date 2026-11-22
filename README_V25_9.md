# Horizon v25.9 — Privacy Surface & Bilingual Audit

This development increment adds static checks and review guidance for privacy and bilingual coverage. It does not change application behavior.

## Run
```bash
python qa_v25_9.py
```

Expected result: **14/14 passed** in the supplied package.

The checks confirm that the English and Vietnamese UI dictionaries each contain 82 matching, non-empty keys; the 20 major profiles have core bilingual descriptions and caveats; and all 13 subject labels have English and Vietnamese values. Static privacy-surface checks did not find obvious direct-identifier input widgets or obvious write/database primitives in `app.py`.

## Important limits
These are source-code checks only. They do not inspect Railway/Streamlit infrastructure, server logs, secrets, backups, dependencies, network traffic, actual browser behavior, translation quality, legal compliance, or third-party data processing. Read `PRIVACY_REVIEW_V25_9.md`, `BILINGUAL_AUDIT_V25_9.md`, and `RELEASE_READINESS_V25_9.md` before any public release.

The previous v25.8 integration report is retained as historical evidence; the v25.8 QA chain was not rerun as part of this v25.9 check because its nested historical scripts exceeded the available execution window. v24 and the live Railway deployment are unchanged.
