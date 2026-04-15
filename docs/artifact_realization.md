# Artifact Realization

Artifact realization is the layer that turns a chosen workflow recipe into a
concrete scaffold for the finished output.

If the host needs a starter markdown or JSON structure rather than only the
block list, the next surface is [artifact_templates.md](/Users/noveltokens/a_person_index/docs/artifact_templates.md).

It does not render the artifact by itself.

It tells the host what blocks the artifact should contain, what realization form
fits the declared capabilities, and what must remain visible while the host
uses its own tools to materialize the result.

## Why this layer exists

Recommendation tells the host what path fits.

Workflow recipes tell the host what sequence to follow.

Artifact realization is the next layer down. It tells the host what the finished
artifact should actually be built from.

Without that layer, the system still stops too early and leaves the host to
invent the artifact structure ad hoc.

This includes machine-readable outputs such as structured result bundles, not
only markdown cards, memos, or tables.

## What it includes

Artifact realization can make explicit:

- the workflow recipe being realized
- the artifact class, expression profile, and actualization protocol in play
- the preferred realization form in the current host
- the realization blocks that should appear in the artifact
- the evidence partitions that must remain visible
- the next steps before polishing or export

## Typical order

For artifact work, the clean order is:

1. classify the run
2. choose the comparison shape when contextual or pairwise work is involved
3. run comparison preflight when needed
4. declare host capabilities
5. use `recommend_next_path`
6. choose the workflow recipe
7. use artifact realization to get the concrete scaffold
8. use artifact templates if the host needs a first-draft structure to fill
9. render the finished output with host tools

## Boundary rule

Artifact realization does not make A Person Index a renderer.

It defines the semantic scaffold of the artifact so the host can realize it
without inventing new meaning or losing provenance.

The template layer sits one step after this. It gives the host a starter
markdown or JSON structure derived from the same workflow recipe and selected
realization form.
