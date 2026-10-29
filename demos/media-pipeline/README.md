# Demo 5 — Media pipeline agent

**Intent:** ffmpeg-backed media ops for agents: image resize/convert + video trim, thumbnail, burn-in subtitles.

## Endpoints

| Step | Path |
|------|------|
| Image resize | `POST /v1/image/resize` |
| Image convert | `POST /v1/image/convert` |
| Video trim | `POST /v1/video/trim` |
| Thumbnail | `POST /v1/video/thumbnail` |
| Subtitles | `POST /v1/video/subtitle` |
| Optional compress | `POST /v1/video/compress` |

**Note:** MCP video/audio tools may enforce smaller file limits than REST (base64 overhead). Prefer REST for large files.

## Run

```bash
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"
python3 media_pipeline.py image photo.jpg --width 1280 --height 720
python3 media_pipeline.py video clip.mp4 --start 0 --end 15 --thumb-at 3 --srt captions.srt
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

> Resize `hero.png` to 1280x720 WebP. Trim `demo.mp4` to 0–12s, grab a thumbnail at 2s, burn in `captions.srt`.

## Agent system brief

```
You are a media pipeline agent using FreeDailyPro image/video endpoints.
Prefer REST for large media. No live camera/mic. Files are not stored after processing.
```
