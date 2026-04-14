# Assessment Workflow

Use this workflow when a user pastes multiple assessment results and asks A Person Index to "use what it can."

This is the default workflow for a single mixed stack. It is not the whole story for contextual, relational, or multi-subject comparison.

## Goal

Turn raw assessment names and outputs into:

1. matched framework records
2. clear unmatched items
3. relevant index programs or curated packs
4. motif and interaction context
5. bounded synthesis, without pretending the repo itself is the runtime

## Recommended sequence

### 1. Match framework names first

Prefer:

- `find_framework_records(refs=[...])` with one short label per framework
- `find_framework_records(text=...)` only for short fuzzy recovery passes

Good refs:

- `MBTI`
- `Big Five`
- `Human Design`
- `Natal Astrology`
- `StrengthsFinder`
- `Love Language`

Do not start with a full raw assessment dump as one `text` query unless you are doing best-effort recovery.

### 2. Surface unmatched items early

If a framework is not indexed, say so plainly.

Current examples that may be missing from a user’s stack:

- `True Colors`
- `R-Drive`

### 3. Check curated packs before building by hand

Use:

- `list_protocol_packs(featured=true)`
- `fetch_curated_protocol_pack(...)`

Only use `fetch_protocol_pack(...)` when:

- you know the exact program name or ID
- there is no reviewed curated pack for the task

### 4. Use motifs only after framework matching is stable

Good next calls:

- `trace_to_motifs`
- `list_related_motifs`
- `list_interaction_hypotheses`

Bad pattern:

- searching interaction hypotheses with raw type labels like `ENFP 4w3 Manifesting Generator`

Better pattern:

- match frameworks first
- then trace matched frameworks or constructs into motifs

### 5. Preserve the layer boundaries in the answer

State clearly:

- what came from canonical framework records
- what came from house motifs or interaction hypotheses
- what is your downstream synthesis or judgment

### 6. Be explicit about symbolic systems

For `Human Design` and `Natal Astrology`:

- keep them in the synthesis if the user uses them
- do not describe them as psychometric baselines
- treat them as symbolic meaning layers unless a downstream runtime says otherwise

## Good answer shape

1. matched frameworks
2. unmatched frameworks
3. relevant curated pack or program
4. motif summary
5. interaction hypotheses
6. limits and caveats

For most end users, the answer should usually describe the lived pattern more than the internal variable names. The technical scaffold should remain available, not dominant.

## Anti-patterns

- using `find_framework_records(text=<entire report>)` as the only match step
- treating `[]` from one fuzzy search as proof the framework does not exist
- assuming `fetch_protocol_spec` means the protocol has been run
- hiding missing coverage
- flattening symbolic systems into trait claims

See also:

- [advanced_modes.md](/Users/noveltokens/a_person_index/docs/advanced_modes.md)
- [comparison_shapes.md](/Users/noveltokens/a_person_index/docs/comparison_shapes.md)
- [expression_and_artifacts.md](/Users/noveltokens/a_person_index/docs/expression_and_artifacts.md)
- [multi_subject_comparison.md](/Users/noveltokens/a_person_index/docs/multi_subject_comparison.md)
