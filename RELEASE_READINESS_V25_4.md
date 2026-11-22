# v25.4 Release Readiness

Status: **Development / controlled testing only**.

## Completed offline checks
- 20 major profiles, 13 EMASI subjects, and 260 audit pairs retained.
- 186 source-claim rows retained across 86 distinct HTTPS URLs.
- All 20 majors appear in the source-claim register and academic source registry.
- All source-claim rows have institution, title, source type, and a scope/limitation note.
- 78 programme-availability records are explicitly distinguished from evidence for curriculum or EMASI subject mappings.
- Root and `data/` JSON registries remain synchronized.
- Application and URL-audit script syntax checked.

## Still required
1. Run the live URL auditor in a network-enabled environment.
2. Manually review every URL against the exact claim and course classification.
3. Resolve the 68 subject-guidance entries that lack claim-level references.
4. Obtain and compare EMASI grade-level syllabi and learning outcomes for all 13 subjects.
5. Test all pages and interactions in English and Vietnamese on desktop and mobile.
6. Review privacy, survey-data handling, access control, and deployment configuration.
7. Obtain Vietnamese academic terminology review.

No public release is approved by this audit. Do not replace v24 or the existing Railway deployment.
