"""Offline QA for v25.3 source-register completeness and safety of evidence claims."""
import ast,csv,json,pathlib
R=pathlib.Path(__file__).resolve().parent
checks=[]
def ck(x,m): checks.append((bool(x),m))
maj=json.loads((R/'data/majors.json').read_text(encoding='utf-8'))
subs=json.loads((R/'data/emasi_subjects.json').read_text(encoding='utf-8'))['subjects']
with (R/'SOURCE_CLAIM_REGISTER.csv').open(encoding='utf-8-sig',newline='') as f: reg=list(csv.DictReader(f))
with (R/'EMASI_13x20_AUDIT_MATRIX.csv').open(encoding='utf-8-sig',newline='') as f: matrix=list(csv.DictReader(f))
ck(len(maj)==20,'20 major profiles retained')
ck(len(subs)==13,'13 EMASI subjects retained')
ck(len(matrix)==260,'260 major-subject audit pairs retained')
ck(len(reg)==186,'186 source-claim rows retained')
ck(all(r.get('URL','').startswith('https://') for r in reg),'All source register URLs use HTTPS')
ck(all(r.get('Institution','').strip() and r.get('Source Title','').strip() and r.get('Source Type','').strip() for r in reg),'Every source row has institution, title and source type')
ck(all(r.get('Scope / Limitation','').strip() for r in reg),'Every source row has an explicit scope/limitation')
ck(len({r['URL'] for r in reg})==86,'86 distinct URLs retained')
ck((R/'audit_source_urls.py').exists(),'Optional live URL audit tool included')
ck((R/'SOURCE_URL_LIVE_AUDIT.csv').exists() is False,'No unrun live URL audit is falsely presented as completed')
ck((R/'majors.json').read_bytes()==(R/'data/majors.json').read_bytes(),'Root and data major registries synchronized')
ck((R/'academic_sources.json').read_bytes()==(R/'data/academic_sources.json').read_bytes(),'Root and data source registries synchronized')
try: ast.parse((R/'app.py').read_text(encoding='utf-8')); ck(True,'app.py syntax valid')
except SyntaxError as e: ck(False,f'app.py syntax invalid: {e}')
for ok,msg in checks: print(('PASS' if ok else 'FAIL')+' '+msg)
print(f'Summary: {sum(ok for ok,_ in checks)}/{len(checks)} passed')
if not all(ok for ok,_ in checks): raise SystemExit(1)
