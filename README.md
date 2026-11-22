# Horizon v25.5 — Bilingual Academic Exploration Platform (Development Candidate)

Horizon is a student-led exploration prototype for EMASI high-school students. It helps students explore possible connections among interests, current school subjects, academic disciplines, university majors and possible career areas.

## Languages
- English
- Tiếng Việt

The major profile sections, academic evidence labels and EMASI subject names have paired English/Vietnamese content. Official university names, programme titles and source-page titles remain in their original published language so that students can locate and verify the source.

## Current EMASI subject inventory
The selector includes 13 subjects: Mathematics, Literature, English, Physics, Biology, Chemistry, Music, Fine Arts, ICT, Economics and Law, Technology, Geography and History.

Geography and History were added as exploratory inputs (S12 and S13). Their presence does not mean that every university programme requires them. Subject connections are suggestions for exploration, not universal admission prerequisites or judgements of student suitability.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open `http://localhost:8501`.

## Deploy to Railway (private test first)
The repository includes a `Procfile` and `RAILWAY_DEPLOY.md`. Deploy from a private GitHub repository and restrict access to invited testers where the hosting plan supports it. A private source repository does not automatically make the deployed website private; configure access control separately.

## Project structure
- `app.py` — Streamlit application
- `majors.json` and `data/majors.json` — 20 bilingual major profiles
- `academic_sources.json` and `data/academic_sources.json` — source and claim records
- `data/emasi_subjects.json` — the 13-subject inventory
- `data/emasi_mapping_protocol.json` — evidence and mapping rules
- `qa_check.py` — original offline structural QA
- `qa_v25_2.py` — evidence transparency and data-integrity QA
- `qa_v25_3.py` — source-register completeness and integrity QA
- `audit_source_urls.py` — optional live URL reachability check (does not verify claim accuracy)
- `SOURCE_AUDIT_GUIDE.md` — instructions for live and manual source review
- `SOURCE_URL_INVENTORY_V25_2.csv` — 86 distinct URLs consolidated from 186 source occurrences
- `QA_RESULTS_V25_2.txt` — v25.2 QA results
- `QA_RESULTS_V25_3.txt` — v25.3 QA results
- `SOURCE_URL_INVENTORY_V25_2.csv` — 86 distinct URLs consolidated from 186 source occurrences

## Evidence and limitations
University programme pages and curricula support descriptions of university-level subject areas. They do not automatically establish EMASI course equivalence or universal admission requirements. EMASI mapping remains exploratory until the actual EMASI syllabi and grade-level learning outcomes are compared with the relevant university curricula. Requirements vary by institution, programme, pathway and admission year.

## Validation status

This v25.3 package builds on the v25.2 consolidated evidence audit and per-major evidence coverage display. It adds an explicit scope/limitation note to every source-claim row and includes an optional live URL reachability audit script. See `HORIZON_V25_1_AUDIT_REPORT.md`, `HORIZON_V25_2_IMPROVEMENT_REPORT.md`, `EMASI_13x20_AUDIT_MATRIX.csv`, `SOURCE_CLAIM_REGISTER.csv`, `SOURCE_URL_INVENTORY_V25_2.csv`, and `RELEASE_READINESS_V25_2.md`.
The offline QA scripts check JSON integrity, bilingual field coverage, subject inventory consistency, source metadata, HTTPS URL format, absence of CJK characters in user-facing app/data files and Python syntax. v25.3 additionally checks that all 186 source-claim rows have an explicit scope/limitation. Run `python audit_source_urls.py` in a network-enabled environment to check URL reachability; this does not prove claim accuracy. The build does not provide Vietnamese academic copy-editing or replace a full browser/mobile interaction test.

## v25.5 evidence coverage audit
- Run `python build_evidence_coverage_report.py` to regenerate the per-major evidence inventory.
- Run `python qa_v25_5.py` to reconcile report counts against the source register and EMASI audit matrix.
- The inventory is not academic validation; see `EVIDENCE_COVERAGE_REPORT_V25_5.md` and `RELEASE_READINESS_V25_5.md`.
