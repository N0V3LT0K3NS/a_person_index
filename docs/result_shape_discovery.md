# Result Shape Discovery

Result atom normalization is much easier when a runtime can first ask a simpler
question:

What result slots does this framework actually expose?

This surface answers that question.

It gives a framework's construct-level result shape in a way that is useful for
downstream runtimes and agent hosts:

- construct IDs
- construct names
- scoring types
- motif trace availability
- starter atom entry templates

## Why this exists

The result atom schema tells a consumer what a normalized atom must look like.

The normalization helper turns construct-level output into that shape.

But a consumer still needs a clean way to discover:

- which constructs belong to a framework
- what kind of scoring language each construct uses
- which starter output type is the best default hint

Without that, runtimes still have to inspect raw framework files or improvise
construct references.

## What it returns

For a named framework, the result-shape surface returns:

- framework identity
- construct count
- construct-level scoring types
- normalization hints
- mapped motif IDs where they exist
- starter result-atom entry templates

## What it does not do

This surface does not execute the normalization step itself.

It is the discovery layer that should come before normalization when the
consumer still needs to inspect the construct map for a framework.

## Typical sequence

1. fetch the framework result shape
2. choose the constructs you actually have outputs for
3. fill the starter entry templates with real values
4. pass those entries to the result atom normalization helper

## CLI

```bash
python3 scripts/query_registry.py result-shape "Big Five"
```

## MCP

Use `fetch_framework_result_shape` when a runtime needs the construct IDs,
scoring types, motif trace availability, and starter atom slots for a framework
before it normalizes anything.

Example call:

```json
{
  "framework": "big-five"
}
```

The required parameter is `framework` (framework slug, short name, or alias).
The tool accepts any value that resolves via `find_framework_records`.
