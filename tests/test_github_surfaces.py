from __future__ import annotations

from pathlib import Path

import yaml


def test_github_workflows_and_issue_templates_parse(repo_root):
    paths = [
        repo_root / ".github" / "workflows" / "ci.yml",
        repo_root / ".github" / "workflows" / "netlify-deploy.yml",
        repo_root / ".github" / "workflows" / "codex-task.yml",
        repo_root / ".github" / "workflows" / "dispatch-codex-queue-item.yml",
        repo_root / ".github" / "workflows" / "dispatch-ready-codex-queue.yml",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "codex_task.yml",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "config.yml",
        repo_root / ".github" / "codex" / "task_queue.yaml",
    ]
    for path in paths:
        assert path.exists(), f"Missing GitHub surface: {path}"
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert parsed is not None, f"GitHub surface did not parse: {path}"


def test_codex_automation_context_exists(repo_root):
    path = repo_root / ".github" / "codex" / "automation_context.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "A Person Index (API)" in text
    assert "generated/manifest.json" in text


def test_codeowners_exists(repo_root):
    path = repo_root / ".github" / "CODEOWNERS"
    assert path.exists()
    assert "@N0V3LT0K3NS" in path.read_text(encoding="utf-8")


def test_codex_task_workflow_validates_openai_api_key(repo_root):
    path = repo_root / ".github" / "workflows" / "codex-task.yml"
    text = path.read_text(encoding="utf-8")
    assert "Validate OpenAI API key configuration" in text
    assert "your-api-key-here" in text
    assert "sk-proj-" in text
    assert "Remove workflow scratch artifacts" in text
    assert "codex-last-message.txt" in text


def test_codex_automation_doc_covers_repo_workflow_permissions(repo_root):
    path = repo_root / "docs" / "codex_automation.md"
    text = path.read_text(encoding="utf-8")
    assert "Workflow permissions must be set to `Read and write permissions`" in text
    assert "Allow GitHub Actions to create and approve pull requests" in text
    assert "not permitted to create or approve pull requests" in text


def test_netlify_workflow_handles_missing_secrets_gracefully(repo_root):
    path = repo_root / ".github" / "workflows" / "netlify-deploy.yml"
    text = path.read_text(encoding="utf-8")
    assert "Check Netlify configuration" in text
    assert "Skipping Netlify deploy because required secrets are missing." in text
    assert "steps.netlify.outputs.can_deploy == 'true'" in text
