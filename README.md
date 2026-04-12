# Personality Instrument Registry

Personality Instrument Registry is a Git-native, agent-readable knowledge base for personality tests, typology systems, psychometric instruments, symbolic self-description systems, and adjacent person-labeling frameworks.

The repository is the product in milestone 1. Canonical source data lives in structured YAML files, is validated with typed Python models, and is exported into generated JSON and simple browsable docs.

## Three-layer model

Each instrument is represented in three distinct layers:

1. Source-truth layer: what the instrument or its source materials say about itself.
2. Meta-ontology layer: standardized house annotations applied through the shared ontology.
3. Inferred comparative layer: house synthesis, critique, crosswalks, and practical notes.

Do not collapse these layers into one blended narrative.

## Repository shape

```text
.
├── docs/
├── generated/
├── instruments/
├── ontology/
├── schemas/
├── scripts/
├── site/
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
python3 scripts/query_registry.py audit --needs-official-resource
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
- valid YAML and typed schema conformance
- globally unique IDs
- ID prefix and snake_case linting
- ontology enum membership
- annotation cardinality
- required annotation coverage
- cross-reference integrity
- relationship type validity
- instrument/version/construct consistency

Broken references or missing required annotation dimensions fail validation.

## Ontology

The ontology is versioned in `ontology/registry.yaml`. Dimensions and enum-backed value sets live in `ontology/dimensions.yaml` and `ontology/enums/*.yaml`.

Minimum required annotation dimensions are documented in:

- [docs/annotation_guide.md](/Users/noveltokens/a_person_index/docs/annotation_guide.md)
- [src/personality_registry/constants.py](/Users/noveltokens/a_person_index/src/personality_registry/constants.py)

## Generated outputs

Generated outputs are written to:

- `generated/index.json`: aggregate registry summary
- `generated/search.json`: search-oriented flattened records
- `generated/audit.json`: curation-depth and coverage summary per instrument
- `generated/instruments/*.json`: per-instrument exports
- `generated/registry.json`: full export payload
- `site/`: simple static HTML documentation

Generated files are deterministic and can be rebuilt locally.

## Retrieval workflows

The repository includes a query CLI for exact lookup, filter retrieval, text search, relationship lookup, and side-by-side comparison.

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

When adding or editing content, keep source claims, ontology annotations, and house inferences clearly separated.
