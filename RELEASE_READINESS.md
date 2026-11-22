# Horizon v24 — Release Readiness

## Current state
v24 is a corrected bilingual working package prepared for a controlled test deployment. It is not yet certified as a public release.

## Completed
- 20 major profiles retained.
- Five academic profile sections have English and Vietnamese content in all 20 profiles.
- Academic evidence source-type labels display in Vietnamese when the Vietnamese interface is selected.
- Geography (S12) and History (S13) are included in the 13-subject inventory and interactive subject selector.
- Root and `data/` copies of the major and academic-source registries are synchronized.
- Offline structural QA and Python syntax checks pass; see `QA_RESULTS.txt`.
- Private-test deployment instructions and Railway start command are included.

## Required before student pilot
1. Install dependencies in a network-enabled environment and run the Streamlit app.
2. Test both languages across home, network, major detail, comparison, reflection and about pages.
3. Test the network interactions and all 13 subject choices.
4. Test phone and desktop layouts.
5. Configure access control before sharing the deployed URL.
6. Have a Vietnamese academic editor review technical terminology.
7. Obtain EMASI syllabi and grade-level learning outcomes before claiming exact subject-to-major curriculum alignment.

## Important limits
The website is an exploration aid, not an aptitude test, admission predictor or major-selection decision-maker. Subject guidance is exploratory and should not be interpreted as a universal prerequisite. Existing university source records need periodic live-link and programme-year review.

## Deployment gate
Proceed with a private test deployment only after the owner confirms this v24 package. Do not switch the site to public visibility until interaction, access-control and privacy checks are complete.
