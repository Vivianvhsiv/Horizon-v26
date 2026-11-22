"""Offline structural and evidence-transparency QA for Horizon v25.2.
Does not claim live URL validation, EMASI syllabus equivalence, or browser QA.
"""
import ast, csv, json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parent
majors=json.loads((ROOT/'data/majors.json').read_text(encoding='utf-8'))
subjects=json.loads((ROOT/'data/emasi_subjects.json').read_text(encoding='utf-8'))['subjects']
app=(ROOT/'app.py').read_text(encoding='utf-8')
checks=[]
def ck(ok,msg): checks.append((bool(ok),msg))
ck(len(majors)==20,'20 canonical majors retained')
ck(len(subjects)==13,'13 EMASI subjects retained')
guidance=[(major,item) for major,profile in majors.items() for item in profile.get('emasi_subject_guidance',[])]
ck(len(guidance)==109,'109 existing subject-guidance records retained')
ck(all(item.get('subject_id') for _,item in guidance),'Every guidance record has a subject identifier')
ck(all(item.get('claim_id') for _,item in guidance),'Every guidance record has a claim identifier (even if source is pending)')
ck(all(item.get('evidence_status_en') and item.get('evidence_status_vi') for _,item in guidance),'Every guidance record has bilingual evidence status')
ck(all(item.get('evidence_scope_en') and item.get('evidence_scope_vi') for _,item in guidance),'Every guidance record has bilingual evidence scope')
ref_records=[(major,item,ref) for major,item in guidance for ref in item.get('evidence_refs',[])]
ck(all(ref.get('url','').startswith('https://') for _,_,ref in ref_records),'All attached claim-level evidence URLs use HTTPS')
ck(all(ref.get('institution') and ref.get('title') for _,_,ref in ref_records),'All attached references have institution and title metadata')
ck(sum(1 for _,item in guidance if item.get('evidence_refs'))==41,'41 guidance entries have attached claim-level references')
ck(sum(1 for _,item in guidance if not item.get('evidence_refs'))==68,'68 guidance entries remain visibly unsourced/pending')
ck(sum(len(p.get('emasi_subject_connections',[])) for p in majors.values())==0,'No unverified formal EMASI connections promoted')
ck('Evidence coverage for this major:' in app and 'Mức độ bao phủ bằng chứng cho ngành này:' in app,'Per-major bilingual evidence coverage shown in UI')
ck('do not verify EMASI syllabus alignment' in app,'UI explicitly limits what university references prove')
ck((ROOT/'EMASI_13x20_AUDIT_MATRIX.csv').exists(),'260-pair matrix retained')
with (ROOT/'EMASI_13x20_AUDIT_MATRIX.csv').open(encoding='utf-8-sig') as f: matrix=list(csv.DictReader(f))
ck(len(matrix)==260,'Exactly 260 major-subject pairs in audit matrix')
with (ROOT/'SOURCE_CLAIM_REGISTER.csv').open(encoding='utf-8-sig') as f: register=list(csv.DictReader(f))
ck(len(register)==186,'186 source occurrences retained in source-claim register')
ck(len({r['URL'] for r in register})==86,'86 distinct URLs represented in source-claim register')
for name in ['majors.json','academic_sources.json']:
 ck((ROOT/name).read_bytes()==(ROOT/'data'/name).read_bytes(),f'{name} root/data copies synchronized')
try: ast.parse(app); ck(True,'app.py syntax valid')
except SyntaxError as e: ck(False,f'app.py syntax error: {e}')
for ok,msg in checks: print(('PASS' if ok else 'FAIL')+' '+msg)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
