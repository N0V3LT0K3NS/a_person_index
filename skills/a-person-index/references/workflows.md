# A Person Index Workflows

## Quick task map

### Understand the substrate

- MCP: `registry://manifest`, `registry://current-state`
- CLI: `python3 scripts/query_registry.py audit --format json`

### Compare frameworks

- MCP tools:
  - `find_framework_records`
  - `compare_frameworks`
  - `trace_to_motifs`
  - `list_related_motifs`
  - `list_interaction_hypotheses`
- CLI:
  - `python3 scripts/query_registry.py compare MBTI Enneagram`
  - `python3 scripts/query_registry.py trace MBTI`

### Run a named method

- MCP tools:
  - `fetch_protocol_spec`
  - `list_protocol_packs`
  - `fetch_protocol_pack`
- CLI:
  - `python3 scripts/query_registry.py programs ILENS`
  - `python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram`

### Prepare research-safe returns

- MCP tools:
  - `fetch_result_atom_schema`
  - `fetch_research_models`
  - `fetch_research_promotion_policy`
- CLI:
  - `python3 scripts/query_registry.py result-atom-schema`
  - `python3 scripts/query_registry.py research-models`
  - `python3 scripts/query_registry.py research-promotion`

## Output patterns

### Comparative memo

- state the frameworks
- separate source language from house language
- name overlap strength
- name breaks or incommensurabilities
- cite motifs or interactions only as house synthesis

### Pack-based runtime prep

- name the index program
- name the scoped frameworks
- list required techniques
- list motif and interaction coverage
- state the return contract

### Research-safe return

- choose one approved contribution model
- keep it structured
- avoid raw personal corpora
