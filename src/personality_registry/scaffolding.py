from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from personality_registry.seed_data import (
    ONTOLOGY_DIMENSIONS,
    ONTOLOGY_ENUMS,
    ONTOLOGY_REGISTRY,
    default_placeholder_bundle,
)


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=False)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_ontology(root: Path) -> None:
    write_yaml(root / "ontology" / "registry.yaml", ONTOLOGY_REGISTRY)
    write_yaml(root / "ontology" / "dimensions.yaml", ONTOLOGY_DIMENSIONS)
    for enum_name, values in ONTOLOGY_ENUMS.items():
        write_yaml(root / "ontology" / "enums" / f"{enum_name}.yaml", {"values": values})


def write_bundle(root: Path, slug: str, bundle: dict[str, Any]) -> None:
    target = root / "instruments" / slug
    for filename, payload in bundle.items():
        path = target / filename
        if filename.endswith(".md"):
            write_text(path, str(payload))
        else:
            write_yaml(path, payload)


def scaffold_placeholder_instrument(
    root: Path,
    slug: str,
    canonical_name: str,
    instrument_id: str | None = None,
    overwrite: bool = False,
) -> Path:
    target = root / "instruments" / slug
    if target.exists() and any(target.iterdir()) and not overwrite:
        raise FileExistsError(f"{target} already exists; pass overwrite=True to replace it")

    bundle = default_placeholder_bundle(slug=slug, canonical_name=canonical_name, instrument_id=instrument_id)
    write_bundle(root, slug, bundle)
    return target
