# Capability Model

A Person Index should not hard-code itself to one host.

It should reason about what a host can do in abstract terms, then choose the
right comparative and actualization path from there.

## Why this layer exists

Different agents expose different tool names and integrations.

What matters is not the brand name of the tool. What matters is whether the
host can:

- read source material
- call adjacent MCPs or APIs
- run code
- render structured text
- render tables
- render diagrams
- emit JSON
- persist artifacts

The capability model gives the meta-skill a stable vocabulary for that.

Host profiles sit one layer above this.

They expand a known environment such as Codex Desktop or Claude Code into a
seeded capability set, but the capability records remain the real planning
primitive.

## Core rule

Capabilities are downstream execution affordances.

They do not decide comparative meaning.

A Person Index still decides:

- what the comparison means
- what a valid artifact class is
- what actualization protocol fits
- what must stay visible in the final output

The capability layer only helps answer:

- what is possible here
- what is the smallest good realization path
- what should stay conversational versus become an artifact

## Current capability kinds

The current registry names a small set of capability kinds:

- input
- execution
- rendering
- visualization
- network
- persistence
- packaging

These are intentionally broad. They are meant to survive host churn better than
tool-specific naming.

## How to use this layer

The recommended order is:

1. inspect a known host profile if one already fits the environment
2. inspect available capabilities abstractly
3. classify the run
4. use `recommend_next_path` if you need the smallest disciplined recommendation
5. choose the analysis mode
6. choose the artifact class or actualization protocol if needed
7. choose the expression profile that fits the audience
8. choose the workflow recipe that operationalizes the path
9. use the host's actual tools only after the semantic path is clear

## MCP

Use `recommend_next_path` when capabilities are already declared and the next
disciplined step is the real question.

Example call:

```json
{
  "mode": "mode_bounded_single_subject",
  "hosts": ["host_claude_code"],
  "capabilities": ["cap_markdown_write", "cap_structured_text_render"]
}
```

All parameters are optional. If nothing is provided, the tool defaults to
`mode_run_planning` and returns a conservative recommendation.

Optional parameters:

- `mode` (string) — analysis mode ID or name (note: `mode`, not `run_mode`)
- `comparison_shape` (string) — comparison shape ID or name when contextual or
  pairwise work is already declared
- `hosts` (array of strings) — declared host profile IDs or names; expands
  into a conservative capability set
- `capabilities` (array of strings) — declared capability IDs or names
- `artifact` (string) — bias the recommendation toward a specific artifact
  class ID or name
- `text` (string) — free-text hint used to infer mode and comparison shape
  when none is declared explicitly

## Important caution

A stronger host environment does not authorize a stronger claim.

If the host can render a graph, spreadsheet, or PDF, that only changes the
delivery options.

It does not change:

- evidence quality
- framework coverage
- missingness
- the limits of the comparison

That boundary is the point of this layer.
