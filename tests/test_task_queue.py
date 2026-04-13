from __future__ import annotations

from personality_registry.task_queue import (
    get_task_record,
    load_task_queue,
    render_codex_issue_payload,
)


def test_task_queue_loads_and_has_expected_seed_items(repo_root):
    queue = load_task_queue(repo_root)
    assert queue["version"] == 1
    task_ids = {task["id"] for task in queue["tasks"]}
    assert "task_add_rdrive_framework" in task_ids
    assert "task_crosswalk_densification_core" in task_ids


def test_render_codex_issue_payload_includes_sources_and_verification(repo_root):
    queue = load_task_queue(repo_root)
    payload = render_codex_issue_payload(queue, "task_add_political_compass_framework")
    assert payload["title"] == "[Codex Task]: Add Political Compass as a political-worldview framework with explicit methodology cautions"
    assert "## Objective" in payload["body"]
    assert "## Suggested source bundle" in payload["body"]
    assert "https://www.politicalcompass.org/test" in payload["body"]
    assert "python3 scripts/export_schemas.py" in payload["body"]


def test_get_task_record_raises_for_unknown_task(repo_root):
    queue = load_task_queue(repo_root)
    try:
        get_task_record(queue, "does_not_exist")
    except KeyError as error:
        assert "does_not_exist" in str(error)
    else:
        raise AssertionError("Expected KeyError for unknown task queue item")
