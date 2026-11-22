import json, ast, pathlib, csv
ROOT=pathlib.Path(__file__).resolve().parent
majors=json.loads((ROOT/'data/majors.json').read_text(encoding='utf-8'))
subjects=json.loads((ROOT/'data/emasi_subjects.json').read_text(encoding='utf-8'))['subjects']
app=(ROOT/'app.py').read_text(encoding='utf-8')
checks=[]
def ck(ok,msg): checks.append((bool(ok),msg))
ck(len(majors)==20,'20 canonical majors retained')
ck(len(subjects)==13,'13 EMASI subjects retained')
ck(sum(len(v.get('emasi_subject_guidance',[])) for v in majors.values())==109,'109 existing subject-guidance entries retained')
ck(sum(len(v.get('emasi_subject_connections',[])) for v in majors.values())==0,'No unsupported formal EMASI connections promoted')
ck('Academic disciplines are university-level fields' in app,'English UI distinguishes academic disciplines from school subjects')
ck('Các lĩnh vực học thuật là lĩnh vực nghiên cứu ở bậc đại học' in app,'Vietnamese UI distinguishes academic disciplines from school subjects')
ck((ROOT/'EMASI_13x20_AUDIT_MATRIX.csv').exists(),'260-pair audit matrix exists')
with (ROOT/'EMASI_13x20_AUDIT_MATRIX.csv').open(encoding='utf-8-sig') as f: matrix=list(csv.DictReader(f))
ck(len(matrix)==260,'Audit matrix contains exactly 260 pairs')
ck((ROOT/'SOURCE_CLAIM_REGISTER.csv').exists(),'Source-to-claim register exists')
for name in ['majors.json','academic_sources.json']:
 ck((ROOT/name).read_bytes()==(ROOT/'data'/name).read_bytes(),f'{name} root/data copies synchronized')
try: ast.parse(app); ck(True,'app.py syntax valid')
except SyntaxError as e: ck(False,f'app.py syntax error: {e}')
for ok,msg in checks: print(('PASS' if ok else 'FAIL')+' '+msg)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
