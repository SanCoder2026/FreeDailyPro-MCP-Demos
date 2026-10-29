# FreeDailyPro MCP & API demos

Demo agents and scripts for **[FreeDailyPro](https://www.freedailypro.com/developers)** — privacy-first PDF, PowerPoint, media, and text tools for AI agents.

| | |
|--|--|
| Developers | https://www.freedailypro.com/developers |
| MCP endpoint | `https://api.freedailypro.com/mcp` (header `X-API-Key`) |
| REST base | https://api.freedailypro.com |
| Registry | `com.freedailypro/tools` |
| llms.txt | https://api.freedailypro.com/llms.txt |
| OpenAPI | https://api.freedailypro.com/openapi.json |
| Docs | https://api.freedailypro.com/docs |

**Surface:** 215+ REST endpoints · 211+ MCP tools  
**Trial:** 20,000 calls/mo (no card) · Paid: $24 / $69 / $129

## Setup

```bash
git clone https://github.com/SanCoder2026/FreeDailyPro-MCP-Demos.git
cd FreeDailyPro-MCP-Demos
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"   # from developers page — never commit
```

MCP client install: see [llms-install.md](./llms-install.md).

## Demos

| Folder | Workflow |
|--------|----------|
| [`demos/pdf-processing/`](./demos/pdf-processing/) | Merge → split → compress → watermark → redact → fill forms |
| [`demos/pptx-from-markdown/`](./demos/pptx-from-markdown/) | JSON / Markdown → PowerPoint |
| [`demos/document-cleanup/`](./demos/document-cleanup/) | Flatten / watermark PDF + clean / redact PPTX |
| [`demos/content-repurposing/`](./demos/content-repurposing/) | Text + SEO + Markdown→PPTX |
| [`demos/media-pipeline/`](./demos/media-pipeline/) | Image resize/convert + video trim/thumbnail/subtitle |

### Quick runs

```bash
# PDF merge + compress
cd demos/pdf-processing
python3 pdf_pipeline.py merge a.pdf b.pdf -o out/merged.pdf
python3 pdf_pipeline.py compress out/merged.pdf

# Markdown → PPTX
cd demos/pptx-from-markdown
python3 build_deck.py from-markdown outline.example.md
python3 build_deck.py from-json slides.example.json
```

## MCP snippet (Claude Desktop / Cursor)

```json
{
  "mcpServers": {
    "freedailypro": {
      "url": "https://api.freedailypro.com/mcp",
      "headers": {
        "X-API-Key": "YOUR_API_KEY"
      }
    }
  }
}
```

## Honest limits

- Files are processed in memory and **not stored** after the response.
- Browser tools on FreeDailyPro.com are **separate** from this API (~10 uses/day).
- **Not in the API yet:** OCR, Word/Excel conversion, live camera/mic.
- Scripts use REST; agent prompts in each README show MCP orchestration.

## License

MIT — see [LICENSE](./LICENSE).
