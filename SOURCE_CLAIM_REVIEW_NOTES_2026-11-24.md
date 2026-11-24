# Claim-level review notes — 24 November 2026

## Reviewed and tightened in this pass

### Psychology — claim 1: APA undergraduate learning goals

**Previous wording:** Undergraduate psychology education includes scientific inquiry, critical thinking, research methods and statistics.

**Revised wording:** The APA Guidelines for the Undergraduate Psychology Major, Version 3.0, define five broad learning-goal areas: content knowledge and applications; scientific inquiry and critical thinking; values in psychological science; communication, psychological literacy and technology skills; and personal and professional development.

**Source:** American Psychological Association, *Guidelines for the Undergraduate Psychology Major, Version 3.0* (approved August 2023): https://www.apa.org/ed/precollege/undergraduate-major

**Reason for change:** The earlier wording compressed a broader professional guideline into a short list of subjects/skills and risked implying a uniform curriculum. The revised claim names the five learning-goal areas and the status explicitly says this is APA guidance, not a uniform course requirement at every university. The redundant duplicate APA URL was removed from this claim.

### Cognitive Science — claim 5: UC Irvine 2026–27 comparison

**Review finding:** UC Irvine's official 2026–27 comparison explicitly distinguishes its B.S. in Cognitive Sciences from its B.S. in Psychology. Both list psychology fundamentals, statistics, programming and a science background; the Cognitive Sciences route additionally lists calculus and computational/statistical-learning core options.

**Source:** University of California, Irvine, Department of Cognitive Sciences: https://www.cogsci.uci.edu/undergraduate/

**Scope:** This is an institution- and catalogue-year-specific comparison. It is not a universal difference between all Cognitive Science and Psychology degrees, nor evidence of equivalence with EMASI subjects.

### MIT programme availability sources: four profile records

The generic MIT *Academic Program* PDF was replaced with the exact MIT Course Catalog department page for each listed undergraduate programme:

| Major | Exact official catalogue page |
|---|---|
| Economics | https://catalog.mit.edu/schools/humanities-arts-social-sciences/economics/ |
| Political Science | https://catalog.mit.edu/schools/humanities-arts-social-sciences/political-science/ |
| Chemistry | https://catalog.mit.edu/schools/science/chemistry/ |
| Physics | https://catalog.mit.edu/schools/science/physics/ |

**Reason for change:** The old generic PDF was an institution-wide academic-program overview. The new links are programme-specific department/catalogue pages, making the evidence trail more direct. The register continues to distinguish programme availability from course-level curriculum evidence. These pages must not be used to imply admissions requirements or EMASI syllabus equivalence.

## Register integrity

- The APA duplicate source was removed from one claim.
- The four MIT source URLs/titles were replaced with programme-specific catalogue pages.
- `academic_sources.json` and `SOURCE_CLAIM_REGISTER.csv` were regenerated from the same source records.
- Current expected source occurrences: 185 (down from 186 because one duplicate APA source was removed).

## Remaining review status

This is a targeted review of the claims and source records listed above, not completion of the full 65-claim semantic audit. Other claim families still need exact-page checks, especially programme availability, institution-specific curriculum classification (core/required/elective), and any profile statements about skills, research areas or career exploration that are not represented in the claim register.

## Additional programme-evidence scope review

A second pass found a repeated overstatement risk in programme-directory claims: a broad directory page or a programme list should not be described as verified for every exact degree title unless the exact undergraduate award is visible on that institution's current official page.

Changes made:
- Reclassified the first programme-reference claim for Computer Science, Data Science, Biology, Mechanical Engineering, Finance, Environmental Science, Architecture, Electrical Engineering, Civil Engineering, Sociology, Linguistics, Education, Accounting, and Communication & Media Studies as programme-availability evidence rather than implying curriculum evidence.
- Downgraded the programme-directory claim statuses for Psychology, Computer Science, Data Science, Economics, Biology, Mechanical Engineering, Finance, Chemistry, Physics, Environmental Science, Architecture, Electrical Engineering, Civil Engineering, Political Science, Sociology, Linguistics, Education, Accounting, and Communication & Media Studies. The register now asks for exact programme-title and undergraduate-award confirmation on each current institutional page before treating every entry as verified.
- Narrowed the Vietnamese-German University 2025 application-guideline entries under Mechanical Engineering and Electrical Engineering: they may support only programme names/admissions information explicitly stated in the document, not course content, curriculum or subject mappings.
- Rebuilt the CSV register from the JSON source of truth. Expected source occurrences remain 185.

## Latest completed CI baseline (before this additional register edit)

On commit `8f234f9fbba4715d620834afb8cdbc5175e1d929`:
- Structural QA: 609/609 passed.
- Streamlit AppTest: 1 passed.
- Live source URL audit: 88 unique URLs checked; 80 reachable; 8 flagged for manual review.
- URL audit CSV artifact uploaded successfully.

The additional programme-status/source-scope edits above were committed after that run and require a fresh CI run. The earlier 86-URL / 76-reachable report is superseded by this 88-URL result.

