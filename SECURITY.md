# Security Policy

## Scope

A Person Index is primarily a public knowledge substrate and static/generated artifact repository. It does not aim to be a raw personal-data store, an authentication surface, or a person-level inference runtime.

Security work in this repo should focus on:

- supply-chain hygiene for Python and Node dependencies
- integrity of generated artifacts and automation workflows
- least-privilege handling of deployment and GitHub credentials
- keeping raw user data out of canonical source files
- keeping research contribution contracts privacy-minimizing by default

## Reporting

If you find a security issue in this repo or its automation:

1. Do not open a public issue with exploit details.
2. Report it privately to the repository owner through GitHub security reporting or a private maintainer channel.
3. Include the affected path, reproduction steps, impact, and any mitigation you already tested.

## Repository-specific expectations

- Do not commit secrets, tokens, or personal datasets.
- Treat `.github/workflows/` and deployment configuration as high-sensitivity surfaces.
- Treat research contribution shapes as structured summaries, not as a place to store raw personal corpora.
- Prefer read-only interfaces for agent access unless a reviewed write path is explicitly introduced.

## Verification

Before merging changes that affect automation, generated outputs, or interfaces, run:

```bash
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
npm run mcp:test
python3 -m pytest
```
