"""Build a conservative, reproducible evidence-coverage inventory for Horizon.

This is a documentation/coverage audit, not a validation of academic claims.
It deliberately does not promote university curriculum references to EMASI
syllabus matches or admissions prerequisites.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read_csv(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(name, rows, fields):
    with (ROOT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def main():
    majors = json.loads((ROOT / "data/majors.json").read_text(encoding="utf-8"))
    claims = read_csv("SOURCE_CLAIM_REGISTER.csv")
    matrix = read_csv("EMASI_13x20_AUDIT_MATRIX.csv")
    by_claim = defaultdict(Counter)
    for row in claims:
        by_claim[row["Major"]][row["Claim Type"]] += 1
    by_matrix = defaultdict(list)
    for row in matrix:
        by_matrix[row["Major"]].append(row)

    types = sorted({r["Claim Type"] for r in claims})
    fields = ["Major", "Source Claim Rows", "Distinct Source URLs", "Programme Availability Only Rows",
              "Curriculum Context Rows", "Disciplinary Evidence Rows", "Professional Guidance Rows",
              "Other Claim Rows", "EMASI Subject Pairs", "Pairs With Current Guidance",
              "Pairs With No Guidance Entry", "Pairs Marked Exploratory Not EMASI Verified",
              "Pairs With Attached Reference Count", "EMASI Syllabus Verified Pairs"]
    report = []
    for major in majors:
        crows = [r for r in claims if r["Major"] == major]
        mrows = by_matrix[major]
        c = by_claim[major]
        programme = c["Programme availability evidence"]
        curriculum = c["Curriculum evidence for exploratory subject guidance"] + c["Curriculum scope"] + c["Institution-specific curriculum and course classification"] + c["Institution-specific curriculum comparison"] + c["Institution-specific curriculum structure"] + c["Cross-institution curriculum context"] + c["Programme existence / official curriculum reference"]
        disciplinary = c["Disciplinary evidence"]
        professional = c["Professional education guidance"]
        other = len(crows) - programme - curriculum - disciplinary - professional
        report.append({
            "Major": major,
            "Source Claim Rows": len(crows),
            "Distinct Source URLs": len({r["URL"].strip() for r in crows if r["URL"].strip()}),
            "Programme Availability Only Rows": programme,
            "Curriculum Context Rows": curriculum,
            "Disciplinary Evidence Rows": disciplinary,
            "Professional Guidance Rows": professional,
            "Other Claim Rows": other,
            "EMASI Subject Pairs": len(mrows),
            "Pairs With Current Guidance": sum(bool(r["Current Guidance Role"].strip()) for r in mrows),
            "Pairs With No Guidance Entry": sum(r["Audit Status"].strip() == "No current guidance entry" for r in mrows),
            "Pairs Marked Exploratory Not EMASI Verified": sum("not verified against emasi syllabus" in r["Audit Status"].lower() for r in mrows),
            "Pairs With Attached Reference Count": sum(bool(r["Attached Reference Count"].strip()) and r["Attached Reference Count"].strip() not in ("0", "0.0") for r in mrows),
            "EMASI Syllabus Verified Pairs": sum("verified against emasi" in r["Audit Status"].lower() and "not verified" not in r["Audit Status"].lower() for r in mrows),
        })

    write_csv("EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv", report, fields)
    totals = Counter()
    for row in report:
        for key in fields[1:]: totals[key] += int(row[key])
    all_urls = len({r["URL"].strip() for r in claims if r["URL"].strip()})
    claim_types = Counter(r["Claim Type"] for r in claims)
    lines = [
        "# Horizon v25.5 — Evidence Coverage Inventory",
        "",
        "## Purpose and interpretation",
        "This report describes the contents and status labels in the current source register and EMASI audit matrix. It is a coverage inventory, not an academic validation. Counts do not establish source quality, claim accuracy, causal relevance, or universal degree requirements.",
        "",
        "## Dataset totals",
        f"- Major profiles: {len(majors)}",
        f"- EMASI subjects per profile: 13",
        f"- Major–subject audit pairs: {len(matrix)}",
        f"- Source-claim register rows: {len(claims)}",
        f"- Distinct URLs in source register: {all_urls}",
        f"- Programme availability rows: {claim_types['Programme availability evidence']} (these establish only the listed programme availability/label, not EMASI subject alignment).",
        f"- Pairs with an existing guidance role: {totals['Pairs With Current Guidance']}",
        f"- Pairs with no current guidance entry: {totals['Pairs With No Guidance Entry']}",
        f"- Pairs explicitly labelled exploratory / not verified against EMASI syllabus: {totals['Pairs Marked Exploratory Not EMASI Verified']}",
        f"- Pairs labelled as EMASI-syllabus-verified in the matrix: {totals['EMASI Syllabus Verified Pairs']}",
        "",
        "## Evidence boundaries",
        "1. Programme availability is not curriculum evidence and is not a subject prerequisite.",
        "2. University curriculum references can provide exploratory disciplinary context, but do not prove equivalence to EMASI grade-level learning outcomes.",
        "3. An attached reference count is a register/matrix bookkeeping field; it does not prove that every cited page supports the specific subject-to-major suggestion.",
        "4. No EMASI syllabus-verified pair is currently labelled in the matrix. Do not describe any mapping as formally verified until the relevant EMASI syllabus and learning outcomes are reviewed pair by pair.",
        "5. This report does not assess URL reachability. Run audit_source_urls.py separately; reachability is not content validation.",
        "",
        "## Per-major inventory",
        "| Major | Claims | URLs | Programme availability | Curriculum context | Guidance pairs | No guidance | Exploratory / not EMASI-verified |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in report:
        lines.append(f"| {r['Major']} | {r['Source Claim Rows']} | {r['Distinct Source URLs']} | {r['Programme Availability Only Rows']} | {r['Curriculum Context Rows']} | {r['Pairs With Current Guidance']} | {r['Pairs With No Guidance Entry']} | {r['Pairs Marked Exploratory Not EMASI Verified']} |")
    lines += ["", "## Files", "- `EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv`: machine-readable per-major counts.", "- `SOURCE_CLAIM_REGISTER.csv`: underlying source/claim records.", "- `EMASI_13x20_AUDIT_MATRIX.csv`: underlying subject-pair status records.", ""]
    (ROOT / "EVIDENCE_COVERAGE_REPORT_V25_5.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote EVIDENCE_COVERAGE_BY_MAJOR_V25_5.csv ({len(report)} majors)")
    print(f"Wrote EVIDENCE_COVERAGE_REPORT_V25_5.md ({len(matrix)} pairs; {len(claims)} claims; {all_urls} URLs)")

if __name__ == "__main__":
    main()
