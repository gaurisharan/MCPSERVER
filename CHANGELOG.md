# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows Semantic Versioning.

---

## [0.1.0] - 2026-09-24

### Added
- MCP server configuration for integration with VS Code.
- Local `stdio` MCP server support.
- VS Code MCP configuration through `.vscode/mcp.json`.
- Integration with VS Code Agent for calling MCP tools.
- `ask_llm` MCP tool for sending questions to Gemini.
- `get_weather` MCP tool for retrieving current weather data using the free Open-Meteo API.
- `wikipedia_summary` MCP tool for retrieving English Wikipedia summaries.
- Python virtual environment for isolated project dependencies.
- `.env` support for storing API credentials locally.
- `.gitignore` configuration for excluding:
  - `.venv/`
  - `__pycache__/`
  - Python bytecode files
  - `.env`
  - macOS system files

### Changed
- Configured VS Code to launch the MCP server using the project's Python virtual environment.
- Connected the MCP server to VS Code's Agent/Chat interface.
- Enabled MCP tools for use directly from VS Code Chat.

### Infrastructure
- Added project dependency management through `requirements.txt`.
- Added local development configuration under `.vscode/`.
- Configured the MCP server to run through `server.py`.

---

## [0.2.0] - 2026-09-25

### Added
- Initial MCP server implementation.
- Research Assistant MCP server.
- Initial MCP tools:
  - `ask_llm`
  - `get_weather`
  - `wikipedia_summary`
- Local Python development environment.
- VS Code MCP server integration.
- VS Code Agent tool integration.

### Integration
- MCP server successfully registered with VS Code.
- MCP tools successfully exposed to VS Code Chat.
- Configured local `stdio` communication between VS Code and the MCP server.

---

<!--
## [Unreleased]

Future releases may include:

- Additional research and web-access tools.
- More LLM providers.
- Improved error handling.
- Tool input validation.
- Logging and debugging improvements.
- Automated testing.
- Additional documentation and usage examples.
-->

## Versioning Guide
Semantic Versioning - MAJOR.MINOR.PATCH

| Change                                 | Version change | Example         |
| -------------------------------------- | -------------- | --------------- |
| Breaking/incompatible change           | **MAJOR**      | `1.0.0 → 2.0.0` |
| New functionality, backward-compatible | **MINOR**      | `0.1.0 → 0.2.0` |
| Bug fix / small correction             | **PATCH**      | `0.2.0 → 0.2.1` |
