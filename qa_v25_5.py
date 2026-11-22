"""Offline QA for v25.5 evidence-coverage inventory."""
import csv, json, pathlib, subprocess, sys
R = pathlib.Path(__file__).resolve().parent
checks = []
def ck(ok, label): checks.append((bool(ok), label))

def rows(name):
    with (R/name).open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

claims = rows('SOURCE_CLAIM_REGISTER.csv')
matrix = rows('EMASI_13x20_AUDIT_MATRIX.csv')
majors = json.loads((R/'data/majors.json').read_text(encoding='utf-8'))
summary = rows('EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv')
ck(len(summary) == 20, 'Coverage report contains all 20 majors')
ck(len(matrix) == 260, 'Input matrix contains 260 major-subject pairs')
ck(len(claims) == 186, 'Input register contains 186 source-claim rows')
ck(sum(int(r['Source Claim Rows']) for r in summary) == len(claims), 'Per-major claim counts reconcile to source register')
ck(sum(int(r['EMASI Subject Pairs']) for r in summary) == len(matrix), 'Per-major pair counts reconcile to audit matrix')
ck(sum(int(r['Programme Availability Only Rows']) for r in summary) == 78, 'Programme-availability rows remain separately classified')
ck(sum(int(r['Pairs With No Guidance Entry']) for r in summary) == 151, 'No-guidance pair count reconciles')
ck(sum(int(r['Pairs Marked Exploratory Not EMASI Verified']) for r in summary) == 109, 'Exploratory pair count reconciles')
ck(sum(int(r['EMASI Syllabus Verified Pairs']) for r in summary) == 0, 'No unsupported EMASI verification is asserted')
ck({r['Major'] for r in summary} == set(majors), 'Coverage report major names match profile registry')
report = (R/'EVIDENCE_COVERAGE_REPORT_V25_5.md').read_text(encoding='utf-8')
ck('not an academic validation' in report.lower(), 'Report states that it is not academic validation')
ck('Programme availability is not curriculum evidence' in report, 'Report separates programme availability from curriculum evidence')
ck('No EMASI syllabus-verified pair is currently labelled' in report, 'Report preserves EMASI syllabus verification boundary')
for ok, label in checks: print(('PASS ' if ok else 'FAIL ') + label)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
