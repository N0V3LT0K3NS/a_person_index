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

## Phase 2: House Synthesis and Protocol Substrate

Status: active and materially underway

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

Still to do in this phase:
- richer mapping density across more framework seams
- cleaner merge of the widened repo identity into `main`

## Phase 3: Research Promotion and Evidence Flow

Status: next

Goal:
- let downstream runtimes and human contributors feed structured, privacy-minimizing evidence back into the repo

Target deliverables:
- staging distinctions such as anecdotal, aggregated, reviewed, promoted
- research audit surfaces
- better distinction between canonical truth, house synthesis, and emerging pattern evidence
- contributor-side tooling and richer audit surfaces around promotion candidates

## Phase 4: Agent and Runtime Surfaces

Status: planned

Goal:
- make the repo callable as infrastructure by systems such as `GNOMY`

Target deliverables:
- stable agent manifest
- richer protocol-pack catalogs and downstream service bundles
- lightweight API or richer MCP surface
- improved machine-readable service contracts

## Phase 5: Comparative Depth and Empirical Refinement

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
