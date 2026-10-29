#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from client import post_json, post_file, save_binary

OUT = Path("out")

def from_json(path: Path, dest: Path) -> Path:
    payload = json.loads(path.read_text())
    r = post_json("/v1/pptx/from-json", payload)
    if r.status_code >= 400 or r.content[:2] != b"PK":
        r = post_file(
            "/v1/pptx/from-json",
            files={"file": (path.name, path.read_bytes(), "application/json")},
        )
    return save_binary(r, dest)

def from_markdown(path: Path, dest: Path) -> Path:
    md = path.read_text(encoding="utf-8")
    r = post_json("/v1/pptx/from-markdown", {"markdown": md})
    if r.status_code >= 400 or r.content[:2] != b"PK":
        r = post_file("/v1/pptx/from-markdown", files={"file": (path.name, md.encode(), "text/markdown")})
    return save_binary(r, dest)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["from-json", "from-markdown"])
    ap.add_argument("path", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    dest = args.out or (OUT / ("from-json.pptx" if args.mode == "from-json" else "from-markdown.pptx"))
    if args.mode == "from-json":
        from_json(args.path, dest)
    else:
        from_markdown(args.path, dest)

if __name__ == "__main__":
    main()
