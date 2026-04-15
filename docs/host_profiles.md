# Host Profiles

Host profiles are the convenience layer that sits just above the capability
model.

They let A Person Index say, "this is a known host environment with a typical
set of capabilities," without turning host identity into a source of semantic
truth.

## Why this layer exists

The capability model is the stable abstraction.

It is the right layer for deciding what is possible in a host environment:

- can the host write files
- can it emit JSON
- can it render tables
- can it run code
- can it call adjacent MCPs or APIs

But many real operator flows start from a known host, not from a hand-declared
capability list.

Host profiles exist so a planning or actualization path can begin with:

- Codex Desktop
- Claude Code
- Claude Desktop
- Hermes remote wrapper

and expand that into the right capability set before the host chooses an
artifact or workflow path.

## Core rule

Host profiles are a planning convenience.

They do not decide:

- comparative meaning
- evidence quality
- what a valid artifact class is
- what a comparison shape means

They only help answer:

- what this host can probably do
- what path is realistic here
- what should stay conversational versus become an artifact

## Current seeded host profiles

The initial registry seeds a small set of known host environments:

- Codex Desktop
- Claude Code
- Claude Desktop
- Hermes Remote Wrapper

These are intentionally conservative.

If a host is known to vary heavily by environment, the profile should represent
the smallest dependable capability set rather than the most optimistic one.

## How to use this layer

Use host profiles when the host is already known and you do not want to
reconstruct the capability set by hand.

Examples:

```bash
python3 scripts/query_registry.py hosts
python3 scripts/query_registry.py hosts "Codex Desktop"
python3 scripts/query_registry.py recommend-path --host "Codex Desktop" --text "make a human model card"
python3 scripts/query_registry.py comparison-preflight "Contextual Time Slices" \
  --host "Claude Code" \
  --declare slice_labels="earlier self,later self" \
  --declare comparison_question="What changed?"
python3 scripts/query_registry.py artifact-realization "Structured Result Bundle Technical" \
  --host "Codex Desktop"
```

If the host is not known or the environment is unusual, fall back to capability
declaration directly instead of pretending the host profile is exact.

## Important caution

Host profiles are not a replacement for real host inspection.

They are the repo's current best structured guess about a known environment.

If the live host contradicts the seeded profile, trust the live environment and
update the host profile later through normal source changes.
