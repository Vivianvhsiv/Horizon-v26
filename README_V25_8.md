# Horizon v25.8 — Final Integration & Regression QA

This is an offline QA increment. It adds a cross-artifact integration gate without changing the app's major-matching logic or promoting exploratory subject guidance to verified relationships.

## Run
```bash
python qa_v25_8.py
```

Expected result for this package: **46/46 passed**.

The script also runs the previous offline QA chain. It checks structural consistency across 20 major profiles, 13 EMASI exploration subjects, 260 major-subject matrix pairs, 186 source-register rows, traceability ledgers, and v25.7 human-review queues.

A passing result is not academic verification, live URL verification, EMASI syllabus validation, browser/mobile testing, or a privacy/security certification.
