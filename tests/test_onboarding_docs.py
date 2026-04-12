from __future__ import annotations


def test_onboarding_docs_exist(repo_root):
    required_paths = [
        repo_root / "AGENTS.md",
        repo_root / "docs" / "current_state.md",
        repo_root / "docs" / "mcp.md",
        repo_root / "docs" / "roadmap.md",
        repo_root / "docs" / "protocol_pack_grammar.md",
        repo_root / "docs" / "protocol_packs.md",
    ]
    for path in required_paths:
        assert path.exists(), f"Missing onboarding document: {path}"


def test_readme_links_to_onboarding_surface(repo_root):
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in readme
    assert "docs/current_state.md" in readme
    assert "docs/mcp.md" in readme
    assert "docs/roadmap.md" in readme
    assert "docs/protocol_pack_grammar.md" in readme
    assert "docs/protocol_packs.md" in readme
    assert "generated/manifest.json" in readme
