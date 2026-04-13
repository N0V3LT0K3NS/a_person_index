from __future__ import annotations

import argparse
import json

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.task_queue import load_task_queue, render_codex_issue_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Codex task issue payload from the queue.")
    parser.add_argument("task_id", help="Task ID from .github/codex/task_queue.yaml")
    parser.add_argument(
        "--queue",
        default=".github/codex/task_queue.yaml",
        help="Path to the task queue relative to repo root.",
    )
    parser.add_argument("--format", choices=("json", "title", "body"), default="json")
    args = parser.parse_args()

    queue = load_task_queue(root, queue_path=args.queue)
    payload = render_codex_issue_payload(queue, args.task_id)

    if args.format == "title":
        print(payload["title"])
    elif args.format == "body":
        print(payload["body"])
    else:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
