---
name: a-person-index-actualization
description: Use when a task involves turning A Person Index findings into a concrete artifact or downstream deliverable, or when the host needs to inspect its own capabilities, classify the run, and choose an actualization path without losing A Person Index boundaries.
---

# A Person Index Actualization

Use this skill when the task is no longer only "understand the stack" and is now
"use the stack to make the right thing."

This skill sits above `$a-person-index`.

If the main task is still deciding what kind of run this is or what the host
can do, start with `$a-person-index-meta` first.

It does not replace the comparative core. It helps the host:

- inspect available capabilities
- classify the run
- pick an artifact class or actualization protocol
- use A Person Index as semantic authority
- use external tools only for realization

## Core stance

- A Person Index defines comparative meaning.
- The host environment provides capabilities.
- Actualization is downstream of comparison, not a replacement for it.
- External tools may render, package, visualize, or persist an output, but they should not redefine what the comparison means.

## Workflow

### 1. Inspect host capabilities

Before choosing an output path, look for capabilities rather than specific tool
brands.

If the host is already one of the repo's known environments, start with the
host profile and let it expand into a capability set:

```bash
python3 scripts/query_registry.py hosts
python3 scripts/query_registry.py hosts "Codex Desktop"
python3 scripts/query_registry.py recommend-path --host "Codex Desktop" --text "make a human model card"
```

Typical capability questions:

- Can I read local files?
- Can I write files?
- Can I run code?
- Can I render markdown?
- Can I produce tables?
- Can I produce diagrams or graphs?
- Can I call MCP servers or web APIs?
- Can I create a structured bundle?

Do not over-describe the environment unless the user cares. Use it to choose the path.

### 2. Classify the run

Use A Person Index mode surfaces first:

```bash
python3 scripts/query_registry.py modes
python3 scripts/query_registry.py modes "Run Planning"
```

Typical run shapes:

- bounded single-subject pass
- architecture analysis
- run planning
- artifact actualization
- contextual comparison
- trace review

If the mode is unclear, state the mode you believe you are in before proceeding.

### 3. Pick the right artifact class or actualization protocol

Use:

```bash
python3 scripts/query_registry.py artifacts
python3 scripts/query_registry.py actualization
python3 scripts/query_registry.py workflows
python3 scripts/query_registry.py recommend-path --mode "Artifact Actualization" --capability "Markdown Write"
python3 scripts/query_registry.py actualization --mode "Artifact Actualization"
```

Choose the smallest artifact that fits the request.

Do not jump to a graph or PDF when a memo or markdown handoff is the better first realization.

For contextual and pairwise work, start from the dedicated comparison programs
before falling back to a single-subject program:

- `proto_contextual_comparison`
- `proto_pairwise_relational_comparison`

### 4. Run comparison preflight when the work is contextual or pairwise

Do not move from comparison shape directly to artifact choice if the comparison
is still underspecified.

Use:

```bash
python3 scripts/query_registry.py comparison-preflight "Pairwise Relational Question" \
  --declare left_stack_label="person a" \
  --declare right_stack_label="person b" \
  --declare relationship_context="friends" \
  --declare comparison_question="Where do their motives align or strain?" \
  --host "Claude Code" \
  --capability "Markdown Write" \
  --capability "Table Render"
```

### 5. Pull the comparative core from A Person Index

Use `$a-person-index` surfaces for:

- framework matching
- motifs and interactions
- program or pack selection
- research-safe return rules

The artifact should be downstream of that work, not a substitute for it.

### 6. Realize the output with the tools actually available

Examples:

- if you can write markdown, produce a strong memo or handoff file
- if you can render tables, produce a context matrix or pairwise sheet
- if you can generate diagrams, add a visual only when it clarifies rather than decorates
- if you can emit structured data, package a result bundle for downstream use
- if the work is contextual or pairwise and you can emit structured data, prefer a comparison-aware result bundle over forcing the output through a table renderer

Before you start writing or rendering, turn the chosen workflow recipe into a
concrete scaffold:

```bash
python3 scripts/query_registry.py artifact-realization "Context Matrix Explanatory" \
  --host "Codex Desktop" \
  --capability "Markdown Write" \
  --capability "Table Render"
python3 scripts/query_registry.py artifact-realization "Structured Result Bundle Technical" \
  --host "Codex Desktop"
```

That surface tells you the selected realization form, the required blocks the
artifact should contain, and what evidence partitions must remain visible.

If you want a starter markdown or JSON structure after that, ask for the
artifact template rather than rebuilding the first draft yourself:

```bash
python3 scripts/query_registry.py artifact-template "Human Model Card Mixed" \
  --host "Codex Desktop"
python3 scripts/query_registry.py artifact-template "Structured Result Bundle Technical" \
  --host "Codex Desktop" \
  --format json
```

### 7. Preserve provenance and expression fit

Always preserve the difference between:

- canonical framework content
- house synthesis
- named program behavior
- downstream judgment
- external realization work

Also choose the right expression depth:

- tacit or phenomenological for ordinary user-facing explanation
- explanatory when the user wants some scaffold
- technical for contributor or debugging contexts

If expression fit is part of the uncertainty, inspect the structured surface:

```bash
python3 scripts/query_registry.py expressions --artifact "Comparative Memo"
python3 scripts/query_registry.py workflows --artifact "Comparative Memo"
```

## Anti-patterns

- Do not use external tools to improvise semantics that A Person Index did not supply.
- Do not treat a renderer as an authority on comparison.
- Do not hide missingness because the artifact "looks better" without it.
- Do not default to the most technical voice when the user wants the phenomenon.
- Do not force every task into a heavyweight artifact.

## References

- For compact command and mode mappings, read [references/workflows.md](references/workflows.md).
