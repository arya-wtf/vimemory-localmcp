# ViMemory — MCP Server (for Claude Desktop)

This lets your team **save and recall memory straight from Claude Desktop**.
It's a thin local connector: it forwards each call to the ViMemory gateway
on your VPS using each person's own API key. Memory stays isolated per person.

```
Claude Desktop  ──(stdio)──▶  this MCP server  ──(HTTPS + your key)──▶  Gateway (VPS)
```

---

## What each teammate installs (one time, ~3 minutes)

### 1. Get the code + dependencies

```bash
# clone the project (or copy just the local-mcp/ folder)
git clone https://github.com/<you>/vimemory.git
cd vimemory/local-mcp

# install (Python 3.10+)
pip install -r requirements.txt
```

> Tip: find your Python path with `which python3` — you'll need it below.

### 2. Add it to Claude Desktop

Open Claude Desktop config:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add (or merge) this, filling in the three values:

```json
{
  "mcpServers": {
    "vimemory": {
      "command": "/full/path/to/python3",
      "args": ["/full/path/to/vimemory/local-mcp/server.py"],
      "env": {
        "MEMORY_GATEWAY_URL": "https://vimemory.xyz",
        "MEMORY_API_KEY": "msk_your_personal_key"
      }
    }
  }
}
```

- `command` — your Python path (from `which python3`).
- `args` — the absolute path to `server.py`.
- `MEMORY_GATEWAY_URL` — your gateway's address.
- `MEMORY_API_KEY` — **their own** `msk_...` key (you minted it with `manage.py adduser`).

### 3. Restart Claude Desktop

You'll see **vimemory** in the tools list (the 🔌 / tools icon).

---

## How they use it

Just talk to Claude:

- *"Save this decision to my memory: Project-X is 500k/mo on the Pro tier."* → `save_memory`
- *"What do we know about Project-X pricing?"* → `search_memory`
- *"List my recent memories."* → `list_memory`
- *"Delete memory abc123."* → `delete_memory`

Then in OpenWebUI / another model, they recall the same memory (see `../OPENWEBUI.md`).

---

## Tools exposed

| Tool | What it does |
|---|---|
| `save_memory` | Store a summary/decision (text, title, thread, tags). |
| `search_memory` | Recall relevant context by meaning. |
| `list_memory` | List recent saved memories. |
| `delete_memory` | Delete one memory by id. |

---

## Troubleshooting

- **Tool doesn't appear:** check the JSON is valid (no trailing commas) and paths are absolute. Fully quit and reopen Claude Desktop.
- **"Missing config" in logs:** `MEMORY_GATEWAY_URL` or `MEMORY_API_KEY` not set in the `env` block.
- **401 errors:** wrong/expired API key. Re-issue with `manage.py adduser` on the VPS.
- **Connection errors:** confirm `https://<gateway>/health` returns `{"ok":true}` from that machine.
