# Program Pack Grammar

This document defines the canonical syntax for generated program packs.

## What a program pack is

A program pack is a downstream-ready bundle assembled from existing registry primitives.

The internal `protocol_pack` naming remains in the grammar and generated artifacts for compatibility, even as the public product language increasingly refers to these as `program packs`.

It is not source truth.
It is not a new ontology object.
It is a generated runtime bundle that packages:

- one protocol
- its technique bundle
- scoped canonical records
- scoped motif traces
- relevant mappings
- relevant interaction hypotheses
- execution order
- output contract
- return contract

## Why packs exist

Without packs, a downstream agent has to call many separate primitives and decide how to compose them.

With packs, the repo can supply a pre-assembled operational bundle for a defined task such as:

- `ILENS`
- `Human Model Card`
- `Translation Memo`

## Canonical section order

Every program pack should follow this section order:

1. `pack`
2. `protocol`
3. `techniques`
4. `targets`
5. `canonical_records`
6. `motif_summary`
7. `relevant_mappings`
8. `interaction_hypotheses`
9. `input_contract`
10. `execution_order`
11. `output_contract`
12. `return_contract`

## Section grammar

### `pack`

Identity and scope metadata for the assembled bundle.

Required keys:
- `id`
- `grammar_id`
- `protocol_id`
- `protocol_name`
- `target_count`
- `target_framework_ids`
- `target_construct_ids`
- `target_labels`

### `protocol`

Expanded protocol spec from `protocols/registry.yaml`.

### `techniques`

Expanded technique records referenced by the protocol.

### `targets`

Resolved framework or construct entity references that define the pack scope.

### `canonical_records`

Minimal framework records for the instruments touched by the pack scope.

### `motif_summary`

Aggregated motif traces for the scoped targets.

### `relevant_mappings`

Deduplicated mapping payloads derived from the scoped traces.

### `interaction_hypotheses`

Deduplicated interaction hypotheses filtered by both scope and protocol relevance.

### `input_contract`

The protocol's required and optional inputs.

### `execution_order`

Suggested ordered sequence for using the pack.

### `output_contract`

Primary outputs expected from the downstream runtime.

### `return_contract`

Preferred contribution models for returning structured feedback to this repo, plus the result atom schema when relevant.

## Construction rules

- A pack is always assembled from existing source and house records. Do not hand-author a pack as a new canonical object.
- The protocol record remains authoritative for purpose, required inputs, optional inputs, and primary outputs.
- Framework targets should expand through their constructs when tracing motifs.
- Construct targets should preserve both construct identity and parent framework identity.
- Motifs should be derived from mappings and traces, not selected ad hoc.
- Interaction hypotheses should be filtered by both target scope and protocol relevance.
- If the protocol can use result atoms, include the result atom schema in the return contract.
- Packs should preserve epistemic bracketing. A pack does not erase symbolic vs empirical differences.

## Generative syntax

The canonical generative form is:

```text
protocol_pack :=
  pack
  + protocol
  + techniques
  + optional scoped targets
  + scoped canonical records
  + scoped motif summary
  + scoped relevant mappings
  + scoped interaction hypotheses
  + input contract
  + execution order
  + output contract
  + return contract
```

The canonical machine-readable grammar is also emitted to:

- [generated/protocol_pack_grammar.json](/Users/noveltokens/a_person_index/generated/protocol_pack_grammar.json)
- [site/data/protocol_pack_grammar.json](/Users/noveltokens/a_person_index/site/data/protocol_pack_grammar.json)

For curated pack lifecycle, maintenance, and source catalog rules, also see:

- [docs/protocol_packs.md](/Users/noveltokens/a_person_index/docs/protocol_packs.md)

## Example commands

```bash
python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram
python3 scripts/query_registry.py program-pack "Translation Memo" --framework "Human Design" --framework "Natal Astrology"
python3 scripts/query_registry.py program-pack-grammar
```

## Future authoring rule

If future packs need new fields, update both:

1. the generated grammar payload
2. this document

Do not introduce one-off pack shapes for individual protocols.
