# Horizon v25.0.0 — Change log

## Implemented in this development build
- Added a Major Intention selector to My Exploration Network.
- Selector options are generated directly from the `MAJORS` dictionary loaded from `majors.json`; no duplicate hard-coded list.
- Supports up to three intended majors and a separate Undecided option.
- Stores canonical major keys regardless of display language.
- Student-stated majors are added as explicit student-intention edges and included in the candidate list even when interest tags do not match.
- Network focus highlights all explicitly selected majors and their existing discipline/career branches before inferred interest-based areas.
- Interest and subject connections remain supporting context; no suitability score is presented.

## Not yet certified
- This is a development build, not a production deployment.
- Subject relationship evidence, all 20 major profiles, all source claims, reflection workflow, privacy behavior, responsive layout, and live Railway behavior still require separate audits.
- The Undecided checkbox currently clears intended-major selection for that submission; students can still explore using interests and current subjects.
