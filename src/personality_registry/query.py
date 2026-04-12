from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from personality_registry.audit import audit_summary, bundle_audit_entry
from personality_registry.extensions import ExtensionRegistryData, load_extensions_strict
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


def _entity_catalog(repository: RepositoryData) -> dict[str, dict[str, str]]:
    catalog: dict[str, dict[str, str]] = {}
    for bundle in repository.instruments.values():
        instrument = bundle.instrument
        catalog[instrument.id] = {
            "entity_type": "instrument",
            "entity_id": instrument.id,
            "label": instrument.canonical_name,
            "instrument_id": instrument.id,
            "instrument_label": instrument.canonical_name,
            "slug": bundle.slug,
        }
        for construct in bundle.constructs:
            catalog[construct.id] = {
                "entity_type": "construct",
                "entity_id": construct.id,
                "label": construct.name,
                "instrument_id": instrument.id,
                "instrument_label": instrument.canonical_name,
                "slug": bundle.slug,
            }
    return catalog


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


def resolve_construct(repository: RepositoryData, ref: str):
    normalized = _normalize(ref)
    candidates = []
    for bundle in repository.instruments.values():
        for construct in bundle.constructs:
            names = {
                construct.id,
                construct.name,
                construct.short_name or "",
            }
            if normalized in {_normalize(name) for name in names if name}:
                candidates.append((bundle, construct))
    if not candidates:
        raise KeyError(f"No construct found for '{ref}'")
    if len(candidates) > 1:
        raise KeyError(
            f"Reference '{ref}' is ambiguous across {[construct.id for _, construct in candidates]}"
        )
    return candidates[0]


def resolve_entity_reference(repository: RepositoryData, ref: str) -> dict[str, str]:
    try:
        bundle = resolve_instrument(repository, ref)
        return {
            "entity_type": "instrument",
            "entity_id": bundle.instrument.id,
            "label": bundle.instrument.canonical_name,
            "instrument_id": bundle.instrument.id,
            "instrument_label": bundle.instrument.canonical_name,
            "slug": bundle.slug,
        }
    except KeyError:
        bundle, construct = resolve_construct(repository, ref)
        return {
            "entity_type": "construct",
            "entity_id": construct.id,
            "label": construct.name,
            "instrument_id": bundle.instrument.id,
            "instrument_label": bundle.instrument.canonical_name,
            "slug": bundle.slug,
        }


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


def _resolve_extension_item(items: list[Any], ref: str, label_fields: tuple[str, ...]) -> Any:
    normalized = _normalize(ref)
    candidates = []
    for item in items:
        names = {getattr(item, "id", "")}
        for field_name in label_fields:
            value = getattr(item, field_name, None)
            if isinstance(value, str):
                names.add(value)
        if normalized in {_normalize(name) for name in names if name}:
            candidates.append(item)
    if not candidates:
        raise KeyError(f"No extension record found for '{ref}'")
    if len(candidates) > 1:
        raise KeyError(
            f"Reference '{ref}' is ambiguous across {[getattr(item, 'id', '(no id)') for item in candidates]}"
        )
    return candidates[0]


def resolve_motif(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.motifs, ref, ("name",))


def resolve_protocol(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.protocols, ref, ("name",))


def resolve_technique(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.techniques, ref, ("name",))


def resolve_contribution_model(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.contribution_models, ref, ("name",))


def _mapping_payload(
    mapping,
    motif_index: dict[str, Any],
    entity_catalog: dict[str, dict[str, str]],
) -> dict[str, Any]:
    source_ref = entity_catalog.get(
        mapping.source_entity_id,
        {
            "entity_type": mapping.source_entity_type,
            "entity_id": mapping.source_entity_id,
            "label": mapping.source_entity_id,
            "instrument_id": "",
            "instrument_label": "",
            "slug": "",
        },
    )
    motif = motif_index[mapping.target_entity_id]
    return {
        "id": mapping.id,
        "source_entity_type": mapping.source_entity_type,
        "source_entity_id": mapping.source_entity_id,
        "source_label": source_ref["label"],
        "source_instrument_id": source_ref["instrument_id"],
        "source_instrument_label": source_ref["instrument_label"],
        "target_entity_id": mapping.target_entity_id,
        "target_label": motif.name,
        "relationship_type": mapping.relationship_type,
        "relationship_strength": mapping.relationship_strength,
        "confidence": mapping.confidence,
        "status": mapping.status,
        "rationale": mapping.rationale,
        "notes": mapping.notes,
    }


def motif_record(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    motif_ref: str,
) -> dict[str, Any]:
    motif = resolve_motif(extensions, motif_ref)
    entity_catalog = _entity_catalog(repository)
    motif_index = {item.id: item for item in extensions.motifs}
    linked_mappings = [
        _mapping_payload(mapping, motif_index, entity_catalog)
        for mapping in extensions.mappings
        if mapping.target_entity_id == motif.id
    ]
    linked_instruments = sorted(
        {
            payload["source_instrument_id"]
            for payload in linked_mappings
            if payload["source_instrument_id"]
        }
    )
    return {
        "motif": motif.model_dump(mode="json"),
        "mapping_count": len(linked_mappings),
        "linked_instrument_ids": linked_instruments,
        "linked_mappings": linked_mappings,
    }


def find_motifs(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    *,
    text: str | None = None,
    tag: str | None = None,
    related_to: str | None = None,
) -> list[dict[str, Any]]:
    motif_index = {item.id: item for item in extensions.motifs}
    entity_catalog = _entity_catalog(repository)
    mapping_counts: dict[str, int] = {}
    related_motif_ids: set[str] | None = None
    if related_to:
        trace_payload = trace_entity_to_motifs(repository, extensions, related_to)
        related_motif_ids = {entry["motif"]["id"] for entry in trace_payload["motif_summary"]}

    for mapping in extensions.mappings:
        mapping_counts[mapping.target_entity_id] = mapping_counts.get(mapping.target_entity_id, 0) + 1

    results: list[dict[str, Any]] = []
    for motif in extensions.motifs:
        if tag and tag not in motif.tags:
            continue
        if related_motif_ids is not None and motif.id not in related_motif_ids:
            continue
        if text:
            blob = "\n".join([motif.id, motif.name, motif.summary, motif.description, *motif.tags]).lower()
            if _normalize(text) not in _normalize(blob):
                continue
        linked_sources = [
            entity_catalog.get(mapping.source_entity_id, {}).get("label", mapping.source_entity_id)
            for mapping in extensions.mappings
            if mapping.target_entity_id == motif.id
        ]
        results.append(
            {
                "id": motif.id,
                "name": motif.name,
                "status": motif.status,
                "motif_kind": motif.motif_kind,
                "summary": motif.summary,
                "tags": motif.tags,
                "related_dimensions": motif.related_dimensions,
                "mapping_count": mapping_counts.get(motif.id, 0),
                "linked_sources": sorted(set(linked_sources)),
            }
        )
    return sorted(results, key=lambda item: item["name"].lower())


def trace_entity_to_motifs(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    ref: str,
) -> dict[str, Any]:
    entity = resolve_entity_reference(repository, ref)
    entity_catalog = _entity_catalog(repository)
    motif_index = {motif.id: motif for motif in extensions.motifs}

    relevant_mappings = []
    for mapping in extensions.mappings:
        if mapping.source_entity_type == entity["entity_type"] and mapping.source_entity_id == entity["entity_id"]:
            relevant_mappings.append(mapping)
            continue
        if entity["entity_type"] == "instrument" and mapping.source_entity_type == "construct":
            source_catalog = entity_catalog.get(mapping.source_entity_id)
            if source_catalog and source_catalog["instrument_id"] == entity["instrument_id"]:
                relevant_mappings.append(mapping)

    direct_payloads = [
        _mapping_payload(mapping, motif_index, entity_catalog)
        for mapping in relevant_mappings
        if mapping.source_entity_type == entity["entity_type"] and mapping.source_entity_id == entity["entity_id"]
    ]

    construct_groups: dict[str, list[dict[str, Any]]] = {}
    for mapping in relevant_mappings:
        if mapping.source_entity_type != "construct":
            continue
        construct_groups.setdefault(mapping.source_entity_id, []).append(
            _mapping_payload(mapping, motif_index, entity_catalog)
        )

    construct_mappings = [
        {
            "construct": entity_catalog[construct_id],
            "mappings": sorted(items, key=lambda item: item["target_label"].lower()),
        }
        for construct_id, items in sorted(
            construct_groups.items(),
            key=lambda item: entity_catalog[item[0]]["label"].lower(),
        )
    ]

    motif_summary: list[dict[str, Any]] = []
    motif_groups: dict[str, list[dict[str, Any]]] = {}
    for mapping in relevant_mappings:
        motif_groups.setdefault(mapping.target_entity_id, []).append(
            _mapping_payload(mapping, motif_index, entity_catalog)
        )

    for motif_id, items in sorted(motif_groups.items(), key=lambda item: motif_index[item[0]].name.lower()):
        motif_summary.append(
            {
                "motif": motif_index[motif_id].model_dump(mode="json"),
                "mapping_count": len(items),
                "source_labels": sorted({item["source_label"] for item in items}),
                "relationship_types": sorted({item["relationship_type"] for item in items}),
                "mappings": items,
            }
        )

    return {
        "entity": entity,
        "direct_mappings": direct_payloads,
        "construct_mappings": construct_mappings,
        "motif_summary": motif_summary,
    }


def find_protocols(
    extensions: ExtensionRegistryData,
    *,
    text: str | None = None,
    consumer: str | None = None,
) -> list[dict[str, Any]]:
    results = []
    for protocol in extensions.protocols:
        if consumer and consumer not in protocol.downstream_consumers:
            continue
        if text:
            blob = "\n".join(
                [
                    protocol.id,
                    protocol.name,
                    protocol.summary,
                    protocol.purpose,
                    *protocol.downstream_consumers,
                    *protocol.required_inputs,
                    *protocol.optional_inputs,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(protocol.model_dump(mode="json"))
    return sorted(results, key=lambda item: item["name"].lower())


def protocol_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    protocol = resolve_protocol(extensions, ref)
    techniques_by_id = {technique.id: technique for technique in extensions.techniques}
    return {
        "protocol": protocol.model_dump(mode="json"),
        "techniques": [
            techniques_by_id[technique_id].model_dump(mode="json")
            for technique_id in protocol.technique_ids
            if technique_id in techniques_by_id
        ],
    }


def find_techniques(extensions: ExtensionRegistryData, *, text: str | None = None) -> list[dict[str, Any]]:
    results = []
    for technique in extensions.techniques:
        if text:
            blob = "\n".join(
                [technique.id, technique.name, technique.summary, technique.purpose, *technique.steps]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(technique.model_dump(mode="json"))
    return sorted(results, key=lambda item: item["name"].lower())


def technique_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    technique = resolve_technique(extensions, ref)
    protocol_ids = [
        protocol.id for protocol in extensions.protocols if technique.id in protocol.technique_ids
    ]
    return {
        "technique": technique.model_dump(mode="json"),
        "used_by_protocol_ids": protocol_ids,
    }


def find_contribution_models(
    extensions: ExtensionRegistryData,
    *,
    text: str | None = None,
) -> list[dict[str, Any]]:
    results = []
    for item in extensions.contribution_models:
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.purpose,
                    item.privacy_posture,
                    *item.required_fields,
                    *item.optional_fields,
                    *item.promotion_path,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def contribution_model_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_contribution_model(extensions, ref)
    return {"contribution_model": item.model_dump(mode="json")}


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
    needs_multiple_claims: bool = False,
    needs_multiple_inferences: bool = False,
    needs_multiple_risks: bool = False,
    needs_multiple_use_cases: bool = False,
    needs_official_or_semi_official_resource: bool = False,
) -> dict:
    entries: list[dict] = []
    for bundle in sorted(repository.instruments.values(), key=lambda item: item.instrument.canonical_name.lower()):
        entry = bundle_audit_entry(bundle)
        coverage = entry["coverage"]

        if needs_crosswalks and coverage["has_crosswalks"]:
            continue
        if needs_multiple_resources and coverage["has_multiple_resources"]:
            continue
        if needs_multiple_claims and coverage["has_multiple_claims"]:
            continue
        if needs_multiple_inferences and coverage["has_multiple_inferences"]:
            continue
        if needs_multiple_risks and coverage["has_multiple_risks"]:
            continue
        if needs_multiple_use_cases and coverage["has_multiple_use_cases"]:
            continue
        if needs_official_or_semi_official_resource and coverage["has_official_or_semi_official_resource"]:
            continue

        entries.append(entry)

    return {
        "summary": audit_summary([bundle_audit_entry(bundle) for bundle in repository.instruments.values()]),
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


def load_extensions_for_query(root: Path) -> ExtensionRegistryData:
    return load_extensions_strict(root)


def dumps_json(payload: object) -> str:
    return json.dumps(payload, indent=2)
