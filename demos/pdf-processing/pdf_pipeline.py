#!/usr/bin/env python3
"""PDF pipeline demo against api.freedailypro.com — no key embedded."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from client import post_file, save_binary

OUT = Path("out")

def merge(paths: list[Path], dest: Path) -> Path:
    files = [("files", (p.name, p.read_bytes(), "application/pdf")) for p in paths]
    # Some gateways expect repeated file fields named "files" or "file"
    r = post_file("/v1/pdf/merge", files=files)
    if r.status_code >= 400:
        # fallback: try "file" repeated
        files2 = [("file", (p.name, p.read_bytes(), "application/pdf")) for p in paths]
        r = post_file("/v1/pdf/merge", files=files2)
    return save_binary(r, dest)

def compress(src: Path, dest: Path) -> Path:
    r = post_file("/v1/pdf/compress/balanced", files={"file": (src.name, src.read_bytes(), "application/pdf")})
    return save_binary(r, dest)

def watermark(src: Path, dest: Path, text: str) -> Path:
    r = post_file(
        "/v1/pdf/watermark",
        files={"file": (src.name, src.read_bytes(), "application/pdf")},
        data={"text": text, "opacity": "0.25"},
    )
    return save_binary(r, dest)

def redact(src: Path, dest: Path, page: int, x: float, y: float, w: float, h: float) -> Path:
    boxes = {str(page): [{"x": x, "y": y, "w": w, "h": h}]}
    r = post_file(
        "/v1/redact-pdf",
        files={"file": (src.name, src.read_bytes(), "application/pdf")},
        data={"boxes": json.dumps(boxes)},
    )
    return save_binary(r, dest)

def parse_form(src: Path) -> dict:
    r = post_file("/v1/fillable-forms/parse", files={"file": (src.name, src.read_bytes(), "application/pdf")})
    r.raise_for_status()
    return r.json()

def fill_form(src: Path, dest: Path, values: dict, flatten: bool = True) -> Path:
    r = post_file(
        "/v1/fillable-forms/fill",
        files={"file": (src.name, src.read_bytes(), "application/pdf")},
        data={"values": json.dumps(values), "flatten": "true" if flatten else "false"},
    )
    return save_binary(r, dest)

def split(src: Path, dest: Path, ranges: str) -> Path:
    r = post_file(
        "/v1/pdf/split",
        files={"file": (src.name, src.read_bytes(), "application/pdf")},
        data={"ranges": ranges},
    )
    return save_binary(r, dest)

def main() -> None:
    p = argparse.ArgumentParser(description="FreeDailyPro PDF pipeline demo")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("merge"); m.add_argument("pdfs", nargs="+", type=Path); m.add_argument("-o", "--out", type=Path, default=OUT/"merged.pdf")
    c = sub.add_parser("compress"); c.add_argument("pdf", type=Path); c.add_argument("-o", "--out", type=Path, default=OUT/"compressed.pdf")
    w = sub.add_parser("watermark"); w.add_argument("pdf", type=Path); w.add_argument("--text", default="CONFIDENTIAL"); w.add_argument("-o", "--out", type=Path, default=OUT/"watermarked.pdf")
    r = sub.add_parser("redact"); r.add_argument("pdf", type=Path); r.add_argument("--box", required=True, help="page,x,y,w,h fractional"); r.add_argument("-o", "--out", type=Path, default=OUT/"redacted.pdf")
    s = sub.add_parser("split"); s.add_argument("pdf", type=Path); s.add_argument("--ranges", default="1-1"); s.add_argument("-o", "--out", type=Path, default=OUT/"split.bin")
    pf = sub.add_parser("parse-form"); pf.add_argument("pdf", type=Path)
    ff = sub.add_parser("fill-form"); ff.add_argument("pdf", type=Path); ff.add_argument("--values", required=True, help='JSON object e.g. {"fullName":"Jane"}'); ff.add_argument("-o", "--out", type=Path, default=OUT/"filled.pdf")

    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    if args.cmd == "merge":
        merge(args.pdfs, args.out)
    elif args.cmd == "compress":
        compress(args.pdf, args.out)
    elif args.cmd == "watermark":
        watermark(args.pdf, args.out, args.text)
    elif args.cmd == "redact":
        page, x, y, w, h = args.box.split(",")
        redact(args.pdf, args.out, int(page), float(x), float(y), float(w), float(h))
    elif args.cmd == "split":
        split(args.pdf, args.out, args.ranges)
    elif args.cmd == "parse-form":
        print(json.dumps(parse_form(args.pdf), indent=2))
    elif args.cmd == "fill-form":
        fill_form(args.pdf, args.out, json.loads(args.values))

if __name__ == "__main__":
    main()
