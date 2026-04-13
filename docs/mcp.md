# MCP Interface

A Person Index now exposes a read-only MCP adapter for agent-native access.

## Why it exists

The Python CLI remains the canonical maintainer and query interface, but downstream runtimes such as `GNOMY` benefit from a standard agent-facing surface.

The MCP adapter solves that by exposing the existing registry primitives through:

- resources
- tools
- prompts

The MCP layer is an adapter, not a second source of truth.

## Fastest safe onboarding

For a newly arrived agent, the fastest reliable sequence is:

1. `orient_agent`
2. `registry://quickstart`
3. `registry://current-state`
4. `list_protocol_packs(featured=true)`

If the task is specifically an ILENS-style pass, read `registry://ilens-walkthrough` or use the `ilens-walkthrough` prompt before expanding a full pack.

If the task involves pasted user assessment results, then use [docs/assessment_workflow.md](/Users/noveltokens/a_person_index/docs/assessment_workflow.md) before improvising with motif or pack calls.

## Ready-to-share status

The MCP surface is now ready for serious local and nearby-agent use.

What is currently proven:

- repo-owned smoke and contract tests
- Claude Code via explicit strict MCP config
- Claude Desktop via the app MCP config file
- Hermes via a remote wrapper around the same stdio server

Client setup and tested commands live in [docs/mcp_clients.md](/Users/noveltokens/a_person_index/docs/mcp_clients.md).

## Companion Codex skill

If Codex is the host, the recommended companion skill is `$a-person-index`.

Canonical repo copy:

- [skills/a-person-index/SKILL.md](/Users/noveltokens/a_person_index/skills/a-person-index/SKILL.md)
- local install target: `$CODEX_HOME/skills/a-person-index`

That skill should:

- prefer MCP when it is configured
- fall back to the query CLI when MCP is unavailable
- choose program packs before rebuilding a workflow manually
- preserve the boundary between canonical records, house synthesis, index programs, and research contributions

The skill is a host-specific operator guide. The MCP remains the actual interface surface.

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

Run the deeper contract test:

```bash
npm run mcp:contract
```

Run both:

```bash
npm run mcp:test
```

## Exposed resources

- `registry://manifest`
- `registry://quickstart`
- `registry://current-state`
- `registry://roadmap`
- `registry://assessment-workflow`
- `registry://ilens-walkthrough`
- `registry://research-promotion`
- `registry://protocol-packs`
- `registry://protocol-pack/{pack_id}`
- `registry://protocol-pack-grammar`
- `registry://instrument/{slug}`

## Exposed tools

- `orient_agent`
- `find_framework_records`
- `compare_frameworks`
- `trace_to_motifs`
- `list_related_motifs`
- `list_interaction_hypotheses`
- `fetch_protocol_spec`
- `list_protocol_packs`
- `fetch_curated_protocol_pack`
- `fetch_protocol_pack_summary`
- `fetch_protocol_pack`
- `fetch_protocol_pack_grammar`
- `fetch_result_atom_schema`
- `fetch_research_models`
- `fetch_research_promotion_policy`

## Exposed prompts

- `registry-arrival`
- `assessment-results-intake`
- `ilens-walkthrough`
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

## Product-language note

The MCP surface still uses a `registry://` URI scheme for compatibility.

That scheme names the access surface, not the entire product. The product is A Person Index. Within it, the canonical registry remains one important layer.

## Versioning and constraints

- The MCP layer is currently read-only.
- The MCP adapter depends on Node, not Python MCP, because the official Python MCP SDK requires Python 3.10+ while this repo currently targets Python 3.9+.
- If the Python runtime baseline rises later, the adapter can be reconsidered.
- The strongest current production claim is local and nearby-agent readiness, not hosted remote service readiness.
