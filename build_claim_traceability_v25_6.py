"""Build a conservative, row-level evidence traceability inventory for Horizon v25.6.

This script creates stable IDs for existing source-register rows. It deliberately
DOES NOT infer that a source supports an EMASI subject mapping. The matrix's
Claim ID values are retained separately because the current files do not
provide a reliable row-level foreign key to SOURCE_CLAIM_REGISTER.csv.
"""
from pathlib import Path
import csv, re, json
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent

def read_csv(name):
    with (ROOT / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(name, fields, rows):
    with (ROOT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

def slug(s):
    return re.sub(r'[^A-Z0-9]+', '-', s.upper()).strip('-')[:18] or 'MAJOR'

claims = read_csv('SOURCE_CLAIM_REGISTER.csv')
matrix = read_csv('EMASI_13x20_AUDIT_MATRIX.csv')
ledger=[]
for i, r in enumerate(claims, 1):
    url=(r.get('URL') or '').strip()
    host=urlparse(url).netloc.lower() if url else ''
    ctype=(r.get('Claim Type') or '').strip()
    status=(r.get('Claim Status') or '').strip()
    if ctype == 'Programme availability evidence':
        evidence_scope='PROGRAMME_AVAILABILITY_ONLY'
        boundary='Supports programme listing/availability only; not curriculum content or school-subject alignment.'
    elif 'Curriculum' in ctype:
        evidence_scope='CURRICULUM_CONTEXT_REVIEW_REQUIRED'
        boundary='Potential curriculum context; inspect the cited page and exact claim before using it for a subject relationship.'
    elif ctype == 'Disciplinary evidence':
        evidence_scope='DISCIPLINARY_CONTEXT_ONLY'
        boundary='Broad disciplinary context only; does not establish EMASI subject alignment.'
    elif 'Professional' in ctype:
        evidence_scope='PROFESSIONAL_GUIDANCE_CONTEXT'
        boundary='Professional guidance context only; not a school-subject prerequisite unless explicitly supported.'
    else:
        evidence_scope='OTHER_SCOPE_MANUAL_REVIEW'
        boundary='Claim type requires manual scope review before use.'
    ledger.append({
        'Source Row ID': f"SRC-{slug(r.get('Major',''))}-{i:03d}",
        'Major':r.get('Major',''), 'Original Claim Number':r.get('Claim Number',''),
        'Claim Type':ctype, 'Claim Status (Original)':status,
        'Institution':r.get('Institution',''), 'Source Title':r.get('Source Title',''),
        'URL':url, 'URL Host':host, 'Source Type':r.get('Source Type',''),
        'Original Scope / Limitation':r.get('Scope / Limitation',''),
        'Conservative Evidence Scope':evidence_scope,
        'Use Boundary':boundary,
        'Content Reviewed in v25.6':'No — inventory only',
        'Supports EMASI Mapping':'Not established',
    })

write_csv('SOURCE_TRACEABILITY_LEDGER_V25_6.csv', list(ledger[0]), ledger)

# Keep matrix claim IDs separate; there is no defensible source-row join key.
mx=[]
for i,r in enumerate(matrix,1):
    mx.append({
      'Matrix Pair ID':f"MAP-{i:03d}", 'Major':r.get('Major',''),
      'Subject ID':r.get('Subject ID',''), 'EMASI Subject':r.get('EMASI Subject',''),
      'Current Guidance Role':r.get('Current Guidance Role',''),
      'Matrix Claim ID (Original)':r.get('Claim ID',''),
      'Attached Reference Count (Original)':r.get('Attached Reference Count',''),
      'Institutions Referenced (Original)':r.get('Institutions Referenced',''),
      'Audit Status (Original)':r.get('Audit Status',''),
      'Audit Note (Original)':r.get('Audit Note',''),
      'Source Register Row Link':'UNRESOLVED — no reliable row-level key in supplied files',
      'EMASI Syllabus Validation':'NOT PROVIDED / NOT VERIFIED',
    })
write_csv('MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv', list(mx[0]), mx)

# Summarize traceability gaps, without upgrading source status.
from collections import Counter
counts=Counter(x['Conservative Evidence Scope'] for x in ledger)
url_missing=sum(not x['URL'] for x in ledger)
non_https=sum(bool(x['URL']) and not x['URL'].lower().startswith('https://') for x in ledger)
report=f'''# Horizon v25.6 — Evidence Traceability & Claim Verification Inventory

## Purpose
This release adds stable row IDs and a conservative traceability inventory to the existing evidence files. It is an offline documentation and data-integrity improvement, **not** a content verification or academic validation.

## What changed
- Every row in `SOURCE_CLAIM_REGISTER.csv` now has a stable `Source Row ID` in `SOURCE_TRACEABILITY_LEDGER_V25_6.csv`.
- The ledger preserves original claim fields and adds a conservative evidence-scope label and a plain-language use boundary.
- Every row in `EMASI_13x20_AUDIT_MATRIX.csv` now has a stable `Matrix Pair ID` in `MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv`.
- The crosswalk explicitly records whether the original matrix claim ID can be joined to a source-register row. No unsupported joins are guessed.

## Current inventory
- Source-register rows: {len(ledger)}
- Major–subject matrix pairs: {len(mx)}
- Rows classified as programme availability only: {counts['PROGRAMME_AVAILABILITY_ONLY']}
- Rows classified as curriculum context requiring page-level review: {counts['CURRICULUM_CONTEXT_REVIEW_REQUIRED']}
- Rows classified as broad disciplinary context only: {counts['DISCIPLINARY_CONTEXT_ONLY']}
- Rows classified as professional guidance context: {counts['PROFESSIONAL_GUIDANCE_CONTEXT']}
- Rows requiring other manual scope review: {counts['OTHER_SCOPE_MANUAL_REVIEW']}
- Missing URL fields: {url_missing}
- Non-HTTPS URL fields: {non_https}

## Important traceability limitation
The supplied source register uses a `Claim Number` that repeats within majors, while the matrix uses a separate `Claim ID` format. The supplied files do not establish a reliable row-level foreign key between these records. Therefore v25.6 **does not claim that a particular source-register row supports a particular matrix pair**. The crosswalk preserves the original identifiers and marks the link unresolved until a human-reviewed mapping is supplied.

## Evidence boundaries
1. A programme listing does not establish curriculum content, subject prerequisites, or EMASI alignment.
2. A curriculum page may provide context, but its exact content must be reviewed against the wording of the claim.
3. A URL being present, reachable, or hosted by a university does not prove that it supports the claim.
4. Attached-reference counts and institution lists remain original bookkeeping fields; they are not independently validated by this release.
5. No EMASI grade-level syllabus or learning-outcome comparison is supplied in this dataset. No subject-major pair is upgraded to verified.

## Required next step
Create a human-reviewed source-to-claim crosswalk using the actual cited pages and exact claim wording. Then compare relevant claims with the official EMASI grade-level syllabus and learning outcomes. Keep uncertain relationships labelled exploratory.
'''
(ROOT/'EVIDENCE_TRACEABILITY_REPORT_V25_6.md').write_text(report,encoding='utf-8')

readme='''# Horizon v25.6 — Evidence Traceability Development\n\nThis package adds row-level IDs and conservative source-scope inventory files. It does not alter the app's matching logic, public deployment, or the protected v24 baseline.\n\n## New files\n- `SOURCE_TRACEABILITY_LEDGER_V25_6.csv` — stable IDs and scope boundaries for source-register rows.\n- `MATRIX_TRACEABILITY_CROSSWALK_V25_6.csv` — stable IDs for matrix pairs and explicit unresolved source-row linkage.\n- `EVIDENCE_TRACEABILITY_REPORT_V25_6.md` — limitations and next validation steps.\n- `build_claim_traceability_v25_6.py` — reproducible generator.\n- `qa_v25_6.py` — offline QA.\n\nRun: `python build_claim_traceability_v25_6.py && python qa_v25_6.py`\n\nNo live URL check, source-page content review, EMASI syllabus validation, browser test, or privacy review is claimed.\n'''
(ROOT/'README_V25_6.md').write_text(readme,encoding='utf-8')
(ROOT/'V25_6_CHANGELOG.md').write_text('''# v25.6 changelog\n\n- Added deterministic row-level source IDs without changing original source rows.\n- Added conservative evidence-scope labels and use boundaries.\n- Added matrix pair IDs and a separate crosswalk.\n- Explicitly marked source-register-to-matrix joins unresolved where no reliable foreign key exists.\n- Added a reproducible generator and offline QA.\n- No app logic, v24 baseline, or Railway deployment changed.\n''',encoding='utf-8')
(ROOT/'VERSION.txt').write_text('Horizon v25.6 — Evidence Traceability Development\n',encoding='utf-8')
print(f'Generated {len(ledger)} source rows and {len(mx)} matrix rows')
