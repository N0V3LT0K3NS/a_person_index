# Research Promotion

This document defines how research contributions can influence the repo.

## Why this exists

The research stream should improve house synthesis and protocols without turning:

- raw user feedback
- one-off anecdotes
- downstream agent outputs

into canonical truth.

The promotion registry is the guardrail for that.

## Source of truth

The research-promotion source of truth is:

- [research/promotion_registry.yaml](/Users/noveltokens/a_person_index/research/promotion_registry.yaml)

It defines:

- promotion stages
- promotion pathways
- review expectations
- valid target layers and outcomes

## What it governs

The promotion registry governs how these contribution models can move forward:

- [research/contribution_models.yaml](/Users/noveltokens/a_person_index/research/contribution_models.yaml)
- [research/result_atom_schema.yaml](/Users/noveltokens/a_person_index/research/result_atom_schema.yaml)

It is the bridge between:

- research intake
- reviewed pattern formation
- changes to house synthesis or protocol records

## Current pathways

The current staged pathways are:

- `Mapping Vote -> mapping revision`
- `Pairwise Relation Judgment -> interaction hypothesis`
- `Result Atom Bundle -> comparative analysis`
- `Distilled Observation -> house inference`
- `Protocol Feedback -> protocol revision`

## Core rules

- Do not promote single contributions directly into house synthesis.
- House-synthesis and protocol changes require a reviewed stage.
- Comparative analysis is allowed as a research-stream output without direct promotion.
- Promotion should preserve conflict, provenance, and scope.
- Canonical framework records remain separate from research promotion.

## Generated and query surfaces

The registry emits and serves this policy through:

- [generated/research_promotion.json](/Users/noveltokens/a_person_index/generated/research_promotion.json)
- [site/data/research_promotion.json](/Users/noveltokens/a_person_index/site/data/research_promotion.json)
- `python3 scripts/query_registry.py research-promotion`
- `python3 scripts/query_registry.py research-promotion --contribution-model "Mapping Vote"`

## Maintenance rule

If you change contribution-model promotion paths, update both:

1. [research/contribution_models.yaml](/Users/noveltokens/a_person_index/research/contribution_models.yaml)
2. [research/promotion_registry.yaml](/Users/noveltokens/a_person_index/research/promotion_registry.yaml)

They should stay aligned.
