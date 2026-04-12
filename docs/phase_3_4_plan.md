# Phase 3 And 4 Plan

This document compresses the next implementation sequence after the current substrate build-out.

## Planning stance

The next priority is not more abstract ontology work.

The next priority is to use the current substrate through `GNOMY` and other consumers, then let that usage reveal what needs tightening before building the larger empirical research operations layer.

## Phase 3: Downstream Consumer Integration

Status: next

Goal:
- prove and harden this repository as a shared dependency surface for real runtimes

### Repo work

- stabilize the MCP and CLI consumer contract
- expand protocol packs where repeated use reveals real demand
- fill motif and interaction gaps exposed during runtime usage
- tighten manifest and onboarding around consumer integration
- sharpen the public docs and site so consumers understand the substrate on arrival

### GNOMY work

- connect to the repo through MCP or CLI
- fetch curated or dynamic protocol packs
- normalize runtime outputs into result atoms
- use motifs, mappings, and interactions during synthesis
- return only approved research contribution shapes

### Completion signal

Phase 3 is working when `GNOMY` can use this repo without re-deriving its logic by hand.

## Phase 4: Research Ops And Review Surfaces

Status: planned after consumer integration pressure is visible

Goal:
- turn contribution governance into an actual evidence and review loop

### Repo work

- add research audit surfaces
- add candidate-review outputs such as mapping-review queues and interaction candidates
- add promotion logs or reviewed-change summaries
- keep promotion policy and contribution schemas aligned

### External research ops work

- receive structured contributions
- anonymize and deduplicate them
- aggregate by seam, mapping, interaction, and protocol
- produce review-ready candidate outputs
- feed reviewed proposals back into this repo

### Completion signal

Phase 4 is working when research contribution traffic produces reviewable candidate changes rather than just sitting as abstract allowed shapes.

## Later but not immediate: Generalized Framework Model

The repo still uses an instrument-centered canonical model.

That is acceptable for now because the immediate bottleneck is not storage viability. It is runtime use and contract pressure.

A broader `framework` model should be designed after Phase 3 reveals where the current instrument shape is actually too narrow.

## Open questions to carry through Phase 3

- Which protocol packs become heavily used enough to deserve curated support?
- Which result-atom shapes recur across consumers besides `GNOMY`?
- Where does the current instrument-centered model feel too narrow in real use?
- What research contributions are actually worth collecting, rather than merely possible to collect?
- Which review surfaces would save the most curator time first?

## Sequence rule

Use the substrate first.

Do not build the full research operations layer before runtime usage reveals what the evidence flow actually looks like.
