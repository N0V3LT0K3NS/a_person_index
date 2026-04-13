# Strategic Backlog

This document is the durable planning note for the next major work around A Person Index.

Use it to preserve the current thinking while it is fresh, especially across:

- consumer integration
- corpus expansion
- comparative densification
- research operations design
- documentation and site polish
- automation and maintenance standards

This is a planning memo, not a release-status document. Pair it with:

- [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
- [docs/roadmap.md](/Users/noveltokens/a_person_index/docs/roadmap.md)
- [docs/phase_3_4_plan.md](/Users/noveltokens/a_person_index/docs/phase_3_4_plan.md)
- [docs/expansion_program.md](/Users/noveltokens/a_person_index/docs/expansion_program.md)

## Planning stance

The repo is no longer blocked on basic architecture.

The next work is about:

1. proving the substrate under real consumer use
2. increasing comparative density where use reveals thin spots
3. expanding the corpus through bounded, source-disciplined PRs
4. designing the next evidence loop without prematurely turning this repo into the full research-ops system

The main sequence should remain:

1. use the substrate through `GNOMY` and other consumers
2. fix the actual friction revealed by that use
3. deepen motifs, crosswalks, interactions, and framework coverage
4. build review-friendly research surfaces
5. only then consider larger schema broadening where pressure proves it necessary

## What is already done

These are not speculative goals anymore:

- the repo is framed coherently as **A Person Index (API)**
- the five product layers are explicit
- the MCP surface is real, read-only, and tested
- Claude Code, Claude Desktop, and Hermes setup paths are documented and proven
- the companion skill exists in-repo
- the site exists and is deployed
- queue-driven Codex PR automation is working end to end
- DAT is now a real seed framework record
- onboarding and first-contact agent flow are materially better than they were

That means the repo is in a real operating state now. The backlog below is about depth and leverage, not rescue.

## Workstream 1: Consumer Integration

This is still the highest-value next tranche.

### Goal

Make `GNOMY` and other consumers use A Person Index as a real dependency surface instead of recreating its comparative logic manually.

### Why it matters

This is the pressure that will tell us:

- which packs are actually useful
- where the motif layer is too thin
- where interaction hypotheses are missing
- where the MCP contract is awkward
- where result-atom handling is underspecified

### Repo-side work

- stabilize the MCP, CLI, manifest, and generated-artifact contract
- keep arrival docs sharp for cold-start agents
- add repo-side examples that mirror actual consumer calls
- add regression tests for real consumer workflows, not just isolated primitives

### Consumer-side work

- wire `GNOMY` to MCP first, CLI second
- use curated packs before manual reconstruction
- normalize runtime outputs into result atoms
- keep person-level inference in `GNOMY`, not here
- return only approved research-safe payload shapes

### Candidate deliverables

- a GNOMY integration checklist
- a minimal example client that exercises:
  - framework matching
  - program-pack summary retrieval
  - full pack retrieval
  - motif trace
  - interaction retrieval
  - result-atom schema use
- a bounded end-to-end example from pasted assessments to downstream synthesis prep

### Completion signal

Phase 3 is materially working when `GNOMY` can use this repo without re-deriving its method library by hand.

## Workstream 2: MCP And Interface Hardening

The MCP is ready for serious local and nearby-agent use, but there is still meaningful hardening work worth doing.

### What is already solved

- onboarding tool exists
- onboarding resources exist
- fuzzy framework matching is better
- protocol-pack summary exists as progressive disclosure
- compare outputs now suggest likely next queries
- worked ILENS walkthrough exists

### What still looks high-value

- add richer end-to-end contract tests that behave like a real consumer
- keep the CLI, MCP, docs, and manifest aligned as one interface family
- consider a batch-fetch primitive if real consumer runs show too much process-spawn overhead
- consider more explicit machine-readable execution scaffolding inside packs
  - example: recommended tool calls by step
  - example: expected intermediate outputs
- keep the read-only stance unless there is a genuinely well-governed reason to change it

### Open design ideas

- a batch surface that returns multiple requested artifacts in one call
- richer pack metadata for agents that want to follow the sequence mechanically
- possibly a consumer-friendly full-registry snapshot strategy for local reasoning

### Not the immediate goal

- a hosted multi-tenant remote MCP service
- write endpoints into the canonical repo

## Workstream 3: Result-Atom Normalization

This is one of the clearest remaining seams between user data and program execution.

### Why it matters

We now have:

- contribution models
- result atom schema
- programs
- packs

But there is still no canonical helper that turns raw framework output into clean result atoms.

### Core problem

Agents can retrieve the schema, but they still have to improvise the translation from:

- `Openness: Very High`
- `ENFP`
- `4w3 sx`

into structured result atoms with the right framework and construct IDs.

### Candidate directions

- a repo-side helper that maps raw assessment output into result atoms when the framework is known
- a framework-specific construct-list or result-shape discovery surface
- a maintained examples library showing correct result-atom decomposition for common frameworks

### Boundary caution

This repo can define and support the contract.

The actual person-level usage of result atoms still belongs in `GNOMY` or another consumer runtime.

### Priority

High. This may be the single most leverage-heavy repo-side improvement for consumer usability.

## Workstream 4: Comparative Density

The next biggest qualitative gain is not another abstract layer. It is more comparative intelligence.

### Current bottleneck

Motifs are useful, but interaction hypotheses and construct-level seams are where the best synthesis quality emerges.

The current repo is still thin in several recurring seams:

- trait ↔ typology
- attachment ↔ care-signaling
- social-strategic seams
- symbolic meaning ↔ identity adhesion
- creativity-task ↔ openness / ideation / abstraction seams
- performance-task ↔ trait-language non-equivalence seams

### What to add

- more construct-level crosswalks with explicit non-equivalence where needed
- more interaction hypotheses, especially where real user stacks keep surfacing the same tensions
- better motif coverage only where it creates actual comparative leverage
- more contrast edges, not just overlap edges

### Important principle

Do not create density for its own sake.

Prefer:

- seams that recur in real consumer use
- seams that reduce interpretive flattening
- seams that improve pack usefulness

## Workstream 5: Corpus Expansion

The next frameworks should still be added as bounded, source-disciplined PRs.

### Current likely order

1. seed source enrichment
2. R-Drive
3. Political Compass
4. Remote Associates / associative creativity
5. Alternative Uses Task
6. crosswalk and interaction densification around the new seams
7. True Colors cleanup

### Why these matter

#### Seed source enrichment

- strengthens what already exists
- improves the evidence floor for downstream synthesis
- is low-risk and compounds across the whole corpus

#### R-Drive

- already appears in real user stacks
- unusually dense
- fills motivational and behavioral seams that other indexed systems do not cover well

#### Political Compass

- extends the comparative substrate into worldview and ideology space
- creates new seams for motive, values, and worldview interpretation

#### Remote Associates and Alternative Uses

- make the creativity/ideation family less one-note
- help separate divergent ideation, associative linkage, and broad trait openness

#### True Colors

- useful for real-world coverage
- lower research priority than the items above

### Source discipline

Use:

- [docs/research_authoring_standard.md](/Users/noveltokens/a_person_index/docs/research_authoring_standard.md)
- [docs/source_landscape.md](/Users/noveltokens/a_person_index/docs/source_landscape.md)
- [.github/codex/task_queue.yaml](/Users/noveltokens/a_person_index/.github/codex/task_queue.yaml)

Do not treat discovery surfaces as stronger authorities than they are.

## Workstream 6: Research Ops Design

This is worth laying out now, even if the full implementation should wait until consumer pressure is clearer.

### What already exists

- research contribution models
- promotion registry
- result atom schema
- governance stance about staged evidence

### What does not exist yet

- the operational contribution store
- aggregation jobs
- review queues
- promotion logs backed by real contribution flow
- curator-facing candidate surfaces

### Clean split

#### In this repo

- contribution schemas
- promotion policy
- reviewed house changes
- possibly derived audit or candidate summary surfaces

#### Outside this repo

- contribution storage
- anonymization
- deduplication
- clustering
- aggregation
- review workflow operations

### Candidate repo-side next steps

- mapping-review queue outputs
- interaction-candidate outputs
- protocol-feedback cluster summaries
- promotion-log summaries or reviewed-change traces

### Open question

Which research returns are actually worth collecting at scale once consumers start using the substrate heavily?

## Workstream 7: Documentation And Site

The landing page is in much better shape, but the inner content can still improve.

### High-value doc work

- keep first-contact docs extremely short and sequenced
- add more concrete worked examples
- keep public language aligned around:
  - canonical registry
  - house synthesis
  - techniques
  - index programs
  - runtime packs
  - research stream

### High-value site work

- improve inner site pages, not just the landing page
- make search, compare, motifs, programs, and research pages feel equally intentional
- keep the site low-tech and fast, but clearer and more confident
- expose more “how to use this” pathways, not just “what is in it”

### Candidate additions

- a better “first use” page for agents and humans
- richer examples on compare and program pages
- clearer “what happens next” guidance on pack and research surfaces

## Workstream 8: Automation And Maintenance

The automation path is real now, so the next task is to keep it disciplined.

### Keep doing

- one queue item to one primary seam
- source bundle in Git before PR generation
- full verification path in repo docs and workflows
- small, auditable PRs

### Additions worth considering

- stronger queue statuses such as `done` and `blocked` where helpful
- richer audit tests for stale counts and stale queue state
- lightweight dead-link or public-doc consistency checks if they stay low-noise
- more examples of good Codex task specs for research-expansion work

### Important constraint

Automation should reduce editorial drag, not reduce editorial standards.

## Retained Ideas From First-Contact Agent Review

These ideas came from actual cold-start agent use and should remain visible:

### Already addressed or partly addressed

- onboarding tool instead of onboarding prose alone
- fuzzy matching improvements
- protocol-pack summary for progressive disclosure
- suggested next queries from compare results
- worked ILENS walkthrough

### Still worth pursuing

- result-atom normalization support
- more explicit execution scaffolding inside packs
- batch or bundled retrieval if runtime pressure proves it necessary
- even better discovery of when the companion skill should be used

## Open Questions

- Which seams show the most real-world synthesis pain once `GNOMY` uses this heavily?
- Which new frameworks appear often enough in user stacks to justify immediate inclusion?
- Which pack scopes deserve curated support rather than dynamic assembly only?
- How much normalization help belongs in this repo versus in consumers?
- At what point does the instrument-centered model actually become too narrow?
- Which review surfaces would save the most curator time first?

## Non-goals To Keep Repeating

This repo should still not become:

- the person-level inference engine
- the raw personal-data store
- the consumer quiz product
- the hosted research-ops database
- a write-open MCP surface without clear governance

## Short execution sequence

If work resumes later, the cleanest sequence is:

1. integrate `GNOMY` against the current MCP and pack surfaces
2. capture the first real consumer frictions
3. implement result-atom normalization support or equivalent helpers
4. add R-Drive and Political Compass through bounded PRs
5. deepen interaction hypotheses and crosswalk density
6. add creativity-family follow-ons
7. add research audit and candidate-review surfaces

## Administrative note

Treat this document as the standing strategy memo for “what next and why.”

It should be updated when:

- major new workstreams become real
- a major idea here is completed
- an open question is materially answered by runtime use
