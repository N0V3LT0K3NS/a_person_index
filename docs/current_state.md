# Current State

This document compresses what the repository currently is, what is complete, and what is still ahead.

## One-line status

The repo is now A Person Index: a working personhood-framework index plus a first house synthesis, technique, program, pack, and research substrate that can act as the comparative core for richer downstream protocols and artifacts.

Public landing page: [a-person-index.netlify.app](https://a-person-index.netlify.app)

Release status: [docs/release_status.md](/Users/noveltokens/a_person_index/docs/release_status.md)

Standing planning memo: [docs/strategic_backlog.md](/Users/noveltokens/a_person_index/docs/strategic_backlog.md)

## Current shipped scope

As of the current branch state, the repo includes:

- 16 seeded canonical framework records in the current instrument-centered schema
- 7 named analysis modes
- 6 artifact classes
- 4 actualization protocols
- 11 house motifs
- 18 construct or instrument mappings into motifs
- 7 interaction hypotheses
- 6 reusable techniques
- 6 index program specs
- 6 curated program packs
- 5 research contribution models
- 5 research promotion pathways
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

### Technique library and index programs

- Techniques are first-class records rather than scattered prompt fragments
- Index programs such as `Paradox Finder`, `ILENS`, `Human Model Card`, and `Translation Memo` are explicitly modeled as consumers of the index
- Runtime packs are now a callable bundle shape rather than an implicit orchestration task left to downstream agents
- Curated program packs now have a source catalog, generated artifacts, and stable discovery surfaces for downstream agents

### Research stream

- Contribution models for mapping votes, relation judgments, result-atom bundles, distilled observations, and protocol feedback
- A typed promotion registry that governs how research can move from intake to reviewed house synthesis or protocol revision
- A normalized result atom schema for downstream runtimes such as `GNOMY`

### Operational layer

- CLI query surface
- read-only MCP adapter
- repo-owned MCP smoke and contract tests
- tested Claude Code MCP path
- documented Claude Desktop MCP path
- documented Hermes MCP path with environment-specific remote assumptions
- Deterministic generated outputs
- Static documentation site
- Three generated landing-page directions for the public site
- Contribution and governance docs
- GitHub issue and PR templates
- Codex task workflow scaffold
- queue-driven Codex task dispatch for bounded expansion PRs
- batched ready-queue dispatch for bounded multi-PR expansion bursts
- CI workflow
- Netlify deployment workflow

### Conceptual framing

- the repo is now explicitly treated as a comparative core, not only a registry
- the boundaries between ontology, programs, downstream realization, and research return are clearer
- the system can be described not only as a data substrate, but as a reusable comparative grammar for downstream protocols

## What this repo is not yet

- Not yet a generalized top-level `framework` registry beyond the current instrument-centered canonical corpus
- Not yet a full HTTP API
- Not yet a person-level inference engine
- Not yet a hosted remote MCP service
- Not yet a full research operations pipeline with storage, aggregation, review queues, and promotion logs
- Not yet a standardized artifact-rendering runtime
- Not yet a multi-subject comparison runtime with persistence or account linkage

## Highest-value current use

Right now the repo is most useful as:

1. a canonical registry of personhood systems
2. a comparative translation substrate
3. a technique, index-program, and curated-pack library for downstream runtimes
4. a comparative core for richer protocol and artifact work in downstream agents
5. a first contextual and pairwise comparison substrate
6. a research intake contract for privacy-minimizing return traffic

## Immediate next work

The next highest-value tranche is:

1. integrate `GNOMY` and other consumers against the current substrate and stabilize the contract
2. deepen motif mappings and interaction hypotheses across the strongest framework seams exposed by use
3. add research audit and candidate-review surfaces on top of the promotion registry
4. broaden the canonical model only where real consumer pressure proves the current instrument-first shape too narrow
