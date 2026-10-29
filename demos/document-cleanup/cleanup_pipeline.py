#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from client import post_file, save_binary

OUT = Path("out")

def flatten_pdf(src: Path, dest: Path) -> Path:
    r = post_file("/v1/pdf/flatten", files={"file": (src.name, src.read_bytes(), "application/pdf")})
    return save_binary(r, dest)

def watermark_pdf(src: Path, dest: Path, text: str) -> Path:
    r = post_file("/v1/pdf/watermark", files={"file": (src.name, src.read_bytes(), "application/pdf")}, data={"text": text})
    return save_binary(r, dest)

def clean_pptx(src: Path, dest: Path) -> Path:
    r = post_file("/v1/pptx/clean", files={"file": (src.name, src.read_bytes(), "application/vnd.openxmlformats-officedocument.presentationml.presentation")})
    return save_binary(r, dest)

def redact_pptx(src: Path, dest: Path, pattern: str) -> Path:
    r = post_file(
        "/v1/pptx/redact",
        files={"file": (src.name, src.read_bytes(), "application/vnd.openxmlformats-officedocument.presentationml.presentation")},
        data={"pattern": pattern},
    )
    return save_binary(r, dest)

def compress_pptx(src: Path, dest: Path) -> Path:
    r = post_file("/v1/pptx/compress/medium", files={"file": (src.name, src.read_bytes(), "application/vnd.openxmlformats-officedocument.presentationml.presentation")})
    return save_binary(r, dest)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=["pdf", "pptx"])
    p.add_argument("path", type=Path)
    p.add_argument("--redact")
    p.add_argument("--mark", default="COPY")
    args = p.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.kind == "pdf":
        flat = flatten_pdf(args.path, OUT / "flattened.pdf")
        watermark_pdf(flat, OUT / "share-safe.pdf", args.mark)
    else:
        cleaned = clean_pptx(args.path, OUT / "cleaned.pptx")
        cur = cleaned
        if args.redact:
            cur = redact_pptx(cur, OUT / "redacted.pptx", args.redact)
        compress_pptx(cur, OUT / "share-safe.pptx")

if __name__ == "__main__":
    main()
