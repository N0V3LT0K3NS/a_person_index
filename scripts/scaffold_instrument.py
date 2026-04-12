from __future__ import annotations

import argparse

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.scaffolding import scaffold_placeholder_instrument


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a starter instrument scaffold.")
    parser.add_argument("--slug", required=True, help="Folder slug under instruments/")
    parser.add_argument("--name", required=True, help="Canonical instrument name")
    parser.add_argument("--instrument-id", help="Override the derived instrument ID")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing instrument folder",
    )
    args = parser.parse_args()

    target = scaffold_placeholder_instrument(
        root=root,
        slug=args.slug,
        canonical_name=args.name,
        instrument_id=args.instrument_id,
        overwrite=args.overwrite,
    )
    print(f"Scaffolded {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
