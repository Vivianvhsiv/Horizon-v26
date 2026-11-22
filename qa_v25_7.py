"""Offline QA for v25.7 human evidence review workflow."""
import csv,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parent
checks=[]
def ck(v,s):checks.append((bool(v),s))
def rows(n):
 with (R/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
src=rows('SOURCE_PAGE_REVIEW_QUEUE_V25_7.csv'); mx=rows('MATRIX_PAIR_REVIEW_QUEUE_V25_7.csv')
led=rows('SOURCE_TRACEABILITY_LEDGER_V25_6.csv'); cross=rows('MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv')
ck(len(src)==len(led)==186,'Source review queue covers every ledger row')
ck(len(mx)==len(cross)==260,'Matrix review queue covers every major-subject pair')
ck([r['Source Row ID'] for r in src]==[r['Source Row ID'] for r in led],'Source IDs and source row order preserved')
ck([r['Matrix Pair ID'] for r in mx]==[r['Matrix Pair ID'] for r in cross],'Matrix IDs and pair order preserved')
ck(all(r['Review Decision (UNREVIEWED/ACCEPTED/REJECTED/NEEDS FOLLOW-UP)']=='UNREVIEWED' for r in src),'All source reviews start unreviewed')
ck(all(not r['Reviewer'] and not r['Exact Supporting Passage or Precise Paraphrase'] for r in src),'No reviewer evidence is fabricated')
ck(all(r['Guidance Decision (KEEP EXPLORATORY/REVISE/REMOVE/ELIGIBLE FOR FURTHER REVIEW)']=='KEEP EXPLORATORY' for r in mx),'All matrix guidance remains exploratory by default')
ck(all(not r['EMASI Official Document / Version'] and not r['Exact EMASI Evidence or Precise Paraphrase'] for r in mx),'No EMASI syllabus evidence is fabricated')
ck(all(r['Proposed Source Row IDs (human-confirmed only)']=='' for r in mx),'No unsupported source-to-matrix link is guessed')
ck((R/'HUMAN_EVIDENCE_REVIEW_PROTOCOL_V25_7.md').exists(),'Human review protocol included')
ck('not a verified status' in (R/'HUMAN_EVIDENCE_REVIEW_PROTOCOL_V25_7.md').read_text(encoding='utf-8'),'Protocol distinguishes further review from verification')
ck((R/'build_review_workflow_v25_7.py').exists(),'Reproducible queue generator included')
for script in ['qa_check.py','qa_v25.py','qa_v25_1.py','qa_v25_2.py','qa_v25_3.py','qa_v25_4.py','qa_v25_5.py','qa_v25_6.py']:
 p=R/script
 if p.exists():
  z=subprocess.run([sys.executable,str(p)],capture_output=True,text=True)
  ck(z.returncode==0,f'Existing {script} passes')
for ok,s in checks:print(('PASS ' if ok else 'FAIL ')+s)
print(f'Summary: {sum(x for x,_ in checks)}/{len(checks)} passed')
if not all(x for x,_ in checks):raise SystemExit(1)
