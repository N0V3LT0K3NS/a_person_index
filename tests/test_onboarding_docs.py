from __future__ import annotations

from personality_registry.task_queue import get_task_record, load_task_queue


def test_onboarding_docs_exist(repo_root):
    required_paths = [
        repo_root / "AGENTS.md",
        repo_root / "CHANGELOG.md",
        repo_root / "CONTRIBUTING.md",
        repo_root / "SECURITY.md",
        repo_root / "skills" / "a-person-index" / "SKILL.md",
        repo_root / "skills" / "a-person-index" / "agents" / "openai.yaml",
        repo_root / "skills" / "a-person-index" / "references" / "workflows.md",
        repo_root / "skills" / "a-person-index-actualization" / "SKILL.md",
        repo_root / "skills" / "a-person-index-actualization" / "agents" / "openai.yaml",
        repo_root / "skills" / "a-person-index-actualization" / "references" / "workflows.md",
        repo_root / "skills" / "a-person-index-meta" / "SKILL.md",
        repo_root / "skills" / "a-person-index-meta" / "agents" / "openai.yaml",
        repo_root / "skills" / "a-person-index-meta" / "references" / "workflows.md",
        repo_root / "docs" / "release_status.md",
        repo_root / "docs" / "strategic_backlog.md",
        repo_root / "docs" / "agent_quickstart.md",
        repo_root / "docs" / "assessment_workflow.md",
        repo_root / "docs" / "ilens_walkthrough.md",
        repo_root / "docs" / "current_state.md",
        repo_root / "docs" / "advanced_modes.md",
        repo_root / "docs" / "comparison_shapes.md",
        repo_root / "docs" / "comparison_preflight.md",
        repo_root / "docs" / "host_profiles.md",
        repo_root / "docs" / "capability_model.md",
        repo_root / "docs" / "artifact_realization.md",
        repo_root / "docs" / "artifact_templates.md",
        repo_root / "docs" / "result_atom_normalization.md",
        repo_root / "docs" / "expression_model.md",
        repo_root / "docs" / "actualization_protocols.md",
        repo_root / "docs" / "workflow_recipes.md",
        repo_root / "docs" / "expression_and_artifacts.md",
        repo_root / "docs" / "multi_subject_comparison.md",
        repo_root / "docs" / "index_programs.md",
        repo_root / "docs" / "codex_automation.md",
        repo_root / "docs" / "research_authoring_standard.md",
        repo_root / "docs" / "source_landscape.md",
        repo_root / "docs" / "expansion_program.md",
        repo_root / "docs" / "site_design_options.md",
        repo_root / "docs" / "mcp.md",
        repo_root / "docs" / "roadmap.md",
        repo_root / "docs" / "protocol_pack_grammar.md",
        repo_root / "docs" / "protocol_packs.md",
        repo_root / "docs" / "research_promotion.md",
        repo_root / "docs" / "system_boundaries.md",
        repo_root / "docs" / "phase_3_4_plan.md",
        repo_root / "examples" / "mcp" / "README.md",
        repo_root / "examples" / "mcp" / "claude-code.mcp.json.example",
        repo_root / "examples" / "mcp" / "claude-desktop-config.json.example",
        repo_root / "examples" / "mcp" / "hermes-wrapper.sh.example",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "codex_task.yml",
        repo_root / ".github" / "pull_request_template.md",
        repo_root / ".github" / "workflows" / "codex-task.yml",
        repo_root / ".github" / "workflows" / "dispatch-ready-codex-queue.yml",
    ]
    for path in required_paths:
        assert path.exists(), f"Missing onboarding document: {path}"


def test_readme_links_to_onboarding_surface(repo_root):
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "Fast arrival path" in readme
    assert "If you need the deeper map after that" in readme
    assert "AGENTS.md" in readme
    assert "CHANGELOG.md" in readme
    assert "CONTRIBUTING.md" in readme
    assert "SECURITY.md" in readme
    assert "docs/agent_quickstart.md" in readme
    assert "docs/assessment_workflow.md" in readme
    assert "docs/ilens_walkthrough.md" in readme
    assert "docs/release_status.md" in readme
    assert "docs/strategic_backlog.md" in readme
    assert "docs/current_state.md" in readme
    assert "docs/advanced_modes.md" in readme
    assert "docs/comparison_shapes.md" in readme
    assert "docs/comparison_preflight.md" in readme
    assert "docs/host_profiles.md" in readme
    assert "docs/capability_model.md" in readme
    assert "docs/artifact_realization.md" in readme
    assert "docs/artifact_templates.md" in readme
    assert "docs/result_atom_normalization.md" in readme
    assert "docs/expression_model.md" in readme
    assert "docs/actualization_protocols.md" in readme
    assert "docs/workflow_recipes.md" in readme
    assert "docs/expression_and_artifacts.md" in readme
    assert "docs/multi_subject_comparison.md" in readme
    assert "docs/index_programs.md" in readme
    assert "docs/codex_automation.md" in readme
    assert "docs/research_authoring_standard.md" in readme
    assert "docs/source_landscape.md" in readme
    assert "docs/expansion_program.md" in readme
    assert "docs/site_design_options.md" in readme
    assert "docs/mcp.md" in readme
    assert "docs/roadmap.md" in readme
    assert "docs/protocol_pack_grammar.md" in readme
    assert "docs/protocol_packs.md" in readme
    assert "docs/research_promotion.md" in readme
    assert "docs/system_boundaries.md" in readme
    assert "docs/phase_3_4_plan.md" in readme
    assert "examples/mcp" in readme
    assert "generated/manifest.json" in readme


def test_readme_seed_corpus_mentions_current_creativity_anchor(repo_root):
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "16 source-backed seed framework records" in readme
    assert "Divergent Association Task" in readme


def test_mcp_clients_doc_lists_four_validation_layers(repo_root):
    text = (repo_root / "docs" / "mcp_clients.md").read_text(encoding="utf-8")
    assert "validated in four layers" in text
    assert "4. Hermes remote-host assumptions and wrapper path checked" in text


def test_changelog_tracks_unreleased_post_release_work(repo_root):
    text = (repo_root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## Unreleased" in text
    assert "Divergent Association Task as the 16th seeded framework record" in text


def test_task_queue_marks_dat_as_completed(repo_root):
    queue = load_task_queue(repo_root)
    task = get_task_record(queue, "task_add_divergent_association_task")
    assert task["status"] == "done"
