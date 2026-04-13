from __future__ import annotations

import argparse
import json

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.task_queue import list_task_records, load_task_queue


def main() -> int:
    parser = argparse.ArgumentParser(description="List Codex queue tasks by status and priority.")
    parser.add_argument(
        "--queue",
        default=".github/codex/task_queue.yaml",
        help="Path to the task queue relative to repo root.",
    )
    parser.add_argument(
        "--status",
        action="append",
        dest="statuses",
        help="Filter to one or more task statuses such as ready or blocked.",
    )
    parser.add_argument(
        "--priority",
        action="append",
        dest="priorities",
        help="Filter to one or more priorities such as highest, high, or medium.",
    )
    parser.add_argument("--limit", type=int, help="Optional maximum number of tasks to emit.")
    parser.add_argument("--format", choices=("json", "ids", "titles"), default="json")
    args = parser.parse_args()

    queue = load_task_queue(root, queue_path=args.queue)
    tasks = list_task_records(
        queue,
        statuses=set(args.statuses or []),
        priorities=set(args.priorities or []),
        limit=args.limit,
    )

    if args.format == "ids":
        for task in tasks:
            print(task["id"])
    elif args.format == "titles":
        for task in tasks:
            print(task["title"])
    else:
        print(json.dumps(tasks, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
