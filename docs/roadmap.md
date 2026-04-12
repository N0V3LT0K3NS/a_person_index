# Roadmap

This roadmap codifies where the repository has come from, where it is now, and what the next layers should be.

## North star

Build a Git-native, agent-readable comparative atlas of personhood frameworks, then use that atlas to support translation, synthesis protocols, and eventually research-backed understanding of recurring circuitry across systems.

## Phase 1: Canonical Registry

Status: complete

Goal:
- establish a validated canonical corpus for personality and adjacent frameworks

Delivered:
- instrument-centered data model
- ontology and enum system
- 15 seeded framework records
- claims, resources, annotations, inferences, crosswalks, risks, use cases, and notes
- generated JSON exports
- static docs site
- validation and tests

## Phase 2: House Synthesis And Protocol Substrate

Status: complete enough for real consumer integration

Goal:
- add the first translation and downstream-consumption layer without breaking the canonical corpus

Delivered so far:
- motifs
- construct-to-motif mappings
- interaction hypotheses
- technique registry
- protocol registry
- protocol-pack query surface and grammar
- curated protocol-pack catalog and generated pack artifacts
- read-only MCP adapter over the Python query surface
- research contribution models
- research promotion registry
- result atom schema
- motif, protocol, interaction, research, and curated-pack query surfaces
- stronger repo-level onboarding, manifesting, and agent-arrival docs

## Phase 3: Downstream Consumer Integration

Status: next

Goal:
- prove the repository as a shared dependency surface for real consumers such as `GNOMY`

Target deliverables:
- stable consumer contract across MCP, CLI, manifest, and generated artifacts
- successful `GNOMY` use of protocol packs, result atoms, motifs, and interaction hypotheses
- contract hardening based on real runtime pressure
- richer protocol-pack coverage where repeated use justifies it
- cleaner merge of the widened repo identity into `main`

## Phase 4: Research Ops And Evidence Review

Status: planned

Goal:
- turn research governance into an operational evidence loop

Target deliverables:
- contribution intake outside the canonical corpus
- anonymization, deduplication, and aggregation
- research audit surfaces
- candidate-review outputs for mappings, interactions, and protocols
- promotion logs and reviewed-change traces

## Phase 5: Generalized Framework Model

Status: planned

Goal:
- broaden the canonical model beyond the current instrument-centered shape when real usage reveals where it is too narrow

Target deliverables:
- clearer umbrella `framework` model
- subtype-aware canonical records
- backward-compatible migration path from the current instrument-first corpus

## Phase 6: Comparative Depth And Empirical Refinement

Status: planned

Goal:
- increase comparative density and eventually use structured real-world signals to refine the map

Target deliverables:
- denser construct-level crosswalks
- denser motif coverage
- more secondary and critical source coverage
- aggregate mapping and interaction evidence from downstream systems
- research-backed refinement of house motifs and interaction hypotheses

## Out of scope for this repo

This repository should not become:

- a consumer quiz app
- a scoring engine
- a raw personal-data warehouse
- the full person-level inference runtime

Those belong elsewhere. This repo should remain the map, the method library, and the structured substrate.
