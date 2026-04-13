---
name: a-person-index
description: Use when a task involves comparing personhood frameworks, tracing motifs, fetching index program packs, interpreting A Person Index outputs, or using the A Person Index MCP/CLI surfaces from Codex. Best for translation memos, ILENS prep, Paradox Finder workflows, and research-safe return formatting.
---

# A Person Index

Use this skill when Codex needs to operate A Person Index as a comparative substrate rather than treat it as a generic repo.

## Core stance

- A Person Index is the product.
- The canonical registry is only one layer inside it.
- Keep `source claims`, `house synthesis`, `index programs`, and `research evidence` clearly separated.
- Do not turn symbolic analogy into equivalence.
- Prefer scoped program packs for known tasks instead of manually reconstructing motifs, mappings, and interactions.

## Preferred interface order

1. If the A Person Index MCP is configured, use it first.
2. If MCP is unavailable but the repo is present locally, use the query CLI from the repo.
3. Use generated JSON or docs only when tool access is unavailable or when a static artifact is specifically needed.

Typical local repo path in this environment:

```text
/Users/noveltokens/a_person_index
```

Typical MCP entrypoint in that repo:

```bash
npm run mcp:serve
```

## Common workflows

### 1. Orient to the substrate

Use this when arriving cold or when another agent needs the current contract.

Prefer:
- MCP resource `registry://manifest`
- MCP resource `registry://quickstart`
- MCP resource `registry://current-state`
- MCP prompt `registry-arrival`

CLI fallback:

```bash
python3 scripts/query_registry.py audit --format json
cat generated/manifest.json
```

### 2. Compare frameworks or translation surfaces

Use this when the task is comparative, translational, or “what overlaps and what does not?”

Prefer:
- `find_framework_records`
- `compare_frameworks`
- `trace_to_motifs`
- `list_related_motifs`
- `list_interaction_hypotheses`

CLI fallback:

```bash
python3 scripts/query_registry.py compare MBTI Enneagram
python3 scripts/query_registry.py trace MBTI
python3 scripts/query_registry.py motifs --related-to MBTI
python3 scripts/query_registry.py interactions --related-to MBTI
```

Output rule:
- distinguish direct source claims from house motif/inference language
- explicitly name weak overlap, different layer, or incommensurability when appropriate

### 3. Use index programs and program packs

Use this when the task is already recognizable as a named method such as ILENS, Translation Memo, Human Model Card, or Paradox Finder.

Prefer:
- `fetch_protocol_spec`
- `list_protocol_packs`
- `fetch_curated_protocol_pack`
- `fetch_protocol_pack`
- `fetch_protocol_pack_grammar`

CLI fallback:

```bash
python3 scripts/query_registry.py programs ILENS
python3 scripts/query_registry.py program-packs --featured
python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram
python3 scripts/query_registry.py program-pack-grammar
```

Pack rule:
- if the task matches an existing program, fetch the pack first
- if you do not know which pack exists, call `list_protocol_packs(featured=true)` before guessing
- only decompose into individual motif/mapping calls when no pack exists or when auditing the pack itself

### 3a. Ingest user assessment results

Use this when a user pastes a mixed stack of assessments and asks what A Person Index can do with it.

Prefer:
- MCP resource `registry://assessment-workflow`
- `find_framework_records` with short `refs`
- `list_protocol_packs(featured=true)`

Intake rule:
- do not begin with one giant `text` blob if you can extract likely framework labels first
- call out missing or unindexed frameworks explicitly
- only claim a program was executed if you actually used its pack or spec as the basis for the synthesis

### 4. Format research-safe return traffic

Use this when another system wants to send structured insight back without polluting canonical records.

Prefer:
- `fetch_result_atom_schema`
- `fetch_research_models`
- `fetch_research_promotion_policy`

CLI fallback:

```bash
python3 scripts/query_registry.py result-atom-schema
python3 scripts/query_registry.py research-models
python3 scripts/query_registry.py research-promotion
```

Return rule:
- prefer `mapping_vote`, `pairwise_relation_judgment`, `result_atom_bundle`, `distilled_observation`, or `protocol_feedback`
- do not send raw chats, diaries, or broad narrative corpora as canonical input

## Anti-patterns

- Do not describe A Person Index as “just a registry”.
- Do not blur canonical records and house synthesis.
- Do not assume a framework label is equivalent to a person-level truth.
- Do not rebuild pack choreography by hand if a pack already exists.
- Do not treat research contributions as promoted truth.

## References

- For compact command and task mappings, read [references/workflows.md](references/workflows.md).
