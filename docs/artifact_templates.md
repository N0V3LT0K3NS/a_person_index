# Artifact Templates

Artifact templates are the step after artifact realization.

Artifact realization tells the host:

- which workflow recipe fits
- which realization form fits this host
- which blocks the finished artifact must contain

Artifact templates take that one step further and return a starter markdown or
JSON structure the host can actually fill.

## Why this layer exists

Before this surface, a host could see the required blocks and still have to
reconstruct the starter artifact by hand.

That was enough for a careful operator, but it still left too much room for
unnecessary variation in the first draft.

This layer exists so A Person Index can say:

- here is the correct scaffold
- here is the likely filename shape
- here is the starter markdown or JSON structure

without becoming the renderer or the final author of the artifact.

## Core rule

Templates are starter structures, not finished outputs.

They should preserve:

- workflow recipe identity
- selected realization form
- required blocks
- required evidence partitions

They should not pretend that placeholders are grounded findings.

## How to use this layer

The intended sequence is:

1. recommend the path
2. prepare artifact realization
3. prepare artifact template
4. fill the template with grounded comparative content
5. only then polish or export the finished artifact

Examples:

```bash
python3 scripts/query_registry.py artifact-template "Human Model Card Mixed" \
  --host "Codex Desktop"

python3 scripts/query_registry.py artifact-template "Structured Result Bundle Technical" \
  --host "Codex Desktop" \
  --format json
```

## What kinds of templates exist

The current surface produces two broad template kinds:

- markdown document templates for cards, memos, sheets, and similar
- JSON object templates for result bundles and machine-readable outputs

The template is derived from the workflow recipe's existing realization blocks.
It does not invent a second artifact grammar.

## Important caution

The template is intentionally incomplete.

It should help the host start cleanly, but the host still has to supply:

- grounded findings
- declared missingness
- provenance-aware judgment
- audience-appropriate expression

If a host fills the template with content that outruns the comparison, that is
still a host error, not a property of the template layer.
