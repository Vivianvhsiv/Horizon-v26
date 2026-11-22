"""Offline privacy-surface and bilingual-coverage QA for Horizon v25.9.
These checks inspect source/configuration only; they are not a security audit
or a live browser/network assessment.
"""
import ast, json, pathlib, re, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
checks=[]
def ck(v,label): checks.append((bool(v),label))
app=(R/'app.py').read_text(encoding='utf-8')
# Extract literal translation dictionary from app.py without importing Streamlit.
tree=ast.parse(app); T=None
for node in ast.walk(tree):
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='T' for t in node.targets):
        try: T=ast.literal_eval(node.value)
        except Exception: pass
        break
ck(isinstance(T,dict) and {'English','Tiếng Việt'}.issubset(T),'English and Vietnamese UI dictionaries are statically extractable')
if isinstance(T,dict) and {'English','Tiếng Việt'}.issubset(T):
    en,vi=T['English'],T['Tiếng Việt']
    ck(set(en)==set(vi),f'UI translation keys match (English={len(en)}, Vietnamese={len(vi)})')
    ck(all(isinstance(x,str) and x.strip() for x in en.values()) and all(isinstance(x,str) and x.strip() for x in vi.values()),'All UI dictionary translations are non-empty strings')
else:
    en,vi={},{}
maj=json.loads((R/'majors.json').read_text(encoding='utf-8'))
subjects=json.loads((R/'data/emasi_subjects.json').read_text(encoding='utf-8'))['subjects']
ck(len(maj)==20 and all(x.get('name_vi') and x.get('overview') and x.get('overview_vi') and x.get('caveat') and x.get('caveat_vi') for x in maj.values()),'All 20 major profiles contain core English/Vietnamese descriptions and caveats')
ck(len(subjects)==13 and all(x.get('name_en') and x.get('name_vi') for x in subjects),'All 13 EMASI subject labels have English and Vietnamese values')
# Privacy surface: confirm no obvious direct-identifier input widgets are present.
identifier_patterns=[r'st\.text_input\([^\n]*(?:name|email|phone|address|student.?id)', r'st\.text_area\([^\n]*(?:name|email|phone|address|student.?id)']
ck(not any(re.search(p,app,re.I) for p in identifier_patterns),'No obvious name/email/phone/address/student-ID input widget found in app.py')
# Inspect persistence/network-write primitives; reads and downloads are not treated as writes.
write_patterns=[r"Path\.write_text\(", r"requests\.(?:post|put|patch|delete)\(", r"firebase|supabase|mongodb|postgresql|mysql"]
ck(not any(re.search(p,app,re.I) for p in write_patterns),'No obvious local write, outbound write request, or database client reference found in app.py')
ck('st.session_state' in app,'User selections are represented in Streamlit session state')
ck('download' in app.lower(),'Application includes an explicit summary-download feature requiring user-facing privacy notice')
# Required limitation and privacy guidance docs.
for f in ['PRIVACY_REVIEW_V25_9.md','BILINGUAL_AUDIT_V25_9.md','RELEASE_READINESS_V25_9.md']:
    ck((R/f).is_file() and (R/f).stat().st_size>200,f'{f} exists and is populated')
# Syntax regression for app and the new QA script.
for f in ['app.py','qa_v25_9.py']:
    try: ast.parse((R/f).read_text(encoding='utf-8')); ok=True
    except Exception: ok=False
    ck(ok,f'{f} parses as valid Python')
for ok,label in checks: print(('PASS ' if ok else 'FAIL ')+label)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
