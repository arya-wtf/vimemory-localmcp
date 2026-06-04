#!/usr/bin/env python3
"""Memory Share — MCP server (stdio).

A thin pass-through that lets Claude Desktop save/recall memory via the
Memory Share gateway running on your VPS. All real work (embedding, vector
search, per-user isolation) happens in the gateway. This process just:

  - exposes MCP tools to Claude
  - forwards each call to the gateway over HTTPS with the user's API key

Each teammate runs their own copy with their own API key, so memory stays
isolated per person.

Config (environment variables):
  MEMORY_GATEWAY_URL   e.g. https://memory.elux.space   (required)
  MEMORY_API_KEY       your personal msk_... key          (required)

Run: python server.py   (Claude Desktop launches this for you — see README)
"""
import os
import sys
import httpx
from mcp.server.fastmcp import FastMCP

GATEWAY_URL = os.environ.get("MEMORY_GATEWAY_URL", "").rstrip("/")
API_KEY = os.environ.get("MEMORY_API_KEY", "")

if not GATEWAY_URL or not API_KEY:
    # Fail loudly to stderr so Claude Desktop's MCP log shows the reason.
    print(
        "[memory-share] Missing config. Set MEMORY_GATEWAY_URL and MEMORY_API_KEY "
        "in your Claude Desktop MCP env.",
        file=sys.stderr,
    )

mcp = FastMCP("memory-share")

_HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
_TIMEOUT = 30.0


def _post(path: str, payload: dict) -> dict:
    r = httpx.post(f"{GATEWAY_URL}{path}", json=payload, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def _get(path: str, params: dict | None = None) -> dict:
    r = httpx.get(f"{GATEWAY_URL}{path}", params=params, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def _delete(path: str) -> dict:
    r = httpx.delete(f"{GATEWAY_URL}{path}", headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


@mcp.tool()
def save_memory(text: str, title: str = "", thread: str = "", tags: list[str] | None = None) -> str:
    """Save a summary or decision to your private memory so other AI models can recall it later.

    Use this when the user asks to remember something, or after settling an
    important decision/context. Save a clean, concise summary — not a raw dump.

    Args:
        text: The content to remember (a tidy summary works best).
        title: Short title for the memory.
        thread: Project or conversation group, e.g. "project-x".
        tags: Optional keywords, e.g. ["pricing", "project-x"].
    """
    data = _post("/save", {
        "text": text,
        "title": title or None,
        "thread": thread or None,
        "tags": tags or [],
    })
    return f"Saved to your memory (id={data.get('memory_id')}, {data.get('chunks')} chunk(s))."


@mcp.tool()
def search_memory(query: str, limit: int = 5) -> str:
    """Recall relevant context from your private memory by meaning (not keywords).

    Use this at the start of a task to load what you already know, or whenever
    the user references past decisions/projects.

    Args:
        query: What you want to recall, in natural language.
        limit: How many chunks to return (default 5).
    """
    data = _post("/search", {"query": query, "limit": limit})
    ctx = data.get("context", "").strip()
    if not ctx:
        return "No relevant memory found."
    return ctx


@mcp.tool()
def list_memory(limit: int = 20) -> str:
    """List your most recent saved memories (titles + dates), newest first.

    Args:
        limit: How many to list (default 20).
    """
    data = _get("/list", {"limit": limit})
    mems = data.get("memories", [])
    if not mems:
        return "No memories saved yet."
    lines = []
    for m in mems:
        tags = f" [{m['tags']}]" if m.get("tags") else ""
        thread = f" · {m['thread']}" if m.get("thread") else ""
        lines.append(f"- {m.get('title') or '(untitled)'}{thread}{tags}  ({m['created_at']})  id={m['id']}")
    return "\n".join(lines)


@mcp.tool()
def delete_memory(memory_id: str) -> str:
    """Delete one memory by its id (get the id from list_memory).

    Args:
        memory_id: The id of the memory to delete.
    """
    _delete(f"/memory/{memory_id}")
    return f"Deleted memory {memory_id}."


if __name__ == "__main__":
    mcp.run()
