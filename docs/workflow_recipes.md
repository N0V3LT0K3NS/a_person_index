# Workflow Recipes

Workflow recipes are the operational layer that sits beneath recommendation and
above host-specific realization.

They answer a practical question:

"Given this run mode, artifact, expression profile, actualization protocol, and
current capabilities, what is the smallest disciplined sequence I should follow
here?"

## What a workflow recipe is

A workflow recipe is not a new source of meaning.

It does not redefine frameworks, motifs, interactions, or named programs.

It is a reusable execution pattern that binds together:

- a run mode
- an artifact class
- an expression profile
- an actualization protocol
- a minimum capability set

## What it is for

Workflow recipes help hosts move from:

- planning
- recommendation
- abstract actualization guidance

into:

- a concrete next sequence
- a bounded artifact path
- a repeatable operator move

without inventing that path ad hoc every time.

Workflow recipes now also carry realization blocks, so the host can move from
"what is the path?" to "what should the finished artifact actually contain?"
without inventing that structure from memory.

Current recipes now cover explanatory memos, context matrices, pairwise sheets,
technical handoffs, human model cards, and structured result bundles.

## Relationship to other layers

Use the layers in this order:

1. analysis mode says what kind of run this is
2. comparison shape makes the contextual or pairwise scaffold explicit when relevant
3. comparison preflight checks that the declared scaffold is actually ready
4. capabilities say what the host can actually do
5. recommendation says what artifact, expression, and protocol fit
6. workflow recipe says how to execute that path here
7. artifact realization turns the chosen recipe into a concrete scaffold
8. host tools realize the final output

## Boundary rule

Workflow recipes live in this repo because they preserve semantic discipline.

They still do not make this repo the owner of every renderer, UI, or product
runtime. They define the recipe, not every possible implementation.
