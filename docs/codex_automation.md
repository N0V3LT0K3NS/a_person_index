# Codex Automation

This document explains how GitHub-triggered Codex work should run against A Person Index.

## Purpose

The goal is not to let automation improvise against the repo.

The goal is to give Codex enough context, constraints, and verification steps that automated changes behave like disciplined repo work rather than random patch generation.

## Supported entry points

The repo supports two GitHub-triggered paths:

1. Manual dispatch through `.github/workflows/codex-task.yml`
2. Structured issues created from `.github/ISSUE_TEMPLATE/codex_task.yml`

Both routes converge on the same context bundle and verification path.

For larger recurring research or corpus-expansion work, the repo now also supports a queue-driven path:

3. Manual queue dispatch through `.github/workflows/dispatch-codex-queue-item.yml`
4. Machine-readable queue items in `.github/codex/task_queue.yaml`
5. Batched queue dispatch through `.github/workflows/dispatch-ready-codex-queue.yml`

## Required secrets

Add these repository secrets before enabling the workflow:

- `OPENAI_API_KEY`

That secret must be a real OpenAI Platform API key, not the repo's placeholder string and not just a ChatGPT app login context.

Practical rules:

- use a key that starts with `sk-` or `sk-proj-`
- make sure it belongs to a Platform project/account with active billing or credits
- do not paste `your-api-key-here` from a local shell profile into GitHub secrets

The `codex-task.yml` workflow now fails fast if the secret is empty, still set to a placeholder, or malformed. That is intentional: it is better to stop immediately than to burn runner time and then fail deep inside the Codex action.

The workflow uses the default `GITHUB_TOKEN` for checkout, branch creation, PR creation, and optional issue comments.

Repository setting requirement:

- GitHub repo Settings -> Actions -> General -> Workflow permissions must be set to `Read and write permissions`

If that repo-level setting remains on `Read repository contents permission`, the workflow can still check out the repo, run Codex, and pass verification, but it will fail at the PR step with GitHub's `not permitted to create or approve pull requests` error. The YAML `permissions:` block does not override that repository-level cap.

The `codex-task.yml` workflow should use the official [`openai/codex-action`](https://github.com/openai/codex-action) rather than shelling directly into a raw `codex exec` install on the runner. That action handles installing the CLI and configuring a secure Responses API proxy for GitHub Actions.

For bounded research-expansion work, the workflow currently runs Codex with:

- `safety-strategy: drop-sudo`
- `sandbox: danger-full-access`

That combination keeps the GitHub-hosted runner non-root while still allowing Codex to fetch source material and use normal shell/network access during expansion tasks.

## Context bundle

Codex automation should read this context first:

- [AGENTS.md](/Users/noveltokens/a_person_index/AGENTS.md)
- [README.md](/Users/noveltokens/a_person_index/README.md)
- [CONTRIBUTING.md](/Users/noveltokens/a_person_index/CONTRIBUTING.md)
- [docs/current_state.md](/Users/noveltokens/a_person_index/docs/current_state.md)
- [docs/architecture.md](/Users/noveltokens/a_person_index/docs/architecture.md)
- [docs/index_programs.md](/Users/noveltokens/a_person_index/docs/index_programs.md)
- [docs/system_boundaries.md](/Users/noveltokens/a_person_index/docs/system_boundaries.md)
- [docs/phase_3_4_plan.md](/Users/noveltokens/a_person_index/docs/phase_3_4_plan.md)
- [docs/research_authoring_standard.md](/Users/noveltokens/a_person_index/docs/research_authoring_standard.md)
- [docs/expansion_program.md](/Users/noveltokens/a_person_index/docs/expansion_program.md)
- [generated/manifest.json](/Users/noveltokens/a_person_index/generated/manifest.json)

The workflow also stores a compact execution context in `.github/codex/automation_context.md`.

## Default verification path

Codex automation should run:

```bash
python3 scripts/export_schemas.py
python3 scripts/validate.py
python3 scripts/build_index.py
python3 scripts/generate_docs.py
npm run mcp:smoke
python3 -m pytest
```

If a task intentionally does not require part of the path, that exception should be explained in the PR body.

## Design rules

- Keep the workflow read-write only where necessary.
- Keep repo logic in the repo, not duplicated in the workflow.
- Prefer creating a PR over pushing directly to `main`.
- Keep the branch prefix `codex/`.
- Keep source truth, house synthesis, programs, and research evidence clearly separated.
- Keep one queue item to one primary seam so PRs stay reviewable.

## Queue-driven expansion work

For recurring framework, source, crosswalk, and interaction work:

1. define a bounded task in `.github/codex/task_queue.yaml`
2. make sure the task names its objective, acceptance criteria, context paths, sources, and verification path
3. dispatch it through `.github/workflows/dispatch-codex-queue-item.yml`
4. let the resulting `codex-task` issue trigger the existing PR workflow

The queue renderer is:

```bash
python3 scripts/render_codex_task_from_queue.py task_add_rdrive_framework
```

The queue lister is:

```bash
python3 scripts/list_codex_queue_tasks.py --status ready --priority highest --format ids
```

This is the preferred path for repeatable research-expansion work because it keeps:

- the task spec in Git
- the source bundle visible
- the verification path explicit
- the resulting PR bounded

Queue-dispatched `codex-task` runs now rerender the canonical task spec from `.github/codex/task_queue.yaml` on the GitHub runner using `task_id`. They do not rely on an issue body surviving GitHub workflow input plumbing perfectly.

The workflow also removes its own temporary task files before PR creation so automation artifacts do not leak into the resulting branch.

## Batch dispatch

Use `.github/workflows/dispatch-ready-codex-queue.yml` when you want a small burst of bounded expansion PR attempts from the ready queue.

Guidelines:

- keep the batch limit small
- prefer `highest` and `high` first
- do not dispatch the whole queue just because it exists
- review PR load like a human editor, not a job queue

## Recommended use

Use the Codex workflow for:

- bounded repo improvements
- corpus deepening
- doc and site hardening
- generated-surface maintenance
- structured follow-up work from issue templates
- queue-driven framework and crosswalk expansion

Do not use it for:

- raw research data intake
- runtime person-level inference
- secrets-heavy operations outside repo maintenance

## Relationship to CI

The Codex workflow complements CI. It does not replace it.

- `ci.yml` verifies repo health
- `netlify-deploy.yml` publishes the static site
- `codex-task.yml` prepares a scoped implementation PR
- `dispatch-codex-queue-item.yml` turns queue items into issue-triggered Codex PR runs
