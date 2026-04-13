# MCP Examples

These are shareable example surfaces for configuring A Person Index as a read-only MCP dependency.

Use them as templates, not as canonical source of truth.

Canonical implementation and usage docs:

- [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
- [docs/mcp_clients.md](/Users/noveltokens/a_person_index/docs/mcp_clients.md)

Files here:

- `claude-code.mcp.json.example`
  Example strict config for Claude Code. Replace the placeholder repo path before use.
- `claude-desktop-config.json.example`
  Example fragment for Claude Desktop's MCP config. Merge it into the app config instead of replacing the whole file.
- `hermes-wrapper.sh.example`
  Example wrapper script for Hermes or another client that wants a stable stdio entrypoint.
