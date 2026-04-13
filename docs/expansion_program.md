# Expansion Program

This document summarizes the next bounded expansion PRs for A Person Index and how they should be dispatched.

Use it with:

- [docs/research_authoring_standard.md](/Users/noveltokens/a_person_index/docs/research_authoring_standard.md)
- [.github/codex/task_queue.yaml](/Users/noveltokens/a_person_index/.github/codex/task_queue.yaml)
- [docs/codex_automation.md](/Users/noveltokens/a_person_index/docs/codex_automation.md)

## Why this exists

The repo now has enough structure that the bottleneck is not architecture. It is disciplined corpus deepening.

That means:

- richer sources
- better notes and references
- denser crosswalks
- more interaction hypotheses
- selected new frameworks that real users actually bring in

The work should happen through bounded PRs, not one giant “make it richer” branch.

## Current source jump-off points

These are useful starting points, but not equivalent authorities.

### SimilarMinds

Use for:

- discovery of real-world folk frameworks
- ecosystem context
- site-native systems such as R-Drive

Reference:

- [SimilarMinds home](https://similarminds.com/index.html)
- [R-Drive info](https://similarminds.com/rdrive_nfo.html)

### Open Source Psychometrics Project

Use for:

- open implementations
- open-data ecosystem context
- alternative open measures and documentation

Reference:

- [OpenPsychometrics about](https://openpsychometrics.org/about/)
- [Open Jungian Type Scales](https://openpsychometrics.org/tests/OJTS/)

### Political Compass

Use for:

- the canonical record of that specific framework
- question framing and axis model

Reference:

- [Political Compass test](https://www.politicalcompass.org/test)
- [Political Compass about](https://www.politicalcompass.org/about)

### Divergent Association Task

Use for:

- divergent-thinking measurement
- the creativity-measures family

Reference:

- [DAT home](https://www.datcreativity.com/)
- [DAT about](https://www.datcreativity.com/about)

## Priority order

### 1. Seed source enrichment

Why first:

- it improves the current corpus immediately
- it makes every later crosswalk and synthesis claim better grounded
- it is the safest way to increase quality and reference density quickly

Queue item:

- `task_seed_source_enrichment`

### 2. R-Drive

Why next:

- it is already a real missing framework in your own assessment stack
- it is unusually dense
- it creates immediate downstream value for GNOMY and other consumers

Queue item:

- `task_add_rdrive_framework`

### 3. Political Compass

Why next:

- it broadens the repo into worldview and political-orientation territory
- it is widely recognizable
- it creates a new comparative seam for motive, values, and worldview work

Queue item:

- `task_add_political_compass_framework`

### 4. Creativity-measures family

Why next:

- it opens a useful axis adjacent to openness, abstraction, ideation, and novelty
- it gives the repo more cognitive-process instrumentation instead of only person-type systems

Queue item:

- `task_add_creativity_family_frameworks`

### 5. Crosswalk and interaction densification

Why after those:

- better seams depend on having the source objects first
- this is where synthesis quality rises the most once the frameworks exist

Queue item:

- `task_crosswalk_densification_core`

### 6. True Colors cleanup

Why lower priority:

- useful for coverage
- lower research value than the items above

Queue item:

- `task_add_true_colors_framework`

## Dispatch flow

### Local preview

```bash
python3 scripts/render_codex_task_from_queue.py task_add_rdrive_framework
```

### GitHub-triggered dispatch

Use the manual workflow:

- `.github/workflows/dispatch-codex-queue-item.yml`

That workflow opens a `codex-task` issue from the queue item, and the existing Codex automation turns that issue into a PR.

## Operating rule

One queue item should produce one primary PR.

If a task reveals a second large seam, split it into a follow-up queue item instead of smuggling it into the same PR.
