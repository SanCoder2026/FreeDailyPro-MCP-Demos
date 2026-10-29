# FreeDailyPro MCP — install for agents / llms

Remote MCP server (no local install):

- **URL:** `https://api.freedailypro.com/mcp`
- **Auth header:** `X-API-Key: <key from https://www.freedailypro.com/developers>`
- **Registry:** `com.freedailypro/tools`
- **Machine-readable:** https://api.freedailypro.com/llms.txt
- **REST base:** https://api.freedailypro.com
- **OpenAPI:** https://api.freedailypro.com/openapi.json

## Claude Desktop / Cursor JSON

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

## Env for REST demos in this repo

```bash
export FREEDAILYPRO_API_KEY="YOUR_API_KEY"
pip install -r requirements.txt
```

Trial: 20,000 calls/mo. Files processed in memory; not stored after response. Gaps: OCR, Word/Excel, camera/mic.
