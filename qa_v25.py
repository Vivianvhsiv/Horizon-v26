import json, ast, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parent
app=(ROOT/'app.py').read_text(encoding='utf-8')
majors=json.loads((ROOT/'data/majors.json').read_text(encoding='utf-8'))
checks=[]
def ck(ok,msg): checks.append((bool(ok),msg))
ck(len(majors)==20,'20 majors retained')
ck('max_selections=3' in app,'major selector limited to three')
ck('for major, info in MAJORS.items()' in app and 'major_label_to_key' in app,'selector generated from canonical major database')
ck('st.session_state.chosen_majors' in app,'intended majors stored in session state')
ck('Student-selected major intention' in app,'student intention represented as explicit graph edge')
ck('if intended_majors:' in app,'explicit intention takes priority in network focus')
ck('undecided' in app.lower(),'undecided path exists')
try: ast.parse(app); ck(True,'Python syntax valid')
except SyntaxError as e: ck(False,f'Python syntax invalid: {e}')
for ok,msg in checks: print(('PASS' if ok else 'FAIL')+' '+msg)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
