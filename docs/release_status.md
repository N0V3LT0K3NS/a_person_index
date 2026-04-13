# Release Status

This document states the current release posture of A Person Index in compact operational terms.

## Current release

- version: `v0.1.0`
- status: stable first public release
- default branch: `main`
- primary site: [a-person-index.netlify.app](https://a-person-index.netlify.app)

## Ready now

- canonical curation in Git-backed YAML
- generated JSON export consumption
- static docs and browse site
- CLI-based querying and validation
- read-only MCP consumption for local and nearby agents
- companion skill usage for Codex-class hosts
- queue-driven Codex expansion-task dispatch
- downstream runtime use by systems such as `GNOMY`

## Explicit non-goals of this release

- person-level inference runtime
- scoring engine for every framework
- raw personal-data storage
- hosted remote MCP service
- research operations backend with intake, aggregation, and review queues

## Best current interfaces

1. `generated/manifest.json`
2. `docs/current_state.md`
3. `docs/mcp.md`
4. `docs/mcp_clients.md`
5. `scripts/query_registry.py`
6. `.github/codex/task_queue.yaml`
7. `.github/workflows/dispatch-codex-queue-item.yml`
8. `npm run mcp:serve`

## Release quality bar met

- validation passes
- generated outputs build deterministically
- docs generation passes
- pytest passes
- MCP smoke and contract tests pass
- Claude Code client path tested
- Claude Desktop client path scripted and documented
- Hermes client path tested

## What comes next

The next work is adjacent, not missing:

1. integrate `GNOMY` and other consumers against the current substrate
2. expand motifs, mappings, and interaction hypotheses where real consumer pressure reveals gaps
3. build the research operations layer outside the canonical repo
4. broaden the canonical model beyond the current instrument-first shape only where real use proves it necessary
