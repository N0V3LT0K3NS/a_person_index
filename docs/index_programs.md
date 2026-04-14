# Index Programs

This document explains the composable analysis layer inside A Person Index.

## Why this layer exists

The repo is not only a place to store frameworks.

Its real power is that it can:

- cohere many personhood frameworks into one comparative workspace
- translate across them without pretending they are identical
- run semantic, inferential, and structured comparative analysis across them
- give downstream systems reusable building blocks instead of one-off prompt fragments

That is why A Person Index needs a clear middle layer between raw framework data and full person-level runtimes.

## The composition ladder

Think of the system as legos at three scales:

1. Techniques
   Smallest reusable operations.
   Examples: `Paradox Scan`, `Cross-Framework Translation`, `Result Atom Decomposition`.

2. Index programs
   Named composed analyses or synthesis workflows built from techniques, and sometimes from smaller programs.
   Examples: `Paradox Finder`, `Translation Memo`, `ILENS`, `Human Model Card`,
   `Contextual Comparison Memo`, `Pairwise Relational Comparison`.

3. Program packs
   Scoped runtime bundles that hydrate an index program with frameworks, motifs, mappings, interaction hypotheses, and return contracts.

## What counts as a technique

Use a technique when the thing is:

- atomic
- reusable across many programs
- not very consumer-specific
- better described as an operation than as a product

Examples:

- `tech_paradox_scan`
- `tech_cross_framework_translation`
- `tech_result_atom_decomposition`

## What counts as an index program

Use an index program when the thing is:

- a named analysis workflow
- composed from multiple techniques
- useful as a standalone callable unit
- likely to be reused by downstream systems
- more opinionated than the ontology itself

Examples:

- `proto_paradox_finder`
- `proto_translation_memo`
- `proto_ilens`
- `proto_human_model_card`
- `proto_contextual_comparison`
- `proto_pairwise_relational_comparison`

Programs are stored in [protocols/registry.yaml](/Users/noveltokens/a_person_index/protocols/registry.yaml). The internal registry path still says `protocols`, but the public product concept is `index programs`.

## What counts as a program pack

Use a program pack when:

- the downstream task is already known
- scope should be stable and discoverable
- another agent should not have to assemble motifs and mappings manually
- the bundle is repeated enough to deserve a maintained entry

Program packs sit between raw program specs and ad hoc runtime assembly.

## Example ladder

One clean example is:

1. `tech_paradox_scan`
   Detect contradictions and layer mismatches.
2. `proto_paradox_finder`
   Package paradox scanning, contradiction preservation, and baseline-versus-adaptation framing into a reusable analysis pass.
3. `proto_ilens`
   Use `Paradox Finder` plus translation and result-atom decomposition inside a larger synthesis workflow.
4. `ppk_ilens_core_trait_motive_stack`
   Hydrate `ILENS` with a reviewed scope and return contract for repeated downstream use.

Another clean example is:

1. `tech_stable_vs_adaptive_split`
   Keep baseline versus context-driven behavior distinct.
2. `proto_contextual_comparison`
   Compare repeated or context-tagged slices without forcing every delta into a
   story of permanent personality change.
3. `ppk_contextual_core_trait_motive_stack`
   Hydrate that comparison frame with a reviewed Big Five / MBTI / Enneagram
   scope for repeated contextual work.

## Practical rule

When deciding where a new thing belongs, ask:

- Is this the smallest reusable operation?
  Make it a technique.
- Is this a named analysis workflow that composes operations?
  Make it an index program.
- Is this a reviewed, scoped, runtime-ready bundle?
  Make it a program pack.

## Relationship to GNOMY

`GNOMY` should consume these layers, not recreate them.

It can:

- call a program pack
- inspect the program spec
- apply the listed techniques
- use motifs and interactions supplied by the pack
- return only approved research shapes

It should not have to reinvent the comparative grammar of the repo every time it runs.

## Programs versus actualization protocols

An index program is still inside the comparative core of A Person Index.

An actualization protocol is a downstream workflow that uses an index program as
its semantic anchor while also using other tools for things like:

- file or corpus handling
- visualization
- document rendering
- graph generation
- context-aware delivery

This distinction matters.

A Person Index should define:

- what the comparison means
- what the named workflow is
- what boundaries and caveats must be preserved
- what artifact semantics are valid

Downstream agents or adjacent repos may define:

- how the artifact is rendered
- where it is stored
- how the user interacts with it

See:

- [actualization_protocols.md](/Users/noveltokens/a_person_index/docs/actualization_protocols.md)
- [expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md)
