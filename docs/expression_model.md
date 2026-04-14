# Expression Model

A Person Index should not force every valid comparative result to sound the same.

The analysis core may remain constant while the expression surface changes
depending on audience, task, artifact, and level of desired scaffolding.

This document defines expression as a structured layer rather than a purely
stylistic afterthought.

## What expression controls

Expression determines:

- how much internal scaffolding becomes visible
- how phenomenon-first or structure-first the voice becomes
- how much provenance remains explicit in the surface text
- how a downstream artifact feels to its intended audience

It does not change the underlying comparative meaning.

## Profiles

The current structured profiles are:

- `expr_tacit`
- `expr_explanatory`
- `expr_technical`
- `expr_mixed`

These align with the simpler expression modes already used by artifact classes:

- `tacit`
- `explanatory`
- `technical`
- `mixed`

## Recommended use

For most end users, prefer tacit or explanatory rendering.

Use technical rendering when the audience is a contributor, maintainer, agent,
or debugging context that genuinely needs direct access to the scaffolding.

Use mixed rendering only when the artifact truly serves more than one audience
at once.

## Relationship to artifacts

Artifact classes may declare a default expression mode.

That default is a starting point, not a prison. The host may still choose a
different expression profile when the audience clearly calls for it, but the
change should be deliberate.

## Relationship to actualization

Expression belongs between comparative understanding and final realization.

The practical order is:

1. classify the run
2. inspect capabilities
3. choose or recommend the next path
4. choose the artifact class if needed
5. choose the expression profile
6. realize the result using host tools

## Boundary rule

Expression profiles define rendering stance and visibility rules.

They do not redefine canonical truth, ontology annotations, or house synthesis.
