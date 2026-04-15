# Agent Guide

This repository is A Person Index (API), an agent-readable knowledge substrate for personhood frameworks.

If Codex is the host and the companion skill is installed, prefer `$a-person-index` for comparative work, program-pack use, and research-safe return formatting. The skill is an operating layer on top of this repo's MCP and CLI surfaces, not a second source of truth.

If you only need the fast arrival path, prefer [docs/agent_quickstart.md](/Users/noveltokens/a_person_index/docs/agent_quickstart.md) and [docs/assessment_workflow.md](/Users/noveltokens/a_person_index/docs/assessment_workflow.md) before reading the deeper repo map.

If you are arriving cold, do this first:

1. [README.md](/Users/noveltokens/a_person_index/README.md)
2. [docs/agent_quickstart.md](/Users/noveltokens/a_person_index/docs/agent_quickstart.md)
3. [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
4. [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
5. [docs/assessment_workflow.md](/Users/noveltokens/a_person_index/docs/assessment_workflow.md)

Only then deepen as needed:

- Status and direction:
  [docs/release_status.md](/Users/noveltokens/a_person_index/docs/release_status.md),
  [docs/roadmap.md](/Users/noveltokens/a_person_index/docs/roadmap.md),
  [docs/strategic_backlog.md](/Users/noveltokens/a_person_index/docs/strategic_backlog.md),
  [docs/architecture.md](/Users/noveltokens/a_person_index/docs/architecture.md),
  [docs/system_boundaries.md](/Users/noveltokens/a_person_index/docs/system_boundaries.md),
  [docs/phase_3_4_plan.md](/Users/noveltokens/a_person_index/docs/phase_3_4_plan.md)
- Programs, packs, and runtime use:
  [docs/index_programs.md](/Users/noveltokens/a_person_index/docs/index_programs.md),
  [docs/protocol_pack_grammar.md](/Users/noveltokens/a_person_index/docs/protocol_pack_grammar.md),
  [docs/protocol_packs.md](/Users/noveltokens/a_person_index/docs/protocol_packs.md),
  [docs/ilens_walkthrough.md](/Users/noveltokens/a_person_index/docs/ilens_walkthrough.md),
  [docs/gnomy_integration.md](/Users/noveltokens/a_person_index/docs/gnomy_integration.md)
- Advanced and downstream-facing use:
  [docs/advanced_modes.md](/Users/noveltokens/a_person_index/docs/advanced_modes.md),
  [docs/comparison_shapes.md](/Users/noveltokens/a_person_index/docs/comparison_shapes.md),
  [docs/comparison_preflight.md](/Users/noveltokens/a_person_index/docs/comparison_preflight.md),
  [docs/capability_model.md](/Users/noveltokens/a_person_index/docs/capability_model.md),
  [docs/artifact_realization.md](/Users/noveltokens/a_person_index/docs/artifact_realization.md),
  [docs/expression_model.md](/Users/noveltokens/a_person_index/docs/expression_model.md),
  [docs/actualization_protocols.md](/Users/noveltokens/a_person_index/docs/actualization_protocols.md),
  [docs/workflow_recipes.md](/Users/noveltokens/a_person_index/docs/workflow_recipes.md),
  [docs/expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md),
  [docs/multi_subject_comparison.md](/Users/noveltokens/a_person_index/docs/multi_subject_comparison.md)
- Clients and operations:
  [docs/mcp_clients.md](/Users/noveltokens/a_person_index/docs/mcp_clients.md),
  [docs/codex_automation.md](/Users/noveltokens/a_person_index/docs/codex_automation.md),
  [CONTRIBUTING.md](/Users/noveltokens/a_person_index/CONTRIBUTING.md),
  [SECURITY.md](/Users/noveltokens/a_person_index/SECURITY.md),
  [CHANGELOG.md](/Users/noveltokens/a_person_index/CHANGELOG.md)
- Research and expansion:
  [docs/research_authoring_standard.md](/Users/noveltokens/a_person_index/docs/research_authoring_standard.md),
  [docs/source_landscape.md](/Users/noveltokens/a_person_index/docs/source_landscape.md),
  [docs/expansion_program.md](/Users/noveltokens/a_person_index/docs/expansion_program.md),
  [docs/research_promotion.md](/Users/noveltokens/a_person_index/docs/research_promotion.md),
  [generated/manifest.json](/Users/noveltokens/a_person_index/generated/manifest.json)

## What this repo is

The repo has five distinct product layers:

1. Canonical registry
   Source-faithful framework records, currently centered on instruments.
2. House synthesis substrate
   Motifs, construct mappings, and interaction hypotheses.
3. Technique library
   Atomic reusable operations such as `Paradox Scan`.
4. Index programs and runtime packs
   Composed programs such as `Paradox Finder`, `ILENS`, and `Human Model Card`, plus scoped packs for downstream runtimes.
5. Research stream
   Privacy-minimizing contribution models, promotion policy, and the result atom schema.

Do not collapse those layers into one.

## Source of truth

Edit source files, not generated outputs.

Canonical sources:
- [instruments](/Users/noveltokens/a_person_index/instruments)
- [ontology](/Users/noveltokens/a_person_index/ontology)
- [motifs/registry.yaml](/Users/noveltokens/a_person_index/motifs/registry.yaml)
- [modes/registry.yaml](/Users/noveltokens/a_person_index/modes/registry.yaml)
- [comparison_shapes/registry.yaml](/Users/noveltokens/a_person_index/comparison_shapes/registry.yaml)
- [docs/comparison_preflight.md](/Users/noveltokens/a_person_index/docs/comparison_preflight.md)
- [capabilities/registry.yaml](/Users/noveltokens/a_person_index/capabilities/registry.yaml)
- [docs/artifact_realization.md](/Users/noveltokens/a_person_index/docs/artifact_realization.md)
- [expression/registry.yaml](/Users/noveltokens/a_person_index/expression/registry.yaml)
- [artifacts/registry.yaml](/Users/noveltokens/a_person_index/artifacts/registry.yaml)
- [actualization/registry.yaml](/Users/noveltokens/a_person_index/actualization/registry.yaml)
- [workflow_recipes/registry.yaml](/Users/noveltokens/a_person_index/workflow_recipes/registry.yaml)
- [mappings/construct_to_motif.yaml](/Users/noveltokens/a_person_index/mappings/construct_to_motif.yaml)
- [interactions/registry.yaml](/Users/noveltokens/a_person_index/interactions/registry.yaml)
- [techniques/registry.yaml](/Users/noveltokens/a_person_index/techniques/registry.yaml)
- [protocols/registry.yaml](/Users/noveltokens/a_person_index/protocols/registry.yaml) for index program specs
- [protocol_packs/catalog.yaml](/Users/noveltokens/a_person_index/protocol_packs/catalog.yaml)
- [research/contribution_models.yaml](/Users/noveltokens/a_person_index/research/contribution_models.yaml)
- [research/promotion_registry.yaml](/Users/noveltokens/a_person_index/research/promotion_registry.yaml)
- [research/result_atom_schema.yaml](/Users/noveltokens/a_person_index/research/result_atom_schema.yaml)

Do not manually edit:
- [generated](/Users/noveltokens/a_person_index/generated)
- [site](/Users/noveltokens/a_person_index/site)
- [schemas](/Users/noveltokens/a_person_index/schemas)

Compatibility note:

- `registry://...` URIs
- `protocols/registry.yaml`
- `protocol_packs/`

remain stable for compatibility. Treat them as implementation surfaces, not the product’s preferred public language.

## Core rules

- Keep source claims, ontology annotations, and house inferences separate.
- Treat motifs, mappings, and interaction hypotheses as house synthesis, not source truth.
- Treat index programs as downstream consumers of the map, not the map itself.
- Treat research contributions as staged evidence, not immediate canonical fact.
- Do not put raw user chats or personal corpora into canonical framework records.

## Local workflow

Typical safe sequence after changes:

```bash
python3 scripts/validate.py
python3 scripts/export_schemas.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
python3 -m pytest
```

## Service primitives

Useful local commands for agents:

```bash
python3 scripts/query_registry.py orient
python3 scripts/query_registry.py find --ref "Big Five"
python3 scripts/query_registry.py compare MBTI Enneagram
python3 scripts/query_registry.py trace MBTI
python3 scripts/query_registry.py motifs --related-to MBTI
python3 scripts/query_registry.py interactions --related-to "Attachment Style Frameworks"
python3 scripts/query_registry.py programs ILENS
python3 scripts/query_registry.py program-packs --featured
python3 scripts/query_registry.py program-packs ppk_ilens_core_trait_motive_stack
python3 scripts/query_registry.py program-pack-summary ILENS --framework "Big Five" --framework MBTI --framework Enneagram
python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram
python3 scripts/query_registry.py program-pack-grammar
python3 scripts/query_registry.py research-promotion
python3 scripts/query_registry.py techniques "Paradox Scan"
python3 scripts/query_registry.py result-atom-schema
python3 scripts/query_registry.py research-models
python3 scripts/query_registry.py audit --needs-official-resource
npm run mcp:serve
npm run mcp:test
./scripts/test_claude_code_mcp.sh
```

Shareable client examples:

- [examples/mcp](/Users/noveltokens/a_person_index/examples/mcp)

## Downstream role

This repo is meant to serve runtimes such as `GNOMY`.
`GNOMY` is a lead consumer, not the only intended consumer.

It should provide:
- canonical framework records
- ontology annotations
- crosswalks
- motifs and construct mappings
- interaction hypotheses
- reusable techniques
- index program specs
- research contribution models
- the result atom schema

It should not perform full person-level inference itself.

## Companion skill

Optional Codex companion skill:

- name: `$a-person-index`
- canonical repo path: [skills/a-person-index](/Users/noveltokens/a_person_index/skills/a-person-index)
- expected local install path: `$CODEX_HOME/skills/a-person-index`
- job: help Codex use the MCP and CLI surfaces in the right order and preserve source vs house vs research boundaries

## Expansion orchestration

For recurring framework, crosswalk, and source-enrichment work, prefer queue-driven automation:

- queue: [.github/codex/task_queue.yaml](/Users/noveltokens/a_person_index/.github/codex/task_queue.yaml)
- renderer: [scripts/render_codex_task_from_queue.py](/Users/noveltokens/a_person_index/scripts/render_codex_task_from_queue.py)
- lister: [scripts/list_codex_queue_tasks.py](/Users/noveltokens/a_person_index/scripts/list_codex_queue_tasks.py)
- dispatch workflow: [.github/workflows/dispatch-codex-queue-item.yml](/Users/noveltokens/a_person_index/.github/workflows/dispatch-codex-queue-item.yml)
- batch dispatch workflow: [.github/workflows/dispatch-ready-codex-queue.yml](/Users/noveltokens/a_person_index/.github/workflows/dispatch-ready-codex-queue.yml)

That path keeps the source bundle, acceptance criteria, and verification path versioned in Git before a PR is attempted.
