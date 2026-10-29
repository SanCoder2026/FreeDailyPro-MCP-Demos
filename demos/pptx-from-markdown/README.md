# Demo 4 — PPTX deck builder agent

**Intent:** Agent-driven decks from structured JSON or Markdown via FreeDailyPro PowerPoint API.

## Endpoints

| Step | Path |
|------|------|
| From JSON | `POST /v1/pptx/from-json` |
| From Markdown | `POST /v1/pptx/from-markdown` |
| From CSV | `POST /v1/pptx/from-csv` |
| Optional extract | `POST /v1/pptx/extract/text` |

## Run

```bash
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"
python3 build_deck.py from-json slides.json
python3 build_deck.py from-markdown outline.md
```

See `slides.example.json` for shape.

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

> Build a 5-slide investor update deck as JSON (title, bullets, notes) and call FreeDailyPro pptx/from-json with brand color #4FD8C4 if the API accepts a theme/color field. Return the .pptx.

## Agent system brief

```
You are a deck builder. Prefer pptx/from-json for structured slides and pptx/from-markdown for outlines.
Output real editable PPTX. No fake "AI design" claims — layout follows FreeDailyPro templates.
```
