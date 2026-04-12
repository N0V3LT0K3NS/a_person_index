# Personality Instrument Registry

Personality Instrument Registry is the current canonical slice of a broader Git-native, agent-readable registry for personhood frameworks, house synthesis motifs, reusable comparative techniques, downstream protocols, and privacy-minimizing research intake.

The repository began as an instrument registry in milestone 1. It now explicitly carries four product layers:

1. Canonical registry
2. House synthesis substrate
3. Technique and protocol library
4. Research stream

Canonical source data still lives in structured YAML files, is validated with typed Python models, and is exported into generated JSON and browsable docs.

## Three-layer model

Each instrument is represented in three distinct layers:

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
3. Technique and protocol library
   Reusable comparative methods plus downstream protocol specs such as `ILENS`.
4. Research stream
   Contribution models for mapping votes, result-atom bundles, and distilled observations.

These layers should collaborate, but they should not be conflated.

## Repository shape

```text
.
├── docs/
├── generated/
├── interactions/
├── instruments/
├── mappings/
├── motifs/
├── ontology/
├── protocols/
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
- `mappings/construct_to_motif.yaml` stores provisional construct-to-motif and instrument-to-motif mappings.
- `interactions/registry.yaml` stores house interaction hypotheses across motifs and constructs.
- `techniques/registry.yaml` stores reusable comparative methods.
- `protocols/registry.yaml` stores downstream protocol specs such as `ILENS` and `Human Model Card`.
- `research/contribution_models.yaml` stores privacy-minimizing contribution models for future research intake.
- `research/result_atom_schema.yaml` stores the normalized downstream result-atom contract for runtime exchange.

The active, fully populated corpus remains instrument-centered for now. The new top-level directories formalize the next architecture layer without forcing a premature package rename.

## Seed corpus

The repository currently ships with 15 source-backed seed instruments spanning psychometric, workplace, relational, and symbolic systems:

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
- Attachment Style Frameworks
- VIA Character Strengths
- HEXACO

Each seed instrument is expected to carry at least two resources and at least one outgoing crosswalk. Systems with stable major outputs should also carry multiple top-level constructs so the starter corpus remains comparative, not just descriptive.

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
python3 scripts/query_registry.py protocols ILENS
python3 scripts/query_registry.py result-atom-schema
python3 scripts/query_registry.py research-models
python3 scripts/query_registry.py audit --needs-official-resource
python3 scripts/query_registry.py audit --needs-multiple-claims
python3 -m pytest
```

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

## Ontology

The ontology is versioned in `ontology/registry.yaml`. Dimensions and enum-backed value sets live in `ontology/dimensions.yaml` and `ontology/enums/*.yaml`.

Minimum required annotation dimensions are documented in:

- [docs/annotation_guide.md](/Users/noveltokens/a_person_index/docs/annotation_guide.md)
- [docs/editorial_style_guide.md](/Users/noveltokens/a_person_index/docs/editorial_style_guide.md)
- [docs/architecture.md](/Users/noveltokens/a_person_index/docs/architecture.md)
- [docs/gnomy_integration.md](/Users/noveltokens/a_person_index/docs/gnomy_integration.md)
- [docs/research_contribution_guide.md](/Users/noveltokens/a_person_index/docs/research_contribution_guide.md)
- [src/personality_registry/constants.py](/Users/noveltokens/a_person_index/src/personality_registry/constants.py)

## Generated outputs

Generated outputs are written to:

- `generated/index.json`: aggregate registry summary
- `generated/search.json`: search-oriented flattened records
- `generated/audit.json`: curation-depth and coverage summary per instrument
- `generated/index.json`: aggregate registry summary plus product-layer counts
- `generated/instruments/*.json`: per-instrument exports
- `generated/registry.json`: full export payload, including house synthesis, protocol, and research registries
- `site/`: self-contained static documentation site, including browse, audit, search, and comparison pages
- `site/data/*.json`: deployed data payloads used by the static site at runtime

Generated files are deterministic and can be rebuilt locally.

## Retrieval workflows

The repository includes a query CLI for exact lookup, filter retrieval, text search, relationship lookup, and side-by-side comparison over the canonical instrument corpus.

The generated static site now exposes the same corpus through:

- `site/index.html`: registry browse entry point
- `site/search.html`: client-side search over shipped registry data
- `site/compare.html`: generated comparison index
- `site/comparisons/*.html`: pairwise comparison pages derived from recorded crosswalks

The motif, protocol, and research registries are now available through dedicated CLI surfaces and dedicated site pages:

- `python3 scripts/query_registry.py trace MBTI`
- `python3 scripts/query_registry.py motifs --related-to MBTI`
- `python3 scripts/query_registry.py interactions --related-to MBTI`
- `python3 scripts/query_registry.py protocols ILENS`
- `python3 scripts/query_registry.py techniques "Paradox Scan"`
- `python3 scripts/query_registry.py result-atom-schema`
- `python3 scripts/query_registry.py research-models`

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

When adding or editing content:

- keep source claims, ontology annotations, and house inferences clearly separated
- treat motifs and mappings as house synthesis, not source truth
- treat protocols as downstream consumers of the map, not the map itself
- treat research contributions as staged evidence, not immediate canonical fact

## Downstream role

This repo is meant to serve downstream runtimes such as `GNOMY`.

It should eventually provide:

- canonical framework records
- crosswalks and construct mappings
- house motifs
- reusable comparative techniques
- protocol specs
- research-backed caveats and refinements

`ILENS` now lives conceptually in the protocol layer, not as the ontology itself.
