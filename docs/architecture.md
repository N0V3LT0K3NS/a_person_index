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

These five are the core layers owned directly by the repo.

## Adjacent downstream layers

Real use already reaches beyond the five core layers into three adjacent concerns:

1. Actualization and orchestration
   Using A Person Index as the comparative core while another host or repo uses additional tools to enrich, structure, visualize, or deliver the work.

2. Expression and artifact rendering
   Turning the same analysis core into different conversational voices or finalized artifacts for different audiences.

3. Contextual and multi-subject comparison
   Applying the comparative grammar across time, role, relationship, or multiple people without confusing that runtime work with canonical records.

4. Capability-aware orchestration
   Using an abstract capability model so hosts can inspect what they can do here
   before they choose a downstream actualization path.

These adjacent layers are important, but they should not silently collapse back into the ontology or canonical corpus.

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

## Architectural reading

The simplest accurate way to think about the whole system is:

- A Person Index is the comparative core
- downstream protocols actualize that core
- capability-aware planning determines what downstream path is actually available here
- downstream expression layers render it for specific audiences or artifacts
- contextual and multi-subject workflows apply the same grammar across more than one slice of personhood evidence

That makes the repo more than a registry, but it does not make the repo itself the whole runtime.

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

Companion docs:

- [advanced_modes.md](/Users/noveltokens/a_person_index/docs/advanced_modes.md)
- [actualization_protocols.md](/Users/noveltokens/a_person_index/docs/actualization_protocols.md)
- [expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md)
- [multi_subject_comparison.md](/Users/noveltokens/a_person_index/docs/multi_subject_comparison.md)

## Relationship to ILENS

`ILENS` is an index program, not the ontology itself.

The ontology should stay broad enough to support ILENS, Human Model Card workflows, translation memos, paradox scans, and future downstream programs that are not yet designed.
