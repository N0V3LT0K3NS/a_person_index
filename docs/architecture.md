# Architecture

This repository is no longer only an instrument catalog.

It now has four distinct product layers:

1. Canonical registry
   Structured records for instruments and adjacent personhood frameworks in their own terms.

2. House synthesis substrate
   Motifs, mappings, and interaction hypotheses that let the repo compare frameworks through a shared interlingua without pretending they are identical.

3. Technique and protocol library
   Reusable comparative methods and downstream synthesis protocols such as `ILENS` and `Human Model Card`.

4. Research stream
   Privacy-minimizing contribution models for collecting mapping feedback, pairwise judgments, result-atom bundles, and distilled observations.

## Why this split matters

The registry, synthesis layer, protocols, and research stream should not collapse into one bucket.

- Canonical framework data should remain attributable and stable.
- House motifs and mappings should remain clearly marked as provisional or inferred.
- Protocols should be treated as consumers of the map, not as the map itself.
- Research contributions should be staged before they become house inference.

## Current phase boundary

The active, fully validated domain remains the instrument corpus.

Phase 2 adds:

- `motifs/`
- `mappings/`
- `interactions/`
- `techniques/`
- `protocols/`
- `research/`

These directories formalize the larger architecture without breaking the current milestone-1 corpus.

Companion docs:

- [current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
- [roadmap.md](/Users/noveltokens/a_person_index/docs/roadmap.md)

## Relationship to GNOMY

`GNOMY` is a downstream runtime and user-facing inference layer.

This repo should serve GNOMY by supplying:

- canonical framework records
- ontology annotations
- crosswalks
- motifs and construct mappings
- reusable techniques
- protocol specs
- research-backed caveats

GNOMY, in turn, can send back normalized and privacy-minimizing research contributions rather than raw personal corpora.

## Service primitives

The near-term callable surface for downstream agents should center on a few durable primitives:

- find canonical framework records
- compare framework records
- trace an instrument or construct to house motifs
- fetch house interaction hypotheses for motifs, constructs, or frameworks
- fetch protocol specs and their required techniques
- fetch research contribution models and the result-atom schema for safe return traffic

These are intentionally smaller than full person-level synthesis. They make the repo useful to runtimes like GNOMY without moving person-level inference into this codebase.

## Relationship to ILENS

`ILENS` is a protocol, not the ontology itself.

The ontology should stay broad enough to support ILENS, Human Model Card workflows, translation memos, paradox scans, and future downstream protocols that are not yet designed.
