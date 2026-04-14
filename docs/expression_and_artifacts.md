# Expression and Artifacts

Expression is not only presentation polish.

It changes how the same comparative understanding becomes legible to a reader,
user, collaborator, or downstream system.

This document separates:

- analysis core
- conversational expression
- finalized artifact rendering

## Analysis core versus expression

The analysis core is where A Person Index does its comparative work:

- framework matching
- crosswalks
- motifs
- interaction hypotheses
- programs and packs
- research-safe return structure

Expression decides how much of that scaffolding becomes visible.

The default should not always sound like a variable dump.

For the structured profile layer that now sits underneath these choices, see
[expression_model.md](/Users/noveltokens/a_person_index/docs/expression_model.md).

## Default conversational posture

For most end users, the strongest default is:

- understand the technical structure fully
- speak mostly in terms of the lived pattern or phenomenon
- keep internal ontology labels and pack names available, but not dominant

This usually reads more like:

- "there is a recurring tension between fast ignition and sustained structure"

than:

- "your high X plus low Y implies variable Z"

The technical structure is still there. It is just not the whole voice.

## Technical depth modes

Different contexts may need different explicitness.

Three simple tiers are useful:

1. Phenomenological or tacit
   Good for ordinary user-facing explanation.

2. Explanatory
   Good when the user wants to know how the reading was built without drowning in ontology.

3. Technical or contributor-facing
   Good for debugging, meta-analysis, research authoring, or building on the system.

The right question is not "should this be technical or not?"

The right question is "how much of the scaffolding should this audience see?"

## Artifact families

Some outputs should remain conversational.

Others should become artifacts.

Examples of artifact families include:

- human-model-card-style documents
- comparative memos
- context- or role-based comparison sheets
- relational comparison matrices
- graphs or maps
- markdown handoff files such as `agent.md`, `soul.md`, or other downstream-facing files
- machine-readable result bundles

These examples do not define the system exhaustively. They are seed classes.

## Artifact grammar

A useful artifact usually has to answer these questions:

1. What is the scope?
   One person, one run, one relationship, one comparison, one timespan?

2. What is the audience?
   End user, collaborator, agent, maintainer, researcher?

3. What voice is appropriate?
   Phenomenological, explanatory, technical, or mixed?

4. What evidence partition must remain visible?
   Canonical, house synthesis, program behavior, downstream judgment?

5. What realization form is needed?
   Conversation, markdown, graph, card, bundle, PDF, table?

6. What external tools, if any, are needed to realize it well?

That is the beginning of an artifact grammar.

Workflow recipes and artifact realization now provide the first structured path
from artifact class to concrete scaffold. They still do not define every final
renderer, but they do define what blocks a host should preserve when building
the artifact.

## Contribution and extension

Artifact classes should be extendable.

Contributors do not need to be limited to a fixed short list if they preserve:

- the comparative core
- the audience and voice logic
- the evidence partitions
- the repo boundary rules

## Boundary rule

This repo can define:

- artifact semantics
- artifact classes
- output grammar

It does not need to implement every renderer, UI, or storage system that might
realize those artifacts.
