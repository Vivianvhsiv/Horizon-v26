# Horizon v26.0 — Final Release Candidate (RC)

**Status: Release candidate for supervised/controlled testing only. Not approved for unrestricted public release.**

## Scope

This package consolidates the v25.9 development state and its documentation, evidence registers, traceability artifacts, human-review queues, bilingual UI, and offline QA scripts. It does not change the v24 historical baseline or any live Railway deployment.

## What has been checked

- Static bilingual UI key parity and non-empty translation values.
- Presence and bilingual core fields for 20 major profiles and 13 EMASI subject labels.
- Structural consistency of the 260 major-subject matrix pairs and 186 source-register rows.
- Traceability identifiers and review queue coverage, where covered by the v25.8 integration QA.
- Python syntax and selected offline regression checks.

The v25.9 privacy/bilingual QA script reports **14/14 checks passed** in this package. The earlier v25.8 integration QA is included; see `QA_RESULTS_V25_8.txt` for its recorded result. These are static/offline checks, not proof of academic correctness, production security, or successful browser operation.

## Release blockers before public launch

1. **Academic source review:** Open each cited page and verify that the exact page content supports the claim recorded for it. Programme-existence evidence must not be presented as curriculum or prerequisite evidence.
2. **EMASI curriculum validation:** Obtain the applicable official EMASI syllabi/learning outcomes and review each proposed subject relationship. Until then, relationships remain exploratory and must not be labeled as confirmed EMASI requirements.
3. **Privacy and security review:** Review actual hosting configuration, access controls, logs, retention, downloads, secrets, and any third-party processing. Static source inspection cannot establish these.
4. **Browser and device QA:** Test the deployed candidate in current desktop and mobile browsers, including English/Vietnamese switching, network interaction, selection flows, and downloadable summaries.
5. **Vietnamese editorial review:** Have a fluent reviewer check terminology, clarity, and consistency in context.
6. **Owner/school approval:** Confirm permission to use school identity, survey data, and any school-specific curriculum materials. Do not publish raw survey responses or identifiable student information.

## Release decision

**Current decision: HOLD public release.** The package may be used for controlled testing with appropriate supervision and without exposing private survey data. Reassess only after all blockers above have evidence of completion and the release owner approves deployment.

## Version protection

- Preserve the approved v24 baseline unchanged.
- Do not deploy this RC to the live Railway service without explicit authorization and a rollback plan.
- Keep a dated copy of the current live deployment/source before any future deployment.
