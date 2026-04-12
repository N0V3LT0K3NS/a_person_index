# System Boundaries

This document states what belongs in this repository, what belongs in `GNOMY`, and what likely belongs in a later research operations layer.

## Core stance

This repository is a shared substrate.

It is essential for `GNOMY`, but it is not only for `GNOMY`.

It should remain useful to:

- `GNOMY`
- future synthesis runtimes
- curation agents
- compare or translation tools
- future research tooling

## What belongs here

This repo owns:

- canonical framework records
- ontology annotations
- house motifs, mappings, and interaction hypotheses
- comparative techniques
- downstream protocol specs
- curated protocol packs
- research contribution schemas
- research promotion policy
- agent-facing access surfaces such as CLI, generated artifacts, and MCP

This repo is the map, the method library, and the governance layer.

## What does not belong here

This repo should not become:

- the full person-level inference engine
- the raw personal-data store
- the consumer UI
- the scoring runtime for every framework
- the operational research database

Those are adjacent systems, not this repository.

## What belongs in GNOMY

`GNOMY` should own:

- user-facing or analyst-facing runtime behavior
- intake of user evidence
- local person-level synthesis
- report generation
- protocol execution on real people
- adaptation to context, history, and interaction

`GNOMY` should call this repo for:

- canonical records
- protocol packs
- motif traces
- interaction hypotheses
- result-atom schema
- research contribution models
- research promotion policy

## What likely belongs in a later research ops layer

A later research operations layer should own:

- intake and storage of structured contributions
- anonymization and deduplication
- aggregation and clustering
- review queues
- candidate generation
- promotion logs

That layer may feed reviewed proposals back into this repo, but it should not collapse into this repo.

## Boundary table

### This repo

- source of truth for framework and house-synthesis knowledge
- protocol and technique definitions
- contribution and promotion contracts
- agent-readable access surface

### GNOMY

- runtime synthesis engine
- person-level application of the substrate
- protocol execution against real user evidence
- optional structured return traffic

### Research ops layer

- operational evidence handling
- review workflow
- aggregation and promotion support

## Practical rule

When deciding whether something belongs here, ask:

Is this a durable shared knowledge object, a reusable method, or a governance rule?

If yes, it probably belongs here.

Is it specific to a live person, a runtime execution, or an operational evidence pipeline?

If yes, it probably belongs elsewhere.
