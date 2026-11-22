# Horizon v25.4 — Source Audit Reliability

This is a development package based on the v25.3 consolidated project.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run offline checks
```bash
python qa_check.py
python qa_v25.py
python qa_v25_2.py
python qa_v25_3.py
python qa_v25_4.py
python test_url_auditor.py
```

## Optional live URL reachability check
```bash
python audit_source_urls.py
```
This writes `SOURCE_URL_LIVE_AUDIT.csv`. It checks reachability only, not whether the page supports the associated claim. Inspect redirects, access restrictions, content, and exact claim alignment manually.

## Release status
Development / controlled testing only. No production deployment was performed. Keep v24 and the current Railway deployment unchanged until all release gates in `RELEASE_READINESS_V25_4.md` are completed.
