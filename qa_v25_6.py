"""Offline QA for Horizon v25.6 traceability inventory."""
import csv, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
checks=[]
def ck(v,s): checks.append((bool(v),s))
def rows(n):
 with (R/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
claims=rows('SOURCE_CLAIM_REGISTER.csv'); ledger=rows('SOURCE_TRACEABILITY_LEDGER_V25_6.csv')
matrix=rows('EMASI_13x20_AUDIT_MATRIX.csv'); cross=rows('MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv')
ck(len(ledger)==len(claims)==186,'Every source-register row has one ledger row')
ck(len(cross)==len(matrix)==260,'Every matrix pair has one crosswalk row')
ck(len({r['Source Row ID'] for r in ledger})==len(ledger),'Source Row IDs are unique')
ck(len({r['Matrix Pair ID'] for r in cross})==len(cross),'Matrix Pair IDs are unique')
ck(all(r['Source Row ID'] and r['URL']==claims[i]['URL'] for i,r in enumerate(ledger)),'Ledger preserves source URLs in original row order')
ck(all(r['Major']==claims[i]['Major'] and r['Source Title']==claims[i]['Source Title'] for i,r in enumerate(ledger)),'Ledger preserves major and source title')
ck(sum(r['Conservative Evidence Scope']=='PROGRAMME_AVAILABILITY_ONLY' for r in ledger)==78,'Programme availability remains separately scoped')
ck(all(r['Supports EMASI Mapping']=='Not established' for r in ledger),'No source row is promoted to EMASI mapping evidence')
ck(all(r['Source Register Row Link'].startswith('UNRESOLVED') for r in cross),'Unproven source-to-matrix joins remain explicitly unresolved')
ck(all(r['EMASI Syllabus Validation']=='NOT PROVIDED / NOT VERIFIED' for r in cross),'No unsupported syllabus verification is asserted')
ck(all(r['URL Host'] for r in ledger if r['URL'].startswith('https://')),'HTTPS URLs have parsed host fields')
ck((R/'build_claim_traceability_v25_6.py').exists(),'Reproducible generator is included')
report=(R/'EVIDENCE_TRACEABILITY_REPORT_V25_6.md').read_text(encoding='utf-8')
ck('does not claim that a particular source-register row supports a particular matrix pair' in report,'Report explains missing row-level foreign key')
ck('No subject-major pair is upgraded to verified' in report,'Report preserves validation boundary')
# Existing QA chain
for script in ['qa_check.py','qa_v25.py','qa_v25_1.py','qa_v25_2.py','qa_v25_3.py','qa_v25_4.py','qa_v25_5.py']:
 p=R/script
 if p.exists():
  result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True)
  ck(result.returncode==0,f'Existing {script} passes')
for ok,label in checks: print(('PASS ' if ok else 'FAIL ')+label)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks): raise SystemExit(1)
