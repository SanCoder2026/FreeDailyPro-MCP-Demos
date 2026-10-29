#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from client import post_file, save_binary

OUT = Path("out")

def resize_image(src: Path, dest: Path, width: int, height: int) -> Path:
    r = post_file(
        "/v1/image/resize",
        files={"file": (src.name, src.read_bytes())},
        data={"width": str(width), "height": str(height)},
    )
    return save_binary(r, dest)

def convert_image(src: Path, dest: Path, fmt: str = "webp") -> Path:
    r = post_file(
        "/v1/image/convert",
        files={"file": (src.name, src.read_bytes())},
        data={"format": fmt},
    )
    return save_binary(r, dest)

def trim_video(src: Path, dest: Path, start: float, end: float) -> Path:
    r = post_file(
        "/v1/video/trim",
        files={"file": (src.name, src.read_bytes())},
        data={"start": str(start), "end": str(end)},
    )
    return save_binary(r, dest)

def thumbnail(src: Path, dest: Path, at: float) -> Path:
    r = post_file(
        "/v1/video/thumbnail",
        files={"file": (src.name, src.read_bytes())},
        data={"time": str(at)},
    )
    return save_binary(r, dest)

def burn_subs(src: Path, dest: Path, srt: Path) -> Path:
    r = post_file(
        "/v1/video/subtitle",
        files={
            "file": (src.name, src.read_bytes()),
            "subtitles": (srt.name, srt.read_bytes(), "application/x-subrip"),
        },
    )
    # some APIs take srt as form field text
    if r.status_code >= 400:
        r = post_file(
            "/v1/video/subtitle",
            files={"file": (src.name, src.read_bytes())},
            data={"srt": srt.read_text(encoding="utf-8")},
        )
    return save_binary(r, dest)

def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    img = sub.add_parser("image"); img.add_argument("path", type=Path); img.add_argument("--width", type=int, default=1280); img.add_argument("--height", type=int, default=720); img.add_argument("--format", default="webp")
    vid = sub.add_parser("video"); vid.add_argument("path", type=Path); vid.add_argument("--start", type=float, default=0); vid.add_argument("--end", type=float, default=10); vid.add_argument("--thumb-at", type=float, default=1); vid.add_argument("--srt", type=Path)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.cmd == "image":
        resized = resize_image(args.path, OUT / "resized.bin", args.width, args.height)
        convert_image(resized if resized.suffix else args.path, OUT / f"converted.{args.format}", args.format)
    else:
        trimmed = trim_video(args.path, OUT / "trimmed.mp4", args.start, args.end)
        thumbnail(trimmed, OUT / "thumb.jpg", args.thumb_at)
        if args.srt:
            burn_subs(trimmed, OUT / "subtitled.mp4", args.srt)

if __name__ == "__main__":
    main()
