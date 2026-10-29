# Demo 2 — Document cleanup agent

**Intent:** Prepare docs for sharing: flatten PDFs, watermark, clean PPTX (strip notes/comments/author), redact sensitive strings in decks.

## Endpoints

| Step | Path |
|------|------|
| Flatten PDF | `POST /v1/pdf/flatten` |
| Watermark PDF | `POST /v1/pdf/watermark` |
| Clean PPTX | `POST /v1/pptx/clean` |
| Redact PPTX | `POST /v1/pptx/redact` |
| Compress PPTX | `POST /v1/pptx/compress/medium` |

## Run

```bash
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"
python3 cleanup_pipeline.py pdf path/to/file.pdf
python3 cleanup_pipeline.py pptx path/to/deck.pptx --redact "SECRET"
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


## Example prompts

> Clean `board-deck.pptx` for external sharing: remove notes, comments, hidden slides, and author metadata. Then redact any occurrence of "Acme Internal". Compress medium for email.

> Flatten `signed-contract.pdf` so form fields cannot be edited, then watermark "COPY".

## Agent system brief

```
You are a document cleanup agent. Use FreeDailyPro flatten/watermark for PDFs and clean/redact/compress for PPTX.
Goal: share-safe artifacts. Do not claim OCR or Word/Excel conversion — not available on this API.
```
