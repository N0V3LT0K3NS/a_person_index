# MCP Interface

This repository now exposes a read-only MCP adapter for agent-native access.

## Why it exists

The Python CLI remains the canonical maintainer and query interface, but downstream runtimes such as `GNOMY` benefit from a standard agent-facing surface.

The MCP adapter solves that by exposing the existing registry primitives through:

- resources
- tools
- prompts

The MCP layer is an adapter, not a second source of truth.

## Implementation stance

- Transport: stdio
- Runtime: Node.js
- SDK: `@modelcontextprotocol/sdk`
- Backend logic: delegated to the existing Python query CLI

This keeps business logic in one place.

## Current command surface

Start the server locally:

```bash
npm run mcp:serve
```

Run the smoke test:

```bash
npm run mcp:smoke
```

## Exposed resources

- `registry://manifest`
- `registry://current-state`
- `registry://roadmap`
- `registry://research-promotion`
- `registry://protocol-packs`
- `registry://protocol-pack/{pack_id}`
- `registry://protocol-pack-grammar`
- `registry://instrument/{slug}`

## Exposed tools

- `find_framework_records`
- `compare_frameworks`
- `trace_to_motifs`
- `list_related_motifs`
- `list_interaction_hypotheses`
- `fetch_protocol_spec`
- `list_protocol_packs`
- `fetch_curated_protocol_pack`
- `fetch_protocol_pack`
- `fetch_protocol_pack_grammar`
- `fetch_result_atom_schema`
- `fetch_research_models`
- `fetch_research_promotion_policy`

## Exposed prompts

- `registry-arrival`
- `protocol-pack-authoring`

## Maintenance rule

The MCP adapter should remain thin.

Do:
- call into the existing Python query/build surface
- expose only stable primitives
- keep onboarding, grammar, and manifest resources aligned

Do not:
- reimplement registry logic in Node
- mutate canonical records through MCP
- let MCP responses drift from CLI semantics

## Versioning and constraints

- The MCP layer is currently read-only.
- The MCP adapter depends on Node, not Python MCP, because the official Python MCP SDK requires Python 3.10+ while this repo currently targets Python 3.9+.
- If the Python runtime baseline rises later, the adapter can be reconsidered.
