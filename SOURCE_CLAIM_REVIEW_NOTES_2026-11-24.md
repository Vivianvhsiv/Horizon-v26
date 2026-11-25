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
- Current verified source occurrences: 186. The APA duplicate was removed from the Psychology claim; the complete register count is calculated from all remaining claim-source pairs.

## Remaining review status

This is a targeted review of the claims and source records listed above, not completion of the full 65-claim semantic audit. Other claim families still need exact-page checks, especially programme availability, institution-specific curriculum classification (core/required/elective), and any profile statements about skills, research areas or career exploration that are not represented in the claim register.

## Additional programme-evidence scope review

A second pass found a repeated overstatement risk in programme-directory claims: a broad directory page or a programme list should not be described as verified for every exact degree title unless the exact undergraduate award is visible on that institution's current official page.

Changes made:
- Reclassified the first programme-reference claim for Computer Science, Data Science, Biology, Mechanical Engineering, Finance, Environmental Science, Architecture, Electrical Engineering, Civil Engineering, Sociology, Linguistics, Education, Accounting, and Communication & Media Studies as programme-availability evidence rather than implying curriculum evidence.
- Downgraded the programme-directory claim statuses for Psychology, Computer Science, Data Science, Economics, Biology, Mechanical Engineering, Finance, Chemistry, Physics, Environmental Science, Architecture, Electrical Engineering, Civil Engineering, Political Science, Sociology, Linguistics, Education, Accounting, and Communication & Media Studies. The register now asks for exact programme-title and undergraduate-award confirmation on each current institutional page before treating every entry as verified.
- Narrowed the Vietnamese-German University 2025 application-guideline entries under Mechanical Engineering and Electrical Engineering: they may support only programme names/admissions information explicitly stated in the document, not course content, curriculum or subject mappings.
- Rebuilt the CSV register from the JSON source of truth. Verified source occurrences: 186, regenerated from the JSON source of truth.

## Latest completed CI baseline (before this additional register edit)

On commit `8f234f9fbba4715d620834afb8cdbc5175e1d929`:
- Structural QA: 609/609 passed.
- Streamlit AppTest: 1 passed.
- Live source URL audit: 88 unique URLs checked; 80 reachable; 8 flagged for manual review.
- URL audit CSV artifact uploaded successfully.

The additional programme-status/source-scope edits above were committed after that run and require a fresh CI run. The earlier 86-URL / 76-reachable report is superseded by this 88-URL result.

## Additional official-source scope review — 24 November 2026

### Programme availability pages

- **Vietnamese-German University (VGU), 2025 Bachelor Application Guideline:** the document explicitly labels a table “VGU Bachelor Programs” and lists programme labels including Architecture, Civil Engineering and Construction Management, Computer Science, Electrical and Computer Engineering, Mechanical Engineering, Finance and Accounting, and a Major in Economics. This is valid evidence that those programme labels appeared in the 2025 application guideline. It is not a curriculum source, and the grouped labels must not be silently expanded into separate degree awards (for example, “Electrical Engineering” alone) or used to infer course content. Keep the existing scope limited to application/programme-list evidence.
- **University of Economics Ho Chi Minh City (UEH), Standard Programs:** the current programme overview explicitly lists Finance, Corporate Accounting, Economics and related named pathways. It is stronger than a generic university homepage for programme availability, but programme names must remain exact (for example, Corporate Accounting is not automatically identical to every Accounting degree).
- **Ton Duc Thang University (TDTU), Standard Programmes:** the official undergraduate programme list explicitly includes Accounting, Computer Science, Environmental Science, Architecture and Finance and Banking, among other programmes. This supports the listed programme labels only; it does not establish curriculum requirements.
- **Vietnam National University HCMC — University of Science (HCMUS), Module Handbook:** the page exposes module groupings including compulsory pre-major requirements and general-education electives. It is a module handbook for the faculty/programme context shown, not a general curriculum source for every major in Horizon. Its pre-major Computer Science module list includes programming, data structures and algorithms, databases, operating systems and computer systems; the same page also separates general-education electives such as Biology, Chemistry, Physics and Environmental Science. Do not describe those electives as CS prerequisites.

### Curriculum evidence

- **VinUniversity, B.S. Mechanical Engineering Curriculum Framework (2025, Intake 6):** the indexed framework separates College Core, Major Core, Major Foundation, Area of Concentration, internship and capstone. It lists calculus, linear algebra, probability/statistics, differential equations, physics, chemistry, programming, statics/mechanics, thermodynamics, dynamics, fluid mechanics, heat transfer, mechatronics and control. This is useful institution- and intake-specific curriculum evidence. It does not support universal Mechanical Engineering prerequisites or a direct EMASI subject equivalence.
- **VinUniversity, B.S. Electrical and Computer Engineering framework (2025; stated cohorts 2023–2027):** the framework identifies a College Core section including probability/statistics, calculus, differential equations and linear algebra. Any additional claim about electrical engineering major-core content must be checked against the full framework sections, not inferred from the College Core table alone.

### Resulting interpretation

These spot-checks strengthen a small number of named programme-availability and curriculum references, but they do not complete the page-by-page review of all 65 claims. Exact programme titles, award level, cohort and course classification remain essential. Directory or application pages are not interchangeable with curriculum pages, and a course listed under general education or electives must not be relabelled as a compulsory major prerequisite.

## Data Science — VinUniversity cohort-specific curriculum check

- Replaced the generic VinUniversity academic-catalogue index attached to the Data Science cross-institution claim with a specific institution-level curriculum claim.
- The official VinUniversity programme page identifies the B.S. Data Science degree structure (including College Core, Major/Discipline Requirements, Discipline Electives, Free Electives, projects, internship and capstone) and publishes course descriptions such as Discrete Mathematics, Data Science Programming, Machine Learning, Databases and Data Visualization.
- Added the official 2025–2029 cohort curriculum framework PDF as the cohort-specific framework source. The claim is now explicitly limited to VinUniversity and that published cohort framework; it must not be generalized into universal Data Science prerequisites or assumed EMASI subject equivalence.
- The programme page and framework should be treated as complementary: the webpage supports the displayed programme/course descriptions, while the PDF establishes the stated cohort scope. Course status must follow the actual framework classification rather than being inferred from a course description alone.


### Economics — curriculum claim: Notre Dame and Stanford degree-specific requirements

- Rechecked the official Notre Dame Economics major requirements and Stanford Economics B.S. requirements pages.
- Rewrote the claim to distinguish Notre Dame's six-course core (including microeconomics, macroeconomics, Statistics for Economics and Econometrics) from Calc B, which is explicitly a prerequisite, not one of the named core courses.
- Rewrote the Stanford portion to name the B.S.-specific quantitative core: Theory of Probability I, Econometrics, Linear Algebra/Multivariable Calculus, and Functions of a Real Variable.
- Added scope notes so the Stanford B.S. is not generalized to the B.A. or other institutions. These sources provide university-level curriculum context only; they do not establish universal admissions prerequisites or verified EMASI subject equivalence.
- Sources: https://economics.nd.edu/undergraduate/economics-major/requirements/ and https://economics.stanford.edu/undergraduate/major/economics-bs

## Follow-up source-page verification — 25 November 2026

### Cognitive Science — claim 5: UC Irvine 2026–27 comparison

**Exact-page check:** Reopened the official UC Irvine Department of Cognitive Sciences undergraduate comparison and cross-checked the 2026–27 catalogue degree requirements for the B.S. in Cognitive Sciences and B.S. in Psychology.

**Confirmed details:** Both degree routes list psychology fundamentals, three statistics courses, programming, and a six-course science background. The B.S. in Cognitive Sciences additionally requires two single-variable calculus courses, a Cognitive Sciences research seminar, and selection from computational/statistical-learning core options including Statistical Learning, Computational Lab Skills, Cognitive Modeling and Neural Analytics. The Psychology B.S. has a different upper-division psychology core and research-methods structure.

**Decision:** KEEP, with institution- and catalogue-year-specific scope. The existing claim accurately describes the principal differences, but must not be generalized to other universities or treated as an EMASI subject-equivalence claim.

**Official pages inspected:**
- https://www.cogsci.uci.edu/undergraduate/
- https://catalogue.uci.edu/schoolofsocialsciences/departmentofcognitivesciences/cognitivesciences_bs/
- https://www.cogsci.uci.edu/undergraduate/bspsych.php

**Limit:** This is one claim-level verification, not completion of the full 65-claim audit.

### Computer Science — claim 3: HCMUT curriculum context

**Exact-page check:** Inspected HCMUT's official international study-program page for the Bachelor of Engineering in Computer Science.

**Confirmed details on the page's displayed referential curriculum:** Year 1 includes Calculus, Discrete Structures, Discrete Structures for Computing, General Chemistry, General Physics, Introduction to Computing, Linear Algebra, Programming Fundamentals and Physics Experiments. Year 2 includes Computer Architecture, Data Structures and Algorithms, Database Systems, Object-Oriented Programming, Operating Systems, Mathematical Modeling, Numerical Methods, and Probability and Statistics. Later years include algorithms design and analysis, computer networks, programming languages and software engineering.

**Decision:** KEEP as institution-specific curriculum context. The page labels the displayed curriculum as referential and directs readers to a separate location for detailed/latest updates. Do not imply that this exact plan is universal across Computer Science degrees, and do not infer that any EMASI high-school subject is an admissions prerequisite or syllabus-equivalent.

**Official page inspected:** https://oisp.hcmut.edu.vn/en/study-programs/bachelor-degree/computer-science

**Limit:** This verifies the HCMUT portion of the multi-institution claim only; UCL, NUS and VinUniversity require their own exact-page checks.

### Data Science — claim 3: UCL curriculum context

**Exact-page check:** Inspected UCL's official Data Science BSc course page for 2026 entry and its published course structure.

**Confirmed details:** UCL describes the degree as combining statistical foundations with computing skills and algorithmic reasoning. Its listed compulsory modules include database systems, calculus and linear algebra, probability and statistics, practical statistics, programming fundamentals, algorithms and data structures, statistical design and data ethics, statistical machine learning, inference at scale and a final-year project. The page identifies application areas such as medicine and commerce as specialist options rather than implying that all students follow identical domain pathways.

**Decision:** KEEP as institution-specific curriculum context for mathematics, statistics, computing/programming, data management and machine learning. Retain the caveat that course balance and options vary by programme and year. This is not evidence of EMASI syllabus equivalence or a universal admissions prerequisite.

**Official page inspected:** https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/data-science-bsc-2026

**Limit:** This verifies the UCL portion only; other institutions and the ACM curriculum guidance in the same multi-source claim require separate checks.
