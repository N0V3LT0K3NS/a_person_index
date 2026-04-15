# A Person Index (API)

A Person Index (API) is a Git-native, agent-readable comparative core for personhood frameworks, house synthesis motifs, composable analysis techniques, index programs, runtime packs, and privacy-minimizing research intake.

It is not only a catalog of frameworks. It is also the semantic and methodological center that downstream agents can use for richer protocol work, artifact generation, and contextual comparison without collapsing those things back into canonical truth.

Live site: [a-person-index.netlify.app](https://a-person-index.netlify.app)

Landing directions: [site/landing-options.html](/Users/noveltokens/a_person_index/site/landing-options.html) and [docs/site_design_options.md](/Users/noveltokens/a_person_index/docs/site_design_options.md)

Companion Codex skill: `$a-person-index` can sit above the MCP and CLI surfaces to help Codex compare frameworks, fetch program packs, and keep source, house, and research layers distinct. The canonical repo copy lives at [skills/a-person-index](/Users/noveltokens/a_person_index/skills/a-person-index).

Companion actualization skill: `$a-person-index-actualization` can sit above the comparative core when the task is to inspect available host capabilities, choose a run mode, and materialize an artifact or handoff without losing provenance. The repo copy lives at [skills/a-person-index-actualization](/Users/noveltokens/a_person_index/skills/a-person-index-actualization).

Companion meta skill: `$a-person-index-meta` can inspect the current host environment abstractly, map available tools into capability records, classify the run, and choose the next A Person Index path before deeper work begins. The repo copy lives at [skills/a-person-index-meta](/Users/noveltokens/a_person_index/skills/a-person-index-meta).

The recommendation surface can now take a run hint plus declared capabilities
and suggest the next disciplined artifact and actualization path rather than
forcing hosts to reconstruct that logic ad hoc each time.

Host profiles now sit above the capability model too, so a known environment
such as Codex Desktop, Claude Code, Claude Desktop, or the Hermes remote
wrapper can expand into a conservative capability set before planning and
actualization begin.

Expression profiles are now first-class too, so the system can explicitly say
how visible the scaffolding should be when the same comparative result is
rendered for different audiences.

Workflow recipes now sit beneath that recommendation layer, so the system can
also name the smallest repeatable execution sequence that fits the run,
artifact, expression, and capability shape.

Contextual and pairwise work now also has first-class comparison shapes, so the
system can name the comparison scaffold itself before it chooses artifacts or
execution paths.

Comparison preflight now sits beneath that too, so a host can verify whether
the chosen contextual or pairwise scaffold is actually declared well enough to
proceed before it recommends or renders downstream work.

Artifact realization now sits beneath workflow recipes, so a host can turn a
chosen path into a concrete artifact scaffold without treating A Person Index
itself as the renderer.

Artifact templates now sit beneath artifact realization, so a host can also ask
for a starter markdown or JSON structure derived from the same workflow recipe
instead of rebuilding the first draft from scratch.

Result atom normalization now sits alongside the research-return layer too, so
downstream runtimes can turn construct-level outputs into schema-shaped bundles
without improvising framework IDs, construct IDs, provenance defaults, or motif
trace.

The repository began as an instrument registry in milestone 1. It now explicitly carries five product layers:

1. Canonical registry
2. House synthesis substrate
3. Technique library
4. Index programs and runtime packs
5. Research stream

Canonical source data still lives in structured YAML files, is validated with typed Python models, and is exported into generated JSON and browsable docs.

## Start Here

Do not try to read the whole repo on first arrival.

Fast arrival path:

1. [AGENTS.md](/Users/noveltokens/a_person_index/AGENTS.md)
2. [docs/agent_quickstart.md](/Users/noveltokens/a_person_index/docs/agent_quickstart.md)
3. [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
4. [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
5. [docs/assessment_workflow.md](/Users/noveltokens/a_person_index/docs/assessment_workflow.md)

If you need the deeper map after that:

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
  [docs/host_profiles.md](/Users/noveltokens/a_person_index/docs/host_profiles.md),
  [docs/capability_model.md](/Users/noveltokens/a_person_index/docs/capability_model.md),
  [docs/artifact_realization.md](/Users/noveltokens/a_person_index/docs/artifact_realization.md),
  [docs/artifact_templates.md](/Users/noveltokens/a_person_index/docs/artifact_templates.md),
  [docs/result_atom_normalization.md](/Users/noveltokens/a_person_index/docs/result_atom_normalization.md),
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

## Per-record layers

Each framework record in the current instrument-centered schema is represented in three distinct layers:

1. Source-truth layer: what the instrument or its source materials say about itself.
2. Meta-ontology layer: standardized house annotations applied through the shared ontology.
3. Inferred comparative layer: house synthesis, critique, crosswalks, and practical notes.

Do not collapse these layers into one blended narrative.

## Product layers

This repo now distinguishes between:

1. Canonical registry
   Source-faithful records for instruments and adjacent personhood frameworks.
2. House synthesis substrate
   Motifs and mappings used as a translation interlingua across frameworks.
3. Technique library
   The smallest reusable lego units such as `Paradox Scan`, `Cross-Framework Translation`, and `Result Atom Decomposition`.
4. Index programs and runtime packs
   Composed programs such as `ILENS`, `Translation Memo`, `Human Model Card`, and `Paradox Finder`, plus scoped runtime bundles that hydrate those programs with motifs, mappings, interactions, and return contracts.
5. Research stream
   Contribution models, promotion policy, and result-atom exchange contracts for mapping votes, result-atom bundles, and distilled observations.

These layers should collaborate, but they should not be conflated.
This repo is a shared substrate for multiple downstream consumers. `GNOMY` is a lead consumer, not the only one.

Around that core, there are adjacent downstream concerns that matter but should not be silently folded into ontology:

- actualization and orchestration protocols
- user-facing expression and artifact rendering
- contextual and multi-subject comparison

The repo increasingly defines the grammar for those layers even when their runtime implementation lives elsewhere.

For Codex specifically, the companion skill is an optional usage layer on top of the substrate:

- skill name: `$a-person-index`
- canonical repo path: `skills/a-person-index`
- local install target: `$CODEX_HOME/skills/a-person-index`
- role: teach Codex how to use MCP resources, tools, prompts, and CLI fallbacks without blurring the repo's layers

## Repository shape

```text
.
├── actualization/
├── artifacts/
├── capabilities/
├── comparison_shapes/
├── docs/
├── generated/
├── interactions/
├── instruments/
├── modes/
├── mappings/
├── motifs/
├── ontology/
├── protocols/
├── protocol_packs/
├── research/
├── schemas/
├── scripts/
├── site/
├── techniques/
├── src/personality_registry/
└── tests/
```

Key conventions:

- `instrument.yaml` stores canonical identity and metadata.
- `versions.yaml` stores version history.
- `constructs.yaml` stores scales, types, or facets.
- `claims.yaml` stores source-facing claims.
- `resources.yaml` stores source material and references.
- `annotations.yaml` stores house ontology labels.
- `inferences.yaml` stores house interpretation.
- `crosswalks.yaml` stores structured relationships.
- `risks.yaml` stores misuse or distortion hazards.
- `use_cases.yaml` stores practical fit and utility.
- `notes.md` stores human-readable narrative context.
- `motifs/registry.yaml` stores provisional house translation motifs.
- `modes/registry.yaml` stores named run modes for advanced comparative work.
- `comparison_shapes/registry.yaml` stores explicit scaffolds for contextual and pairwise comparison before artifact or protocol selection begins.
- `docs/comparison_preflight.md` explains how contextual and pairwise runs are checked for readiness before recommendation or execution.
- `hosts/registry.yaml` stores known host profiles that expand into conservative capability sets for planning and actualization.
- `docs/artifact_realization.md` explains how a chosen workflow recipe becomes a concrete artifact scaffold before host rendering begins.
- `docs/artifact_templates.md` explains how a chosen workflow recipe becomes a starter markdown or JSON structure a host can fill.
- `docs/result_atom_normalization.md` explains how known construct-level outputs become schema-shaped result atom bundles for downstream transport or research return.
- `capabilities/registry.yaml` stores the abstract host capability model used by the meta-skill and actualization layer.
- `artifacts/registry.yaml` stores artifact classes and their evidence and capability expectations.
- `actualization/registry.yaml` stores downstream actualization protocols that use A Person Index as the comparative core.
- `mappings/construct_to_motif.yaml` stores provisional construct-to-motif and instrument-to-motif mappings.
- `interactions/registry.yaml` stores house interaction hypotheses across motifs and constructs.
- `techniques/registry.yaml` stores reusable comparative methods.
- `protocols/registry.yaml` stores index program specs such as `ILENS`, `Paradox Finder`, and `Human Model Card`.
- `protocol_packs/catalog.yaml` stores curated, stable program-pack scopes for repeated downstream use.
- `research/contribution_models.yaml` stores privacy-minimizing contribution models for future research intake.
- `research/promotion_registry.yaml` stores the staged promotion policy that governs how research can influence house synthesis or protocol revision.
- `research/result_atom_schema.yaml` stores the normalized downstream result-atom contract for runtime exchange.
- `docs/result_atom_normalization.md` documents the repo-side helper that turns known construct-level outputs into schema-shaped result atom bundles.

The active, fully populated corpus remains instrument-centered for now. The new top-level directories formalize the broader A Person Index architecture without forcing a premature internal package rename.

## Composability model

A Person Index is meant to feel like legos:

1. Techniques
   Atomic reusable operations such as `Paradox Scan`.
2. Index programs
   Composed analyses or synthesis workflows such as `Paradox Finder`, `Translation Memo`, `ILENS`, or `Human Model Card`.
3. Runtime packs
   Scoped bundles that hydrate an index program with the exact frameworks, motifs, mappings, interaction hypotheses, and research return contracts needed for a task.

The internal registry path is still `protocols/registry.yaml`, but the public product concept is `index programs`.

## Compatibility surfaces

Some names intentionally remain stable for compatibility:

- `registry://...` on the MCP surface
- `protocols/registry.yaml`
- `protocol_packs/`

These are implementation and compatibility surfaces, not the product’s preferred public language.

## Seed corpus

The repository currently ships with 16 source-backed seed framework records spanning psychometric, workplace, relational, symbolic, and creativity-task systems:

- Big Five / OCEAN
- MBTI
- Enneagram
- DISC
- Kolbe
- CliftonStrengths
- Love Languages
- Dark Triad
- CQS
- Culture Index
- Human Design
- Natal Astrology
- Divergent Association Task
- Attachment Style Frameworks
- VIA Character Strengths
- HEXACO

Each seed framework record is expected to carry at least two resources and at least one outgoing crosswalk. Systems with stable major outputs should also carry multiple top-level constructs so the starter corpus remains comparative, not just descriptive.

## What This Is Not

- Not a quiz product
- Not a scoring engine
- Not a consumer-facing "find your type" app
- Not a database-first system in milestone 1
- Not a claim that all frameworks share the same evidence type
- Not a reason to mix raw user material into canonical framework records

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
npm install
```

## Common commands

```bash
python3 scripts/seed_registry.py
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/lint_ids.py
python3 scripts/build_index.py
python3 scripts/export_json.py
python3 scripts/generate_docs.py
python3 scripts/query_registry.py find --family trait_personality
python3 scripts/query_registry.py show MBTI --section constructs
python3 scripts/query_registry.py compare "Big Five" MBTI
python3 scripts/query_registry.py trace MBTI
python3 scripts/query_registry.py motifs --related-to MBTI
python3 scripts/query_registry.py interactions --related-to MBTI
python3 scripts/query_registry.py programs ILENS
python3 scripts/query_registry.py program-packs --featured
python3 scripts/query_registry.py program-packs ppk_ilens_core_trait_motive_stack
python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram
python3 scripts/query_registry.py program-pack-grammar
python3 scripts/query_registry.py research-promotion
python3 scripts/query_registry.py result-atom-schema
python3 scripts/query_registry.py research-models
npm run mcp:serve
npm run mcp:smoke
npm run mcp:contract
npm run mcp:test
python3 scripts/list_codex_queue_tasks.py --status ready --format ids
./scripts/test_claude_code_mcp.sh
python3 scripts/query_registry.py audit --needs-official-resource
python3 scripts/query_registry.py audit --needs-multiple-claims
python3 -m pytest
```

Tested client setup paths:

- [docs/mcp_clients.md](/Users/noveltokens/a_person_index/docs/mcp_clients.md)
- [scripts/write_claude_desktop_mcp_config.sh](/Users/noveltokens/a_person_index/scripts/write_claude_desktop_mcp_config.sh)
- [scripts/write_claude_mcp_config.sh](/Users/noveltokens/a_person_index/scripts/write_claude_mcp_config.sh)
- [scripts/test_claude_code_mcp.sh](/Users/noveltokens/a_person_index/scripts/test_claude_code_mcp.sh)
- [scripts/test_hermes_remote_mcp.sh](/Users/noveltokens/a_person_index/scripts/test_hermes_remote_mcp.sh)
- [examples/mcp](/Users/noveltokens/a_person_index/examples/mcp)

## Codex Companion Skill

If Codex is the host, use the companion skill when the task is specifically about operating A Person Index rather than just reading a file in the repo.

Use `$a-person-index` for:

- framework comparison
- motif tracing
- program-pack retrieval
- ILENS or Paradox Finder prep
- research-safe return formatting

The skill does not replace the MCP. It teaches Codex how to use the MCP and CLI surfaces correctly.

Canonical repo copy:

- [skills/a-person-index/SKILL.md](/Users/noveltokens/a_person_index/skills/a-person-index/SKILL.md)
- [skills/a-person-index/references/workflows.md](/Users/noveltokens/a_person_index/skills/a-person-index/references/workflows.md)

For a cold-start MCP session, the intended flow is:

```bash
python3 scripts/query_registry.py orient
python3 scripts/query_registry.py find --ref "Big Five" --ref MBTI --ref Enneagram
python3 scripts/query_registry.py program-packs --featured
python3 scripts/query_registry.py program-pack-summary ILENS --framework "Big Five" --framework MBTI --framework Enneagram
```

For bounded expansion work, the repo also carries:

- queue: [.github/codex/task_queue.yaml](/Users/noveltokens/a_person_index/.github/codex/task_queue.yaml)
- renderer: [scripts/render_codex_task_from_queue.py](/Users/noveltokens/a_person_index/scripts/render_codex_task_from_queue.py)
- workflow: [.github/workflows/dispatch-codex-queue-item.yml](/Users/noveltokens/a_person_index/.github/workflows/dispatch-codex-queue-item.yml)

## Add a new instrument

Use the scaffold command to create a valid starter entry:

```bash
python3 scripts/scaffold_instrument.py --slug hexad --name "Hexad User Types"
```

Then:

1. Fill out `instrument.yaml`.
2. Add or refine versions, constructs, claims, and resources.
3. Complete the minimum required annotation dimensions.
4. Add risks, use cases, and notes.
5. Run validation and rebuild generated outputs.

## Validation

Validation enforces:

- required files per instrument
- required extension registry files
- valid YAML and typed schema conformance
- globally unique IDs
- ID prefix and snake_case linting
- ontology enum membership
- annotation cardinality
- required annotation coverage
- cross-reference integrity
- relationship type validity
- instrument/version/construct consistency
- motif and protocol cross-reference integrity
- interaction hypothesis cross-reference integrity
- result atom schema availability for downstream runtimes

Broken references or missing required annotation dimensions fail validation.

## Contribution and automation

Repo contribution and automation surfaces are documented in:

- [CONTRIBUTING.md](/Users/noveltokens/a_person_index/CONTRIBUTING.md)
- [SECURITY.md](/Users/noveltokens/a_person_index/SECURITY.md)
- [docs/codex_automation.md](/Users/noveltokens/a_person_index/docs/codex_automation.md)
- [.github/ISSUE_TEMPLATE/codex_task.yml](/Users/noveltokens/a_person_index/.github/ISSUE_TEMPLATE/codex_task.yml)
- [.github/pull_request_template.md](/Users/noveltokens/a_person_index/.github/pull_request_template.md)

The default verification path is:

```bash
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
npm run mcp:test
python3 -m pytest
```

## Ontology

The ontology is versioned in `ontology/registry.yaml`. Dimensions and enum-backed value sets live in `ontology/dimensions.yaml` and `ontology/enums/*.yaml`.

Minimum required annotation dimensions are documented in:

- [AGENTS.md](/Users/noveltokens/a_person_index/AGENTS.md)
- [docs/annotation_guide.md](/Users/noveltokens/a_person_index/docs/annotation_guide.md)
- [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
- [docs/roadmap.md](/Users/noveltokens/a_person_index/docs/roadmap.md)
- [docs/editorial_style_guide.md](/Users/noveltokens/a_person_index/docs/editorial_style_guide.md)
- [docs/architecture.md](/Users/noveltokens/a_person_index/docs/architecture.md)
- [docs/gnomy_integration.md](/Users/noveltokens/a_person_index/docs/gnomy_integration.md)
- [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
- [docs/protocol_pack_grammar.md](/Users/noveltokens/a_person_index/docs/protocol_pack_grammar.md)
- [docs/research_contribution_guide.md](/Users/noveltokens/a_person_index/docs/research_contribution_guide.md)
- [src/personality_registry/constants.py](/Users/noveltokens/a_person_index/src/personality_registry/constants.py)

## Generated outputs

Generated outputs are written to:

- `generated/index.json`: aggregate API summary
- `generated/search.json`: search-oriented flattened records
- `generated/audit.json`: curation-depth and coverage summary per instrument
- `generated/instruments/*.json`: per-instrument exports
- `generated/manifest.json`: machine-readable onboarding and service-primitives manifest for agents
- `generated/protocol_packs/index.json`: curated program-pack catalog for stable downstream retrieval
- `generated/protocol_packs/*.json`: generated curated program-pack artifacts
- `generated/protocol_pack_grammar.json`: machine-readable grammar for building and validating future program packs
- `generated/research_promotion.json`: machine-readable staged promotion policy for research contributions
- `generated/registry.json`: full export payload, including house synthesis, index-program, and research registries
- `mcp-server/`: read-only Node MCP adapter over the Python query surface
- `site/`: self-contained static documentation site, including browse, audit, search, and comparison pages
- `site/data/*.json`: deployed data payloads used by the static site at runtime

Generated files are deterministic and can be rebuilt locally.

## Retrieval workflows

The repository includes a query CLI for exact lookup, filter retrieval, text search, relationship lookup, and side-by-side comparison over the canonical instrument corpus.

The generated static site now exposes the same corpus through:

- `site/index.html`: A Person Index browse entry point
- `site/search.html`: client-side search over shipped API data
- `site/compare.html`: generated comparison index
- `site/comparisons/*.html`: pairwise comparison pages derived from recorded crosswalks

The motif, protocol, and research registries are now available through dedicated CLI surfaces and dedicated site pages:

- `python3 scripts/query_registry.py trace MBTI`
- `python3 scripts/query_registry.py motifs --related-to MBTI`
- `python3 scripts/query_registry.py interactions --related-to MBTI`
- `python3 scripts/query_registry.py programs ILENS`
- `python3 scripts/query_registry.py program-packs --featured`
- `python3 scripts/query_registry.py program-packs ppk_ilens_core_trait_motive_stack`
- `python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram`
- `python3 scripts/query_registry.py program-pack-grammar`
- `python3 scripts/query_registry.py research-promotion`
- `python3 scripts/query_registry.py techniques "Paradox Scan"`
- `python3 scripts/query_registry.py result-atom-schema`
- `python3 scripts/query_registry.py research-models`

The repo also now exposes a read-only MCP interface for agent-native use:

- `npm run mcp:serve`
- [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
- [docs/protocol_packs.md](/Users/noveltokens/a_person_index/docs/protocol_packs.md)
- [docs/research_promotion.md](/Users/noveltokens/a_person_index/docs/research_promotion.md)

## Deployment

The repo now includes a Netlify deployment workflow at `.github/workflows/netlify-deploy.yml`.

- Pushes to `main` deploy `site/` to Netlify production.
- Pushes to `codex/**` branches deploy preview builds to Netlify.
- To enable it, add GitHub repository secrets:
- `NETLIFY_AUTH_TOKEN`
- `NETLIFY_SITE_ID`

The current Netlify site ID is `cc79449d-0efc-4029-9733-0f0039a37bf4`.

Examples:

```bash
python3 scripts/query_registry.py find --ref "Big Five"
python3 scripts/query_registry.py find --family typology --filter worldview_load=high
python3 scripts/query_registry.py find --text "identity narrative"
python3 scripts/query_registry.py find --related-to MBTI
python3 scripts/query_registry.py compare MBTI Enneagram
```

## Agent workflow

The repository is designed for agent-assisted authoring:

- propose structured YAML patches
- validate locally
- regenerate machine-readable exports
- keep provenance and version history in Git
- use [AGENTS.md](/Users/noveltokens/a_person_index/AGENTS.md) and [generated/manifest.json](/Users/noveltokens/a_person_index/generated/manifest.json) as the default arrival surface

When adding or editing content:

- keep source claims, ontology annotations, and house inferences clearly separated
- treat motifs and mappings as house synthesis, not source truth
- treat index programs as downstream consumers of the map, not the map itself
- treat research contributions as staged evidence, not immediate canonical fact

## Downstream role

This repo is meant to serve downstream runtimes such as `GNOMY`.

It should eventually provide:

- canonical framework records
- crosswalks and construct mappings
- house motifs
- reusable comparative techniques
- index program specs
- research-backed caveats and refinements

`ILENS` now lives conceptually in the index-program layer, not as the ontology itself.
