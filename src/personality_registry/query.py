from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from personality_registry.loader import InstrumentBundle, RepositoryData, load_repository_strict


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _annotation_index(bundle: InstrumentBundle) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for annotation in bundle.annotations:
        if annotation.target_entity_type == "instrument" and annotation.target_entity_id == bundle.instrument.id:
            index.setdefault(annotation.ontology_dimension, []).extend(annotation.ontology_values)
    return {key: sorted(set(values)) for key, values in index.items()}


def _search_blob(bundle: InstrumentBundle) -> str:
    parts = [
        bundle.instrument.id,
        bundle.slug,
        bundle.instrument.canonical_name,
        *bundle.instrument.short_names,
        *bundle.instrument.aliases,
        bundle.instrument.short_description,
        bundle.notes,
        *(claim.claim_text for claim in bundle.claims),
        *(inference.text for inference in bundle.inferences),
        *(construct.name for construct in bundle.constructs),
        *(construct.official_definition or "" for construct in bundle.constructs),
    ]
    return _normalize("\n".join(part for part in parts if part))


def _match_text(bundle: InstrumentBundle, query: str) -> bool:
    return _normalize(query) in _search_blob(bundle)


def _entity_to_instrument_map(repository: RepositoryData) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for bundle in repository.instruments.values():
        mapping[bundle.instrument.id] = bundle.instrument.id
        for version in bundle.versions:
            mapping[version.id] = bundle.instrument.id
        for construct in bundle.constructs:
            mapping[construct.id] = bundle.instrument.id
        for resource in bundle.resources:
            mapping[resource.id] = bundle.instrument.id
        for claim in bundle.claims:
            mapping[claim.id] = bundle.instrument.id
        for annotation in bundle.annotations:
            mapping[annotation.id] = bundle.instrument.id
        for inference in bundle.inferences:
            mapping[inference.id] = bundle.instrument.id
        for crosswalk in bundle.crosswalks:
            mapping[crosswalk.id] = bundle.instrument.id
        for risk in bundle.risks:
            mapping[risk.id] = bundle.instrument.id
        for use_case in bundle.use_cases:
            mapping[use_case.id] = bundle.instrument.id
    return mapping


def _relationship_bundle_ids(repository: RepositoryData, ref_id: str) -> set[str]:
    related: set[str] = set()
    entity_to_instrument = _entity_to_instrument_map(repository)
    for bundle in repository.instruments.values():
        for crosswalk in bundle.crosswalks:
            source_instrument_id = entity_to_instrument.get(crosswalk.source_entity_id)
            target_instrument_id = entity_to_instrument.get(crosswalk.target_entity_id)
            if source_instrument_id == ref_id and target_instrument_id and target_instrument_id != ref_id:
                related.add(target_instrument_id)
            if target_instrument_id == ref_id and source_instrument_id and source_instrument_id != ref_id:
                related.add(source_instrument_id)
    return related


def resolve_instrument(repository: RepositoryData, ref: str) -> InstrumentBundle:
    normalized = _normalize(ref)
    candidates: list[InstrumentBundle] = []
    for bundle in repository.instruments.values():
        names = {
            bundle.instrument.id,
            bundle.slug,
            bundle.instrument.canonical_name,
            *bundle.instrument.short_names,
            *bundle.instrument.aliases,
        }
        if normalized in {_normalize(name) for name in names if name}:
            candidates.append(bundle)
    if not candidates:
        raise KeyError(f"No instrument found for '{ref}'")
    if len(candidates) > 1:
        raise KeyError(f"Reference '{ref}' is ambiguous across {[bundle.instrument.id for bundle in candidates]}")
    return candidates[0]


@dataclass
class QueryResult:
    slug: str
    instrument_id: str
    canonical_name: str
    annotation_index: dict[str, list[str]]
    notes_excerpt: str

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "instrument_id": self.instrument_id,
            "canonical_name": self.canonical_name,
            "annotation_index": self.annotation_index,
            "notes_excerpt": self.notes_excerpt,
        }


def instrument_record(bundle: InstrumentBundle) -> dict:
    return {
        "slug": bundle.slug,
        "instrument": bundle.instrument.model_dump(mode="json"),
        "versions": [item.model_dump(mode="json") for item in bundle.versions],
        "constructs": [item.model_dump(mode="json") for item in bundle.constructs],
        "claims": [item.model_dump(mode="json") for item in bundle.claims],
        "resources": [item.model_dump(mode="json") for item in bundle.resources],
        "annotations": [item.model_dump(mode="json") for item in bundle.annotations],
        "annotation_index": _annotation_index(bundle),
        "inferences": [item.model_dump(mode="json") for item in bundle.inferences],
        "crosswalks": [item.model_dump(mode="json") for item in bundle.crosswalks],
        "risks": [item.model_dump(mode="json") for item in bundle.risks],
        "use_cases": [item.model_dump(mode="json") for item in bundle.use_cases],
        "notes": bundle.notes,
    }


def show_instrument(repository: RepositoryData, ref: str, section: str | None = None) -> dict | list | str:
    bundle = resolve_instrument(repository, ref)
    record = instrument_record(bundle)
    if section is None:
        return record
    if section not in record:
        raise KeyError(f"Unsupported section '{section}'")
    return record[section]


def audit_repository(
    repository: RepositoryData,
    *,
    needs_crosswalks: bool = False,
    needs_multiple_resources: bool = False,
    needs_official_or_semi_official_resource: bool = False,
) -> dict:
    entries: list[dict] = []
    for bundle in sorted(repository.instruments.values(), key=lambda item: item.instrument.canonical_name.lower()):
        officiality_counts: dict[str, int] = {}
        for resource in bundle.resources:
            officiality_counts[resource.officiality] = officiality_counts.get(resource.officiality, 0) + 1

        counts = {
            "resources": len(bundle.resources),
            "crosswalks": len(bundle.crosswalks),
            "constructs": len(bundle.constructs),
        }
        coverage = {
            "has_crosswalks": counts["crosswalks"] > 0,
            "has_multiple_resources": counts["resources"] > 1,
            "has_multiple_constructs": counts["constructs"] > 1,
            "has_official_or_semi_official_resource": any(
                resource.officiality in {"official", "semi_official"} for resource in bundle.resources
            ),
        }

        if needs_crosswalks and coverage["has_crosswalks"]:
            continue
        if needs_multiple_resources and coverage["has_multiple_resources"]:
            continue
        if needs_official_or_semi_official_resource and coverage["has_official_or_semi_official_resource"]:
            continue

        entries.append(
            {
                "slug": bundle.slug,
                "instrument_id": bundle.instrument.id,
                "canonical_name": bundle.instrument.canonical_name,
                "counts": counts,
                "resource_officiality": dict(sorted(officiality_counts.items())),
                "coverage": coverage,
            }
        )

    return {
        "summary": {
            "instrument_count": len(repository.instruments),
            "instruments_with_crosswalks": sum(1 for bundle in repository.instruments.values() if bundle.crosswalks),
            "instruments_with_multiple_resources": sum(
                1 for bundle in repository.instruments.values() if len(bundle.resources) > 1
            ),
            "instruments_with_multiple_constructs": sum(
                1 for bundle in repository.instruments.values() if len(bundle.constructs) > 1
            ),
            "instruments_with_official_or_semi_official_resource": sum(
                1
                for bundle in repository.instruments.values()
                if any(resource.officiality in {"official", "semi_official"} for resource in bundle.resources)
            ),
        },
        "instruments": entries,
    }


def find_instruments(
    repository: RepositoryData,
    *,
    refs: Iterable[str] | None = None,
    families: Iterable[str] | None = None,
    annotation_filters: dict[str, set[str]] | None = None,
    text: str | None = None,
    related_to: str | None = None,
) -> list[InstrumentBundle]:
    refs = list(refs or [])
    families = set(families or [])
    annotation_filters = annotation_filters or {}

    related_ids: set[str] | None = None
    if related_to:
        related_bundle = resolve_instrument(repository, related_to)
        related_ids = _relationship_bundle_ids(repository, related_bundle.instrument.id)

    results: list[InstrumentBundle] = []
    for bundle in repository.instruments.values():
        annotation_index = _annotation_index(bundle)

        if refs:
            normalized_refs = {_normalize(ref) for ref in refs}
            names = {
                bundle.instrument.id,
                bundle.slug,
                bundle.instrument.canonical_name,
                *bundle.instrument.short_names,
                *bundle.instrument.aliases,
            }
            if normalized_refs.isdisjoint({_normalize(name) for name in names if name}):
                continue

        if families and families.isdisjoint(set(bundle.instrument.family)):
            continue

        if annotation_filters:
            failed = False
            for dimension, required_values in annotation_filters.items():
                actual_values = set(annotation_index.get(dimension, []))
                if not required_values.issubset(actual_values):
                    failed = True
                    break
            if failed:
                continue

        if text and not _match_text(bundle, text):
            continue

        if related_ids is not None and bundle.instrument.id not in related_ids:
            continue

        results.append(bundle)

    return sorted(results, key=lambda item: item.instrument.canonical_name.lower())


def query_results(repository: RepositoryData, **kwargs) -> list[QueryResult]:
    bundles = find_instruments(repository, **kwargs)
    return [
        QueryResult(
            slug=bundle.slug,
            instrument_id=bundle.instrument.id,
            canonical_name=bundle.instrument.canonical_name,
            annotation_index=_annotation_index(bundle),
            notes_excerpt=(bundle.notes.strip().splitlines()[0] if bundle.notes.strip() else ""),
        )
        for bundle in bundles
    ]


def compare_instruments(repository: RepositoryData, left: str, right: str) -> dict:
    left_bundle = resolve_instrument(repository, left)
    right_bundle = resolve_instrument(repository, right)
    entity_to_instrument = _entity_to_instrument_map(repository)

    left_annotations = _annotation_index(left_bundle)
    right_annotations = _annotation_index(right_bundle)
    shared_dimensions = sorted(set(left_annotations) & set(right_annotations))

    overlaps = {}
    for dimension in shared_dimensions:
        shared_values = sorted(set(left_annotations[dimension]) & set(right_annotations[dimension]))
        if shared_values:
            overlaps[dimension] = shared_values

    crosswalks: list[dict] = []
    for bundle in repository.instruments.values():
        for crosswalk in bundle.crosswalks:
            source_instrument_id = entity_to_instrument.get(crosswalk.source_entity_id)
            target_instrument_id = entity_to_instrument.get(crosswalk.target_entity_id)
            if {
                source_instrument_id,
                target_instrument_id,
            } == {left_bundle.instrument.id, right_bundle.instrument.id}:
                crosswalks.append(crosswalk.model_dump(mode="json"))

    return {
        "left": {
            "id": left_bundle.instrument.id,
            "canonical_name": left_bundle.instrument.canonical_name,
            "family": left_bundle.instrument.family,
            "annotation_index": left_annotations,
            "constructs": [construct.name for construct in left_bundle.constructs],
        },
        "right": {
            "id": right_bundle.instrument.id,
            "canonical_name": right_bundle.instrument.canonical_name,
            "family": right_bundle.instrument.family,
            "annotation_index": right_annotations,
            "constructs": [construct.name for construct in right_bundle.constructs],
        },
        "shared_annotation_values": overlaps,
        "crosswalks": crosswalks,
    }


def load_repository_for_query(root: Path) -> RepositoryData:
    return load_repository_strict(root)


def dumps_json(payload: object) -> str:
    return json.dumps(payload, indent=2)
