from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_task_queue(root: Path, queue_path: str = ".github/codex/task_queue.yaml") -> dict[str, Any]:
    path = root / queue_path
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Task queue did not parse into a mapping: {path}")
    return payload


def get_task_record(queue: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in queue.get("tasks", []):
        if task.get("id") == task_id:
            return task
    raise KeyError(f"No task queue entry found for '{task_id}'")


def render_codex_issue_payload(queue: dict[str, Any], task_id: str) -> dict[str, Any]:
    task = get_task_record(queue, task_id)
    verification = task.get("verification") or queue.get("default_verification") or []
    lines = [
        "## Objective",
        "",
        task["objective"].strip(),
        "",
        "## Acceptance criteria",
        "",
    ]
    lines.extend(f"- {item}" for item in task.get("acceptance_criteria", []))
    lines.extend(
        [
            "",
            "## Context files or areas",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in task.get("context_paths", []))
    lines.extend(
        [
            "",
            "## Required verification",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in verification)
    lines.extend(
        [
            "",
            "## Primary layer",
            "",
            f"- {task['primary_layer']}",
            "",
            "## Suggested source bundle",
            "",
        ]
    )
    for source in task.get("suggested_sources", []):
        lines.append(
            f"- [{source['label']}]({source['url']})"
            f" — class: `{source['source_class']}`; role: {source['role']}"
        )
    notes = task.get("notes", [])
    if notes:
        lines.extend(
            [
                "",
                "## Notes",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in notes)

    return {
        "id": task["id"],
        "title": f"[Codex Task]: {task['title']}",
        "body": "\n".join(lines).strip() + "\n",
        "status": task.get("status", "ready"),
        "priority": task.get("priority", "unspecified"),
        "verification": verification,
    }
