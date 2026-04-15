# Advanced Modes

A Person Index has a safe default workflow, but real use quickly branches into
different modes.

This document names those modes so they are not unconsciously collapsed into one
"analysis."

## Why this matters

The same substrate can be used for:

- orientation and sync
- bounded single-subject mixed-stack work
- architecture analysis
- run planning
- artifact generation
- contextual comparison
- multi-subject comparison
- trace review of another agent's run

Those are related, but they are not the same task.

## Mode 1: orientation and sync

Use this when the main need is to know:

- what the repo currently contains
- what tools and prompts are available
- what changed since the last run
- what the safe arrival path is

Typical surfaces:

- `orient_agent`
- `registry://quickstart`
- `registry://current-state`
- featured program packs

## Mode 2: bounded single-subject mixed-stack analysis

Use this when a person provides multiple assessment results and wants A Person
Index to use what it can.

This is the default workflow described in
[assessment_workflow.md](/Users/noveltokens/a_person_index/docs/assessment_workflow.md).

## Mode 3: architecture and capability analysis

Use this when the question is not only:

- what does the system say about this person?

but also:

- what can the system do?
- where are the seams?
- what is indexed?
- what is missing?
- what kinds of comparative operations are latent in the current layers?

This is an advanced mode. It is especially useful for builders, contributors,
and technically curious users.

## Mode 4: run planning

Use this when the user does not want execution yet. They want to decide:

- what kind of pass this should be
- what program or pack fits
- what external tools, if any, should help
- what should remain inside A Person Index
- what artifact or output shape is desired

## Mode 5: artifact-oriented actualization

Use this when the output is not only a conversation turn, but a named artifact
or deliverable.

Examples:

- a human-model-card-style document
- a comparative memo
- a markdown handoff file
- a graph or matrix
- a machine-readable result bundle

See [expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md).

## Mode 6: contextual or multi-subject comparison

Use this when the task involves:

- one person across time
- one person across roles or contexts
- two or more people in relation
- multiple people compared side by side

Start with [comparison_shapes.md](/Users/noveltokens/a_person_index/docs/comparison_shapes.md)
before choosing artifacts, protocols, or workflow recipes.

See [multi_subject_comparison.md](/Users/noveltokens/a_person_index/docs/multi_subject_comparison.md).

## Mode 7: trace review

Use this when the thing being reviewed is another agent's A Person Index run.

This is mainly an advanced or internal mode. It can help identify:

- where the host stayed grounded
- where it drifted
- what layers were touched
- what support surface was missing

## "A Person Index only" has two meanings

When a user asks for "A Person Index only," the constraint can mean two
different things.

First, source and surface bounded:

- use only A Person Index tools, resources, prompts, and program logic for the
  comparative work

Second, cognition bounded:

- even if other systems or memories are available, keep the active reasoning and
  recap inside the current A Person Index run

The second boundary is usually harder.

## Practical guidance

If the mode is unclear, name the mode before proceeding.

That often prevents:

- tool sprawl
- cross-system bleed
- accidental overreach
- overly technical answers to a phenomenological question
