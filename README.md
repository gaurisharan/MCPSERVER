# Mini MCP Assistant

A small [MCP](https://modelcontextprotocol.io) server exposing three tools:

| Tool | Source | API key? |
| --- | --- | --- |
| `get_weather(latitude, longitude)` | Open-Meteo | No |
| `wikipedia_summary(topic)` | Wikipedia REST API | No |
| `ask_llm(question, context="")` | Google Gemini | Yes (free tier) |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then paste your Gemini key into .env
```

Get a free key at <https://aistudio.google.com/apikey>. Never commit `.env`.

## Run

Inspect and test the tools in the MCP Inspector:

```bash
mcp dev server.py
```

Or run directly over stdio (an MCP client normally launches this for you):

```bash
python server.py
```

## Connect to an MCP client

Add this to your client's MCP config (Claude Desktop, Cursor, etc.), using
absolute paths. Point `command` at the venv's Python so dependencies resolve:

```json
{
  "mcpServers": {
    "research-assistant": {
      "command": "/absolute/path/to/mini-mcp/.venv/bin/python",
      "args": ["/absolute/path/to/mini-mcp/server.py"]
    }
  }
}
```

On Windows use `...\\.venv\\Scripts\\python.exe`.

## Try it

- "What's the weather in Agra?" (lat 27.1767, lon 78.0081)
- "Summarize Alan Turing from Wikipedia, then explain it simply with ask_llm."

## Notes

- **SDK versions:** MCP Python SDK v2 renamed `FastMCP` to `MCPServer`.
  `server.py` tries the v2 import first and falls back to the v1 one, so it
  works with either.
- **Gemini model:** defaults to `gemini-3.1-flash-lite`. Google retires models
  often (`gemini-2.5-flash` is scheduled for shutdown on 16 Oct 2026), so set
  `GEMINI_MODEL` in `.env` if you need a different one.
- **stdio rule:** never `print()` in `server.py`. Stdout carries the MCP
  protocol; use `logging` (stderr).
- **Next step:** for a real agent, make Gemini the reasoning model in an MCP
  *client* and expose only weather and Wikipedia as tools, so the LLM decides
  which to call.
