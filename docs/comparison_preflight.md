# Comparison Preflight

Comparison preflight is the layer that checks whether a contextual or pairwise
run is actually declared well enough to proceed.

It lives after a comparison shape is chosen and before the host commits to an
artifact, workflow recipe, or rendering path.

## What it does

Comparison preflight validates:

- which declaration fields this comparison shape requires
- which declarations have already been provided
- which required fields are still missing
- which provided values are invalid for the shape
- whether the run is ready for downstream path recommendation

If the run is ready, preflight can also surface the recommended artifact,
expression profile, workflow recipe, and actualization protocol that fit the
declared shape and current host capabilities.

## Why this layer matters

Contextual and pairwise work often fails early, not because the later artifact
or rendering path was weak, but because the comparison itself was underspecified.

This layer prevents the host from acting as though a comparison is clear when
important declarations are still missing.

## Typical order

For contextual and pairwise work, the clean order is:

1. identify the run mode
2. identify the comparison shape
3. run comparison preflight with explicit declarations
4. inspect or declare host capabilities
5. use `recommend_next_path` when you need the smallest disciplined next move
6. choose the workflow recipe and actualization path
7. execute and render only after the comparison scaffold is stable

## Example declarations

For `Contextual Time Slices`, useful declarations include:

- `slice_labels`
- `comparison_question`
- `framework_scope`
- `comparison_limits`

For `Pairwise Relational Question`, useful declarations include:

- `left_stack_label`
- `right_stack_label`
- `relationship_context`
- `comparison_question`
- `scope_limits`

## Boundary rule

Comparison preflight does not produce compatibility truth, developmental truth,
or relational truth.

It only verifies that the comparison scaffold has been declared clearly enough
for later work to stay disciplined.
