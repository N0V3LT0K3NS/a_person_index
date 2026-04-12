# Curated Protocol Packs

This document defines the curated protocol-pack layer for A Person Index.

## What it is

Curated protocol packs are stable, reviewed runtime bundles built from:

- a source catalog entry in [protocol_packs/catalog.yaml](/Users/noveltokens/a_person_index/protocol_packs/catalog.yaml)
- an existing protocol spec
- its technique bundle
- scoped framework or construct targets
- generated motif traces, mappings, and interaction hypotheses

They sit between raw index program specs and fully ad hoc downstream assembly.

## Why they exist

Dynamic protocol packs are useful when an agent already knows its task and scope.

Curated protocol packs exist for repeated, important workflows where the repo should offer:

- a stable name
- a reviewed scope
- a maintained generated artifact
- a predictable bundle for downstream runtimes such as `GNOMY`

## Source of truth

The curated pack source of truth is:

- [protocol_packs/catalog.yaml](/Users/noveltokens/a_person_index/protocol_packs/catalog.yaml)

The internal `protocol_packs` path remains stable for compatibility even though the broader public product language is `program packs`.

Generated artifacts are emitted to:

- [generated/protocol_packs/index.json](/Users/noveltokens/a_person_index/generated/protocol_packs/index.json)
- [generated/protocol_packs](/Users/noveltokens/a_person_index/generated/protocol_packs)
- [site/data/protocol_packs/index.json](/Users/noveltokens/a_person_index/site/data/protocol_packs/index.json)

Do not hand-edit generated pack artifacts.

## Pack lifecycle

1. Add or update a catalog entry.
2. Validate that the referenced protocol, framework IDs, and construct IDs resolve.
3. Rebuild generated outputs.
4. Review the generated artifact shape and scope.
5. Promote the pack to `active` only when it is stable enough for downstream use.

## Catalog grammar

Each curated pack entry should declare:

- `id`
- `protocol_id`
- `status`
- `title`
- `summary`
- `intended_consumers`
- `target_framework_ids`
- `target_construct_ids`
- `featured`
- `notes`

Use `target_framework_ids` for instrument-level scope and `target_construct_ids` only when the curated bundle truly needs part-level specificity.

## Dynamic vs curated

Use dynamic packs when:

- the scope is one-off
- the runtime already knows exactly what it needs
- you do not want to support the combination as a stable surface

Use curated packs when:

- the workflow is repeated
- the scope is reviewed and intentionally named
- another agent should be able to discover and trust it on arrival

## Relationship to index programs

Within A Person Index:

- techniques are the smallest reusable operations
- index programs are the named composed analyses
- curated packs are the runtime-ready scoped bundles

That is why this layer exists. It is the bridge from reusable method to repeated execution.

## Maintenance rules

- Keep the protocol authoritative for purpose, inputs, and primary outputs.
- Keep the grammar authoritative for pack shape.
- Keep the catalog authoritative for curated scopes and stable pack IDs.
- Do not create combinatorial junk. Curate only repeated or strategically important scopes.
- Prefer a small set of featured packs over many barely differentiated ones.
- If a pack meaningfully changes scope or intent, create a new ID instead of silently repurposing the old one.

## Common commands

```bash
python3 scripts/query_registry.py program-packs
python3 scripts/query_registry.py program-packs --featured
python3 scripts/query_registry.py program-packs ppk_ilens_core_trait_motive_stack
python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram
```

## Relationship to MCP

The read-only MCP surface exposes curated pack discovery and retrieval through:

- `registry://protocol-packs`
- `registry://protocol-pack/{pack_id}`
- `list_protocol_packs`
- `fetch_curated_protocol_pack`

That makes curated packs both Git-native and agent-native.
