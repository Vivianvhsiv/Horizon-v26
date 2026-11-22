# Horizon — Historical Full Data and Evidence QA Audit (v22 baseline)

> Historical snapshot only. The 91-entry / 11-subject figures below describe the earlier v22 baseline and are superseded by `FINAL_QA_AUDIT_V24_BILINGUAL.md` (109 guidance entries and 13 subjects). Do not use this file as the current release checklist.

**Date:** 19 November 2026  
**Scope:** 20 major profiles, 91 EMASI subject-guidance entries, 20 academic-source records, and the Streamlit application source.

## Executive result

Horizon remains a research prototype. The audit improves consistency and traceability but does **not** certify every profile as academically verified. Programme availability, curriculum content, admissions prerequisites, and alignment with the actual EMASI syllabus are distinct claims and must remain separate.

## Data integrity checks

- 20 major profiles and 20 corresponding academic-source records are present.
- 91 EMASI subject-guidance entries are present.
- All 11 EMASI subject IDs (S01–S11) occur in the guidance dataset.
- Every guidance entry contains the expected bilingual subject, role, rationale, focus, evidence explanation, claim ID, and evidence-status fields.
- Vietnamese and English subject labels were checked against the supplied EMASI subject dictionary. The English display label for S09 was normalized to **ICT (Information and Communication Technology)**; the Vietnamese label remains **ICT**.
- 181 source links are recorded across the academic-source claim records after this update.
- All 20 major profiles now contain a separate curriculum-evidence claim at profile level. This does not mean all 109 individual EMASI subject suggestions are verified.
- JSON parsing and Python syntax compilation passed.

## Evidence review by profile

| Major | Curriculum evidence status | Guidance entries | Evidence note |
|---|---|---:|---|
| Cognitive Science | Expanded | 5 | Multiple official curricula and disciplinary references; school-subject mapping remains exploratory |
| Psychology | Expanded | 4 | Official curriculum and professional guidance; mapping remains exploratory |
| Computer Science | Expanded | 4 | HCMUT, UCL, NUS and VinUniversity curriculum evidence; institution/cohort scope retained |
| Data Science | Expanded | 10 | Multi-institution and professional curriculum references; each EMASI subject mapping still needs individual review |
| Economics | Curriculum evidence added | 4 | Notre Dame and Stanford; individual EMASI mapping remains exploratory |
| Biology | Expanded this revision | 4 | Stanford and Iowa State curriculum sources added; subplan differences retained |
| Mechanical Engineering | Expanded this revision | 4 | NUS, VinUniversity and Purdue curriculum sources added; cohort/plan scope retained |
| Finance | Curriculum evidence added | 4 | HKU and UIUC; cohort/degree structure matters |
| Chemistry | Expanded this revision | 4 | UC Berkeley, MIT and USTH curriculum sources added |
| Physics | Expanded this revision | 4 | Seoul National University, Cal Poly Pomona and Cornell curriculum sources added |
| Environmental Science | Curriculum evidence added | 5 | HCMUS and Iowa State; interdisciplinary scope retained |
| Architecture | Expanded this revision | 5 | MIT and NUS curriculum sources added; design, computation and building-technology links distinguished |
| Electrical Engineering | Curriculum evidence added | 4 | SIUE, Boston University and UCSD; pathway-specific requirements |
| Civil Engineering | Curriculum evidence added | 4 | Auburn, Illinois and Minnesota; plan-specific scope |
| Political Science | Curriculum evidence added | 4 | Stanford and Rice; research-methods focus |
| Sociology | Curriculum evidence added | 4 | Stanford and Johns Hopkins; research-methods/statistics focus |
| Linguistics | Curriculum evidence added | 4 | Stanford and Penn State; quantitative requirements vary |
| Education | Curriculum evidence added | 5 | UCI and University of Florida; learning/research/measurement focus |
| Accounting | Curriculum evidence added | 4 | Ton Duc Thang University and Foreign Trade University |
| Communication & Media Studies | Programme availability references | 5 | Curriculum-level evidence for each suggested EMASI subject remains incomplete |

## New official curriculum evidence added in this revision

### Biology
- Stanford University — undergraduate Biology major: Biology foundations, lab courses, and breadth courses in Chemistry, Mathematics, Physics, Statistics and/or Computer Science; exact requirements vary by subplan.
- Iowa State University — Biology degree requirements: biology core, calculus and/or statistics, chemistry sequences including organic chemistry/biochemistry, and physics options.

### Chemistry
- UC Berkeley — B.S. Chemistry: chemistry sequence with calculus, physics, multivariable calculus and linear algebra/differential equations.
- MIT — Chemistry Major & ChemFlex: inorganic, biological, organic, chemical science, thermodynamics/kinetics, spectroscopy and laboratory subjects.
- USTH — Bachelor in Chemistry: curriculum page includes analytical, inorganic, organic, physical, instrumental, polymer, materials and biochemistry-related courses. Cohort/year details should be checked before any current admissions claim.

### Physics
- Seoul National University — Physics & Astronomy undergraduate curriculum: mechanics, electromagnetism, electronics/measurement, quantum physics, thermal/statistical physics; electives include linear algebra and computational physics.
- Cal Poly Pomona — Physics major: calculus, computational methods, linear algebra, mechanics, electromagnetism/circuits and general chemistry.
- Cornell University — Physics BA: mechanics/heat, electromagnetism, waves/quantum physics and mathematics.

### Mechanical Engineering
- NUS — Mechanical Engineering curriculum (AY2025/26 onwards): mathematics, differential equations, linear algebra, mechanics/materials, mechatronics/automation, programming and design.
- VinUniversity — Mechanical Engineering: programme structure across general education, professional education, major foundations, concentration electives and capstone design.
- Purdue — Mechanical Engineering 2026–27 curriculum map: calculus, chemistry, physics, multivariable calculus, thermodynamics and mechanics.

### Architecture
- MIT — undergraduate Architecture: design studios, art/design/spatial practices, environmental technologies in buildings, structural design and design computing.
- NUS — BA Architecture curriculum: official cohort-based curriculum structure.


### Additional profiles expanded in this revision
- **Economics:** University of Notre Dame and Stanford — micro/macro economics, calculus, statistics, econometrics and quantitative mathematics.
- **Finance:** HKU and UIUC — accounting, economics, statistics, mathematics, corporate finance, investments and financial markets.
- **Environmental Science:** HCMUS and Iowa State — chemistry, ecology, geology, hydrology, statistics, GIS and supporting sciences.
- **Electrical Engineering:** SIUE, Boston University and UCSD — calculus, physics, programming/computing, circuits and systems; some requirements vary by depth.
- **Civil Engineering:** Auburn, UIUC and University of Minnesota — calculus, physics, chemistry, mechanics, computing and engineering design.
- **Political Science:** Stanford and Rice — methods courses, social-science statistics, data science and research seminars.
- **Sociology:** Stanford and Johns Hopkins — social research methods, data analysis and social statistics.
- **Linguistics:** Stanford and Penn State — phonetics/phonology, syntax, semantics, sociolinguistics, computational linguistics and selected statistics requirements.
- **Education:** UC Irvine and University of Florida — educational research design, statistics/data literacy, learning/development, measurement and educational technology.
- **Accounting:** Ton Duc Thang University and Foreign Trade University — accounting, auditing, tax, business law, economics, mathematics/statistics and information systems.
- **Communication & Media Studies:** Stanford and University of Oregon — communication theory, media/journalism, research methods, statistics, writing and media production.

## Product and research safeguards

1. Recommendations are labelled as exploration guidance, not mandatory school subjects or universal admissions requirements.
2. University course evidence is not treated as proof that the same content is taught in EMASI's current syllabus.
3. A source that confirms a programme exists is not treated as proof of its course content, admissions requirements, or career outcomes.
4. Institution-specific, cohort-specific and pathway-specific conditions are not generalized across universities.
5. No direct source is attached to a particular subject suggestion where the available evidence does not support that connection; those suggestions remain explicitly exploratory.
6. No evidence currently establishes that Horizon improves decision quality. Product impact must be tested with students before making outcome claims.

## Remaining work before a public release

- Obtain official EMASI course outlines/learning outcomes for all 13 subjects and relevant grade levels.
- Complete claim-by-claim review of each EMASI subject suggestion for all profiles. Profile-level curriculum claims are now present for all 20 majors, but this is not equivalent to 109 independently verified subject mappings.
- Review all Data Science guidance entries individually; its broad evidence set must not be mistaken for 10 independently verified mappings.
- Verify all source URLs and cohort dates immediately before public release.
- Conduct a full Streamlit interaction test in both languages, including mobile layout, profile comparison, network interactions, reflection saving/export, empty states and missing-data behavior.
- Run a student usability test and record feedback without claiming effectiveness in advance.

## Release decision

**Not ready for public release.** The present revision is suitable for controlled internal review and further testing only. No ZIP package is issued in this step.
