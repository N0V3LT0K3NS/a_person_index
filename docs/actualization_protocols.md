# Actualization Protocols

A Person Index is often most powerful when it is not the only tool involved.

That does not mean it should lose its boundaries.

This document explains how A Person Index can serve as the comparative core
inside richer downstream workflows.

## Core idea

Use A Person Index for:

- comparative meaning
- framework matching
- motifs, crosswalks, and interactions
- named methods and packs
- research-safe return rules

Use other tools only for adjacent work such as:

- file handling
- corpus parsing
- visualization
- rendering
- storage
- delivery

The important thing is not tool purity. The important thing is semantic
discipline.

See [capability_model.md](/Users/noveltokens/a_person_index/docs/capability_model.md)
for the abstract capability layer that helps hosts decide what realization path
is actually available.

## Why "actualization" matters

Sometimes the user does not merely want a bounded analysis.

They want that analysis to become something more concrete:

- a plan
- a handoff
- a graph
- a document
- a relational comparison
- a reusable downstream object

That step is not only formatting. It is where comparative understanding becomes
usable in context.

Current examples include:

- `Single-Subject Comparative Memo`
- `Human Model Card Realization`
- `Context Matrix Render`
- `Pairwise Relational Sheet`

The contextual and pairwise actualization paths now anchor on dedicated
comparison programs rather than treating comparison as an unstructured
extension of a single-subject pass.

## Suggested protocol shape

One strong general pattern is:

1. declare the run shape
2. if the work is contextual or pairwise, choose a comparison shape
3. run comparison preflight so the comparison scaffold is explicit
4. match and scope the framework layer
5. choose the right program or pack
6. if the path is still unclear, use `recommend_next_path` with declared capabilities
7. run the A Person Index comparative work
8. choose the workflow recipe that fits the recommended artifact, expression, and capability shape
9. use artifact realization to get the concrete scaffold of the chosen artifact
10. decide whether the output should remain conversational or become an artifact
11. if an artifact is needed, use external tools only after the comparative core is stable
12. preserve provenance and layer boundaries in the final output

## Provenance rule

The final result should preserve the distinction between:

- canonical framework content
- house synthesis
- named program behavior
- downstream interpretation
- external rendering or realization work

If those collapse, the output may feel smoother, but it becomes less trustworthy.

## Tool-aware orchestration

Hosts often have additional tools available.

That can be useful.

For example:

- a filesystem or parsing tool can turn messy source material into structured input
- a graphing or spreadsheet tool can render comparative outputs
- a document tool can realize a finalized artifact

But these tools should be downstream helpers, not alternate semantic authorities.

## What belongs in this repo

This repo should define:

- actualization protocol grammar
- allowed artifact semantics
- boundaries and caveats
- the comparative core that the downstream work relies on

This repo should not try to implement every rendering stack, storage backend, or
consumer product.

## Relationship to index programs

An index program is a named comparative method inside A Person Index.

An actualization protocol is the larger downstream choreography in which that
program may sit.

That means:

- a program can be canonical here
- a realization of that program into a PDF, graph, app object, or markdown handoff may live elsewhere

## Relationship to the MCP

The MCP server can expose the comparative core cleanly.

The host agent can then combine that with other tools.

That is often the right design.

The goal is not to move the whole runtime into MCP. The goal is to keep the
comparative center of gravity intact.
