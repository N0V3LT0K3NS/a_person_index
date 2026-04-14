# A Person Index Workflows

## Quick task map

### Understand the substrate

- MCP: `orient_agent`, `registry://quickstart`, `registry://current-state`
- CLI: `python3 scripts/query_registry.py orient`

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
  - `fetch_protocol_pack_summary`
  - `fetch_protocol_spec`
  - `list_protocol_packs`
  - `fetch_protocol_pack`
- CLI:
  - `python3 scripts/query_registry.py programs ILENS`
  - `python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram`
  - `python3 scripts/query_registry.py program-pack-summary ILENS --framework "Big Five" --framework MBTI --framework Enneagram`

### Move from recommendation to execution

- MCP tools:
  - `list_comparison_shapes`
  - `prepare_comparison_run`
  - `recommend_next_path`
  - `fetch_workflow_recipe`
- CLI:
  - `python3 scripts/query_registry.py comparison-shapes --text "compare me across time"`
  - `python3 scripts/query_registry.py comparison-preflight "Contextual Time Slices" --declare slice_labels="earlier,later" --declare comparison_question="What changed?" --capability "Markdown Write"`
  - `python3 scripts/query_registry.py recommend-path --mode "Artifact Actualization" --capability "Markdown Write"`
  - `python3 scripts/query_registry.py workflows --artifact "Comparative Memo"`

### Ingest assessment stacks

- MCP:
  - `assessment-results-intake`
  - `find_framework_records`
  - `list_protocol_packs`
  - `fetch_protocol_pack_summary`
- CLI:
  - `python3 scripts/query_registry.py find --ref "Big Five" --ref MBTI --ref Enneagram`
  - `python3 scripts/query_registry.py program-packs --featured`
  - `python3 scripts/query_registry.py program-pack-summary ILENS --framework "Big Five" --framework MBTI --framework Enneagram`

### Prepare research-safe returns

- MCP tools:
  - `fetch_result_atom_schema`
  - `fetch_research_models`
  - `fetch_research_promotion_policy`
- CLI:
  - `python3 scripts/query_registry.py result-atom-schema`
  - `python3 scripts/query_registry.py research-models`
  - `python3 scripts/query_registry.py research-promotion`

### Dispatch bounded expansion work

- Repo queue:
  - `.github/codex/task_queue.yaml`
- Renderer:
  - `python3 scripts/render_codex_task_from_queue.py task_add_rdrive_framework`
- Lister:
  - `python3 scripts/list_codex_queue_tasks.py --status ready --priority highest --format ids`
- GitHub workflow:
  - `.github/workflows/dispatch-codex-queue-item.yml`
  - `.github/workflows/dispatch-ready-codex-queue.yml`

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
