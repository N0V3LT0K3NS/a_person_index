# A Person Index Architecture

This repository is no longer only an instrument catalog or a simple registry.

It now has five distinct product layers:

1. Canonical registry
   Structured records for instruments and adjacent personhood frameworks in their own terms.

2. House synthesis substrate
   Motifs, mappings, and interaction hypotheses that let the repo compare frameworks through a shared interlingua without pretending they are identical.

3. Technique library
   Atomic comparative methods such as `Paradox Scan`, `Cross-Framework Translation`, and `Result Atom Decomposition`.

4. Index programs and runtime packs
   Composed programs such as `Paradox Finder`, `Translation Memo`, `ILENS`, and `Human Model Card`, plus scoped runtime packs that hydrate those programs with motifs, mappings, interactions, and return contracts.

5. Research stream
   Privacy-minimizing contribution models plus a staged promotion registry for collecting mapping feedback, pairwise judgments, result-atom bundles, and distilled observations without collapsing them straight into truth.

## Why this split matters

The registry, synthesis layer, techniques, index programs, packs, and research stream should not collapse into one bucket.

- Canonical framework data should remain attributable and stable.
- House motifs and mappings should remain clearly marked as provisional or inferred.
- Index programs should be treated as consumers of the map, not as the map itself.
- Research contributions should be staged before they become house inference.

## Composition model

A Person Index is intentionally composable:

1. Techniques are the smallest reusable legos.
2. Index programs compose techniques, and sometimes smaller programs, into a named analysis workflow.
3. Runtime packs scope a program to concrete frameworks or constructs and attach the exact motifs, mappings, interactions, and return contracts needed by a consumer.

That gives the repo a clearer middle layer between raw ontology and full downstream runtime behavior.

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
It is a lead consumer of this repo, not the only intended consumer.

This repo should serve GNOMY by supplying:

- canonical framework records
- ontology annotations
- crosswalks
- motifs and construct mappings
- reusable techniques
- index program specs
- research-backed caveats

GNOMY, in turn, can send back normalized and privacy-minimizing research contributions rather than raw personal corpora.

See also:

- [system_boundaries.md](/Users/noveltokens/a_person_index/docs/system_boundaries.md)
- [phase_3_4_plan.md](/Users/noveltokens/a_person_index/docs/phase_3_4_plan.md)

## Service primitives

The near-term callable surface for downstream agents should center on a few durable primitives:

- find canonical framework records
- compare framework records
- trace an instrument or construct to house motifs
- fetch house interaction hypotheses for motifs, constructs, or frameworks
- fetch index program specs and their required techniques
- fetch a scoped program pack when the downstream task is already known
- fetch research contribution models and the result-atom schema for safe return traffic

These are intentionally smaller than full person-level synthesis. They make the repo useful to runtimes like GNOMY without moving person-level inference into this codebase.

## Relationship to ILENS

`ILENS` is an index program, not the ontology itself.

The ontology should stay broad enough to support ILENS, Human Model Card workflows, translation memos, paradox scans, and future downstream programs that are not yet designed.
