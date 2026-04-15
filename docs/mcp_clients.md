# MCP Clients

This document captures the tested client paths for A Person Index's read-only MCP surface and gives copy-pasteable setup flows.

## Readiness

A Person Index is ready for:

- local stdio MCP use
- nearby runtime use through the existing Node adapter
- downstream agents such as `GNOMY`
- host-specific operator layers such as the Codex companion skill

It is not yet a hosted remote MCP service with auth, rate limiting, or multi-tenant operations.

The repo now also carries seeded host profiles for the currently documented
client paths so planning and actualization can start from a known environment
without hand-declaring every capability every time.

## What is already proven

The MCP surface has been validated in four layers:

1. repo-owned Node SDK smoke and contract tests
2. Claude Code using an explicit strict MCP config
3. Claude Desktop using the app MCP config file
4. Hermes remote-host assumptions and wrapper path checked, but live Hermes CLI execution remains environment-dependent

## Canonical local checks

From the repo root:

```bash
npm run mcp:smoke
npm run mcp:contract
```

These verify the server boots, exposes the expected tools and resources, and returns valid structured payloads for the core comparative and research primitives.

## Claude Code

Claude Code works best here with an explicit config file rather than relying on sticky local MCP state.

Write a local config file with the repo root resolved:

```bash
./scripts/write_claude_mcp_config.sh
```

That writes a config file under `output/claude-code/` by default and prints the path.

Run the tested Claude Code prompt:

```bash
./scripts/test_claude_code_mcp.sh
```

This uses:

- `--mcp-config`
- `--strict-mcp-config`
- `--permission-mode bypassPermissions`
- `--output-format json`

Notes:

- Claude Code auth must already be configured on the machine.
- The script does not mutate repo state.
- If you want a different prompt, pass it as the first argument.

## Claude Desktop

Claude Desktop uses its own MCP config file and does not automatically inherit Claude Code's config.

Default config path on macOS:

```bash
~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Write or update the desktop config entry safely:

```bash
./scripts/write_claude_desktop_mcp_config.sh
```

What the script does:

1. resolves the repo root
2. resolves an absolute `node` path
3. backs up the existing Claude desktop config if present
4. adds or updates the `a-person-index` MCP entry
5. preserves other MCP servers and preferences

After running it:

1. fully quit Claude Desktop with `Cmd-Q`
2. reopen Claude
3. start a new chat
4. ask which MCP servers are available

Template example:

- [examples/mcp/claude-desktop-config.json.example](/Users/noveltokens/a_person_index/examples/mcp/claude-desktop-config.json.example)

## Hermes

Hermes has a documented remote-host path for this MCP, but live execution still
depends on the actual remote environment having the Hermes CLI installed and on
PATH.

The shareable path is:

```bash
./scripts/test_hermes_remote_mcp.sh user@host
```

What the script does:

1. clones or fast-forwards the repo on the remote host
2. creates or updates the Python virtualenv
3. installs Python and Node dependencies
4. writes a wrapper at `~/bin/a-person-index-mcp`
5. registers the MCP in Hermes if missing
6. runs `hermes mcp test a-person-index`
7. runs a real Hermes chat query that must use MCP tools

Hermes-specific assumptions:

- remote host already has the `hermes` CLI installed
- Hermes keeps its bundled Node runtime at `~/.hermes/node/bin`
- the remote user has permission to clone the GitHub repo and write to `~/workspace` and `~/bin`

At the moment, treat Hermes as a documented and partially checked path rather
than as a uniformly proven client path across every environment.

Template examples:

- [examples/mcp/claude-code.mcp.json.example](/Users/noveltokens/a_person_index/examples/mcp/claude-code.mcp.json.example)
- [examples/mcp/claude-desktop-config.json.example](/Users/noveltokens/a_person_index/examples/mcp/claude-desktop-config.json.example)
- [examples/mcp/hermes-wrapper.sh.example](/Users/noveltokens/a_person_index/examples/mcp/hermes-wrapper.sh.example)

## Consumer-facing recommendation

For real downstream consumers:

1. use MCP first
2. use the companion Codex skill only as an operator guide
3. fall back to the CLI only when MCP is unavailable or when running maintainer workflows

## What remains before a stronger "production" claim

For local and nearby-agent use, the MCP is ready now.

For a stronger hosted/shared-service claim, the remaining work would be:

- remote transport and deployment topology
- authentication and authorization
- rate limiting and abuse controls
- observability and error monitoring
- explicit backward-compatibility policy for tool/resource contracts

That is intentionally outside the current scope.
