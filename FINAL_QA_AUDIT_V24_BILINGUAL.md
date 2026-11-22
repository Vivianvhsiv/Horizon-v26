# Horizon v24 — Final Structural QA Audit

## Scope
This audit covers the bilingual major-profile sections, evidence labels, EMASI subject inventory, app/data consistency and static application checks.

## Completed checks
- 20 major profiles retained.
- Five profile sections have aligned English and Vietnamese lists in every major: academic foundations, related disciplines, specialized applications, research directions, and scope/limitations.
- Vietnamese academic-source status, scope, claim labels and source-type labels are present.
- 13 EMASI subjects are registered with unique IDs.
- 109 subject-guidance records are present with bilingual fields; 9 include Geography and 9 include History.
- Geography is S12 and History is S13; both are present in the interactive subject selector.
- Root and `data/` copies of the major and academic-source JSON files are byte-identical.
- No CJK characters remain in the user-facing app and primary data files checked.
- Academic source URLs use HTTPS format.
- Python syntax and JSON parsing checks pass.
- Offline QA script result: 574/574 checks passed.

## Interpretation limits
Geography and History recommendations remain exploratory. They are not represented as universal university prerequisites. University curriculum evidence does not, by itself, prove equivalence with EMASI teaching content. The actual EMASI syllabus and grade-level learning outcomes are still needed for that comparison.

## Not yet verified
- External URLs were not all re-opened and revalidated in this pass.
- Vietnamese academic copy has not received independent native-speaker editorial review.
- Streamlit could not be installed in this environment because package-network access was unavailable. Full browser interaction, mobile layout and deployment access-control tests remain outstanding.

Run `python qa_check.py` to repeat the offline structural checks.
