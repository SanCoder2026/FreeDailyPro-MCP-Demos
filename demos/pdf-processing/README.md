# Demo 1 — PDF processing agent

**Intent:** Show an agent (or script) running a real PDF pipeline: merge → split → compress → watermark → redact → fill forms.

## Endpoints used

| Step | Method | Path |
|------|--------|------|
| Merge | POST | `/v1/pdf/merge` |
| Split | POST | `/v1/pdf/split` |
| Compress | POST | `/v1/pdf/compress/balanced` |
| Watermark | POST | `/v1/pdf/watermark` |
| Redact | POST | `/v1/redact-pdf` |
| Parse form fields | POST | `/v1/fillable-forms/parse` |
| Fill form | POST | `/v1/fillable-forms/fill` |

## Prerequisites

- `FREEDAILYPRO_API_KEY` from https://www.freedailypro.com/developers  
- Sample PDFs in `./samples/` (or pass paths as CLI args)
- `pip install requests`

## Run (REST script)

```bash
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"
python3 pdf_pipeline.py --merge a.pdf b.pdf --out out/
# or exercise subcommands:
python3 pdf_pipeline.py compress input.pdf
python3 pdf_pipeline.py watermark input.pdf --text "CONFIDENTIAL"
python3 pdf_pipeline.py redact input.pdf --box 0,0.1,0.1,0.5,0.08
```

## MCP config

### Claude Desktop (`claude_desktop_config.json`)

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

Exact shape can vary by Claude Desktop version — if your build uses `command`/`args` only for local stdio servers, add FreeDailyPro as a **remote / custom connector** with URL `https://api.freedailypro.com/mcp` and header `X-API-Key`.


### Cursor (`mcp.json` / Settings → MCP)

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

Use the Cursor UI "Add new MCP server" if your version prefers that over hand-editing JSON.


## Example agent prompts

> You have FreeDailyPro MCP. Merge `invoice-a.pdf` and `invoice-b.pdf`, compress the result with balanced mode, watermark it with "INTERNAL", then return the file. Do not store anything locally beyond the download.

> Parse fillable fields on `w9.pdf`, then fill `fullName` and `ein` from the JSON I provide. Prefer flatten=true.

## Agent system brief (MCP)

```
You are a PDF pipeline agent. Prefer FreeDailyPro tools for merge, split, compress, watermark, redact, and fillable form parse/fill.
Coordinates for redact are fractional 0–1 per page. Never invent OCR — FreeDailyPro API has no OCR.
Files are processed in memory and not stored by the API after the response.
```
