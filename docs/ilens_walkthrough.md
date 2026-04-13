# ILENS Walkthrough

This is a worked example of how an agent should use A Person Index for an ILENS-style pass on mixed assessment results.

## Goal

Take a stack like:

- `Big Five`
- `MBTI`
- `Enneagram`
- optional symbolic layers such as `Human Design` or `Natal Astrology`

and turn it into:

1. matched framework records
2. a reviewed or generated ILENS pack
3. motif and interaction context
4. bounded synthesis with explicit caveats

## Recommended MCP sequence

### 1. Orient

Use:

- `orient_agent`

or read:

- `registry://quickstart`
- `registry://assessment-workflow`

### 2. Match frameworks

Prefer exact refs first:

```json
{
  "refs": ["Big Five", "MBTI", "Enneagram", "Human Design", "Natal Astrology"]
}
```

Tool:

- `find_framework_records`

Output expectation:

- matched framework records
- explicit notice of anything missing or unindexed

### 3. Check reviewed pack coverage

Use:

- `list_protocol_packs` with `featured=true`

Then, if a reviewed pack fits:

- `fetch_curated_protocol_pack` with `ppk_ilens_core_trait_motive_stack`

If you need a scoped dynamic pack instead:

- `fetch_protocol_pack_summary` with `ref="ILENS"` and the relevant framework list
- only then `fetch_protocol_pack`

### 4. Compare core empirical and typology layers

Use:

- `compare_frameworks(Big Five, MBTI)`
- `compare_frameworks(Big Five, Enneagram)`
- `compare_frameworks(MBTI, Enneagram)`

Read:

- shared annotation values
- crosswalks
- suggested next queries

### 5. Trace motifs

Use:

- `trace_to_motifs(Big Five)`
- `trace_to_motifs(MBTI)`
- `trace_to_motifs(Enneagram)`

Use symbolic frameworks only as symbolic layers unless the runtime has a stronger reason to weight them otherwise.

### 6. Check interaction hypotheses

Use:

- `list_interaction_hypotheses(related_to=<matched framework>)`

Important:

- if the registry does not have a hypothesis for a seam, say so
- do not pretend absence means irrelevance

### 7. Synthesize

At this point, the downstream runtime performs the person-level work.

The repo provides:

- canonical records
- motifs
- interaction hypotheses
- techniques
- ILENS pack structure

The runtime provides:

- actual result interpretation
- person-level judgment
- final artifact

## What not to do

- do not begin with one giant `text` blob if you can extract framework labels first
- do not call `fetch_protocol_pack` with a vague ref
- do not treat symbolic layers as psychometric baselines
- do not claim ILENS executed if you only read the protocol spec
- do not hide unmatched frameworks

## Best compact pattern

1. `orient_agent`
2. `find_framework_records(refs=[...])`
3. `list_protocol_packs(featured=true)`
4. `fetch_protocol_pack_summary(ref=\"ILENS\", frameworks=[...])`
5. `compare_frameworks(...)`
6. `trace_to_motifs(...)`
7. `list_interaction_hypotheses(...)`
8. downstream synthesis
