# Horizon v25 Development Deployment Notes

This is an independent development build based on the v24 Bilingual Complete QA source. It does not replace the v24 baseline.

## Included change
- Adds `Majors you are considering` to My Exploration Network.
- Options are read directly from the same `MAJORS` data object used to render the Network Map.
- Supports up to three choices and a bilingual Undecided option.
- Explicitly selected majors become primary highlighted nodes; interest and subject links remain supporting context.

## Local checks completed
- `python -m py_compile app.py`
- `python qa_check.py` — 574/574 existing structural checks passed.
- `python qa_v25.py` — 8/8 targeted checks passed.

## Not yet tested
- Live Streamlit browser behavior (Streamlit dependencies were not installed in the build environment).
- Mobile layout and interactive graph behavior in a real browser.
- Full evidence audit, source URL availability, privacy review, and the remaining planned v25 improvements.

## Deploy safely
Deploy this as a separate Railway service/project or a separate GitHub branch. Do not overwrite the existing v24 Public Beta until user acceptance tests pass.
