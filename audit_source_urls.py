"""Conservative live URL reachability audit for Horizon source records.

Run: python audit_source_urls.py [--timeout 15] [--limit 10] [--delay 0.5] [--retries 1]

This checks URL reachability only. It does NOT verify page contents, whether a
source supports a claim, EMASI syllabus equivalence, or admissions requirements.
A 403/429/5xx or timeout is marked REVIEW rather than automatically invalid.
"""
import argparse
import csv
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check_url(url, timeout=15, retries=1, user_agent="HorizonAcademicSourceAudit/1.1"):
    """Return one conservative result dict for a URL; HEAD falls back to GET."""
    last_detail = "No response"
    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            req = urllib.request.Request(
                url,
                headers={"User-Agent": user_agent, "Accept": "text/html,application/pdf,*/*"},
                method=method,
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    status = int(response.status)
                    headers = response.headers
                    return {
                        "URL": url,
                        "HTTP Status": str(status),
                        "Final URL": response.geturl(),
                        "Content Type": headers.get("Content-Type", ""),
                        "Reachability": "REACHABLE" if 200 <= status < 400 else "REVIEW",
                        "Method": method,
                        "Attempts": str(attempt + 1),
                        "Check Detail": "Response received; content not assessed",
                    }
            except urllib.error.HTTPError as exc:
                last_detail = f"{method} HTTP {exc.code}"
                # Some academic sites reject HEAD; GET is attempted next.
                if method == "GET" and exc.code in (403, 404, 410):
                    return {
                        "URL": url, "HTTP Status": str(exc.code), "Final URL": exc.geturl(),
                        "Content Type": exc.headers.get("Content-Type", ""),
                        "Reachability": "REVIEW", "Method": method,
                        "Attempts": str(attempt + 1),
                        "Check Detail": f"{last_detail}; inspect manually (access controls or moved content possible)",
                    }
            except Exception as exc:  # network errors vary by institution and environment
                last_detail = f"{method} {type(exc).__name__}: {exc}"
        if attempt < retries:
            time.sleep(min(2 ** attempt, 4))
    return {
        "URL": url, "HTTP Status": "", "Final URL": url, "Content Type": "",
        "Reachability": "REVIEW", "Method": "HEAD then GET",
        "Attempts": str(retries + 1), "Check Detail": last_detail,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--limit", type=int, default=0, help="0 checks all unique URLs")
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()
    if args.timeout <= 0 or args.delay < 0 or args.retries < 0:
        parser.error("timeout must be > 0; delay and retries must be >= 0")

    with (ROOT / "SOURCE_CLAIM_REGISTER.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    urls = list(dict.fromkeys(r["URL"].strip() for r in rows if r.get("URL", "").strip()))
    if args.limit:
        urls = urls[:args.limit]

    results = []
    for i, url in enumerate(urls, 1):
        result = check_url(url, timeout=args.timeout, retries=args.retries)
        results.append(result)
        print(f"[{i}/{len(urls)}] {result['Reachability']} {result['HTTP Status']} {url}")
        if i < len(urls):
            time.sleep(args.delay)

    out = ROOT / "SOURCE_URL_LIVE_AUDIT.csv"
    fields = ["URL", "HTTP Status", "Final URL", "Content Type", "Reachability", "Method", "Attempts", "Check Detail"]
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    reachable = sum(r["Reachability"] == "REACHABLE" for r in results)
    print(f"Wrote {out.name}: {len(results)} URLs checked; {reachable} reachable; {len(results)-reachable} need manual review.")
    print("Reachability is not evidence validation. Review every URL against its exact claim.")


if __name__ == "__main__":
    main()
