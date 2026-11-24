# Source and claim audit — Horizon Network Map / Explore Majors

Audit date: 2026-11-24  
Branch: `horizon-network-map-fix`  
Scope: 20 major profiles, 65 academic claims, 186 source occurrences, and the visible career / subject-guidance presentation.

## Findings and changes

1. **Generic profile-reference labels were not acceptable.** The major profiles contained links labelled `Reference organisation` and generic titles such as `academic reference 1`. These links were removed from the profile layer rather than displaying a vague or misleading source identity. Claim-level academic sources remain in `academic_sources.json` and are still rendered with the named institution, title and URL.
2. **Career lists are exploratory.** The `careers` field is not individually sourced as a labour-market outcome or promise. The UI now explicitly describes these as illustrative areas to explore, not guaranteed job outcomes or a ranking of pathways. The Vietnamese UI carries the same limitation.
3. **Subject-to-major links remain exploratory.** The 109 EMASI subject suggestions are not verified as EMASI syllabus matches or universal admissions prerequisites. Programme curricula provide context only. No programme-specific verified EMASI subject connections are populated.
4. **Source scope must stay claim-specific.** A university programme directory can support programme availability only when the exact programme label is visible; a curriculum page supports only the listed institution, cohort and degree route. It must not be generalized to all universities or to EMASI requirements.
5. **Data Science subject references were narrowed in the preceding commit.** Each suggestion now has only relevant sources and bilingual statements of what those sources support. Music and Geography remain explicitly exploratory without attached curriculum citations.

## Web spot-checks completed in this pass

The following official pages were opened and inspected for title / page context:

- Dartmouth College, *About the Major* — Cognitive Science.
- University of California, Irvine, *B.S. Degree in Cognitive Sciences*.
- American Economic Association, *What Is Economics?*.
- ABET, *Criteria for Accrediting Engineering Programs, 2025–2026*.
- CFA Institute, *CFA Program* (confirmed this is a professional credential pathway, not an undergraduate Finance degree).
- American Association of Physics Teachers, *Policy and Legislation* (confirmed this page is policy material, not a curriculum reference).
- American Political Science Association homepage (association homepage, not a major curriculum page).
- American Sociological Association, *Teaching & Learning*.
- Linguistic Society of America website (legacy URL redirects to the current LSA domain).
- AACSB homepage (business-school accreditation and membership context, not an Accounting major curriculum).
- National Communication Association homepage.

Additional official curriculum spot-checks surfaced in current search results include UCL Data Science BSc, UCL Computer Science BSc, UCL Psychology BSc, UC San Diego Psychology, and UC San Diego Cognitive Science programme pages.

## Limitations

- A page being reachable is not proof that every claim attached to it is supported.
- Some association, accreditation and programme-directory links are context sources, not curriculum evidence.
- The full 86-URL reachability audit and a page-by-page manual verification of all 65 claims are not represented as complete by this report.
- No career-outcome dataset or graduate-employment evidence is currently attached to the career lists. They are therefore presented as exploratory examples.
- English / Vietnamese content presence is structurally checked; this report does not claim native-editor approval of every Vietnamese sentence.

## Next verification work

- Review each curriculum claim against the exact page, cohort and course classification (core / required / elective / optional).
- Review programme-availability claims against the exact programme label and degree level shown in each official directory.
- Keep any inaccessible, stale or ambiguous source at `Needs manual review` rather than treating it as verified.
