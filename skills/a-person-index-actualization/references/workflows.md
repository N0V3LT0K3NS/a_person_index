# A Person Index Actualization Workflows

## Quick map

### Inspect capabilities, then classify the run

- `python3 scripts/query_registry.py capabilities`
- `python3 scripts/query_registry.py modes`
- look for capability categories such as file read, file write, code execution, markdown rendering, table rendering, diagram rendering, and structured bundle emission

### Choose an artifact class

- `python3 scripts/query_registry.py artifacts`
- `python3 scripts/query_registry.py artifacts --mode "Contextual and Multi-Subject Comparison"`

### Run comparison preflight when comparison shape is explicit

- `python3 scripts/query_registry.py comparison-preflight "Contextual Time Slices" --declare slice_labels="earlier,later" --declare comparison_question="What changed?" --capability "Markdown Write"`
- `python3 scripts/query_registry.py comparison-preflight "Pairwise Relational Question" --declare left_stack_label="person a" --declare right_stack_label="person b" --declare relationship_context="partners" --declare comparison_question="Where do they align or strain?" --capability "Markdown Write" --capability "Table Render"`

### Choose an actualization protocol

- `python3 scripts/query_registry.py actualization`
- `python3 scripts/query_registry.py actualization --mode "Artifact Actualization"`
- `python3 scripts/query_registry.py actualization --artifact "Comparative Memo"`

### Choose a workflow recipe

- `python3 scripts/query_registry.py workflows`
- `python3 scripts/query_registry.py workflows --artifact "Context Matrix"`
- `python3 scripts/query_registry.py workflows --actualization "Context Matrix Render"`

### Turn the workflow recipe into a concrete artifact scaffold

- `python3 scripts/query_registry.py artifact-realization "Context Matrix Explanatory" --capability "Markdown Write" --capability "Table Render"`
- `python3 scripts/query_registry.py artifact-realization "Human Model Card Mixed" --capability "Markdown Write" --capability "Structured Text Render"`

### Pull the comparative core

- use `$a-person-index` for framework matching, motifs, interactions, and program or pack choice

### Realize the output

- memo or handoff when markdown is enough
- matrix when comparative axes must stay visible
- graph when a visual clarifies structure rather than merely decorates
- structured result bundle when another agent or system will consume it
