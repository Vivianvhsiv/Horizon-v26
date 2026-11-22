# Source audit guide

## 1. Run the reachability check

```bash
python audit_source_urls.py
```

Optional arguments:

```bash
python audit_source_urls.py --limit 10 --timeout 15 --delay 0.5
```

The script checks each distinct URL once and writes `SOURCE_URL_LIVE_AUDIT.csv`.

## 2. Interpret results carefully

- `reachable` means the server returned a 2xx/3xx response to HEAD or GET fallback.
- `needs manual review` includes timeouts, blocked requests, server errors and other failures.
- Some legitimate university sites block automated requests. A failed automated check does not prove a page is dead.
- A reachable page may have moved, changed cohort, or no longer support the recorded claim.

## 3. Manual claim review

For every register row, verify:
1. Institution and programme match the recorded claim.
2. The linked page is official and current for the stated cohort/year.
3. Exact course name and course classification (core, required supporting, elective, general education) are visible in the source.
4. The source supports the exact sentence, not merely the broad major.
5. The claim is not generalized to all universities.
6. University curriculum evidence is not described as EMASI syllabus equivalence or a formal admission prerequisite.

Do not change a claim to Verified solely because the URL responds.
