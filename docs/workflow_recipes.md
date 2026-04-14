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

## Relationship to other layers

Use the layers in this order:

1. analysis mode says what kind of run this is
2. comparison shape makes the contextual or pairwise scaffold explicit when relevant
3. capabilities say what the host can actually do
4. recommendation says what artifact, expression, and protocol fit
5. workflow recipe says how to execute that path here
6. host tools realize the final output

## Boundary rule

Workflow recipes live in this repo because they preserve semantic discipline.

They still do not make this repo the owner of every renderer, UI, or product
runtime. They define the recipe, not every possible implementation.
