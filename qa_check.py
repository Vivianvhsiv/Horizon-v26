"""Offline structural QA for Horizon. Run: python qa_check.py"""
import json, pathlib, re, ast, hashlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
errors=[]; checks=[]
def check(ok,msg):
    checks.append((bool(ok),msg))
    if not ok: errors.append(msg)
# JSON and mirror consistency
files=['majors.json','academic_sources.json','emasi_subjects.json','emasi_mapping_protocol.json']
loaded={}
for f in files:
    try: loaded[f]=json.loads((ROOT/f).read_text(encoding='utf-8')); check(True,f'{f}: valid JSON')
    except Exception as e: check(False,f'{f}: invalid JSON ({e})')
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
subject_names={x.get("name_en"):x for x in loaded.get('emasi_subjects.json',{}).get('subjects',[])}
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
subjects=loaded.get('emasi_subjects.json',{}).get('subjects',[])
check(len(subjects)==13,'13 EMASI subjects are registered')
ids=[x.get('id') for x in subjects]
check(len(ids)==len(set(ids)),'EMASI subject IDs are unique')
submap={x.get('name_en'):x for x in subjects}
check(submap.get('Geography',{}).get('id')=='S12' and submap.get('History',{}).get('id')=='S13','Geography S12 and History S13 are registered')
app=(ROOT/'app.py').read_text(encoding='utf-8')
check('("Geography", "Địa lý")' in app and '("History", "Lịch sử")' in app,'Geography and History appear in the interactive subject selector')
# Check the UI language code uses Vietnamese source-type labels.
check('source.get("source_type_vi"' in app,'source type labels use Vietnamese in Vietnamese UI')
# Explicit English–Vietnamese product-language checks.
readme=(ROOT/'README.md').read_text(encoding='utf-8')
check('"English"' in app and '"Tiếng Việt"' in app and '["English","Tiếng Việt"]' in app,
      'language selector offers exactly English and Vietnamese')
check('## Languages' in readme and '- English' in readme and '- Tiếng Việt' in readme,
      'README identifies English and Vietnamese as the supported languages')
# Major profile content must provide Vietnamese equivalents for each displayed field.
major_vi_fields=['name_vi','cluster_vi','overview_vi','preparation_vi','caveat_vi',
                 'disciplines_vi','skills_vi','careers_vi','academic_foundations_vi',
                 'related_disciplines_vi','specialized_applications_vi','research_areas_vi','limitations_vi']
missing_major_vi=[f'{name}.{key}' for name,record in majors.items()
                  for key in major_vi_fields if not record.get(key)]
check(not missing_major_vi,'all 20 major profiles contain English–Vietnamese paired content'+
      (': '+', '.join(missing_major_vi[:8]) if missing_major_vi else ''))
# Keep Vietnamese source/claim labels and subject guidance checked above; do not use
# unrelated Chinese-character absence as a proxy for bilingual quality.
# Explore Majors regression checks
explore_start=app.find('elif page == tr("majors"):')
explore_end=app.find('elif page == tr("compare"):', explore_start)
explore_code=app[explore_start:explore_end] if explore_start >= 0 and explore_end > explore_start else ''
check(explore_start >= 0 and explore_end > explore_start,'Explore Majors page is present')
check('profile_scope_vi' in explore_code and 'source_status_vi' in explore_code,'Explore Majors displays bilingual profile scope and evidence status')
check('subject_inventory_note_vi' in explore_code,'Explore Majors displays the Vietnamese EMASI subject-inventory note')
check('preferred_role_order' in explore_code and 'available_roles' in explore_code,'Explore Majors renders every subject-guidance role, including future categories')
role_values={item.get('role_en') for record in majors.values() for item in record.get('emasi_subject_guidance',[]) if item.get('role_en')}
check('role_order.extend(role for role in available_roles if role not in role_order)' in explore_code,
      f'all {len(role_values)} subject-guidance role categories are rendered')
source_errors=[]
for major,record in sources.items():
    for i,claim in enumerate(record.get('claims',[])):
        if not claim.get('sources'):
            source_errors.append(f'{major}.claims[{i}] has no source')
        for j,source in enumerate(claim.get('sources',[])):
            if not source.get('institution') or not source.get('title') or not source.get('url','').startswith('https://'):
                source_errors.append(f'{major}.claims[{i}].sources[{j}] has incomplete metadata')
check(not source_errors,'all source-register claims have source links and institution/title metadata'+
      (': '+', '.join(source_errors[:8]) if source_errors else ''))
# Data Science subject-reference scope checks
ds_guidance=majors.get('Data Science',{}).get('emasi_subject_guidance',[])
ds_by_subject={item.get('subject_en'):item for item in ds_guidance}
check(len(ds_guidance)==11,'Data Science has 11 EMASI subject suggestions')
check(all(len(item.get('evidence_refs',[])) <= 3 for item in ds_guidance),
      'Data Science subject suggestions use focused references rather than the same broad source list')
check(bool(ds_by_subject.get('Music')) and not ds_by_subject['Music'].get('evidence_refs'),
      'Data Science Music pathway remains explicitly exploratory without a mismatched curriculum citation')
check(bool(ds_by_subject.get('Geography')) and not ds_by_subject['Geography'].get('evidence_refs'),
      'Data Science Geography suggestion remains exploratory without an unsupported source')
ds_ref_errors=[]
for item in ds_guidance:
    for source in item.get('evidence_refs',[]):
        if not source.get('support_en') or not source.get('support_vi') or not source.get('scope_en') or not source.get('scope_vi'):
            ds_ref_errors.append(f"{item.get('subject_en')}: incomplete bilingual source explanation")
check(not ds_ref_errors,'Data Science subject-level source explanations and limitations are bilingual'+
      (': '+', '.join(ds_ref_errors[:5]) if ds_ref_errors else ''))
# Source presentation and scope checks
for name,record in majors.items():
    check('profile_reference_links' not in record,
          f'{name}: no generic placeholder reference links remain in the major profile')
check('Reference organisation' not in app and 'Academic reference' not in app,
      'app does not render generic placeholder reference labels')
check('Illustrative career areas to explore' in app and 'lĩnh vực nghề nghiệp mang tính tham khảo' in app,
      'career areas are explicitly framed as illustrative in English and Vietnamese')
# Check the machine-readable CSV register against the JSON source-of-truth records.
import csv
csv_path=ROOT/'SOURCE_CLAIM_REGISTER.csv'
if csv_path.exists():
    with csv_path.open(encoding='utf-8-sig',newline='') as f:
        csv_rows=list(csv.DictReader(f))
    json_rows=[]
    for major,record in sources.items():
        for i,claim in enumerate(record.get('claims',[]),1):
            for source in claim.get('sources',[]):
                json_rows.append((major,str(i),claim.get('type',''),claim.get('status',''),
                                  source.get('institution',''),source.get('title',''),source.get('url','')))
    csv_rows_norm={(r.get('Major',''),r.get('Claim Number',''),r.get('Claim Type',''),
                    r.get('Claim Status',''),r.get('Institution',''),r.get('Source Title',''),r.get('URL',''))
                   for r in csv_rows}
    json_rows_norm=set(json_rows)
    check(csv_rows_norm==json_rows_norm,
          f'SOURCE_CLAIM_REGISTER.csv matches academic_sources.json ({len(csv_rows_norm)} CSV rows / {len(json_rows_norm)} JSON source rows)')
else:
    check(False,'SOURCE_CLAIM_REGISTER.csv exists')
# Student-centred exploration lens: transparent overlap, self-described strengths, no fit scoring.
check('Your exploration lens' in explore_code and 'Góc nhìn khám phá của bạn' in explore_code,
      'Explore Majors offers a bilingual, optional student exploration lens')
check('interest_pairs = grouped_options(INTEREST_GROUPS)' in explore_code and 'format_func=lambda value: interest_display.get(value, value)' in explore_code,
      'Exploration interest selector stores canonical taxonomy keys while displaying bilingual group labels')
check('shared_topics = sorted(set(profile_interests).intersection(info.get("interests", [])))' in explore_code,
      'Personal topic overlap uses exact selected taxonomy labels only')
check('These are shared catalogue labels only.' in explore_code and 'That does not mean the major is unsuitable' in explore_code,
      'Topic overlap is explicitly not presented as academic evidence or suitability')
check('A strength you have noticed' in explore_code and 'A specific example that makes you think this is a strength' in explore_code,
      'Student strengths are self-described and can be supported by a concrete example')
check('does not automatically claim that this strength is required by or predicts success' in explore_code,
      'Student-provided strengths are not converted into aptitude or success claims')
compare_start=app.find('elif page == tr("compare"):')
compare_code=app[compare_start:] if compare_start >= 0 else ''
check('Shared labels are a browsing aid only' in compare_code and 'Your self-identified strength:' in compare_code,
      'Compare Majors carries the student lens without creating a match score')

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
# Network Map evidence-first regression checks
network_start=app.find('def build_network(')
network_end=app.find('def graphviz_source(', network_start)
network_code=app[network_start:network_end] if network_start >= 0 and network_end > network_start else ''
check(network_start >= 0 and network_end > network_start,'Network Map builder is present')
check('if interest in info["interests"]' not in network_code,'Network Map does not infer majors from shared interest tags')
check('emasi_subject_connections' not in network_code,'Network Map does not infer majors from unverified EMASI subject records')
check('return nodes, edges, selected_majors' in network_code,'Network Map returns only explicitly selected majors as candidates')
check('pages = [tr("home"),tr("network"),tr("majors"),tr("compare"),tr("about")]' in app and 'elif page == tr("reflect"):' not in app,'standalone Reflection page is removed from navigation and routing')
check('cols = st.columns(4)' in app and 'step_icons=["✧","▤","⌘","⚖"]' in app,'homepage workflow contains four steps and no Reflection step')
check('No inferred major matches are shown.' in app,'Network Map explains the current evidence gap')

# Print a single summary after every base and regression check has run.
for ok,msg in checks:
    print(('PASS' if ok else 'FAIL')+'  '+msg)
print(f'\nSummary: {sum(x for x,_ in checks)}/{len(checks)} checks passed')
if errors:
    sys.exit(1)
