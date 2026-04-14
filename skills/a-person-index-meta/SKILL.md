---
name: a-person-index-meta
description: Use when a task requires inspecting the current host environment, mapping available tools into abstract capabilities, classifying the run, and choosing the next A Person Index path before deeper comparative or artifact work begins.
---

# A Person Index Meta

Use this skill before deeper work when the main question is:

"What kind of run is this, what can this host actually do, and what should I do next?"

This skill sits above both `$a-person-index` and `$a-person-index-actualization`.

It does not perform the full comparative pass itself. It chooses the path.

## Core stance

- A Person Index remains the semantic authority.
- The host environment contributes capabilities, not meaning.
- The first job is classification, not output generation.

## Workflow

### 1. Inspect capabilities abstractly

Do not start with tool brands.

Start with capability categories:

- file read
- MCP or API call
- code execution
- markdown write
- structured text render
- table render
- diagram render
- spreadsheet render
- PDF render
- JSON emit
- file write

Use the capability registry when needed:

```bash
python3 scripts/query_registry.py capabilities
python3 scripts/query_registry.py capabilities --artifact "Context Matrix"
python3 scripts/query_registry.py capabilities --actualization "Pairwise Relational Sheet"
python3 scripts/query_registry.py recommend-path --text "compare me across time" --capability "Markdown Write"
```

### 2. Classify the run

Use the mode surfaces next:

```bash
python3 scripts/query_registry.py modes
python3 scripts/query_registry.py modes "Run Planning"
```

Decide whether this is:

- orientation and sync
- bounded single-subject work
- run planning
- artifact actualization
- contextual comparison
- trace review
- architecture analysis

### 3. Choose the next skill path

After capability inspection and run classification:

- use `$a-person-index` for the comparative core
- use `$a-person-index-actualization` when the task should become an artifact or handoff
- stay in planning mode if the path is not stable yet

If the path is almost clear but not yet explicit, prefer `recommend-path` or
`recommend_next_path` before making the choice by hand.

### 4. Say the path before taking it

Before deeper work, name:

- the inferred run mode
- the important capabilities available here
- the next A Person Index surface you will use

Keep this compact unless the user wants the scaffolding.

## Anti-patterns

- Do not confuse tool abundance with interpretive permission.
- Do not jump into rendering before the run shape is clear.
- Do not inspect capabilities at the level of brand names only.
- Do not let the host environment silently override A Person Index boundaries.

## References

- For compact command and decision patterns, read [references/workflows.md](references/workflows.md).
