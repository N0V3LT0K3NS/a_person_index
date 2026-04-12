# Annotation Guide

## Purpose

Annotations are the house ontology layer. They are not source claims and they are not free-form notes.

## Status values

- `explicit`: directly stated by source material
- `implicit`: not directly stated, but clearly implied by structure or output logic
- `inferred`: house judgment based on review or comparison
- `comparative`: meaningful primarily relative to other systems
- `contested`: disputed or unresolved

## Required fields

Each annotation should include:

- `ontology_dimension`
- `ontology_values`
- `annotation_status`
- `confidence`
- `rationale`
- `evidence_links`

## Minimum required instrument dimensions

Every instrument must have instrument-level annotations for:

- `instrument_family`
- `primary_measurement_target`
- `representational_form`
- `temporal_stance`
- `person_ontology`
- `administration_mode`
- `scoring_logic`
- `epistemic_basis`
- `interpretive_burden`
- `granularity`
- `context_sensitivity`
- `change_model`
- `distortion_risk`
- `deployment_context`
- `utility_profile`
- `identity_adhesion_risk`
- `worldview_load`
- `synthesis_value`

## Authoring guidance

- Prefer source-backed evidence links when available.
- Use `comparative` when the value only makes sense in a cross-system frame.
- Use `contested` when multiple reasonable readings remain active.
- Do not use annotations to restate claims that belong in `claims.yaml`.
- Do not use inferences to hide required annotations.
- Treat protocol-specific judgments, such as ILENS fit, as downstream protocol concerns unless they belong in the generalized `synthesis_value` dimension.
