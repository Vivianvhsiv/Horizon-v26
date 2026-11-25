# Horizon Evidence & Source Standard — V26

Last updated: 2026-11-25

## Purpose

Horizon helps students discover concrete academic directions, understand fields, and compare them. It does not assess personal suitability, rank majors, predict success, or make a student's decision.

Every factual academic statement and every displayed academic relationship must be traceable to evidence at the level of the claim. A source link attached to a major profile does not automatically support every item in that profile.

## 1. Evidence record requirements

Each evidence record should identify:

- **Claim** — one precise statement Horizon makes.
- **Source institution / publisher** — who published the evidence.
- **Source title and direct URL** — the exact page, catalogue, framework, or document.
- **What it supports** — the specific portion of the claim supported by the source.
- **Scope** — institution, programme, degree level, cohort/catalogue year, pathway, and whether the item is required, elective, optional, or illustrative when relevant.
- **Verification status** — the review state of this exact claim.
- **Review date and reviewer** — required for future human-reviewed records.

Do not reuse one source as blanket support for unrelated fields.

## 2. Evidence status vocabulary

- **Verified** — the exact source was inspected and directly supports the stated claim within the stated scope.
- **Partially supported** — the source supports only part of the claim, or the exact programme / degree / cohort scope still needs confirmation. Do not present the unsupported portion as fact.
- **Exploratory** — useful as a question or research direction, but not established as a verified relationship.
- **Unreviewed** — not yet checked against the exact source. Do not style it as verified.
- **Needs correction** — source does not support the claim, is stale, or is incorrectly scoped. Remove or rewrite the claim before display as fact.

A URL being reachable is not evidence that it supports a claim. A source being official is not proof that it supports every item in the profile.

## 3. Preferred source hierarchy

1. Current official university academic catalogues, approved programme specifications, cohort-specific curriculum frameworks, and official course descriptions for institution-specific curriculum claims.
2. Official department / faculty programme pages for disciplinary descriptions and programme context.
3. Recognized professional or academic associations for disciplinary definitions, professional education frameworks, and discipline-wide guidance, with their actual scope stated.
4. Peer-reviewed research and authoritative scholarly publications for specific academic concepts or research areas.
5. General reference material may be used only as supplementary context, not as proof of a university requirement.

For curriculum requirements, prefer the applicable official catalogue or approved programme framework. Do not infer requirements from promotional pages or programme directories alone.

## 4. Scope and wording rules

- Distinguish degree requirements, compulsory courses, electives, optional pathways, examples, and suggested preparation.
- Identify institution and cohort/catalogue year whenever curriculum details are stated.
- Never generalize one university's curriculum into a universal requirement for a major.
- Never describe an EMASI school subject as a university prerequisite unless a current, authoritative admissions source explicitly says so.
- University curriculum context does not establish equivalence with EMASI syllabus content.
- Programme availability evidence does not establish curriculum, admissions, accreditation, or personal suitability.
- Career lists and skills are exploratory unless supported by dedicated evidence; do not promise employment outcomes.
- Student interests, strengths, and subject choices are not evidence of aptitude or personal fit.

## 5. Application to the three modules

### Network Map
- Every academic relationship edge must have a claim-level evidence record that explicitly names the relationship.
- Display the supporting claim, verification status, named source, and scope beside the edge.
- Only directly supported, verified relationships may appear as established academic connections.
- Catalogue grouping edges must be clearly identified as Horizon navigation categories, not academic findings.
- Do not create interest-to-major matching or infer personal fit.
- If no suitable claim exists, omit the academic edge rather than fabricate a relationship.

### Explore Majors
- Each displayed academic profile item should expose the exact claim and source that supports it.
- If no direct claim-level record is mapped, label the item as exploratory profile context and state that no direct source is mapped yet.
- Display programme scope and limitations; do not imply that every source validates the whole profile.
- Subject guidance remains exploratory unless a programme-specific claim is separately reviewed.

### Compare Majors
- Keep the side-by-side comparison as the primary student-facing experience.
- For each compared item, show its own supporting claim and sources, not only a general bibliography for the major.
- If one side has stronger evidence than another, make the difference visible; do not imply equal evidence coverage.
- Do not calculate a best-fit score or announce a winning major.

## 6. Current implementation notes

The app uses `academic_sources.json` as its claim-level source register. The shared UI helper matches an individual English profile item only when its wording appears in a recorded claim. This is a conservative traceability aid, not an automated semantic verification system.

- Network Map discipline links are created only when an explicitly named profile item appears in a claim whose status begins with `Verified`, and source metadata is attached to the edge.
- Explore Majors and Compare Majors show matching claim text, status, and source links for individual profile items.
- Items without a direct phrase-level claim match are labelled as exploratory and unsourced at item level.
- Human review is still required for every claim, source passage, and translation. Structural QA does not certify academic correctness.

## 7. Authoritative guidance consulted

- James Madison University, *Curriculum Guidelines for Websites*: states that official university catalogs are the source for curricular requirements and that other materials should direct readers to the catalog.
  https://www.jmu.edu/faculty/faculty-affairs/curriculum/website-guidelines.shtml
- VinUniversity, *Academic Regulations for Full-Time Undergraduate Programs*, Article 3: distinguishes programme structure from course syllabi and describes course content, prerequisites, assessment, and references.
  https://policy.vinuni.edu.vn/all-policies/academic-regulations-for-full-time-undergraduate-programs/
- VinUniversity, *Academic Catalogs*: identifies catalogues and cohort-specific curriculum frameworks as the programme/curriculum reference material.
  https://policy.vinuni.edu.vn/publication/academic-catalogs/

