# Horizon v25.4 — Source Audit Reliability

## Changes
- Reworked the optional URL reachability auditor to use HEAD with GET fallback, bounded retries, content-type capture, redirect destination capture, and conservative manual-review statuses.
- Added QA checks for cross-file consistency between the 20-major registry, 13-subject inventory, source register, academic source registry, and 260-pair audit matrix.
- Explicitly counts the 78 programme-availability records separately from curriculum/disciplinary records so programme existence is not mistaken for evidence of a subject mapping.
- No evidence statuses were upgraded automatically and no mapping was promoted to Verified.
- No production deployment or Railway update was performed.

## Limitations
- Live URL checks were not run in this build environment. Run `python audit_source_urls.py` from a network-enabled environment.
- Reachability does not prove that a page supports a claim. Manual claim-to-source review remains required.
- EMASI grade-level syllabus alignment remains pending until official school syllabi and learning outcomes are available.
- Browser, mobile, privacy, and Vietnamese academic terminology reviews remain release gates.
