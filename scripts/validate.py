from __future__ import annotations

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.validation import collect_validation_errors


def main() -> int:
    errors = collect_validation_errors(root)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
