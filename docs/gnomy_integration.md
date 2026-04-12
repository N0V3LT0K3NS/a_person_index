# GNOMY Integration

`GNOMY` should treat this repository as a knowledge and protocol substrate, not as a place to recreate local inference logic from scratch.

## What GNOMY should read from this repo

- canonical framework records
- ontology annotations
- construct crosswalks
- motif mappings
- techniques
- protocol specs
- research contribution models

## Useful local commands

These commands are meant to be callable from another agent:

```bash
python3 scripts/query_registry.py find --related-to MBTI
python3 scripts/query_registry.py trace MBTI
python3 scripts/query_registry.py motifs --related-to "Attachment Style Frameworks"
python3 scripts/query_registry.py protocols ILENS
python3 scripts/query_registry.py techniques "Paradox Scan"
python3 scripts/query_registry.py research-models
```

## Intended exchange pattern

GNOMY should generally:

1. fetch canonical records and motif traces from this repo
2. perform downstream person-level synthesis locally
3. send back only normalized or distilled research contributions when useful

## What GNOMY should not send back by default

- raw user chats
- raw journals
- direct personal identifiers
- full person-level narrative dumps

Default return shapes should instead resemble:

- result atom bundles
- mapping votes
- pairwise relation judgments
- distilled observations
- protocol feedback
