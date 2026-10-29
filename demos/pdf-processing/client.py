#!/usr/bin/env python3
"""Minimal FreeDailyPro REST helper. Set FREEDAILYPRO_API_KEY."""
from __future__ import annotations
import os, sys
from pathlib import Path
import requests

BASE = "https://api.freedailypro.com"

def api_key() -> str:
    k = os.environ.get("FREEDAILYPRO_API_KEY", "").strip()
    if not k or k == "YOUR_API_KEY":
        print("Set FREEDAILYPRO_API_KEY to a key from https://www.freedailypro.com/developers", file=sys.stderr)
        sys.exit(1)
    return k

def headers() -> dict:
    return {"X-API-Key": api_key()}

def post_json(path: str, payload: dict, timeout: int = 120) -> requests.Response:
    r = requests.post(f"{BASE}{path}", headers={**headers(), "Content-Type": "application/json"}, json=payload, timeout=timeout)
    return r

def post_file(path: str, files: dict, data: dict | None = None, timeout: int = 300) -> requests.Response:
    r = requests.post(f"{BASE}{path}", headers=headers(), files=files, data=data or {}, timeout=timeout)
    return r

def save_binary(r: requests.Response, out: Path) -> Path:
    r.raise_for_status()
    out.write_bytes(r.content)
    print(f"Wrote {out} ({len(r.content)} bytes)")
    return out
