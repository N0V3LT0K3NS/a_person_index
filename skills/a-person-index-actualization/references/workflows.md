# A Person Index Actualization Workflows

## Quick map

### Inspect capabilities, then classify the run

- `python3 scripts/query_registry.py modes`
- look for capability categories such as file read, file write, code execution, markdown rendering, table rendering, diagram rendering, and structured bundle emission

### Choose an artifact class

- `python3 scripts/query_registry.py artifacts`
- `python3 scripts/query_registry.py artifacts --mode "Contextual and Multi-Subject Comparison"`

### Choose an actualization protocol

- `python3 scripts/query_registry.py actualization`
- `python3 scripts/query_registry.py actualization --mode "Artifact Actualization"`
- `python3 scripts/query_registry.py actualization --artifact "Comparative Memo"`

### Pull the comparative core

- use `$a-person-index` for framework matching, motifs, interactions, and program or pack choice

### Realize the output

- memo or handoff when markdown is enough
- matrix when comparative axes must stay visible
- graph when a visual clarifies structure rather than merely decorates
- structured result bundle when another agent or system will consume it
