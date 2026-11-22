# Horizon v26.0 — Final Release Candidate

This is a consolidation and release-governance package based on the v25.9 development tree.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run the v25.9 offline privacy/bilingual checks

```bash
python qa_v25_9.py
```

The script is static/offline. It does not test the live website, inspect Railway configuration, certify security, or verify external academic claims.

## Read first

1. `FINAL_RELEASE_CANDIDATE_V26_0.md`
2. `V26_0_FINAL_ACCEPTANCE_CHECKLIST.md`
3. `RELEASE_READINESS_V25_9.md`
4. `PRIVACY_REVIEW_V25_9.md`
5. `BILINGUAL_AUDIT_V25_9.md`

## Important

This is **not** a public-release approval. Academic source review, EMASI syllabus validation, live privacy/security review, manual browser testing, and human Vietnamese editorial review remain outstanding. The v24 baseline and live Railway deployment are not modified by this package.
