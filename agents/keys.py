#!/usr/bin/env python3
"""
keys.py  —  loads API keys from Whole App/.env so every agent finds them.

.env is gitignored (this repo is public). Copy .env.example to .env and fill it in.
Keys already set in the shell win over .env.

Usage
-----
  python3 agents/keys.py          # check which keys are set and that the Claude key works (free call)
"""

import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"


def load():
    if not ENV.exists():
        return
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if v and k not in os.environ:
            os.environ[k] = v


def check():
    load()
    if not ENV.exists():
        print("No .env yet. Run: cp .env.example .env  (then paste your keys into .env)")
    ok = True
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY          missing")
        ok = False
    else:
        import anthropic
        try:
            anthropic.Anthropic().models.retrieve("claude-opus-5-5")  # free: no tokens used
            print(f"ANTHROPIC_API_KEY          works (…{key[-4:]})")
        except anthropic.AuthenticationError:
            print("ANTHROPIC_API_KEY          rejected: check you pasted the whole key")
            ok = False
        except anthropic.APIError as e:
            print(f"ANTHROPIC_API_KEY          set, but the check failed: {e}")
            ok = False
    for k in ("ANTHROPOLOGIC_EMAIL", "ANTHROPOLOGIC_PASSWORD", "ANTHROPOLOGIC_TENANT_ID", "ANTHROPOLOGIC_FIREBASE_KEY",
              "ANTHROPOLOGIC_BASE_URL"):
        print(f"{k:<27}{'set' if os.environ.get(k) else 'missing'}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if check() else 1)
