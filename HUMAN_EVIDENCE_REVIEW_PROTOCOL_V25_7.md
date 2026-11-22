# Horizon v25.7 — Human Evidence Review Protocol

## Purpose
Provide a repeatable, auditable workflow for reviewing source-page claims and then checking exploratory major–subject guidance against actual EMASI curriculum evidence. This release creates blank review queues; it does not perform or imply human review.

## Files
- `SOURCE_PAGE_REVIEW_QUEUE_V25_7.csv`: one row per source-register record (186 rows).
- `MATRIX_PAIR_REVIEW_QUEUE_V25_7.csv`: one row per major–subject pair (260 rows).

## Stage A — review the cited source page
For each source row, open the exact URL and record the page/section and the smallest passage or precise paraphrase that supports (or fails to support) the original claim. Record whether the claim is supported, partially supported, unclear, or contradicted. Distinguish programme availability, curriculum content, disciplinary context, professional guidance, prerequisites, and school-subject alignment. Do not treat a university course appearing in a degree plan as proof that a high-school subject is required.

A row may be marked `ACCEPTED` only when reviewer, review date, page/section, evidence excerpt/paraphrase, claim-support decision, and scope confirmation are completed. `ACCEPTED` means only that the stated source claim was checked within its stated scope; it does not mean EMASI alignment is proven.

## Stage B — review a major–subject pair
Use the second queue only after reviewing relevant university sources and obtaining the actual EMASI grade-level syllabus or learning outcomes. Record exact EMASI document/version, grade, section/outcome, and supporting text. Link source rows only after a reviewer has checked that each cited page supports the relevant part of the relationship.

`ELIGIBLE FOR FURTHER REVIEW` is not a verified status. It means the reviewer believes the evidence is sufficiently complete to submit to a separate academic/content approval step. Do not publish `verified` based solely on university programme listings, source URL reachability, reference counts, or inferred Claim IDs.

## Decision rules
- `KEEP EXPLORATORY`: evidence is incomplete or only contextual.
- `REVISE`: evidence supports a narrower or different statement.
- `REMOVE`: the source contradicts or does not support the guidance.
- `ELIGIBLE FOR FURTHER REVIEW`: both sides of the relationship have traceable, reviewed evidence; independent approval is still required.

## Current boundary
No source-page review or EMASI syllabus comparison is completed by this package. The CSV fields are intentionally blank, and the existing guidance remains exploratory.
