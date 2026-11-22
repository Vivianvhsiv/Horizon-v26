# Horizon v25.3 Improvement Report

## What changed
The source-claim register previously contained 186 rows, of which 141 had an empty `Scope / Limitation` field. v25.3 fills those empty fields with conservative, claim-type-appropriate limitation language. These additions are metadata safeguards, not new evidence and not source verification.

A new optional script, `audit_source_urls.py`, checks the 86 distinct HTTPS URLs for basic HTTP reachability. It uses HEAD with GET fallback for common HEAD restrictions, supports timeout/delay/limit options, and writes a separate CSV. It never changes claim status. The script was included but not run during packaging because automated reachability results can be blocked or misleading and must be interpreted manually.

A new offline QA script checks source-register completeness, the 20 major / 13 subject / 260 pair inventory, 86 unique URLs, mirrored data files and app syntax.

## Results
- Existing baseline QA: 574/574
- Major intention QA: 8/8
- v25.1 QA: 12/12
- v25.2 QA: 21/21
- v25.3 QA: 13/13
- Python syntax compilation: passed
- ZIP integrity: verified after packaging

These are offline structural checks, not a cumulative certification of academic validity.

## Important unchanged limitations
- 68 subject-guidance records still have no attached claim-level source.
- 41 records have attached references but still require source-to-claim manual review.
- 86 URLs have not been live-checked in this build.
- EMASI grade-level syllabi / learning outcomes are not available for full alignment review.
- The 260 subject-major pairs are an audit matrix, not 260 approved mappings.
- Browser, mobile, privacy/access-control and Vietnamese academic copy-editing remain outstanding.

## Decision
Keep this build in controlled development. Do not replace v24 or the production Railway deployment.
