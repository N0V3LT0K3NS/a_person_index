from __future__ import annotations


def test_onboarding_docs_exist(repo_root):
    required_paths = [
        repo_root / "AGENTS.md",
        repo_root / "CONTRIBUTING.md",
        repo_root / "SECURITY.md",
        repo_root / "docs" / "current_state.md",
        repo_root / "docs" / "index_programs.md",
        repo_root / "docs" / "codex_automation.md",
        repo_root / "docs" / "site_design_options.md",
        repo_root / "docs" / "mcp.md",
        repo_root / "docs" / "roadmap.md",
        repo_root / "docs" / "protocol_pack_grammar.md",
        repo_root / "docs" / "protocol_packs.md",
        repo_root / "docs" / "research_promotion.md",
        repo_root / "docs" / "system_boundaries.md",
        repo_root / "docs" / "phase_3_4_plan.md",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "codex_task.yml",
        repo_root / ".github" / "pull_request_template.md",
        repo_root / ".github" / "workflows" / "codex-task.yml",
    ]
    for path in required_paths:
        assert path.exists(), f"Missing onboarding document: {path}"


def test_readme_links_to_onboarding_surface(repo_root):
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in readme
    assert "CONTRIBUTING.md" in readme
    assert "SECURITY.md" in readme
    assert "docs/current_state.md" in readme
    assert "docs/index_programs.md" in readme
    assert "docs/codex_automation.md" in readme
    assert "docs/site_design_options.md" in readme
    assert "docs/mcp.md" in readme
    assert "docs/roadmap.md" in readme
    assert "docs/protocol_pack_grammar.md" in readme
    assert "docs/protocol_packs.md" in readme
    assert "docs/research_promotion.md" in readme
    assert "docs/system_boundaries.md" in readme
    assert "docs/phase_3_4_plan.md" in readme
    assert "generated/manifest.json" in readme
