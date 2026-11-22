"""Offline integration/regression QA for Horizon v25.8.

Checks structural consistency across application data, evidence registers,
traceability artifacts and human-review queues. It does not validate the
truth of external sources or EMASI curriculum relationships.
"""
import csv, json, pathlib, subprocess, sys, ast
R = pathlib.Path(__file__).resolve().parent
checks = []
def ck(value, label): checks.append((bool(value), label))
def read_csv(name):
    with (R/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
def read_json(name):
    return json.loads((R/name).read_text(encoding='utf-8'))

majors = read_json('majors.json')
academic = read_json('academic_sources.json')
majors_data = read_json('data/majors.json')
academic_data = read_json('data/academic_sources.json')
subjects_doc = read_json('data/emasi_subjects.json')
protocol = read_json('data/emasi_mapping_protocol.json')
source_register = read_csv('SOURCE_CLAIM_REGISTER.csv')
ledger = read_csv('SOURCE_TRACEABILITY_LEDGER_V25_6.csv')
matrix = read_csv('EMASI_13x20_AUDIT_MATRIX.csv')
crosswalk = read_csv('MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv')
source_queue = read_csv('SOURCE_PAGE_REVIEW_QUEUE_V25_7.csv')
matrix_queue = read_csv('MATRIX_PAIR_REVIEW_QUEUE_V25_7.csv')

# Core data synchronization and shape.
ck(majors == majors_data, 'Root and data major registries are byte-equivalent in parsed content')
ck(academic == academic_data, 'Root and data academic-source registries are synchronized')
ck(set(majors) == set(academic), 'Every major has a matching academic-source profile')
ck(len(majors) == 20, 'Exactly 20 major profiles are present')
ck(all(isinstance(v, dict) and all(k in v for k in ['name_vi','overview','overview_vi','caveat','caveat_vi']) for v in majors.values()), 'Major profiles contain core bilingual explanation and caveat fields')
ck(all(isinstance(v.get('subjects'), list) and isinstance(v.get('careers'), list) for v in majors.values()), 'Major subject and career fields retain list structure')

# EMASI subject and protocol integrity.
subjects = subjects_doc.get('subjects', [])
subject_ids = [s.get('id') for s in subjects]
subject_names_en = [s.get('name_en') for s in subjects]
subject_names_vi = [s.get('name_vi') for s in subjects]
ck(len(subjects) == 13, 'Exactly 13 EMASI exploration subjects are present')
ck(len(set(subject_ids)) == 13 and all(subject_ids), 'EMASI subject IDs are present and unique')
ck(len(set(subject_names_en)) == 13 and all(subject_names_en), 'English subject names are present and unique')
ck(len(set(subject_names_vi)) == 13 and all(subject_names_vi), 'Vietnamese subject names are present and unique')
ck(len(protocol.get('relationship_types', [])) == 3, 'Mapping protocol defines three relationship types')
ck('No evidence, no confirmed connection.' in protocol.get('principle',''), 'Mapping protocol preserves its no-evidence/no-confirmation principle')
ck('Pending Verification' in protocol.get('verification_statuses', []), 'Mapping protocol retains pending verification status')

# Matrix, source and review-queue linkage integrity.
ck(len(matrix) == 260 and len(crosswalk) == 260 and len(matrix_queue) == 260, 'All 260 major-subject pairs exist in all three matrix artifacts')
ck(len(source_register) == 186 and len(ledger) == 186 and len(source_queue) == 186, 'All 186 source records exist in register, ledger and review queue')
ck(len({r['Matrix Pair ID'] for r in crosswalk}) == 260, 'Matrix pair IDs are unique')
ck(len({r['Source Row ID'] for r in ledger}) == 186, 'Source row IDs are unique')
ck([r['Matrix Pair ID'] for r in crosswalk] == [r['Matrix Pair ID'] for r in matrix_queue], 'Matrix queue preserves crosswalk IDs and ordering')
ck([r['Source Row ID'] for r in ledger] == [r['Source Row ID'] for r in source_queue], 'Source queue preserves ledger IDs and ordering')
ck(all(r['Major'] in majors for r in matrix), 'Every matrix row references a known major')
ck(all(r['Subject ID'] in subject_ids for r in matrix), 'Every matrix row references a known EMASI subject ID')
ck(all(r['Major'] in majors for r in source_register), 'Every source-register row references a known major')
ck(all(r['Source Register Row Link'].startswith('UNRESOLVED') for r in crosswalk), 'Unconfirmed source-to-matrix links remain unresolved')
ck(all(r['EMASI Syllabus Validation'] == 'NOT PROVIDED / NOT VERIFIED' for r in crosswalk), 'No matrix pair is falsely marked as EMASI syllabus-verified')
ck(all(r['Review Decision (UNREVIEWED/ACCEPTED/REJECTED/NEEDS FOLLOW-UP)'] == 'UNREVIEWED' for r in source_queue), 'Source review decisions remain unreviewed until human input')
ck(all(r['Guidance Decision (KEEP EXPLORATORY/REVISE/REMOVE/ELIGIBLE FOR FURTHER REVIEW)'] == 'KEEP EXPLORATORY' for r in matrix_queue), 'Matrix guidance remains exploratory by default')
ck(all(not r['Exact Supporting Passage or Precise Paraphrase'] for r in source_queue), 'No source passage is fabricated in review queue')
ck(all(not r['Exact EMASI Evidence or Precise Paraphrase'] for r in matrix_queue), 'No EMASI evidence is fabricated in review queue')

# Executable and documentation regression checks.
for name in ['app.py','audit_source_urls.py','build_claim_traceability_v25_6.py','build_evidence_coverage_report.py','build_review_workflow_v25_7.py']:
    try:
        ast.parse((R/name).read_text(encoding='utf-8'))
        ok = True
    except Exception:
        ok = False
    ck(ok, f'{name} parses as valid Python')
for name in ['README_V25_7.md','HUMAN_EVIDENCE_REVIEW_PROTOCOL_V25_7.md','EVIDENCE_TRACEABILITY_REPORT_V25_6.md']:
    ck((R/name).is_file() and (R/name).stat().st_size > 100, f'{name} is present and non-empty')
ck('not a verified status' in (R/'HUMAN_EVIDENCE_REVIEW_PROTOCOL_V25_7.md').read_text(encoding='utf-8'), 'Human review protocol distinguishes review eligibility from verification')

# Run historical QA chain to detect regressions.
for name in ['qa_check.py','qa_v25.py','qa_v25_1.py','qa_v25_2.py','qa_v25_3.py','qa_v25_4.py','qa_v25_5.py','qa_v25_6.py','qa_v25_7.py']:
    result = subprocess.run([sys.executable, str(R/name)], capture_output=True, text=True)
    ck(result.returncode == 0, f'Historical {name} passes')

for ok, label in checks:
    print(('PASS ' if ok else 'FAIL ') + label)
print(f'Summary: {sum(ok for ok, _ in checks)}/{len(checks)} passed')
if not all(ok for ok, _ in checks):
    raise SystemExit(1)
