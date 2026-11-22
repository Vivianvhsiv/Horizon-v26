# Bilingual Coverage Audit — v25.9

The offline QA extracts the literal English and Vietnamese UI dictionaries from `app.py`, compares their key sets, and checks that all 20 major profiles and 13 EMASI subject labels contain the expected bilingual fields.

A matching key set and non-empty values establish structural coverage only. They do not establish translation accuracy, natural Vietnamese phrasing, consistency of academic terminology, accessibility, or visual fit on mobile screens. Those require a fluent human reviewer and browser testing in both languages.

## Human review checklist
- Check academic terms consistently across navigation, major descriptions, subject labels, reflection prompts, and evidence notes.
- Check that Vietnamese phrasing is natural for Vietnamese high-school students and does not imply a deterministic suitability judgement.
- Check line wrapping, truncation, chart/node labels, and download summaries on phone-sized screens.
- Confirm that English and Vietnamese caveats communicate the same limitations.
