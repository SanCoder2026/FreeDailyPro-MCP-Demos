# Demo 3 — Content repurposing agent

**Intent:** Turn a blog draft into SEO meta, social captions, hashtags, and a short PPTX outline deck — deterministic text/SEO tools + Markdown→PPTX (not "AI magic" for word-count).

## Endpoints

| Step | Path |
|------|------|
| Word count | `POST /v1/text/word-count` (works without a key, IP-limited) |
| Slug | `POST /v1/text/slug` |
| Meta tags | `POST /v1/seo/meta-tags` |
| Captions | `POST /v1/seo/caption-generator` |
| Hashtags | `POST /v1/seo/hashtags` |
| Markdown → PPTX | `POST /v1/pptx/from-markdown` |

## Run

```bash
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"
python3 repurpose.py draft.md --title "Ship MCP tools that do real PDF work"
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

> Take this Markdown article. Produce: word count, slug, SEO meta tags, LinkedIn + X captions, hashtags, and a 6-slide PPTX outline via from-markdown.

## Agent system brief

```
You are a content repurposing agent. Use FreeDailyPro text + SEO + pptx/from-markdown tools.
Be honest: grammar-check / paraphrase / caption helpers are utilities — verify brand voice yourself.
```
