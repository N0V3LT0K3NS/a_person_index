# Codex Automation Context

You are working inside A Person Index (API).

## Product model

- The product is A Person Index.
- The canonical registry is one layer inside it, not the whole product.
- The composition model is:
  - techniques
  - index programs
  - runtime packs

## Core docs to read first

1. `AGENTS.md`
2. `README.md`
3. `CONTRIBUTING.md`
4. `docs/current_state.md`
5. `docs/architecture.md`
6. `docs/index_programs.md`
7. `docs/system_boundaries.md`
8. `docs/phase_3_4_plan.md`
9. `generated/manifest.json`

## Hard rules

- Keep source claims, ontology annotations, house synthesis, index programs, and research evidence distinct.
- Do not hand-edit generated outputs.
- Do not move person-level inference into this repo.
- Respect compatibility surfaces such as `registry://...` URIs and `protocols/registry.yaml`.
- Keep Git changes scoped and PR-ready.

## Required verification

Run this sequence unless the task explicitly justifies a narrower path:

```bash
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
npm run mcp:smoke
python3 -m pytest
```

## Output expectation

Open a PR, summarize the changed layers, and report the verification results.
