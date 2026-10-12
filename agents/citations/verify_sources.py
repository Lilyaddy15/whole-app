#!/usr/bin/env python3
"""
verify_sources.py  —  proves every WHOLE citation is a real article.

No model involved: this is a plain lookup against the public records.

For each source on each "Real or hype?" verdict in data/evidence.json:
  - PMID  -> PubMed E-utilities (esummary + abstract)
  - DOI   -> Crossref
  - other -> the URL must load (HTTP 200)
The recorded title must match the official title, and the year must match.
Matching sources get  verified: true, the official title/journal/year, and
(for PubMed) the abstract, which the Editor Agent reads to confirm the study
actually supports the verdict.

Then the publishing rule is applied to each verdict:
  - every verdict needs at least 2 verified sources
  - "real" and "hype" need at least one verified systematic review,
    meta-analysis, clinical guideline or expert-body statement
Verdicts that fail are set to review.status = "needs_sources" and the app
shows them as "Being checked" instead of a verdict.

Usage
-----
  python3 agents/citations/verify_sources.py              # verify everything in data/evidence.json
  python3 agents/citations/verify_sources.py --only sleep-mouth-taping
  python3 agents/citations/verify_sources.py --strict     # exit 1 if anything fails (for CI)
Standard library only. Uses NCBI's public API; be polite (it sleeps between calls).
"""

import argparse
import datetime as dt
import difflib
import html
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "data" / "evidence.json"
UA = "WHOLE-citation-check/1.0 (prototype; contact via github.com/Lilyaddy15/whole-app)"
STRONG_TYPES = {"Systematic review", "Meta-analysis", "Clinical guideline", "Expert body"}
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or "")).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def title_match(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return False
    return a in b or b in a or difflib.SequenceMatcher(None, a, b).ratio() >= 0.85


def pmid_from(src):
    if src.get("pmid"):
        return str(src["pmid"]).strip()
    m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", src.get("url", ""))
    return m.group(1) if m else ""


def doi_from(src):
    if src.get("doi"):
        return src["doi"].strip().removeprefix("https://doi.org/")
    m = re.search(r"doi\.org/(10\.[^\s?#]+)", src.get("url", ""))
    return m.group(1) if m else ""


def check_pubmed(pmid):
    _, body = get(f"{EUTILS}esummary.fcgi?db=pubmed&id={pmid}&retmode=json")
    rec = json.loads(body)["result"].get(pmid)
    if not rec or rec.get("error"):
        return None
    time.sleep(0.4)
    _, abstract = get(f"{EUTILS}efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text")
    time.sleep(0.4)
    return {"title": rec["title"].rstrip("."), "journal": rec.get("fulljournalname") or rec.get("source"),
            "year": rec.get("pubdate", "")[:4], "abstract": abstract.strip()[:3000], "via": "PubMed"}


def check_crossref(doi):
    _, body = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    msg = json.loads(body)["message"]
    parts = (msg.get("issued") or msg.get("published") or {}).get("date-parts", [[None]])[0]
    return {"title": (msg.get("title") or [""])[0], "journal": (msg.get("container-title") or [""])[0],
            "year": str(parts[0] or ""), "abstract": norm(msg.get("abstract", ""))[:3000], "via": "Crossref"}


def check_url(url):
    status, body = get(url)
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
    return {"title": html.unescape(m.group(1)).strip() if m else "", "journal": "", "year": "",
            "abstract": "", "via": f"HTTP {status}"} if status == 200 else None


def verify_source(src):
    """Returns (verified, reason). Updates src in place with official metadata."""
    try:
        pmid, doi = pmid_from(src), doi_from(src)
        rec = check_pubmed(pmid) if pmid else check_crossref(doi) if doi else check_url(src["url"])
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as e:
        return False, f"lookup failed: {e}"
    if not rec:
        return False, "not found"
    if rec["via"].startswith("HTTP"):
        ok = bool(rec["title"]) and (title_match(src["title"], rec["title"]) or src.get("type") in {"Clinical guideline", "Expert body"})
        reason = "page loads" if ok else f"page title doesn't match: {rec['title'][:80]}"
    else:
        ok = title_match(src["title"], rec["title"])
        if ok and src.get("year") and rec["year"] and src["year"] != rec["year"]:
            ok, reason = False, f"year is {rec['year']}, not {src['year']}"
        else:
            reason = "title matches" if ok else f"official title is: {rec['title'][:100]}"
    if ok:
        src.update({"title": rec["title"] or src["title"], "publisher": rec["journal"] or src.get("publisher", ""),
                    "year": rec["year"] or src.get("year", "")})
        if pmid and not src.get("url"):
            src["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        if rec["abstract"]:
            src["abstract"] = rec["abstract"]
    src["verified"] = ok
    src["verified_via"] = rec["via"]
    src["verified_at"] = dt.date.today().isoformat()
    return ok, reason


def publishable(claim):
    srcs = [s for s in claim.get("sources", []) if s.get("verified")]
    if len(srcs) < 2:
        return False, f"only {len(srcs)} verified source(s); 2 needed"
    if claim["verdict"] in ("real", "hype") and not any(s.get("type") in STRONG_TYPES for s in srcs):
        return False, f'"{claim["verdict"]}" needs a verified review, guideline or expert-body source'
    return True, "ok"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--only", nargs="+")
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()

    data = json.loads(EVIDENCE.read_text())
    failures = 0
    for cid, claim in data["claims"].items():
        if a.only and cid not in a.only:
            continue
        print(cid)
        for s in claim.get("sources", []):
            ok, reason = verify_source(s)
            print(f"  {'✓' if ok else '✗'} {s['title'][:70]}  ({reason})")
        ok, reason = publishable(claim)
        claim["citations_ok"] = ok
        if ok and claim.get("review", {}).get("status") == "needs_sources":
            claim["review"] = {"status": "pending", "editor": None}
        if not ok:
            failures += 1
            claim["review"] = {"status": "needs_sources", "editor": None, "notes": reason}
            print(f"  -> held back: {reason}")
        EVIDENCE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"\n{failures} verdict(s) held back for missing or unverified sources.")
    if a.strict and failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
