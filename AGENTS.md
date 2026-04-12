# Agent Guide

This repository is an agent-readable knowledge substrate for personhood frameworks.

If you are arriving cold, start here in this order:

1. [README.md](/Users/noveltokens/a_person_index/README.md)
2. [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
3. [docs/roadmap.md](/Users/noveltokens/a_person_index/docs/roadmap.md)
4. [docs/architecture.md](/Users/noveltokens/a_person_index/docs/architecture.md)
5. [docs/gnomy_integration.md](/Users/noveltokens/a_person_index/docs/gnomy_integration.md)
6. [docs/protocol_pack_grammar.md](/Users/noveltokens/a_person_index/docs/protocol_pack_grammar.md)
7. [generated/manifest.json](/Users/noveltokens/a_person_index/generated/manifest.json)

## What this repo is

The repo has four distinct product layers:

1. Canonical registry
   Source-faithful framework records, currently centered on instruments.
2. House synthesis substrate
   Motifs, construct mappings, and interaction hypotheses.
3. Technique and protocol library
   Reusable methods plus downstream protocols such as `ILENS`.
4. Research stream
   Privacy-minimizing contribution models and the result atom schema.

Do not collapse those layers into one.

## Source of truth

Edit source files, not generated outputs.

Canonical sources:
- [instruments](/Users/noveltokens/a_person_index/instruments)
- [ontology](/Users/noveltokens/a_person_index/ontology)
- [motifs/registry.yaml](/Users/noveltokens/a_person_index/motifs/registry.yaml)
- [mappings/construct_to_motif.yaml](/Users/noveltokens/a_person_index/mappings/construct_to_motif.yaml)
- [interactions/registry.yaml](/Users/noveltokens/a_person_index/interactions/registry.yaml)
- [techniques/registry.yaml](/Users/noveltokens/a_person_index/techniques/registry.yaml)
- [protocols/registry.yaml](/Users/noveltokens/a_person_index/protocols/registry.yaml)
- [research/contribution_models.yaml](/Users/noveltokens/a_person_index/research/contribution_models.yaml)
- [research/result_atom_schema.yaml](/Users/noveltokens/a_person_index/research/result_atom_schema.yaml)

Do not manually edit:
- [generated](/Users/noveltokens/a_person_index/generated)
- [site](/Users/noveltokens/a_person_index/site)
- [schemas](/Users/noveltokens/a_person_index/schemas)

## Core rules

- Keep source claims, ontology annotations, and house inferences separate.
- Treat motifs, mappings, and interaction hypotheses as house synthesis, not source truth.
- Treat protocols as downstream consumers of the map, not the map itself.
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
python3 scripts/query_registry.py find --ref "Big Five"
python3 scripts/query_registry.py compare MBTI Enneagram
python3 scripts/query_registry.py trace MBTI
python3 scripts/query_registry.py motifs --related-to MBTI
python3 scripts/query_registry.py interactions --related-to "Attachment Style Frameworks"
python3 scripts/query_registry.py protocols ILENS
python3 scripts/query_registry.py protocol-pack ILENS --framework MBTI --framework Enneagram
python3 scripts/query_registry.py protocol-pack-grammar
python3 scripts/query_registry.py techniques "Paradox Scan"
python3 scripts/query_registry.py result-atom-schema
python3 scripts/query_registry.py research-models
python3 scripts/query_registry.py audit --needs-official-resource
```

## Downstream role

This repo is meant to serve runtimes such as `GNOMY`.

It should provide:
- canonical framework records
- ontology annotations
- crosswalks
- motifs and construct mappings
- interaction hypotheses
- reusable techniques
- protocol specs
- research contribution models
- the result atom schema

It should not perform full person-level inference itself.
