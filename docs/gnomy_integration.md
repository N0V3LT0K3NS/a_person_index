# GNOMY Integration

`GNOMY` should treat A Person Index as a knowledge, technique, and index-program substrate, not as a place to recreate local inference logic from scratch.

`GNOMY` is a lead consumer of this repo, not the only intended consumer.

Arrival references:

- [AGENTS.md](/Users/noveltokens/a_person_index/AGENTS.md)
- [generated/manifest.json](/Users/noveltokens/a_person_index/generated/manifest.json)
- [docs/mcp.md](/Users/noveltokens/a_person_index/docs/mcp.md)
- [docs/protocol_pack_grammar.md](/Users/noveltokens/a_person_index/docs/protocol_pack_grammar.md)
- [docs/protocol_packs.md](/Users/noveltokens/a_person_index/docs/protocol_packs.md)
- [docs/research_promotion.md](/Users/noveltokens/a_person_index/docs/research_promotion.md)

## What GNOMY should read from this repo

- canonical framework records
- ontology annotations
- construct crosswalks
- motif mappings
- interaction hypotheses
- techniques
- index program specs
- research contribution models
- result atom schema
- research promotion policy

## Useful local commands

These commands are meant to be callable from another agent:

```bash
python3 scripts/query_registry.py find --related-to MBTI
python3 scripts/query_registry.py trace MBTI
python3 scripts/query_registry.py motifs --related-to "Attachment Style Frameworks"
python3 scripts/query_registry.py interactions --related-to "Attachment Style Frameworks"
python3 scripts/query_registry.py programs ILENS
python3 scripts/query_registry.py program-packs --featured
python3 scripts/query_registry.py program-packs ppk_ilens_core_trait_motive_stack
python3 scripts/query_registry.py program-pack ILENS --framework MBTI --framework Enneagram
python3 scripts/query_registry.py program-pack-grammar
python3 scripts/query_registry.py research-promotion
python3 scripts/query_registry.py techniques "Paradox Scan"
python3 scripts/query_registry.py result-atom-schema
python3 scripts/query_registry.py result-shape "Big Five"
python3 scripts/query_registry.py result-atom-bundle --framework "Big Five" --entries-json '[{"construct":"Openness to Experience","output_type":"continuous_score","output_value":"0.74"}]'
python3 scripts/query_registry.py research-models
npm run mcp:serve
```

## Intended exchange pattern

GNOMY should generally:

1. connect to the MCP server or fall back to the local CLI
2. fetch a program pack when a downstream task already has a known program and target scope
3. use result-shape discovery when the runtime still needs framework construct slots and starter atom templates
4. use the result atom normalization helper when local outputs are already decomposed to construct level
5. perform downstream person-level synthesis locally
6. send back only normalized or distilled research contributions when useful

## Boundary split

This repo should own:

- the map
- the comparative method library
- the protocol definitions
- the governance rules for research return traffic

`GNOMY` should own:

- person-level synthesis
- runtime execution against user evidence
- report and interaction behavior
- adaptation to context and user history

Do not move the person-level inference runtime into this repo.

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

## Normalization boundary

Use the repo-side helper when `GNOMY` already knows the framework and already
has construct-level output.

Do not expect this repo to turn a whole person model into atoms automatically.

The helper is for transport normalization, not for replacing the runtime's own
decomposition and synthesis logic.
