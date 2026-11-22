"""Offline structural QA for Horizon. Run: python qa_check.py"""
import json, pathlib, re, ast, hashlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
errors=[]; checks=[]
def check(ok,msg):
    checks.append((bool(ok),msg))
    if not ok: errors.append(msg)
# JSON and mirror consistency
files=['majors.json','academic_sources.json','data/majors.json','data/academic_sources.json','data/emasi_subjects.json','data/emasi_mapping_protocol.json']
loaded={}
for f in files:
    try: loaded[f]=json.loads((ROOT/f).read_text(encoding='utf-8')); check(True,f'{f}: valid JSON')
    except Exception as e: check(False,f'{f}: invalid JSON ({e})')
for a,b in [('majors.json','data/majors.json'),('academic_sources.json','data/academic_sources.json')]:
    check((ROOT/a).read_bytes()==(ROOT/b).read_bytes(),f'{a} matches {b}')
majors=loaded.get('majors.json',{})
sources=loaded.get('academic_sources.json',{})
check(len(majors)==20,'20 major profiles are present')
required=['academic_foundations','related_disciplines','specialized_applications','research_areas','limitations']
for name,record in majors.items():
    for field in required:
        en=record.get(field); vi=record.get(field+'_vi')
        check(isinstance(en,list) and isinstance(vi,list) and len(en)==len(vi) and len(en)>0,f'{name}: bilingual {field} aligned')
        if isinstance(en,list) and isinstance(vi,list):
            for x,y in zip(en,vi): check(isinstance(y,str) and bool(y.strip()) and x!=y,f'{name}: {field} has Vietnamese translation')
    check(name in sources,f'{name}: academic source record exists')
# source bilingual metadata
missing=[]
for name,record in sources.items():
    for key in ['status_vi','scope_vi']:
        if not record.get(key): missing.append(f'{name}.{key}')
    for i,claim in enumerate(record.get('claims',[])):
        for key in ['claim_vi','type_vi','status_vi']:
            if not claim.get(key): missing.append(f'{name}.claims[{i}].{key}')
        for j,src in enumerate(claim.get('sources',[])):
            if not src.get('source_type_vi'): missing.append(f'{name}.claims[{i}].sources[{j}].source_type_vi')
check(not missing,'academic evidence labels and claims have Vietnamese fields'+(': '+', '.join(missing[:8]) if missing else ''))
# Subject guidance bilingual coverage and inventory membership
subject_names={x.get("name_en"):x for x in loaded.get('data/emasi_subjects.json',{}).get('subjects',[])}
guidance_count=0; guidance_errors=[]
for major,record in majors.items():
    for idx,item in enumerate(record.get('emasi_subject_guidance',[])):
        guidance_count += 1
        en=item.get('subject_en','')
        if en not in subject_names: guidance_errors.append(f'{major}[{idx}] unknown subject {en}')
        for key in ['subject_vi','role_vi','why_vi','focus_vi','evidence_vi','evidence_status_vi']:
            if not item.get(key): guidance_errors.append(f'{major}[{idx}].{key}')
check(not guidance_errors,f'{guidance_count} subject-guidance records have bilingual labels and known EMASI subjects'+(': '+', '.join(guidance_errors[:8]) if guidance_errors else ''))
# EMASI subject inventory
subjects=loaded.get('data/emasi_subjects.json',{}).get('subjects',[])
check(len(subjects)==13,'13 EMASI subjects are registered')
ids=[x.get('id') for x in subjects]
check(len(ids)==len(set(ids)),'EMASI subject IDs are unique')
submap={x.get('name_en'):x for x in subjects}
check(submap.get('Geography',{}).get('id')=='S12' and submap.get('History',{}).get('id')=='S13','Geography S12 and History S13 are registered')
app=(ROOT/'app.py').read_text(encoding='utf-8')
check('("Geography", "Địa lý")' in app and '("History", "Lịch sử")' in app,'Geography and History appear in the interactive subject selector')
# Check the UI language code uses Vietnamese source-type labels.
check('source.get("source_type_vi"' in app,'source type labels use Vietnamese in Vietnamese UI')
# No Chinese CJK strings in user-facing app/data/readme files.
for f in ['app.py','majors.json','academic_sources.json','data/emasi_subjects.json','README.md']:
    text=(ROOT/f).read_text(encoding='utf-8')
    check(not re.search(r'[\u3400-\u9fff]',text),f'{f}: no CJK text remains')
# Python syntax
try: ast.parse(app); check(True,'app.py parses successfully')
except SyntaxError as e: check(False,f'app.py syntax error: {e}')
# URL format sanity
bad=[]
for name,record in sources.items():
    for claim in record.get('claims',[]):
        for src in claim.get('sources',[]):
            u=src.get('url','')
            if not u.startswith('https://'): bad.append((name,u))
check(not bad,'all academic source URLs use HTTPS'+(f': {bad[:5]}' if bad else ''))
for ok,msg in checks: print(('PASS' if ok else 'FAIL')+'  '+msg)
print(f'\nSummary: {sum(x for x,_ in checks)}/{len(checks)} checks passed')
if errors: sys.exit(1)
