from __future__ import annotations

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.validation import collect_validation_errors


def main() -> int:
    errors = [item for item in collect_validation_errors(root) if "ID" in item or "duplicate ID" in item]
    if errors:
        print("ID lint failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ID lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
