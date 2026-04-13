# Contributing

This repository is A Person Index: a Git-native comparative substrate for personhood frameworks, house synthesis, index programs, runtime packs, and research-safe return contracts.

## Contribution stance

Contribute here when the change is a durable shared knowledge object, a reusable method, or a governance rule.

Do not use this repo for:

- raw personal data
- one-off person analyses
- runtime-only behavior that belongs in `GNOMY` or another consumer
- unreviewed research claims presented as canonical truth

## Keep the layers separate

Every change should respect the repository layers:

1. Canonical registry
   Source-faithful framework records.
2. House synthesis
   Motifs, mappings, and interaction hypotheses.
3. Technique and program layer
   Reusable techniques, index programs, and runtime packs.
4. Research stream
   Contribution models, promotion policy, and reviewed evidence pathways.

Do not collapse source claims, house synthesis, downstream programs, and research evidence into one blended narrative.

## Contribution paths

Typical contribution types:

- add or deepen a framework record
- add a motif, mapping, or interaction hypothesis
- add or refine a technique
- add or refine an index program
- add or curate a program pack
- improve docs, onboarding, governance, or generated presentation

## Before you change anything

Read these first:

1. [AGENTS.md](/Users/noveltokens/a_person_index/AGENTS.md)
2. [README.md](/Users/noveltokens/a_person_index/README.md)
3. [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
4. [docs/architecture.md](/Users/noveltokens/a_person_index/docs/architecture.md)
5. [docs/index_programs.md](/Users/noveltokens/a_person_index/docs/index_programs.md)
6. [docs/system_boundaries.md](/Users/noveltokens/a_person_index/docs/system_boundaries.md)
7. [SECURITY.md](/Users/noveltokens/a_person_index/SECURITY.md)
8. [generated/manifest.json](/Users/noveltokens/a_person_index/generated/manifest.json)
9. [docs/research_authoring_standard.md](/Users/noveltokens/a_person_index/docs/research_authoring_standard.md)

## Local verification

Run the full verification path before proposing a merge:

```bash
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
npm run mcp:smoke
python3 -m pytest
```

If a change intentionally does not touch one of those layers, say so explicitly in the PR.

## Generated outputs

Do not hand-edit:

- `generated/`
- `site/`
- `schemas/`

Edit source files and regenerate.

## Naming and compatibility

The product is **A Person Index (API)**.

Some internal names intentionally remain for compatibility:

- `registry://...` MCP URIs
- `protocols/registry.yaml`
- `protocol_packs/`

Treat those as compatibility surfaces, not as the product’s primary public language.

## Pull requests

Every PR should make clear:

- what changed
- which layer(s) changed
- why the change belongs in this repo
- what verification ran
- whether generated outputs were rebuilt
- whether downstream consumers such as `GNOMY` are affected

Use the PR template in `.github/pull_request_template.md`.

For recurring framework, crosswalk, and source-enrichment work, prefer a queue item in [.github/codex/task_queue.yaml](/Users/noveltokens/a_person_index/.github/codex/task_queue.yaml) plus the queue-dispatch workflow over writing the whole task from scratch each time.

## Codex automation

If you want GitHub-triggered Codex work, use the Codex task issue template or the manual workflow described in [docs/codex_automation.md](/Users/noveltokens/a_person_index/docs/codex_automation.md).

If the work is part of the longer expansion program, use the queue renderer:

```bash
python3 scripts/render_codex_task_from_queue.py task_seed_source_enrichment
```

## Security

If you are reporting a security issue or changing automation/deployment surfaces, follow [SECURITY.md](/Users/noveltokens/a_person_index/SECURITY.md) and avoid opening a public issue with exploit details.
