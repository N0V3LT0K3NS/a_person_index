from __future__ import annotations

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.scaffolding import write_bundle, write_ontology
from personality_registry.seed_data import SEED_INSTRUMENT_BUNDLES


def main() -> int:
    write_ontology(root)
    for slug, bundle in sorted(SEED_INSTRUMENT_BUNDLES.items()):
        write_bundle(root, slug, bundle)
    print(f"Seeded ontology and {len(SEED_INSTRUMENT_BUNDLES)} instrument folders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
