# Horizon v25.3 Changelog

## Evidence register quality improvements
- Added an explicit scope/limitation note to all 186 source-claim register rows. For previously blank entries, the added text is a conservative usage limitation, not a new finding or source verification.
- Added `audit_source_urls.py`, an optional, rate-limited live URL reachability checker for the 86 distinct source URLs. It writes `SOURCE_URL_LIVE_AUDIT.csv` when the user runs it. It never upgrades evidence status automatically.
- Added `qa_v25_3.py` to validate register completeness, URL format, 20-major/13-subject/260-pair counts, mirrored registries and Python syntax.
- Added an explicit manual-review boundary: HTTP reachability is not proof that a page supports a claim.

## Not changed
- No EMASI subject mapping was promoted to Verified.
- No `emasi_subject_connections` were added.
- No existing evidence status was upgraded.
- No production/Railway deployment was performed.
- Existing v24 and v25.2 package remain unchanged.

## Release status
Development / controlled testing only. Not cleared for broad public release.
