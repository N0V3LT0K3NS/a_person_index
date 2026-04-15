# Result Atom Normalization

A Person Index already defines the result atom schema and the allowed research
contribution models.

This surface adds the missing helper between those two facts.

It exists for the case where a downstream runtime already has
construct-level outputs and needs a schema-shaped bundle without improvising:

- framework and construct IDs
- output type and output value
- source-quality and timestamp defaults
- optional motif trace from the current mapping layer

## What this helper is for

Use result atom normalization when:

- the framework is already known
- the output is already decomposed to construct level
- the runtime needs a clean bundle for downstream synthesis or research return

Typical examples:

- Big Five construct scores already split into Openness, Extraversion, and Neuroticism
- MBTI preference-level outputs already split into E/I, S/N, T/F, and J/P
- attachment or love-language construct selections already resolved to the relevant construct IDs

## What this helper is not for

This helper does not perform full person-level inference.

It also does not try to decompose every whole-test label automatically.

So:

- `Openness: 0.74` is in scope
- `ENFP` is only in scope if the caller already decomposed it into construct-level signals
- a full person synthesis remains downstream in `GNOMY` or another runtime

That boundary matters because this repo should support the transport contract
without quietly becoming the inference runtime.

## Inputs

The normalization helper expects:

- a known framework reference
- a JSON list of entries

Each entry should include:

- `construct`
- `output_type`
- `output_value`

Each entry may also include:

- `confidence`
- `source_quality`
- `timestamp`
- `notes`

Bundle-level defaults can be provided for:

- source quality
- timestamp
- bundle label

An optional comparison shape can also be attached to the bundle metadata when
the bundle is part of a contextual or pairwise run.

## Outputs

The helper returns:

- readiness state
- invalid-entry diagnostics when the input is underspecified or malformed
- the preferred contribution model for return traffic
- the result atom schema
- normalization records showing how each input entry resolved
- a schema-shaped bundle of result atoms

When motif trace is enabled, the helper also attaches current mapped motif IDs
where the construct-to-motif layer supports them.

## CLI

```bash
python3 scripts/query_registry.py result-atom-bundle \
  --framework "Big Five" \
  --entries-json '[{"construct":"Openness to Experience","output_type":"continuous_score","output_value":"0.74","source_quality":"self_reported"}]'
```

## MCP

Use `normalize_result_atom_bundle` when the host already has construct-level
outputs and needs a clean, schema-shaped bundle with provenance defaults and
optional motif trace.

## Boundary caution

Result atom normalization is a contract helper.

It is not canonical truth.
It is not person-level synthesis.
It is not a reason to erase provenance or ambiguity.

Keep source framework identity attached, keep house motif trace optional, and
keep runtime-level interpretation downstream.
