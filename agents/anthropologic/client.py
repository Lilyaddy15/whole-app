#!/usr/bin/env python3
"""
client.py  —  talks to the Anthropologic pipelines over HTTP.

Based on the Anthropologic cURL guide, corrected against what the web app sent
on 2026-10-28: the base URL is api.quilt.ai/anthropologic and the submit body is
flat ({"pipeline", "title", ...params}), not nested under "params".

Credentials come from Whole App/.env (see .env.example). Credits are charged on
submit, so nothing here submits unless the caller asks it to.

Usage
-----
  python3 agents/anthropologic/client.py --check                 # log in only (free)
  python3 agents/anthropologic/client.py --focus discourse "skincare" "US women 25-40" "United States"   # free
  python3 agents/anthropologic/client.py --get RUN_ID --out runs/x.json                                # free
"""

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agents"))
import keys  # noqa: E402

ORIGIN = "https://anthropologic.quilt.ai"
FIREBASE = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="
GO_BROAD = "Go broad — scan everything"
DONE = {"completed", "complete", "succeeded", "done"}
STOPPED = {"failed", "error", "cancelled"}

# Inputs each pipeline takes (from the guide). "query" is fixed per pipeline and filled in here.
PIPELINES = {
    "discourse":    {"credits": 10,  "query": "Discourse analysis",
                     "params": {"topic": "", "cohort": "", "country": "", "date_range": "", "focus": ""}},
    "trends":       {"credits": 10,  "query": "Trends analysis",
                     "params": {"category": "", "cohort": "", "country": "", "date_range": "", "focus": ""}},
    "segmentation": {"credits": 100, "query": "Segments analysis",
                     "params": {"category": "", "country": "", "client_question": "", "research_depth": ""}},
    "futures":      {"credits": 200, "query": "Future analysis",
                     "params": {"category": "", "research_depth": ""}},
}
DATE_RANGES = ["Last month", "Last 3 months", "Last 6 months", "Last year"]
MARKETS = ["Argentina", "Australia", "Brazil", "Canada", "Chile", "Colombia", "Denmark", "Egypt", "Finland",
           "France", "Germany", "Hong Kong", "India", "Indonesia", "Israel", "Italy", "Japan", "Kenya", "Malaysia",
           "Mexico", "Morocco", "Netherlands", "New Zealand", "Nigeria", "Norway", "Pakistan", "Philippines",
           "Poland", "Qatar", "Russia", "Saudi Arabia", "Singapore", "South Africa", "South Korea", "Spain",
           "Sweden", "Switzerland", "Taiwan", "Thailand", "Turkey", "United Arab Emirates", "United Kingdom",
           "United States", "Vietnam"]


def cost(pipeline, params):
    if pipeline == "futures" and params.get("research_depth") == "deep":
        return 5000
    return PIPELINES[pipeline]["credits"]


def validate(pipeline, params):
    """Raise if a run body would be rejected or would hang."""
    if pipeline not in PIPELINES:
        raise ValueError(f"unknown pipeline {pipeline}")
    missing = [k for k in PIPELINES[pipeline]["params"] if not params.get(k)]
    if missing:
        raise ValueError(f"{pipeline}: missing {', '.join(missing)}")
    if "country" in params and params["country"] not in MARKETS:
        raise ValueError(f"{pipeline}: {params['country']} is not one of the 44 Anthropologic markets")
    if "date_range" in params and params["date_range"] not in DATE_RANGES:
        raise ValueError(f"{pipeline}: date_range must be one of {DATE_RANGES}")
    if params.get("research_depth") not in (None, "quick", "deep"):
        raise ValueError(f"{pipeline}: research_depth must be quick or deep")


class Client:
    def __init__(self):
        keys.load()
        need = ["ANTHROPOLOGIC_EMAIL", "ANTHROPOLOGIC_PASSWORD", "ANTHROPOLOGIC_TENANT_ID",
                "ANTHROPOLOGIC_FIREBASE_KEY", "ANTHROPOLOGIC_BASE_URL"]
        missing = [k for k in need if not os.environ.get(k)]
        if missing:
            raise RuntimeError(f"missing in .env: {', '.join(missing)}")
        self.base = os.environ["ANTHROPOLOGIC_BASE_URL"].rstrip("/")
        self.token, self.expires = None, 0

    def _http(self, url, body=None, headers=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method="POST" if data else "GET",
                                     headers={"Content-Type": "application/json", **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"{e.code} from {url.split('?')[0]}: {e.read()[:300].decode(errors='replace')}")

    def login(self):
        if self.token and time.time() < self.expires - 120:
            return
        r = self._http(FIREBASE + os.environ["ANTHROPOLOGIC_FIREBASE_KEY"], {
            "email": os.environ["ANTHROPOLOGIC_EMAIL"], "password": os.environ["ANTHROPOLOGIC_PASSWORD"],
            "tenantId": os.environ["ANTHROPOLOGIC_TENANT_ID"], "returnSecureToken": True,
        }, {"Referer": ORIGIN + "/"})
        self.token, self.expires = r["idToken"], time.time() + int(r.get("expiresIn", 3600))

    def api(self, path, body=None):
        self.login()
        return self._http(f"{self.base}/api/v1/{path}", body, {
            "Authorization": f"Bearer {self.token}", "Origin": ORIGIN, "Referer": ORIGIN + "/"})

    def focus_options(self, pipeline, params):
        """Free pre-step for discourse/trends: focus options tailored to the inputs."""
        p = {k: v for k, v in params.items() if k not in ("date_range", "focus")}
        r = self.api("pipeline/query", {"params": {**p, "query": PIPELINES[pipeline]["query"]}})
        return (r.get("result") or r).get("focus_options") or [GO_BROAD]

    def submit(self, pipeline, params, title):
        """Charges credits. Returns the submit response (run_id, status, credits_used)."""
        validate(pipeline, params)
        return self.api("runs/submit", {**params, "query": PIPELINES[pipeline]["query"],
                                        "pipeline": pipeline, "title": title})

    def get(self, run_id):
        return self.api(f"runs/{run_id}")

    def wait(self, run_id, every=15, timeout=3600):
        start = time.time()
        while time.time() - start < timeout:
            run = self.get(run_id)
            if run.get("status") in DONE | STOPPED:
                return run
            time.sleep(every)
        raise RuntimeError(f"run {run_id} still not finished after {timeout // 60} min")


def payload(run):
    """The guide says the output sits at run.result.result.result; unwrap however deep it really is."""
    p = run
    for _ in range(3):
        if not (isinstance(p, dict) and isinstance(p.get("result"), dict)):
            break
        p = p["result"]
    return p


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="log in with the service account (free)")
    ap.add_argument("--focus", nargs=4, metavar=("PIPELINE", "TOPIC_OR_CATEGORY", "COHORT", "COUNTRY"))
    ap.add_argument("--get", metavar="RUN_ID")
    ap.add_argument("--out", help="with --get: save the payload here")
    a = ap.parse_args()
    try:
        c = Client()
        if a.check:
            c.login()
            print("Anthropologic login works")
        elif a.focus:
            pl, subject, cohort, country = a.focus
            key = "topic" if pl == "discourse" else "category"
            print(json.dumps(c.focus_options(pl, {key: subject, "cohort": cohort, "country": country}), indent=2))
        elif a.get:
            run = c.get(a.get)
            print(f"status: {run.get('status')}")
            if a.out:
                pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(a.out).write_text(json.dumps(payload(run), indent=2, ensure_ascii=False))
                print(f"saved → {a.out}")
        else:
            ap.print_help()
    except RuntimeError as e:
        sys.exit(f"Stopped: {e}")
