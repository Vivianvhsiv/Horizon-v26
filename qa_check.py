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
check(len(majors)==28,'28 major profiles are present')
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
check(not missing_major_vi,'all 28 major profiles contain English–Vietnamese paired content'+
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
# Explore Majors is a searchable catalogue; reflection-note collection is intentionally absent.
check('q = st.text_input(tr("search_major")' not in explore_code and 'if q and q.casefold()' not in explore_code,
      'Explore Majors does not show a separate Search Majors field or filter')
check('Your reflection note' not in explore_code and 'Ghi chú tự suy ngẫm' not in explore_code,
      'Explore Majors does not collect a separate reflection note')
check('explore_strength_note' not in app and 'explore_strength_example' not in app,
      'Reflection-note state is not carried into Explore or Compare Majors')
check('profile_topic_mentions' not in app and 'explore_profile_interests' not in app,
      'Horizon does not present interest-to-major matching or interest-based profile navigation')
compare_start=app.find('elif page == tr("compare"):')
compare_code=app[compare_start:] if compare_start >= 0 else ''
check('There is no overall winner here.' in compare_code and 'not which one is supposedly best for you' in compare_code,
      'Compare Majors explains differences without declaring a best-fit major')
check('Compare the substance of each field' in compare_code,
      'Compare Majors frames comparison around academic substance and student-led next questions')

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
# Claim-level evidence traceability across all three exploration modules.
check('def claims_for_profile_item(major, item):' in app and 'def render_profile_item_evidence(major, item, language):' in app,
      'shared claim-level evidence lookup and bilingual renderer are present')
check('render_profile_item_evidence(name, value, st.session_state.language)' in app,
      'Explore Majors attaches source traceability to individual academic profile items')
check('render_profile_item_evidence(name, item, st.session_state.language)' in app,
      'Compare Majors attaches source traceability to individual compared items')
check('matching_claims = [' in app and 'startswith("verified")' in app,
      'Network Map only creates academic discipline links from explicitly named verified claims')
check('"claim": claim_text' in app and '"claim_status": claim_status' in app,
      'Network Map source records retain the exact supported claim and its verification status')
check('Horizon profile reference' not in app,
      'Network Map does not present generic major-level URLs as claim-level evidence')
check('No direct claim-level source is mapped to this item yet' in app,
      'Unmapped profile items are explicitly labelled exploratory rather than appearing sourced')

# Network Map evidence-first regression checks
network_start=app.find('def build_network(')
network_end=app.find('def graphviz_source(', network_start)
network_code=app[network_start:network_end] if network_start >= 0 and network_end > network_start else ''
check(network_start >= 0 and network_end > network_start,'Network Map builder is present')
check('if interest in info["interests"]' not in network_code,'Network Map does not infer majors from shared interest tags')
check('selected_interests=None' in network_code and 'for interest in selected_interests:' in network_code,
      'Network Map restores student-selected interest fields as visible exploration inputs')
check('Earth & Environmental Systems' in network_code and 'domain::Earth & Environmental Systems' in network_code,
      'Geography-related inputs open a dedicated Earth & Environmental Systems branch in Network Map')
check('for value in selected_interests:' in network_code and '"geograph" in value.casefold()' in network_code,
      'The Earth-systems branch can be triggered by Geography-related interest labels as well as current subjects')
check('"Geology"' in network_code and '"Environmental Science"' in network_code and '"Climate Science"' in network_code and '"Oceanography"' in network_code and '"Hydrology"' in network_code,
      'The Geography branch exposes Geology, Environmental Science, Climate Science, Oceanography and Hydrology')
check('explore earth and environmental systems' in network_code and 'explore earth system field' in network_code and 'source in subject_domain_nodes' in app,
      'The entire Earth-systems branch, including its second-hop fields, is included in the visible highlighted map')
check('chosen_interest_labels = st.multiselect(tr("interest")' in app and 'st.session_state.chosen_interests' in app,
      'Network Map exposes and stores the selected interest fields')
check('no interest-to-major match is inferred' in network_code,
      'Restored interests are not converted into unsupported major matches')
check('emasi_subject_connections' not in network_code,'Network Map does not infer majors from unverified EMASI subject records')
check('return nodes, edges, selected_majors' in network_code,'Network Map returns only explicitly selected majors as candidates')

check('browsed_major = st.session_state.get("network_major_explorer")' in app and 'expanded_majors.add(browsed_major)' in app,
      'The major selected in the Network Map browser is expanded in the graph')
check('focus_keys.append(node_id("major", browsed_major))' in app,
      'The browsed major and its newly expanded directions are highlighted in the graph')
check('major_branch_nodes = {' in app and 'major_branch_targets.update(' in app
      and 'active_nodes = set(focus) | subject_linked_majors | major_branch_nodes | major_branch_targets' in app,
      'Only the selected major branches and their adjacent fields/majors are highlighted in Network Map')
branch_targets_pos = app.find('major_branch_targets.update(')
active_nodes_pos = app.find('active_nodes = set(focus) | subject_linked_majors | major_branch_nodes | major_branch_targets')
check(branch_targets_pos >= 0 and active_nodes_pos > branch_targets_pos,
      'Network Map computes the selected major branch closure before activating it')

# Regression: every source-rendered profile section has bilingual labels.
check('"limitations": ("Scope and limitations references"' in app
      and '"limitations": ("Nguồn về phạm vi và giới hạn"' in app,
      'profile source renderer supports the limitations section in both languages')
# Exploration-direction explanations must be genuinely translated, not merely populated.
exploration_path = ROOT / 'exploration_directions.json'
if exploration_path.exists():
    translation_data = json.loads(exploration_path.read_text(encoding='utf-8'))
    untranslated = [
        f"{major}[{idx}]"
        for major, items in translation_data.get('majors', {}).items()
        for idx, item in enumerate(items)
        if not item.get('why_vi') or item.get('why_vi') == item.get('why')
    ]
    check(not untranslated,
          'all exploration direction explanations have Vietnamese translations'
          + (': ' + ', '.join(untranslated[:12]) if untranslated else ''))
else:
    check(False, 'exploration directions file exists for bilingual QA')
missing_source_types = [
    f"{major}.claims[{i}].sources[{j}]"
    for major, record in sources.items()
    for i, claim in enumerate(record.get('claims', []))
    for j, source in enumerate(claim.get('sources', []))
    if not source.get('source_type_vi')
]
check(not missing_source_types,
      'all source type labels have Vietnamese translations'
      + (': ' + ', '.join(missing_source_types[:12]) if missing_source_types else ''))
# Unexpected cross-disciplinary exploration coverage
exploration_path = ROOT / 'exploration_directions.json'
if exploration_path.exists():
    exploration_data = json.loads(exploration_path.read_text(encoding='utf-8'))
    exploration_majors = exploration_data.get('majors', {})
    check(len(exploration_majors) == 28 and set(exploration_majors) == set(majors.keys()),
          'Unexpected exploration directions cover all 28 Horizon majors')
    direction_total = sum(len(items) for items in exploration_majors.values())
    check(direction_total == 285,
          'Unexpected exploration catalogue contains exactly 285 curated directions')
    check(all(len(items) >= 10 for items in exploration_majors.values()),
          'Every major has at least ten additional exploration directions')
    duplicate_direction_labels = [
        major for major, items in exploration_majors.items()
        if len({item.get('label') for item in items}) != len(items)
    ]
    check(not duplicate_direction_labels,
          'Exploration direction labels are unique within each major'
          + (': ' + ', '.join(duplicate_direction_labels) if duplicate_direction_labels else ''))
    check(all(item.get('explore_with') for items in exploration_majors.values() for item in items),
          'Every exploration direction identifies at least one adjacent field or major')
    check(all(item.get('label') and item.get('label_vi') and item.get('why') and item.get('why_vi') for items in exploration_majors.values() for item in items),
          'Every additional direction has English and Vietnamese labels and explanations')
    check(all(isinstance(target, str) and target.strip() for items in exploration_majors.values() for item in items for target in item.get('explore_with', [])),
          'Cross-disciplinary directions use named adjacent majors or academic fields')
    check('elif adjacent_major and adjacent_major != major' in app and '"related"' in app,
          'Adjacent fields outside the 20-major catalogue can appear as distinct map nodes')
    check('not verified curriculum requirements' in exploration_data.get('_meta', {}).get('description', ''),
          'Additional directions are explicitly scoped as exploratory rather than verified requirements')
else:
    check(False, 'Unexpected exploration directions data file exists')
check('EXPLORATION_DIRECTIONS' in app and 'unexpected direction to explore' in app and 'exploratory connection to another major' in app,
      'Network Map integrates additional exploratory directions and cross-major discovery links')
check('for direction in EXPLORATION_DIRECTIONS.get(major, []):' in network_code
      and 'if major in expanded_set:' in network_code,
      'Network Map generates every major\'s curated directions independently of profile expansion')
check('unrelated majors stay muted' in app and 'các ngành không liên quan vẫn ở trạng thái mờ' in app,
      'Network Map explains that unrelated majors remain muted while the full map stays visible')
renderer_start=app.find('def make_interactive_graph(')
renderer_end=app.find('with st.sidebar:', renderer_start)
renderer_code=app[renderer_start:renderer_end] if renderer_start >= 0 and renderer_end > renderer_start else ''
check('all_exploration_direction_nodes' not in renderer_code
      and 'global_exploration_edge' not in renderer_code
      and 'major_branch_nodes' in renderer_code,
      'Network Map highlights a selected branch without globally activating unrelated branches')
check('backbone_types = {"student", "interest", "subject", "major", "cluster"}' in renderer_code
      and 'item["type"] in backbone_types or key in active_nodes' in renderer_code
      and 'if key not in visible_node_keys:' in renderer_code,
      'Full Map retains its catalogue backbone while limiting detail nodes to selected exploration branches')
check('if not active and edge["relation"] != "contains major":' in renderer_code
      and 'if source not in visible_node_keys or target not in visible_node_keys:' in renderer_code,
      'Only active exploration links and catalogue structure are drawn, preventing unrelated branches from cluttering the map')
check('physics=False' in renderer_code and 'hierarchical=True' in renderer_code
      and 'direction="LR"' in renderer_code and 'nodeSpacing=190' in renderer_code
      and 'levelSeparation=230' in renderer_code,
      'Network Map uses the preserved hierarchical left-to-right layout with deliberate spacing')
check('Unexpected directions to explore' in app and 'not verified degree pathways' in app,
      'Major detail pages explain the exploratory status of unexpected directions')

check('expanded_majors=None' in network_code and 'expanded_set = set(selected_majors) | set(expanded_majors)' in network_code,
      'Every explicitly selected or expanded major can open its own exploration branches')
check('"academic_foundations"' in network_code and '"related_disciplines"' in network_code and '"specialized_applications"' in network_code and '"research_areas"' in network_code,
      'Major exploration branches include foundations, related fields, applications and research')
check('"careers"' in network_code and '"skills"' in network_code,
      'Major exploration branches include career areas and skill context')
check('"Exploratory profile context — not independently verified"' in network_code and '"explore profile direction"' in network_code,
      'Unreviewed profile branches are clearly labelled exploratory rather than verified evidence')
check('possible_owner = selected_node_label.split("::", 1)[0]' in app and 'owner_major = selected_identity.split("::", 1)[0]' in app,
      'Students can continue expanding a major after selecting one of its profile branches')
check('pages = [tr("home"),tr("network"),tr("majors"),tr("compare"),tr("about")]' in app and 'elif page == tr("reflect"):' not in app,'standalone Reflection page is removed from navigation and routing')
check('cols = st.columns(4)' in app and 'step_icons=["✧","▤","⌘","⚖"]' in app,'homepage workflow contains four steps and no Reflection step')
check('No inferred major matches are shown.' in app,'Network Map explains the current evidence gap')

# Print a single summary after every base and regression check has run.
for ok,msg in checks:
    print(('PASS' if ok else 'FAIL')+'  '+msg)
print(f'\nSummary: {sum(x for x,_ in checks)}/{len(checks)} checks passed')
if errors:
    sys.exit(1)
