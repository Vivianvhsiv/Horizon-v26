"""Offline QA for v25.4 source-audit tooling and evidence boundaries."""
import ast, csv, json, pathlib
R = pathlib.Path(__file__).resolve().parent
checks = []
def ck(ok, label): checks.append((bool(ok), label))
maj = json.loads((R/'data/majors.json').read_text(encoding='utf-8'))
subjects = json.loads((R/'data/emasi_subjects.json').read_text(encoding='utf-8'))['subjects']
with (R/'SOURCE_CLAIM_REGISTER.csv').open(encoding='utf-8-sig', newline='') as f: claims = list(csv.DictReader(f))
with (R/'EMASI_13x20_AUDIT_MATRIX.csv').open(encoding='utf-8-sig', newline='') as f: matrix = list(csv.DictReader(f))
with (R/'academic_sources.json').open(encoding='utf-8') as f: sources = json.load(f)
ck(len(maj) == 20, '20 major profiles')
ck(len(subjects) == 13, '13 EMASI subjects')
ck(len(matrix) == 260, '260 audit matrix pairs')
ck(len(claims) == 186, '186 source-claim register rows')
ck(set(r['Major'] for r in claims) == set(maj), 'Every major represented in source-claim register')
ck(all(r['URL'].startswith('https://') for r in claims), 'All claim URLs use HTTPS')
ck(all(r['Institution'] and r['Source Title'] and r['Source Type'] for r in claims), 'Claim rows have institution, title and source type')
ck(all(r['Scope / Limitation'] for r in claims), 'Every claim row states its evidence scope/limitation')
ck(len({r['URL'] for r in claims}) == 86, '86 distinct source URLs')
ck(set(sources) == set(maj), 'Academic source registry covers the same 20 majors')
# Critical distinction: programme availability records are not school-subject mapping evidence.
availability = [r for r in claims if r['Claim Type'] == 'Programme availability evidence']
ck(len(availability) == 78, 'Programme availability claims explicitly countable (not mapping proof)')
ck((R/'audit_source_urls.py').exists(), 'Live URL audit script present')
try:
    ast.parse((R/'audit_source_urls.py').read_text(encoding='utf-8'))
    ck(True, 'Live URL audit script syntax valid')
except SyntaxError as e: ck(False, f'Live URL audit script syntax invalid: {e}')
try:
    ast.parse((R/'app.py').read_text(encoding='utf-8'))
    ck(True, 'Streamlit app syntax valid')
except SyntaxError as e: ck(False, f'Streamlit app syntax invalid: {e}')
ck((R/'majors.json').read_bytes() == (R/'data/majors.json').read_bytes(), 'Major registries synchronized')
ck((R/'academic_sources.json').read_bytes() == (R/'data/academic_sources.json').read_bytes(), 'Source registries synchronized')
for ok, label in checks: print(('PASS' if ok else 'FAIL') + ' ' + label)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
