# v25.3 Release Readiness

Status: **Development / controlled testing only**.

## New offline checks
- 186/186 source-claim rows have an explicit scope/limitation note.
- 86 distinct HTTPS URLs retained.
- Optional live URL audit script included; it has **not** been run as part of this build.
- No automatic evidence-status upgrades.
- No formal EMASI curriculum matches promoted.

## Offline QA
See `QA_RESULTS_V25_3.txt`. These checks validate local structure and metadata only. They do not validate source contents, live links, EMASI syllabus equivalence, admissions requirements, or browser behavior.

## Outstanding release gates
1. Run `python audit_source_urls.py` in a network-enabled environment and manually inspect redirects, blocked responses and failures.
2. Review each source page against its exact claim; URL reachability alone is insufficient.
3. Resolve 68 subject-guidance entries without attached claim-level references.
4. Obtain and review actual EMASI grade-level syllabi and learning outcomes for all 13 subjects.
5. Conduct browser testing of all pages in English and Vietnamese.
6. Conduct mobile and desktop layout/interaction testing.
7. Review privacy, access control and survey-data handling before broad public sharing.
8. Obtain Vietnamese academic terminology review.

Do not replace v24 or the current Railway deployment. No production deployment was performed.
