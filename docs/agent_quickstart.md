# Agent Quickstart

This is the shortest safe arrival path for A Person Index.

## What this is

A Person Index is a comparative substrate for personhood frameworks.

Keep these layers separate:

1. canonical framework records
2. house synthesis motifs, mappings, and interaction hypotheses
3. techniques and index programs
4. runtime packs
5. research contribution and promotion policy

It can also act as the comparative core inside richer downstream workflows, but that does not change the layer boundaries above.

## First moves

If you are using MCP, prefer this order:

1. call `orient_agent`
2. read `registry://quickstart`
3. read `registry://current-state`
4. list featured program packs

If you need the repo docs, start with:

1. [README.md](/Users/noveltokens/a_person_index/README.md)
2. [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
3. [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
4. [docs/assessment_workflow.md](/Users/noveltokens/a_person_index/docs/assessment_workflow.md)
5. [docs/ilens_walkthrough.md](/Users/noveltokens/a_person_index/docs/ilens_walkthrough.md)

## Best-practice tool order

For user-supplied assessment results:

1. resolve framework matches first with `find_framework_records`
2. explicitly note what is unmatched or not yet indexed
3. inspect `list_protocol_packs(featured=true)` before improvising
4. prefer `fetch_protocol_pack_summary` before `fetch_protocol_pack`
5. prefer `fetch_curated_protocol_pack` when a reviewed pack fits
6. use `trace_to_motifs` and `list_interaction_hypotheses` after the framework layer is stable
7. use `fetch_protocol_spec` to understand a program, not to claim it already executed

## Important usage rules

- Prefer `refs` for distinct labels such as `MBTI`, `Big Five`, `Human Design`, or `Love Language`.
- Use `text` for short fuzzy searches, not as a blind dump of an entire report unless you want best-effort matching.
- If `fetch_protocol_pack` is needed, use a real program name or ID such as `ILENS`, `Human Model Card`, `Translation Memo`, or `Paradox Finder`.
- If a framework is symbolic, say so explicitly instead of flattening it into empirical language.
- If a framework is missing, say it is unindexed rather than inventing coverage.

## Expression rule

For most end users, keep the technical scaffolding implicit unless they ask for it.

Explain the phenomenon before the variable names.

Reserve fully technical, ontology-heavy language for contributor, debugging, or meta-analysis contexts.

See:

- [expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md)
- [advanced_modes.md](/Users/noveltokens/a_person_index/docs/advanced_modes.md)

## Common mistakes

- treating house motifs as source truth
- using one giant search blob and assuming `[]` means the framework is absent
- calling `fetch_protocol_pack` with a vague ref like `novel`
- claiming the repo itself performed person-level inference
- failing to mark symbolic systems as symbolic

## If the task becomes more than a basic pass

If the user is really asking for:

- run planning
- architecture analysis
- artifact generation
- contextual comparison
- or multi-subject comparison

do not force that back into a plain intake workflow.

If the host capabilities are already known and you need the next disciplined
step rather than a full execution, use `recommend_next_path` before you start
improvising.

If the work is contextual or pairwise and the comparison shape is already
chosen, run comparison preflight before you treat the path as execution-ready.

If the workflow recipe is already chosen and the next question is what the
finished artifact should actually contain, use artifact realization before you
start rendering.

Use the deeper docs:

- [advanced_modes.md](/Users/noveltokens/a_person_index/docs/advanced_modes.md)
- [comparison_shapes.md](/Users/noveltokens/a_person_index/docs/comparison_shapes.md)
- [comparison_preflight.md](/Users/noveltokens/a_person_index/docs/comparison_preflight.md)
- [capability_model.md](/Users/noveltokens/a_person_index/docs/capability_model.md)
- [artifact_realization.md](/Users/noveltokens/a_person_index/docs/artifact_realization.md)
- [expression_model.md](/Users/noveltokens/a_person_index/docs/expression_model.md)
- [actualization_protocols.md](/Users/noveltokens/a_person_index/docs/actualization_protocols.md)
- [workflow_recipes.md](/Users/noveltokens/a_person_index/docs/workflow_recipes.md)
- [expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md)
- [multi_subject_comparison.md](/Users/noveltokens/a_person_index/docs/multi_subject_comparison.md)
