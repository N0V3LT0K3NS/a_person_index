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
