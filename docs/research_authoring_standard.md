# Research And Authoring Standard

This document sets the quality bar for framework expansion, source deepening, crosswalk densification, and related documentation work in A Person Index.

Use it with [docs/source_landscape.md](/Users/noveltokens/a_person_index/docs/source_landscape.md) when the work depends on external source surfaces or candidate-framework scouting.

## Purpose

The repo should scale by adding reviewed shared knowledge objects, not by accumulating loosely sourced notes.

Every expansion PR should make it obvious:

1. what kind of object is being added or changed
2. what sources justify it
3. what epistemic limits apply
4. what crosswalk or motif value the change creates
5. what verification proves the repo still behaves correctly

## Allowed work types

Use this standard for:

- adding a new framework record
- deepening source and reference coverage for an existing framework
- adding or refining motifs
- adding or refining crosswalks
- adding or refining interaction hypotheses
- adding or refining techniques, index programs, or runtime packs
- adding documentation or generated presentation that explains those changes

Do not use this repo for:

- raw personal data
- one-off person analyses
- unresolved research dumps
- runtime-only heuristics that belong in GNOMY or another consumer

## Source classes

Use source classes explicitly when building or reviewing a framework record.

### Class A: canonical or primary framework source

Examples:

- original framework site or technical manual
- official questionnaire documentation
- original open-access manuscript for an open instrument

Use for:

- naming the framework
- describing intended constructs
- documenting administration or scoring logic

### Class B: independent analytic or critical source

Examples:

- peer-reviewed validation paper
- critical review
- independent methodology discussion

Use for:

- evidence profile
- known psychometric strengths or limitations
- critique, contested validity, or misuse risks

### Class C: implementation or ecosystem source

Examples:

- open implementation site
- public test archive
- ecosystem-specific community documentation

Use for:

- showing how a framework actually circulates in the wild
- connecting users to known implementations
- documenting community language, symbolic role, or identity adhesion risk

Do not use Class C alone to make strong empirical claims.

## Minimum source bundle by framework type

### New non-symbolic framework

Require at least:

- 1 Class A source
- 1 Class B source
- 1 additional source from Class A, B, or C

### New symbolic, folk, or self-published framework

Require at least:

- 1 Class A source
- 1 independent contextual or critical source when available
- explicit caution in annotations, inferences, and risks

If no meaningful independent source exists, say so directly in the notes and keep the evidence profile conservative.

### Existing framework source deepening

Require at least one of:

- a stronger primary source than currently present
- an independent critique or validation source that changes the epistemic picture
- a materially better implementation or ecosystem reference

## Minimum authoring bar for a new framework PR

Every new framework PR should include:

- canonical identity files
- top-level constructs when the framework has stable recurring outputs
- at least 2 claims
- at least 2 inferences
- at least 2 risks
- at least 2 use cases
- at least 2 resources
- at least 1 outgoing crosswalk
- a notes page that explains what the framework is, what it is useful for, and where caution is needed

Target bar for new frameworks after the initial scaffold:

- 3 or more crosswalks
- at least one high-confidence neighbor
- at least one contrast or non-equivalence edge
- motif coverage sufficient for at least one realistic synthesis path

## Minimum authoring bar for crosswalk and interaction work

Crosswalk PRs should state:

- which constructs or frameworks are being related
- whether the relation is overlap, analogy, contrast, or deliberate non-equivalence
- what evidence or rationale supports the relationship
- what misuse or flattening risk applies

Interaction-hypothesis PRs should state:

- the left and right entities
- interaction type
- scope or context
- why the interaction matters for synthesis quality
- whether the claim is strongly supported, weakly supported, or mainly a house hypothesis

## Source-handling rules for the named seed sites

These sites are useful, but they should not all be treated the same way.

### SimilarMinds

Use as:

- discovery surface
- ecosystem context
- folk-framework source for site-native systems such as R-Drive

Do not use as:

- a sole authority for strong empirical claims

Reference:

- [SimilarMinds home](https://similarminds.com/index.html)
- [R-Drive info](https://similarminds.com/rdrive_nfo.html)

### Open Source Psychometrics Project

Use as:

- open implementation and open-data ecosystem source
- implementation reference for open instruments
- source of adjacent open measures and documentation

Do not assume every OpenPsychometrics implementation is the canonical authority for the underlying construct.

Reference:

- [OpenPsychometrics about](https://openpsychometrics.org/about/)
- [Open Jungian Type Scales](https://openpsychometrics.org/tests/OJTS/)

### Political Compass

Use as:

- canonical source for that specific framework
- question and scoring reference for the framework record

Also require:

- independent commentary or critique before making stronger evidence claims

Reference:

- [Political Compass test](https://www.politicalcompass.org/test)
- [Political Compass about](https://www.politicalcompass.org/about)

### Divergent Association Task

Use as:

- primary source for the DAT
- entry point into the divergent-thinking family

Reference:

- [DAT home](https://www.datcreativity.com/)
- [DAT about](https://www.datcreativity.com/about)

### Creative association and divergent-thinking tasks more broadly

Treat tasks such as Remote Associates and Alternative Uses as research instruments that require primary academic sourcing before canonical inclusion.

Use secondary discovery pages only as a starting point for finding the primary papers.

## PR scoping rules

Keep one PR to one primary seam.

Good scopes:

- add one new framework
- deepen one family of existing framework resources
- densify one crosswalk seam
- add one small set of interaction hypotheses around one recurring synthesis problem

Split into separate PRs when:

- a framework addition also requires ontology expansion
- crosswalk work spans unrelated families
- site polish and corpus changes would make review harder
- one "family" idea actually hides multiple different measures with different source lineages

## PR anatomy

Every research-expansion PR should make these visible in the PR body:

- queue task id or bounded manual scope
- source bundle by role and class
- epistemic posture changes, if any
- crosswalk or interaction density changes, if any
- verification path actually run

Use the repo PR template and fill the source-bundle section explicitly.

## Verification

Run the full repo verification path unless a narrower path is justified:

```bash
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
npm run mcp:test
python3 -m pytest
```

## Review questions

Before merging, ask:

1. Is the new or changed object clearly in the right layer?
2. Are the sources good enough for the claims being made?
3. Are epistemic limits stated plainly enough?
4. Did the change add real comparative value, not just more prose?
5. Is the PR bounded enough that another agent or reviewer can actually audit it?
