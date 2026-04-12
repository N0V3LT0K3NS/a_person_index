# Current State

This document compresses what the repository currently is, what is complete, and what is still ahead.

## One-line status

The repo is now a working personhood-framework registry plus a first house synthesis, protocol, and research substrate.

## Current shipped scope

As of the current branch state, the repo includes:

- 15 seeded canonical instrument records
- 11 house motifs
- 16 construct or instrument mappings into motifs
- 7 interaction hypotheses
- 6 reusable techniques
- 3 protocol specs
- 5 research contribution models
- 1 result atom schema

## What is complete

### Canonical registry

- Source-backed seed corpus across psychometric, workplace, relational, and symbolic systems
- Versioned framework records with claims, resources, annotations, inferences, crosswalks, risks, use cases, and notes
- Validation for IDs, YAML shape, ontology values, and cross-references
- Generated JSON exports and static docs

### House synthesis substrate

- First motif layer
- First construct-to-motif mapping layer
- First interaction-hypothesis layer
- Query surfaces for motif tracing and interaction lookup

### Technique and protocol library

- Techniques are first-class records rather than scattered prompt fragments
- Protocols such as `ILENS`, `Human Model Card`, and `Translation Memo` are explicitly modeled as consumers of the registry
- Protocol packs are now a callable runtime bundle shape rather than an implicit orchestration task left to downstream agents

### Research stream

- Contribution models for mapping votes, relation judgments, result-atom bundles, distilled observations, and protocol feedback
- A normalized result atom schema for downstream runtimes such as `GNOMY`

### Operational layer

- CLI query surface
- Deterministic generated outputs
- Static documentation site
- CI workflow
- Netlify deployment workflow

## What this repo is not yet

- Not yet a generalized top-level `framework` registry beyond the current instrument-centered canonical corpus
- Not yet a full API or MCP server
- Not yet a person-level inference engine
- Not yet a research-promotion engine that automatically turns contributions into house mappings or interaction hypotheses
- Not yet merged to `main`

## Highest-value current use

Right now the repo is most useful as:

1. a canonical registry of personhood systems
2. a comparative translation substrate
3. a protocol/spec library for downstream runtimes
4. a research intake contract for privacy-minimizing return traffic

## Immediate next work

The next highest-value tranche is:

1. add protocol-pack and agent-entrypoint surfaces
2. formalize research promotion from contribution -> reviewed pattern -> house synthesis
3. deepen motif mappings and interaction hypotheses across the strongest framework seams
4. keep improving repo onboarding and public presentation until the repo itself is self-explanatory
