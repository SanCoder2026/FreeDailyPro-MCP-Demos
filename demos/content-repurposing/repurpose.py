#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from client import post_json, post_file, save_binary

OUT = Path("out")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--title", required=True)
    args = ap.parse_args()
    text = args.markdown.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    wc = post_json("/v1/text/word-count", {"text": text})
    print("word-count:", wc.status_code, wc.text[:500])

    slug = post_json("/v1/text/slug", {"text": args.title})
    print("slug:", slug.status_code, slug.text[:300])

    meta = post_json("/v1/seo/meta-tags", {
        "title": args.title,
        "description": text[:155].replace("\n", " "),
        "url": "https://www.freedailypro.com/developers",
    })
    print("meta-tags:", meta.status_code, meta.text[:500])

    caps = post_json("/v1/seo/caption-generator", {
        "topic": args.title,
        "platform": "linkedin",
        "tone": "professional",
    })
    print("captions:", caps.status_code, caps.text[:500])

    tags = post_json("/v1/seo/hashtags", {"text": args.title})
    print("hashtags:", tags.status_code, tags.text[:300])

    # Markdown → PPTX (multipart or JSON depending on API; try JSON body with markdown field, then file)
    r = post_json("/v1/pptx/from-markdown", {"markdown": text, "title": args.title})
    if r.status_code >= 400 or "application/json" in r.headers.get("content-type",""):
        r2 = post_file(
            "/v1/pptx/from-markdown",
            files={"file": (args.markdown.name, text.encode(), "text/markdown")},
            data={"title": args.title},
        )
        if r2.status_code < 400 and r2.content[:2] == b"PK":
            save_binary(r2, OUT / "deck.pptx")
        else:
            print("from-markdown response:", r.status_code, r.text[:400], r2.status_code, r2.text[:400])
    else:
        save_binary(r, OUT / "deck.pptx")

    (OUT / "repurpose-summary.json").write_text(json.dumps({
        "title": args.title,
        "word_count_status": wc.status_code,
        "slug_status": slug.status_code,
        "meta_status": meta.status_code,
    }, indent=2))

if __name__ == "__main__":
    main()
