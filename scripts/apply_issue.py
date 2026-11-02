#!/usr/bin/env python3
"""Put a hand-edited issue file into data/issues.js, replacing that topic's content.

  python3 scripts/apply_issue.py runs/beauty/issue-01.json beauty

Keeps the topic's name and colors; every other field comes from the issue file.
Real-or-hype entries only need an id: verdicts are read from data/evidence.json.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
src, topic = pathlib.Path(sys.argv[1]), sys.argv[2]
issue = {k: v for k, v in json.loads(src.read_text()).items() if not k.startswith("_")}
evidence = json.loads((ROOT / "data/evidence.json").read_text())["claims"]
for h in issue.get("hype", []):
    e = evidence.get(h["id"])
    if not e:
        sys.exit(f"{h['id']} has no verdict in data/evidence.json")
    h.setdefault("v", e["verdict"]); h.setdefault("ev", e["evidence"])

js = (ROOT / "data/issues.js").read_text()
m = re.search(rf"^  {topic}:\{{\n(    name:.*\n)", js, re.M)
if not m:
    sys.exit(f"topic {topic} not found in data/issues.js")
end = re.search(r"^  \},?\n", js[m.end():], re.M)
body = ",\n".join(f"    {k}:{json.dumps(v, ensure_ascii=False)}" for k, v in issue.items())
block = f"  {topic}:{{\n{m.group(1).rstrip()}\n{body}\n  }},\n"
js = js[:m.start()] + block + js[m.end() + end.end():]
(ROOT / "data/issues.js").write_text(js)
print(f"{topic}: {len(issue)} fields from {src}")
