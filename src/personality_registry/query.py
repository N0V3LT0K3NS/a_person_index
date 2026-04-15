from __future__ import annotations

import json
import re
from difflib import get_close_matches
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from personality_registry.audit import audit_summary, bundle_audit_entry
from personality_registry.extensions import (
    ArtifactClass,
    ExtensionRegistryData,
    WorkflowRecipe,
    load_extensions_strict,
)
from personality_registry.loader import InstrumentBundle, RepositoryData, load_repository_strict


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


SEARCH_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "assessment",
    "assessments",
    "average",
    "by",
    "for",
    "from",
    "high",
    "in",
    "is",
    "low",
    "medium",
    "moderately",
    "of",
    "or",
    "personality",
    "profile",
    "results",
    "score",
    "scores",
    "system",
    "test",
    "tests",
    "the",
    "to",
    "type",
    "very",
    "with",
}


def _tokenize_search_terms(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    return {
        token
        for token in tokens
        if token not in SEARCH_STOPWORDS and (token.isdigit() or len(token) >= 2)
    }


def _instrument_identity_names(bundle: InstrumentBundle) -> list[str]:
    return [
        bundle.instrument.id,
        bundle.slug,
        bundle.instrument.canonical_name,
        *bundle.instrument.short_names,
        *bundle.instrument.aliases,
    ]


def _annotation_index(bundle: InstrumentBundle) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for annotation in bundle.annotations:
        if annotation.target_entity_type == "instrument" and annotation.target_entity_id == bundle.instrument.id:
            index.setdefault(annotation.ontology_dimension, []).extend(annotation.ontology_values)
    return {key: sorted(set(values)) for key, values in index.items()}


def _search_blob(bundle: InstrumentBundle) -> str:
    parts = [
        *_instrument_identity_names(bundle),
        bundle.instrument.short_description,
        bundle.notes,
        *(claim.claim_text for claim in bundle.claims),
        *(inference.text for inference in bundle.inferences),
        *(construct.name for construct in bundle.constructs),
        *(construct.official_definition or "" for construct in bundle.constructs),
    ]
    return _normalize("\n".join(part for part in parts if part))


def _match_text(bundle: InstrumentBundle, query: str) -> bool:
    query_normalized = _normalize(query)
    search_blob = _search_blob(bundle)
    if query_normalized in search_blob:
        return True

    identity_names = [_normalize(name) for name in _instrument_identity_names(bundle) if name]
    if any(name and name in query_normalized for name in identity_names):
        return True

    query_tokens = _tokenize_search_terms(query)
    if not query_tokens:
        return False

    identity_tokens = _tokenize_search_terms(" ".join(identity_names))
    identity_overlap = query_tokens & identity_tokens
    if identity_overlap:
        if identity_tokens and identity_tokens.issubset(query_tokens):
            return True
        if len(identity_overlap) >= 2:
            return True
        if any(token in query_tokens for token in identity_tokens if len(token) >= 4):
            return True

    if len(query_tokens) > 4:
        return False

    search_tokens = _tokenize_search_terms(search_blob)
    minimum_overlap = 1 if len(query_tokens) == 1 else 2
    return len(query_tokens & search_tokens) >= minimum_overlap


def _format_suggestions(ref: str, names: Iterable[str]) -> str:
    unique_names = sorted({name for name in names if name})
    close_matches = get_close_matches(ref, unique_names, n=4, cutoff=0.45)
    if not close_matches:
        return ""
    return f". Try one of: {', '.join(close_matches)}"


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
    candidate_names: list[str] = []
    for bundle in repository.instruments.values():
        names = {
            bundle.instrument.id,
            bundle.slug,
            bundle.instrument.canonical_name,
            *bundle.instrument.short_names,
            *bundle.instrument.aliases,
        }
        candidate_names.extend(name for name in names if name)
        if normalized in {_normalize(name) for name in names if name}:
            candidates.append(bundle)
    if not candidates:
        suggestions = _format_suggestions(ref, candidate_names)
        raise KeyError(f"No framework record found for '{ref}'{suggestions}")
    if len(candidates) > 1:
        raise KeyError(f"Reference '{ref}' is ambiguous across {[bundle.instrument.id for bundle in candidates]}")
    return candidates[0]


def resolve_construct(repository: RepositoryData, ref: str):
    normalized = _normalize(ref)
    candidates = []
    candidate_names: list[str] = []
    for bundle in repository.instruments.values():
        for construct in bundle.constructs:
            names = {
                construct.id,
                construct.name,
                construct.short_name or "",
            }
            candidate_names.extend(name for name in names if name)
            if normalized in {_normalize(name) for name in names if name}:
                candidates.append((bundle, construct))
    if not candidates:
        suggestions = _format_suggestions(ref, candidate_names)
        raise KeyError(f"No construct found for '{ref}'{suggestions}")
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


def _framework_reference_payload(bundle: InstrumentBundle) -> dict[str, Any]:
    return {
        "slug": bundle.slug,
        "instrument_id": bundle.instrument.id,
        "canonical_name": bundle.instrument.canonical_name,
        "short_names": bundle.instrument.short_names,
        "aliases": bundle.instrument.aliases,
        "family": bundle.instrument.family,
    }


def _resolve_extension_item(items: list[Any], ref: str, label_fields: tuple[str, ...]) -> Any:
    normalized = _normalize(ref)
    candidates = []
    candidate_names: list[str] = []
    for item in items:
        names = {getattr(item, "id", "")}
        for field_name in label_fields:
            value = getattr(item, field_name, None)
            if isinstance(value, str):
                names.add(value)
        candidate_names.extend(name for name in names if name)
        if normalized in {_normalize(name) for name in names if name}:
            candidates.append(item)
    if not candidates:
        suggestions = _format_suggestions(ref, candidate_names)
        raise KeyError(f"No extension record found for '{ref}'{suggestions}")
    if len(candidates) > 1:
        raise KeyError(
            f"Reference '{ref}' is ambiguous across {[getattr(item, 'id', '(no id)') for item in candidates]}"
        )
    return candidates[0]


def resolve_motif(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.motifs, ref, ("name",))


def resolve_protocol(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.protocols, ref, ("name",))


def resolve_protocol_pack_spec(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.protocol_packs, ref, ("title",))


def resolve_technique(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.techniques, ref, ("name",))


def resolve_contribution_model(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.contribution_models, ref, ("name",))


def resolve_promotion_pathway(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(
        extensions.promotion_registry.promotion_pathways,
        ref,
        ("summary",),
    )


def resolve_interaction_hypothesis(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.interaction_hypotheses, ref, ("summary",))


def resolve_analysis_mode(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.analysis_modes, ref, ("name", "summary"))


def resolve_comparison_shape(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(
        extensions.comparison_shapes,
        ref,
        ("name", "summary", "purpose"),
    )


def resolve_capability(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.capabilities, ref, ("name", "summary", "purpose"))


def resolve_host_profile(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.host_profiles, ref, ("name", "summary", "purpose"))


def resolve_expression_profile(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(
        extensions.expression_profiles,
        ref,
        ("name", "summary", "purpose", "expression_mode"),
    )


def resolve_artifact_class(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.artifact_classes, ref, ("name", "summary"))


def resolve_actualization_protocol(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.actualization_protocols, ref, ("name", "summary"))


def resolve_workflow_recipe(extensions: ExtensionRegistryData, ref: str):
    return _resolve_extension_item(extensions.workflow_recipes, ref, ("name", "summary"))


def agent_orientation(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
) -> dict[str, Any]:
    featured_packs = find_protocol_packs(repository, extensions, featured_only=True)
    framework_refs = [
        _framework_reference_payload(bundle)
        for bundle in sorted(repository.instruments.values(), key=lambda item: item.instrument.canonical_name.lower())
    ]
    return {
        "summary": (
            "A Person Index is a comparative substrate for personhood frameworks. "
            "Match frameworks first, then inspect featured program packs, then trace motifs and interactions."
        ),
        "recommended_sequence": [
            "Use find_framework_records with short refs for distinct framework labels.",
            "Call out unmatched or unindexed frameworks explicitly.",
            "Use list_protocol_packs with featured_only=true before guessing at pack refs.",
            "Use fetch_protocol_pack_summary before fetch_protocol_pack when you need a named program.",
            "Use compare_frameworks, trace_to_motifs, and list_interaction_hypotheses after the framework layer is stable.",
        ],
        "available_framework_refs": framework_refs,
        "featured_program_packs": featured_packs,
        "common_mistakes": [
            "Using one giant text blob as the only framework matching step.",
            "Treating motifs as source truth rather than house synthesis.",
            "Calling fetch_protocol_pack with a vague ref instead of a real program name or ID.",
            "Claiming the repo itself performed person-level inference.",
            "Flattening symbolic systems into empirical claims.",
        ],
        "recommended_resources": [
            "registry://manifest",
            "registry://quickstart",
            "registry://current-state",
            "registry://assessment-workflow",
            "registry://ilens-walkthrough",
        ],
        "recommended_prompts": [
            "registry-arrival",
            "assessment-results-intake",
            "ilens-walkthrough",
        ],
        "advanced_docs": [
            "docs/advanced_modes.md",
            "docs/comparison_shapes.md",
            "docs/capability_model.md",
            "docs/host_profiles.md",
            "docs/expression_model.md",
            "docs/actualization_protocols.md",
            "docs/workflow_recipes.md",
            "docs/expression_and_artifacts.md",
            "docs/multi_subject_comparison.md",
        ],
    }


def _extended_entity_ref(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    entity_type: str,
    entity_id: str,
) -> dict[str, str]:
    if entity_type == "motif":
        motif = next((item for item in extensions.motifs if item.id == entity_id), None)
        if motif is not None:
            return {
                "entity_type": "motif",
                "entity_id": motif.id,
                "label": motif.name,
                "instrument_id": "",
                "instrument_label": "",
                "slug": "",
            }
    return _entity_catalog(repository).get(
        entity_id,
        {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "label": entity_id,
            "instrument_id": "",
            "instrument_label": "",
            "slug": "",
        },
    )


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
                    protocol.program_kind,
                    *protocol.downstream_consumers,
                    *protocol.required_inputs,
                    *protocol.optional_inputs,
                    *protocol.component_program_ids,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(protocol.model_dump(mode="json"))
    return sorted(results, key=lambda item: item["name"].lower())


def protocol_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    protocol = resolve_protocol(extensions, ref)
    techniques_by_id = {technique.id: technique for technique in extensions.techniques}
    programs_by_id = {item.id: item for item in extensions.protocols}
    return {
        "protocol": protocol.model_dump(mode="json"),
        "techniques": [
            techniques_by_id[technique_id].model_dump(mode="json")
            for technique_id in protocol.technique_ids
            if technique_id in techniques_by_id
        ],
        "component_programs": [
            programs_by_id[program_id].model_dump(mode="json")
            for program_id in protocol.component_program_ids
            if program_id in programs_by_id
        ],
    }


def _protocol_pack_target_labels(
    repository: RepositoryData,
    framework_ids: Iterable[str],
    construct_ids: Iterable[str],
) -> list[str]:
    labels: list[str] = []
    for framework_id in framework_ids:
        labels.append(resolve_instrument(repository, framework_id).instrument.canonical_name)
    for construct_id in construct_ids:
        _, construct = resolve_construct(repository, construct_id)
        labels.append(construct.name)
    return labels


def find_protocol_packs(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    *,
    text: str | None = None,
    consumer: str | None = None,
    protocol: str | None = None,
    status: str | None = None,
    featured_only: bool = False,
) -> list[dict[str, Any]]:
    protocol_names = {item.id: item.name for item in extensions.protocols}
    protocol_id_filter = resolve_protocol(extensions, protocol).id if protocol else None
    results: list[dict[str, Any]] = []
    for item in extensions.protocol_packs:
        if consumer and consumer not in item.intended_consumers:
            continue
        if protocol_id_filter and item.protocol_id != protocol_id_filter:
            continue
        if status and item.status != status:
            continue
        if featured_only and not item.featured:
            continue
        target_labels = _protocol_pack_target_labels(
            repository,
            item.target_framework_ids,
            item.target_construct_ids,
        )
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.title,
                    item.summary,
                    item.protocol_id,
                    protocol_names.get(item.protocol_id, ""),
                    *item.intended_consumers,
                    *item.target_framework_ids,
                    *item.target_construct_ids,
                    *target_labels,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(
            {
                **item.model_dump(mode="json"),
                "protocol_name": protocol_names.get(item.protocol_id, item.protocol_id),
                "target_count": len(item.target_framework_ids) + len(item.target_construct_ids),
                "target_labels": target_labels,
            }
        )
    return sorted(
        results,
        key=lambda item: (
            0 if item["featured"] else 1,
            item["title"].lower(),
        ),
    )


def protocol_pack_grammar() -> dict[str, Any]:
    return {
        "id": "protocol_pack_grammar_v0_1",
        "summary": "Canonical grammar for assembling downstream program packs from A Person Index primitives.",
        "required_sections": [
            {
                "section": "pack",
                "required_keys": [
                    "id",
                    "grammar_id",
                    "protocol_id",
                    "protocol_name",
                    "target_count",
                    "target_framework_ids",
                    "target_construct_ids",
                    "target_labels",
                ],
            },
            {
                "section": "protocol",
                "required_keys": [
                    "id",
                    "name",
                    "program_kind",
                    "purpose",
                    "summary",
                    "required_inputs",
                    "primary_outputs",
                ],
            },
            {
                "section": "techniques",
                "required_keys": ["id", "name", "purpose", "summary", "steps", "cautions"],
            },
            {
                "section": "canonical_records",
                "required_keys": ["instrument_id", "canonical_name", "slug", "family", "short_description"],
            },
            {
                "section": "motif_summary",
                "required_keys": ["motif", "mapping_count", "source_labels", "relationship_types"],
            },
            {
                "section": "interaction_hypotheses",
                "required_keys": ["id", "left", "right", "interaction_type", "summary", "protocol_relevance"],
            },
            {
                "section": "input_contract",
                "required_keys": ["required_inputs", "optional_inputs"],
            },
            {
                "section": "output_contract",
                "required_keys": ["primary_outputs"],
            },
            {
                "section": "return_contract",
                "required_keys": ["preferred_contribution_model_ids", "contribution_models", "result_atom_schema"],
            },
        ],
        "construction_rules": [
            "A protocol pack is assembled from existing protocol, technique, mapping, interaction, and research records rather than authored as source truth.",
            "Keep the protocol record authoritative for purpose, inputs, optional inputs, and primary outputs.",
            "Treat protocols as index programs: they compose techniques and may compose smaller programs when the analysis warrants it.",
            "Scope the pack to explicit target frameworks or constructs when possible.",
            "Derive motifs through trace and mapping logic instead of manual motif selection.",
            "Filter interaction hypotheses by both target scope and protocol relevance.",
            "Include the result atom schema when the protocol can consume or emit result-atom level reasoning.",
            "Return contribution models should reflect the protocol's likely feedback channel rather than every possible research model.",
        ],
        "targeting_rules": [
            "Framework targets should expand to their canonical construct set for motif tracing.",
            "Construct targets should keep both construct identity and parent framework identity.",
            "A pack may be protocol-only, but scoped packs are preferred for runtime use.",
        ],
        "authoring_template": {
            "pack": {
                "id": "pack_{protocol_id}__{scope}",
                "grammar_id": "protocol_pack_grammar_v0_1",
                "protocol_id": "{protocol_id}",
                "protocol_name": "{protocol_name}",
                "target_count": "{n}",
                "target_framework_ids": ["instr_example"],
                "target_construct_ids": ["con_example"],
                "target_labels": ["Example Target"],
            },
            "protocol": "{expanded protocol record}",
            "techniques": ["{expanded technique records}"],
            "targets": ["{resolved entity references}"],
            "canonical_records": ["{minimal canonical framework records}"],
            "motif_summary": ["{aggregated motif trace entries}"],
            "relevant_mappings": ["{deduplicated mapping payloads}"],
            "interaction_hypotheses": ["{deduplicated interaction payloads}"],
            "input_contract": {
                "required_inputs": ["{protocol.required_inputs}"],
                "optional_inputs": ["{protocol.optional_inputs}"],
            },
            "execution_order": [
                "resolve canonical scope",
                "expand motif trace",
                "expand interaction hypotheses",
                "apply techniques",
                "emit primary outputs",
                "return structured research feedback",
            ],
            "output_contract": {"primary_outputs": ["{protocol.primary_outputs}"]},
            "return_contract": {
                "preferred_contribution_model_ids": ["rcm_example"],
                "contribution_models": ["{expanded contribution model records}"],
                "result_atom_schema": "{expanded result atom schema or null}",
            },
        },
    }


def _protocol_pack_return_model_ids(protocol_id: str) -> list[str]:
    mapping = {
        "proto_paradox_finder": [
            "rcm_pairwise_relation_judgment",
            "rcm_distilled_observation",
            "rcm_protocol_feedback",
        ],
        "proto_ilens": [
            "rcm_result_atom_bundle",
            "rcm_mapping_vote",
            "rcm_pairwise_relation_judgment",
            "rcm_distilled_observation",
            "rcm_protocol_feedback",
        ],
        "proto_human_model_card": [
            "rcm_result_atom_bundle",
            "rcm_distilled_observation",
            "rcm_protocol_feedback",
        ],
        "proto_translation_memo": [
            "rcm_mapping_vote",
            "rcm_pairwise_relation_judgment",
            "rcm_distilled_observation",
            "rcm_protocol_feedback",
        ],
    }
    return mapping.get(protocol_id, ["rcm_protocol_feedback"])


def _protocol_pack_execution_order(protocol_id: str) -> list[str]:
    common = [
        "Resolve canonical framework records for the current target scope.",
        "Trace target frameworks or constructs through the motif layer.",
        "Expand interaction hypotheses relevant to the scoped targets and selected protocol.",
        "Load the protocol's technique bundle and preserve cautions.",
    ]
    protocol_specific = {
        "proto_paradox_finder": [
            "Scan for tensions, contradictions, and layer mismatches across the available signals.",
            "Separate durable paradoxes from merely context-bound disagreement when evidence allows.",
            "Emit paradox candidates and unresolved tension notes instead of forced synthesis.",
        ],
        "proto_ilens": [
            "Normalize result atoms or equivalent part-level inputs when available.",
            "Preserve contradictions, paradoxes, and layer mismatches rather than averaging them away.",
            "Emit synthesized parameters and caveats.",
        ],
        "proto_human_model_card": [
            "Assemble evidence and provenance into a formal system-modeling frame.",
            "Preserve stable paradoxes, deployment conditions, and failure modes.",
            "Emit the report artifact with explicit caveats and known unknowns.",
        ],
        "proto_translation_memo": [
            "Bracket symbolic versus empirical status before claiming overlap.",
            "Explain overlap, divergence, and incommensurability directly.",
            "Emit mismatch warnings and suggested follow-up mappings.",
        ],
    }
    ending = ["Return structured feedback through the preferred research contribution models."]
    return common + protocol_specific.get(protocol_id, []) + ending


def _minimal_canonical_record(bundle: InstrumentBundle) -> dict[str, Any]:
    return {
        "instrument_id": bundle.instrument.id,
        "canonical_name": bundle.instrument.canonical_name,
        "slug": bundle.slug,
        "family": bundle.instrument.family,
        "short_description": bundle.instrument.short_description,
    }


def _pack_id(protocol_id: str, targets: list[dict[str, str]]) -> str:
    if not targets:
        return f"pack_{protocol_id}"
    scope = "__".join(sorted(target["entity_id"] for target in targets))
    return f"pack_{protocol_id}__{scope}"


def _protocol_pack_summary_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    protocol = payload["protocol"]
    return {
        "pack": payload["pack"],
        "summary": {
            "protocol_name": protocol["name"],
            "protocol_kind": protocol["program_kind"],
            "target_labels": payload["pack"]["target_labels"],
            "target_framework_ids": payload["pack"]["target_framework_ids"],
            "target_construct_ids": payload["pack"]["target_construct_ids"],
            "technique_names": [item["name"] for item in payload["techniques"]],
            "component_program_names": [item["name"] for item in payload["component_programs"]],
            "primary_outputs": payload["output_contract"]["primary_outputs"],
            "required_inputs": payload["input_contract"]["required_inputs"],
            "optional_inputs": payload["input_contract"]["optional_inputs"],
            "execution_order": payload["execution_order"],
            "motif_count": len(payload["motif_summary"]),
            "interaction_hypothesis_count": len(payload["interaction_hypotheses"]),
            "preferred_contribution_model_ids": payload["return_contract"]["preferred_contribution_model_ids"],
            "result_atom_schema_id": (
                payload["return_contract"]["result_atom_schema"]["id"]
                if payload["return_contract"]["result_atom_schema"]
                else None
            ),
        },
    }


def protocol_pack(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    ref: str,
    *,
    framework_refs: Iterable[str] | None = None,
    construct_refs: Iterable[str] | None = None,
) -> dict[str, Any]:
    protocol = resolve_protocol(extensions, ref)
    techniques_by_id = {technique.id: technique for technique in extensions.techniques}
    programs_by_id = {item.id: item for item in extensions.protocols}
    contribution_models_by_id = {
        model.id: model.model_dump(mode="json") for model in extensions.contribution_models
    }

    targets: list[dict[str, str]] = []
    seen_target_ids: set[str] = set()
    target_instrument_ids: set[str] = set()
    traces: list[dict[str, Any]] = []

    for framework_ref in framework_refs or []:
        entity = resolve_entity_reference(repository, framework_ref)
        if entity["entity_type"] != "instrument":
            raise KeyError(f"Framework target '{framework_ref}' did not resolve to an instrument.")
        if entity["entity_id"] not in seen_target_ids:
            targets.append(entity)
            seen_target_ids.add(entity["entity_id"])
        target_instrument_ids.add(entity["instrument_id"])
        traces.append(trace_entity_to_motifs(repository, extensions, framework_ref))

    for construct_ref in construct_refs or []:
        entity = resolve_entity_reference(repository, construct_ref)
        if entity["entity_type"] != "construct":
            raise KeyError(f"Construct target '{construct_ref}' did not resolve to a construct.")
        if entity["entity_id"] not in seen_target_ids:
            targets.append(entity)
            seen_target_ids.add(entity["entity_id"])
        target_instrument_ids.add(entity["instrument_id"])
        traces.append(trace_entity_to_motifs(repository, extensions, construct_ref))

    canonical_records = [
        _minimal_canonical_record(bundle)
        for bundle in sorted(repository.instruments.values(), key=lambda item: item.instrument.canonical_name.lower())
        if bundle.instrument.id in target_instrument_ids
    ]

    motif_summary_by_id: dict[str, dict[str, Any]] = {}
    mappings_by_id: dict[str, dict[str, Any]] = {}
    for trace in traces:
        for item in trace["motif_summary"]:
            motif_id = item["motif"]["id"]
            aggregate = motif_summary_by_id.setdefault(
                motif_id,
                {
                    "motif": item["motif"],
                    "mapping_count": 0,
                    "source_labels": set(),
                    "relationship_types": set(),
                },
            )
            aggregate["mapping_count"] += item["mapping_count"]
            aggregate["source_labels"].update(item["source_labels"])
            aggregate["relationship_types"].update(item["relationship_types"])
            for mapping in item["mappings"]:
                mappings_by_id.setdefault(mapping["id"], mapping)
        for mapping in trace["direct_mappings"]:
            mappings_by_id.setdefault(mapping["id"], mapping)
        for construct_group in trace["construct_mappings"]:
            for mapping in construct_group["mappings"]:
                mappings_by_id.setdefault(mapping["id"], mapping)

    motif_summary = [
        {
            "motif": aggregate["motif"],
            "mapping_count": aggregate["mapping_count"],
            "source_labels": sorted(aggregate["source_labels"]),
            "relationship_types": sorted(aggregate["relationship_types"]),
        }
        for _, aggregate in sorted(
            motif_summary_by_id.items(),
            key=lambda item: item[1]["motif"]["name"].lower(),
        )
    ]
    relevant_mappings = sorted(mappings_by_id.values(), key=lambda item: item["id"])

    interaction_payloads: dict[str, dict[str, Any]] = {}
    if targets:
        for target in targets:
            for item in find_interaction_hypotheses(
                repository,
                extensions,
                related_to=target["entity_id"],
                protocol=protocol.id,
            ):
                interaction_payloads.setdefault(item["id"], item)
    else:
        for item in find_interaction_hypotheses(
            repository,
            extensions,
            protocol=protocol.id,
        ):
            interaction_payloads.setdefault(item["id"], item)

    preferred_contribution_model_ids = _protocol_pack_return_model_ids(protocol.id)
    result_atom_relevant = "result atoms" in {
        *protocol.required_inputs,
        *protocol.optional_inputs,
    } or protocol.id in {"proto_paradox_finder", "proto_ilens", "proto_human_model_card"}

    return {
        "pack": {
            "id": _pack_id(protocol.id, targets),
            "grammar_id": "protocol_pack_grammar_v0_1",
            "protocol_id": protocol.id,
            "protocol_name": protocol.name,
            "target_count": len(targets),
            "target_framework_ids": sorted(target_instrument_ids),
            "target_construct_ids": sorted(
                target["entity_id"] for target in targets if target["entity_type"] == "construct"
            ),
            "target_labels": [target["label"] for target in targets],
        },
        "protocol": protocol.model_dump(mode="json"),
        "techniques": [
            techniques_by_id[technique_id].model_dump(mode="json")
            for technique_id in protocol.technique_ids
            if technique_id in techniques_by_id
        ],
        "component_programs": [
            programs_by_id[program_id].model_dump(mode="json")
            for program_id in protocol.component_program_ids
            if program_id in programs_by_id
        ],
        "targets": targets,
        "canonical_records": canonical_records,
        "motif_summary": motif_summary,
        "relevant_mappings": relevant_mappings,
        "interaction_hypotheses": sorted(
            interaction_payloads.values(),
            key=lambda item: item["id"],
        ),
        "input_contract": {
            "required_inputs": protocol.required_inputs,
            "optional_inputs": protocol.optional_inputs,
        },
        "execution_order": _protocol_pack_execution_order(protocol.id),
        "output_contract": {
            "primary_outputs": protocol.primary_outputs,
        },
        "return_contract": {
            "preferred_contribution_model_ids": preferred_contribution_model_ids,
            "contribution_models": [
                contribution_models_by_id[model_id]
                for model_id in preferred_contribution_model_ids
                if model_id in contribution_models_by_id
            ],
            "result_atom_schema": (
                extensions.result_atom_schema.model_dump(mode="json") if result_atom_relevant else None
            ),
        },
    }


def protocol_pack_summary(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    ref: str,
    *,
    framework_refs: Iterable[str] | None = None,
    construct_refs: Iterable[str] | None = None,
) -> dict[str, Any]:
    return _protocol_pack_summary_from_payload(
        protocol_pack(
            repository,
            extensions,
            ref,
            framework_refs=framework_refs,
            construct_refs=construct_refs,
        )
    )


def curated_protocol_pack_record(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    ref: str,
) -> dict[str, Any]:
    spec = resolve_protocol_pack_spec(extensions, ref)
    payload = protocol_pack(
        repository,
        extensions,
        spec.protocol_id,
        framework_refs=spec.target_framework_ids,
        construct_refs=spec.target_construct_ids,
    )
    return {
        "catalog_entry": {
            **spec.model_dump(mode="json"),
            "protocol_name": resolve_protocol(extensions, spec.protocol_id).name,
            "target_labels": _protocol_pack_target_labels(
                repository,
                spec.target_framework_ids,
                spec.target_construct_ids,
            ),
        },
        "protocol_pack": payload,
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


def research_promotion_registry_record(extensions: ExtensionRegistryData) -> dict[str, Any]:
    registry = extensions.promotion_registry.model_dump(mode="json")
    return {
        "promotion_registry": registry,
        "stage_count": len(extensions.promotion_registry.stages),
        "promotion_pathway_count": len(extensions.promotion_registry.promotion_pathways),
    }


def find_promotion_pathways(
    extensions: ExtensionRegistryData,
    *,
    contribution_model: str | None = None,
    target_layer: str | None = None,
    target_outcome_type: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    contribution_model_id = (
        resolve_contribution_model(extensions, contribution_model).id if contribution_model else None
    )
    contribution_models_by_id = {
        item.id: item.name for item in extensions.contribution_models
    }
    results: list[dict[str, Any]] = []
    for pathway in extensions.promotion_registry.promotion_pathways:
        if contribution_model_id and pathway.contribution_model_id != contribution_model_id:
            continue
        if target_layer and pathway.target_layer != target_layer:
            continue
        if target_outcome_type and pathway.target_outcome_type != target_outcome_type:
            continue
        if text:
            blob = "\n".join(
                [
                    pathway.id,
                    pathway.contribution_model_id,
                    contribution_models_by_id.get(pathway.contribution_model_id, ""),
                    pathway.target_layer,
                    pathway.target_outcome_type,
                    pathway.summary,
                    *pathway.stages,
                    *pathway.evidence_requirements,
                    *pathway.reviewer_questions,
                    *pathway.output_artifacts,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(
            {
                **pathway.model_dump(mode="json"),
                "contribution_model_name": contribution_models_by_id.get(
                    pathway.contribution_model_id,
                    pathway.contribution_model_id,
                ),
            }
        )
    return sorted(results, key=lambda item: item["id"])


def promotion_pathway_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    pathway = resolve_promotion_pathway(extensions, ref)
    contribution_model = resolve_contribution_model(extensions, pathway.contribution_model_id)
    stage_index = {
        stage.id: stage.model_dump(mode="json") for stage in extensions.promotion_registry.stages
    }
    return {
        "promotion_pathway": pathway.model_dump(mode="json"),
        "contribution_model": contribution_model.model_dump(mode="json"),
        "stages": [stage_index[stage_id] for stage_id in pathway.stages if stage_id in stage_index],
    }


def result_atom_schema_record(extensions: ExtensionRegistryData) -> dict[str, Any]:
    return {"result_atom_schema": extensions.result_atom_schema.model_dump(mode="json")}


def _resolve_construct_within_bundle(bundle: InstrumentBundle, ref: str):
    normalized = _normalize(ref)
    candidates = []
    candidate_names: list[str] = []
    for construct in bundle.constructs:
        names = {
            construct.id,
            construct.name,
            construct.short_name or "",
        }
        candidate_names.extend(name for name in names if name)
        if normalized in {_normalize(name) for name in names if name}:
            candidates.append(construct)
    if not candidates:
        suggestions = _format_suggestions(ref, candidate_names)
        raise KeyError(
            f"No construct in framework '{bundle.instrument.canonical_name}' matched '{ref}'{suggestions}"
        )
    if len(candidates) > 1:
        raise KeyError(
            f"Construct reference '{ref}' is ambiguous within '{bundle.instrument.canonical_name}' "
            f"across {[construct.id for construct in candidates]}"
        )
    return candidates[0]


def _normalize_result_atom_value(value: Any) -> tuple[str | None, str | None]:
    if value is None:
        return None, "Missing required output value."
    if isinstance(value, str):
        normalized = value.strip()
        if not normalized:
            return None, "Expected a non-empty output value."
        return normalized, None
    if isinstance(value, (int, float, bool)):
        return str(value), None
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True), None
    return str(value), None


def _normalize_optional_text_field(value: Any, *, field_label: str) -> tuple[str | None, str | None]:
    if value is None:
        return None, None
    if not isinstance(value, str):
        return None, f"Expected {field_label} to be a string."
    normalized = value.strip()
    if not normalized:
        return None, f"Expected {field_label} to be a non-empty string."
    return normalized, None


def _construct_motif_ids(
    extensions: ExtensionRegistryData,
    construct_id: str,
) -> list[str]:
    motif_ids = {
        mapping.target_entity_id
        for mapping in extensions.mappings
        if mapping.source_entity_type == "construct" and mapping.source_entity_id == construct_id
    }
    return sorted(motif_ids)


def normalize_result_atom_bundle(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    *,
    framework: str,
    entries: Iterable[dict[str, Any]] | None = None,
    comparison_shape: str | None = None,
    bundle_label: str | None = None,
    default_source_quality: str | None = None,
    default_timestamp: str | None = None,
    include_motif_trace: bool = True,
) -> dict[str, Any]:
    bundle = resolve_instrument(repository, framework)
    comparison_shape_item = resolve_comparison_shape(extensions, comparison_shape) if comparison_shape else None
    contribution_model = resolve_contribution_model(extensions, "rcm_result_atom_bundle")
    entries = list(entries or [])

    normalized_bundle_label, bundle_label_error = _normalize_optional_text_field(
        bundle_label,
        field_label="bundle label",
    )
    normalized_default_source_quality, source_quality_error = _normalize_optional_text_field(
        default_source_quality,
        field_label="default source quality",
    )
    normalized_default_timestamp, timestamp_error = _normalize_optional_text_field(
        default_timestamp,
        field_label="default timestamp",
    )

    bundle_level_errors = [
        error
        for error in [bundle_label_error, source_quality_error, timestamp_error]
        if error
    ]

    invalid_entries: list[dict[str, Any]] = []
    warnings: list[str] = []
    normalization_records: list[dict[str, Any]] = []
    normalized_atoms: list[dict[str, Any]] = []

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            invalid_entries.append(
                {
                    "entry_index": index,
                    "reason": "Each result atom entry must be an object.",
                }
            )
            continue

        construct_ref = entry.get("construct")
        output_type = entry.get("output_type")
        output_value = entry.get("output_value")

        if not isinstance(construct_ref, str) or not construct_ref.strip():
            invalid_entries.append(
                {
                    "entry_index": index,
                    "reason": "Each entry must include a non-empty 'construct' reference.",
                }
            )
            continue

        if not isinstance(output_type, str) or not output_type.strip():
            invalid_entries.append(
                {
                    "entry_index": index,
                    "construct": construct_ref,
                    "reason": "Each entry must include a non-empty 'output_type'.",
                }
            )
            continue

        normalized_output_value, output_value_error = _normalize_result_atom_value(output_value)
        if output_value_error:
            invalid_entries.append(
                {
                    "entry_index": index,
                    "construct": construct_ref,
                    "reason": output_value_error,
                }
            )
            continue

        try:
            construct = _resolve_construct_within_bundle(bundle, construct_ref)
        except KeyError as error:
            invalid_entries.append(
                {
                    "entry_index": index,
                    "construct": construct_ref,
                    "reason": str(error),
                }
            )
            continue

        confidence, confidence_error = _normalize_optional_text_field(
            entry.get("confidence"),
            field_label="confidence",
        )
        source_quality, entry_source_quality_error = _normalize_optional_text_field(
            entry.get("source_quality"),
            field_label="source quality",
        )
        timestamp, entry_timestamp_error = _normalize_optional_text_field(
            entry.get("timestamp"),
            field_label="timestamp",
        )
        notes, notes_error = _normalize_optional_text_field(
            entry.get("notes"),
            field_label="notes",
        )

        optional_errors = [
            error
            for error in [confidence_error, entry_source_quality_error, entry_timestamp_error, notes_error]
            if error
        ]
        if optional_errors:
            invalid_entries.append(
                {
                    "entry_index": index,
                    "construct": construct_ref,
                    "reason": "; ".join(optional_errors),
                }
            )
            continue

        motif_ids = _construct_motif_ids(extensions, construct.id) if include_motif_trace else []
        if include_motif_trace and not motif_ids:
            warnings.append(
                f"{construct.name} ({construct.id}) has no current construct-to-motif mapping."
            )

        atom: dict[str, Any] = {
            "framework_id": bundle.instrument.id,
            "construct_id": construct.id,
            "output_type": output_type.strip(),
            "output_value": normalized_output_value,
        }
        if confidence:
            atom["confidence"] = confidence
        if source_quality or normalized_default_source_quality:
            atom["source_quality"] = source_quality or normalized_default_source_quality
        if timestamp or normalized_default_timestamp:
            atom["timestamp"] = timestamp or normalized_default_timestamp
        if include_motif_trace and motif_ids:
            atom["mapped_motif_ids"] = motif_ids
        if notes:
            atom["notes"] = notes

        normalized_atoms.append(atom)
        normalization_records.append(
            {
                "entry_index": index,
                "input_construct_ref": construct_ref,
                "resolved_construct": {
                    "id": construct.id,
                    "name": construct.name,
                    "short_name": construct.short_name,
                    "scoring_type": construct.scoring_type,
                },
                "mapped_motif_ids": motif_ids,
                "atom": atom,
            }
        )

    if bundle_level_errors or invalid_entries:
        readiness_status = "invalid"
    elif not entries:
        readiness_status = "needs_entries"
    else:
        readiness_status = "ready"

    next_steps: list[str] = []
    if readiness_status == "needs_entries":
        next_steps.append(
            "Provide at least one construct-level result entry with construct, output_type, and output_value."
        )
    if bundle_level_errors:
        next_steps.extend(bundle_level_errors)
    if invalid_entries:
        next_steps.append("Fix invalid result atom entries before using the bundle downstream.")
    if readiness_status == "ready":
        next_steps.append(
            "Use the normalized bundle as downstream runtime input or as research-safe return traffic, while keeping person-level synthesis outside this repo."
        )
        next_steps.append(
            "If returning this bundle to the research stream, keep framework provenance and source quality attached."
        )

    return {
        "framework": _framework_reference_payload(bundle),
        "comparison_shape": (
            comparison_shape_item.model_dump(mode="json") if comparison_shape_item else None
        ),
        "readiness_status": readiness_status,
        "entry_count": len(entries),
        "normalized_atom_count": len(normalized_atoms),
        "bundle_level_defaults": {
            "bundle_label": normalized_bundle_label,
            "source_quality": normalized_default_source_quality,
            "timestamp": normalized_default_timestamp,
            "include_motif_trace": include_motif_trace,
        },
        "result_atom_schema": extensions.result_atom_schema.model_dump(mode="json"),
        "preferred_contribution_model": contribution_model.model_dump(mode="json"),
        "normalization_records": normalization_records,
        "invalid_entries": invalid_entries,
        "warnings": sorted(set(warnings)),
        "bundle": {
            "contribution_model_id": contribution_model.id,
            "result_atom_schema_id": extensions.result_atom_schema.id,
            "framework_id": bundle.instrument.id,
            "framework_name": bundle.instrument.canonical_name,
            "comparison_shape_id": comparison_shape_item.id if comparison_shape_item else None,
            "comparison_shape_name": comparison_shape_item.name if comparison_shape_item else None,
            "bundle_label": normalized_bundle_label,
            "atom_count": len(normalized_atoms),
            "atoms": normalized_atoms,
        },
        "recommended_tools": [
            "fetch_result_atom_schema",
            "fetch_research_models",
            "fetch_research_promotion_policy",
        ],
        "recommended_resources": [
            "registry://result-atom-normalization",
            "registry://research-promotion",
        ]
        + (["registry://comparison-shapes"] if comparison_shape_item else []),
        "next_steps": next_steps,
    }


def _default_result_atom_output_type(scoring_type: str) -> str:
    if scoring_type == "continuous":
        return "continuous_score"
    if scoring_type == "rank_order_grouping":
        return "ranked_preference"
    return "type_assignment"


def _normalization_hint_for_scoring_type(scoring_type: str) -> str:
    if scoring_type == "continuous":
        return "direct_numeric"
    if scoring_type == "rank_order_grouping":
        return "ranked_preference"
    if scoring_type in {"type_assignment", "categorical_or_best_fit", "bipolar_preference"}:
        return "typed_label"
    return "interpretive_judgment"


def framework_result_shape(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    framework: str,
) -> dict[str, Any]:
    bundle = resolve_instrument(repository, framework)
    construct_payloads: list[dict[str, Any]] = []
    scoring_types: set[str] = set()
    normalization_hints: set[str] = set()
    caution_set: set[str] = set()

    for construct in bundle.constructs:
        motif_ids = _construct_motif_ids(extensions, construct.id)
        scoring_types.add(construct.scoring_type)
        normalization_hint = _normalization_hint_for_scoring_type(construct.scoring_type)
        normalization_hints.add(normalization_hint)

        if normalization_hint == "interpretive_judgment":
            caution_set.add(
                "Some constructs use interpretive or heuristic scoring and still need runtime judgment before normalization."
            )
        if not motif_ids:
            caution_set.add(
                "Some constructs do not yet have house motif mappings, so motif trace will be partial."
            )

        construct_payloads.append(
            {
                "id": construct.id,
                "name": construct.name,
                "short_name": construct.short_name,
                "construct_kind": construct.construct_kind,
                "scoring_type": construct.scoring_type,
                "normalization_hint": normalization_hint,
                "official_definition": construct.official_definition,
                "value_range": construct.value_range.model_dump(mode="json") if construct.value_range else None,
                "polarity": construct.polarity.model_dump(mode="json") if construct.polarity else None,
                "mapped_motif_ids": motif_ids,
                "result_atom_entry_template": {
                    "construct": construct.name,
                    "output_type": _default_result_atom_output_type(construct.scoring_type),
                    "output_value": "<fill>",
                },
            }
        )

    construct_payloads.sort(key=lambda item: item["name"].lower())

    return {
        "framework": _framework_reference_payload(bundle),
        "construct_count": len(construct_payloads),
        "scoring_types": sorted(scoring_types),
        "normalization_hints": sorted(normalization_hints),
        "constructs": construct_payloads,
        "bundle_template": {
            "framework": bundle.instrument.canonical_name,
            "entries": [item["result_atom_entry_template"] for item in construct_payloads],
        },
        "normalization_surface": {
            "tool": "normalize_result_atom_bundle",
            "schema_id": extensions.result_atom_schema.id,
            "preferred_contribution_model_id": "rcm_result_atom_bundle",
            "doc": "docs/result_shape_discovery.md",
        },
        "recommended_tools": [
            "fetch_result_atom_schema",
            "normalize_result_atom_bundle",
            "trace_to_motifs",
        ],
        "recommended_resources": [
            "registry://result-shape-discovery",
            "registry://result-atom-normalization",
        ],
        "cautions": sorted(caution_set),
        "next_steps": [
            "Pick the constructs you actually have outputs for, then fill the starter entry templates.",
            "Use normalize_result_atom_bundle once the construct-level values are ready.",
        ],
    }


def find_analysis_modes(
    extensions: ExtensionRegistryData,
    *,
    text: str | None = None,
) -> list[dict[str, Any]]:
    results = []
    for item in extensions.analysis_modes:
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.summary,
                    item.purpose,
                    *item.intent_signals,
                    *item.preferred_entrypoints,
                    *item.typical_outputs,
                    *item.cautions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def analysis_mode_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_analysis_mode(extensions, ref)
    return {"analysis_mode": item.model_dump(mode="json")}


def find_comparison_shapes(
    extensions: ExtensionRegistryData,
    *,
    mode: str | None = None,
    artifact_class: str | None = None,
    protocol: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    mode_id = resolve_analysis_mode(extensions, mode).id if mode else None
    artifact_id = resolve_artifact_class(extensions, artifact_class).id if artifact_class else None
    protocol_id = resolve_protocol(extensions, protocol).id if protocol else None
    scored_results: list[tuple[int, dict[str, Any]]] = []
    for item in extensions.comparison_shapes:
        if mode_id and mode_id not in item.mode_ids:
            continue
        if artifact_id and artifact_id not in item.suitable_artifact_class_ids:
            continue
        if protocol_id and protocol_id not in item.recommended_protocol_ids:
            continue
        score = 0
        if text:
            score = _text_signal_score(
                text,
                [
                    item.id,
                    item.name,
                    item.summary,
                    item.purpose,
                    *item.mode_ids,
                    *item.intent_signals,
                    *item.required_declarations,
                    *item.optional_declarations,
                    *item.suitable_artifact_class_ids,
                    *item.recommended_protocol_ids,
                    *item.cautions,
                ],
            )
            if score <= 0:
                continue
        scored_results.append((score, item.model_dump(mode="json")))

    if text:
        scored_results.sort(key=lambda entry: (-entry[0], entry[1]["name"].lower()))
    else:
        scored_results.sort(key=lambda entry: entry[1]["name"].lower())
    return [item for _, item in scored_results]


def comparison_shape_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_comparison_shape(extensions, ref)
    suitable_artifact_classes = [
        artifact.model_dump(mode="json")
        for artifact in extensions.artifact_classes
        if artifact.id in item.suitable_artifact_class_ids
    ]
    recommended_protocols = [
        protocol.model_dump(mode="json")
        for protocol in extensions.protocols
        if protocol.id in item.recommended_protocol_ids
    ]
    return {
        "comparison_shape": item.model_dump(mode="json"),
        "suitable_artifact_classes": suitable_artifact_classes,
        "recommended_protocols": recommended_protocols,
    }


def _normalize_declaration_value(value: Any, value_kind: str) -> tuple[Any | None, str | None]:
    if value_kind == "string":
        if not isinstance(value, str):
            return None, "Expected a string value."
        normalized = value.strip()
        if not normalized:
            return None, "Expected a non-empty string value."
        return normalized, None

    if value_kind == "string_list":
        if isinstance(value, str):
            normalized_items = [
                item.strip()
                for item in re.split(r"\s*\|\s*|,", value)
                if item.strip()
            ]
        elif isinstance(value, list):
            normalized_items = [
                item.strip()
                for item in value
                if isinstance(item, str) and item.strip()
            ]
            if len(normalized_items) != len(value):
                return None, "Expected a list of non-empty strings."
        else:
            return None, "Expected a string or list of strings."

        if not normalized_items:
            return None, "Expected at least one non-empty string."
        return normalized_items, None

    return None, f"Unsupported declaration value kind '{value_kind}'."


def prepare_comparison_run(
    extensions: ExtensionRegistryData,
    *,
    comparison_shape: str,
    declarations: dict[str, Any] | None = None,
    capability_refs: Iterable[str] | None = None,
    host_profile_refs: Iterable[str] | None = None,
) -> dict[str, Any]:
    shape = resolve_comparison_shape(extensions, comparison_shape)
    declarations = declarations or {}
    host_profile_items, capability_items = _resolve_declared_host_context(
        extensions,
        capability_refs=capability_refs,
        host_profile_refs=host_profile_refs,
    )

    normalized_declarations: dict[str, Any] = {}
    invalid_fields: list[dict[str, str]] = []
    missing_required_fields: list[dict[str, Any]] = []
    unexpected_fields = sorted(
        key for key in declarations if key not in {field.id for field in shape.declaration_fields}
    )

    for field in shape.declaration_fields:
        if field.id not in declarations:
            if field.required:
                missing_required_fields.append(field.model_dump(mode="json"))
            continue
        normalized_value, error = _normalize_declaration_value(
            declarations[field.id],
            field.value_kind,
        )
        if error:
            invalid_fields.append(
                {
                    "field_id": field.id,
                    "label": field.label,
                    "reason": error,
                }
            )
            continue
        normalized_declarations[field.id] = normalized_value

    if invalid_fields:
        readiness_status = "invalid"
    elif missing_required_fields:
        readiness_status = "needs_declarations"
    else:
        readiness_status = "ready"

    path_recommendation = None
    if readiness_status == "ready":
        primary_mode_ref = shape.mode_ids[0] if shape.mode_ids else None
        path_recommendation = recommend_next_path(
            extensions,
            run_mode=primary_mode_ref,
            comparison_shape=shape.id,
            capability_refs=[item.id for item in capability_items],
            host_profile_refs=[item.id for item in host_profile_items],
        )

    next_steps: list[str] = []
    if missing_required_fields:
        labels = ", ".join(field["label"] for field in missing_required_fields)
        next_steps.append(f"Declare the missing required comparison fields: {labels}.")
    if invalid_fields:
        labels = ", ".join(item["label"] for item in invalid_fields)
        next_steps.append(f"Fix invalid comparison field values: {labels}.")
    if unexpected_fields:
        next_steps.append(
            "Remove or rename declarations that are not part of this comparison shape: "
            + ", ".join(unexpected_fields)
            + "."
        )
    if readiness_status == "ready" and not capability_items:
        next_steps.append("Declare host capabilities before choosing the final artifact and workflow path.")
    elif readiness_status == "ready":
        next_steps.append(
            "Use the recommended artifact, expression, workflow, and actualization path, then prepare the concrete artifact realization scaffold."
        )

    suitable_artifact_classes = [
        artifact.model_dump(mode="json")
        for artifact in extensions.artifact_classes
        if artifact.id in shape.suitable_artifact_class_ids
    ]
    recommended_protocols = [
        protocol.model_dump(mode="json")
        for protocol in extensions.protocols
        if protocol.id in shape.recommended_protocol_ids
    ]

    return {
        "comparison_shape": shape.model_dump(mode="json"),
        "readiness_status": readiness_status,
        "declared_host_profiles": [item.model_dump(mode="json") for item in host_profile_items],
        "declared_capabilities": [item.model_dump(mode="json") for item in capability_items],
        "declaration_fields": [field.model_dump(mode="json") for field in shape.declaration_fields],
        "provided_declarations": normalized_declarations,
        "missing_required_fields": missing_required_fields,
        "invalid_fields": invalid_fields,
        "unexpected_fields": unexpected_fields,
        "suitable_artifact_classes": suitable_artifact_classes,
        "recommended_protocols": recommended_protocols,
        "path_recommendation": path_recommendation,
        "recommended_tools": [
            "fetch_comparison_shape",
            "list_capabilities",
            "recommend_next_path",
        ],
        "recommended_resources": [
            "registry://comparison-shapes",
            "registry://comparison-preflight",
            "registry://capability-model",
        ],
        "next_steps": next_steps,
    }


def find_capabilities(
    extensions: ExtensionRegistryData,
    *,
    kind: str | None = None,
    artifact_class: str | None = None,
    actualization_protocol: str | None = None,
    include_optional: bool = True,
    text: str | None = None,
) -> list[dict[str, Any]]:
    artifact_id = resolve_artifact_class(extensions, artifact_class).id if artifact_class else None
    actualization_id = (
        resolve_actualization_protocol(extensions, actualization_protocol).id
        if actualization_protocol
        else None
    )
    results = []
    for item in extensions.capabilities:
        if kind and _normalize(kind) != _normalize(item.capability_kind):
            continue
        if artifact_id:
            matching_artifact = next(
                (artifact for artifact in extensions.artifact_classes if artifact.id == artifact_id),
                None,
            )
            if matching_artifact is None:
                continue
            capability_ids = list(matching_artifact.required_capability_ids)
            if include_optional:
                capability_ids.extend(matching_artifact.optional_capability_ids)
            if item.id not in capability_ids:
                continue
        if actualization_id:
            matching_actualization = next(
                (
                    protocol
                    for protocol in extensions.actualization_protocols
                    if protocol.id == actualization_id
                ),
                None,
            )
            if matching_actualization is None:
                continue
            capability_ids = list(matching_actualization.required_capability_ids)
            if include_optional:
                capability_ids.extend(matching_actualization.optional_capability_ids)
            if item.id not in capability_ids:
                continue
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.capability_kind,
                    item.summary,
                    item.purpose,
                    *item.detection_questions,
                    *item.typical_tool_signals,
                    *item.cautions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def capability_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_capability(extensions, ref)
    used_by_artifact_classes = [
        artifact.model_dump(mode="json")
        for artifact in extensions.artifact_classes
        if item.id in {*artifact.required_capability_ids, *artifact.optional_capability_ids}
    ]
    used_by_host_profiles = [
        profile.model_dump(mode="json")
        for profile in extensions.host_profiles
        if item.id in profile.capability_ids
    ]
    used_by_actualization_protocols = [
        protocol.model_dump(mode="json")
        for protocol in extensions.actualization_protocols
        if item.id in {*protocol.required_capability_ids, *protocol.optional_capability_ids}
    ]
    return {
        "capability": item.model_dump(mode="json"),
        "used_by_host_profiles": used_by_host_profiles,
        "used_by_artifact_classes": used_by_artifact_classes,
        "used_by_actualization_protocols": used_by_actualization_protocols,
    }


def find_host_profiles(
    extensions: ExtensionRegistryData,
    *,
    host_kind: str | None = None,
    capability: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    capability_id = resolve_capability(extensions, capability).id if capability else None
    normalized_kind = _normalize(host_kind) if host_kind else None
    results = []
    for item in extensions.host_profiles:
        if normalized_kind and normalized_kind not in {
            _normalize(item.host_kind),
            _normalize(item.id),
            _normalize(item.name),
        }:
            continue
        if capability_id and capability_id not in item.capability_ids:
            continue
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.host_kind,
                    item.summary,
                    item.purpose,
                    *item.capability_ids,
                    *item.known_tool_signals,
                    *item.cautions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def host_profile_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_host_profile(extensions, ref)
    capabilities = [
        resolve_capability(extensions, capability_id).model_dump(mode="json")
        for capability_id in item.capability_ids
    ]
    supported_artifact_classes = [
        artifact.model_dump(mode="json")
        for artifact in extensions.artifact_classes
        if set(artifact.required_capability_ids).issubset(set(item.capability_ids))
    ]
    return {
        "host_profile": item.model_dump(mode="json"),
        "capabilities": capabilities,
        "supported_artifact_classes": supported_artifact_classes,
    }


def _resolve_declared_host_context(
    extensions: ExtensionRegistryData,
    *,
    capability_refs: Iterable[str] | None = None,
    host_profile_refs: Iterable[str] | None = None,
) -> tuple[list[Any], list[Any]]:
    host_profile_items = [resolve_host_profile(extensions, ref) for ref in host_profile_refs or []]
    capability_by_id: dict[str, Any] = {}
    for profile in host_profile_items:
        for capability_id in profile.capability_ids:
            capability_by_id.setdefault(capability_id, resolve_capability(extensions, capability_id))
    for ref in capability_refs or []:
        item = resolve_capability(extensions, ref)
        capability_by_id[item.id] = item
    return host_profile_items, list(capability_by_id.values())


def find_expression_profiles(
    extensions: ExtensionRegistryData,
    *,
    mode: str | None = None,
    audience: str | None = None,
    artifact_class: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    artifact = resolve_artifact_class(extensions, artifact_class) if artifact_class else None
    requested_mode = _normalize(mode) if mode else None
    results = []
    for item in extensions.expression_profiles:
        if requested_mode and requested_mode not in {
            _normalize(item.expression_mode),
            _normalize(item.id),
            _normalize(item.name),
        }:
            continue
        if audience and _normalize(audience) not in {_normalize(entry) for entry in item.audience_modes}:
            continue
        if artifact and item.expression_mode != artifact.default_expression_mode:
            continue
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.expression_mode,
                    item.summary,
                    item.purpose,
                    *item.audience_modes,
                    *item.visible_by_default,
                    *item.keep_implicit_by_default,
                    *item.good_for,
                    *item.cautions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: (entry["expression_mode"], entry["name"].lower()))


def expression_profile_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_expression_profile(extensions, ref)
    default_for_artifact_classes = [
        artifact.model_dump(mode="json")
        for artifact in extensions.artifact_classes
        if artifact.default_expression_mode == item.expression_mode
    ]
    return {
        "expression_profile": item.model_dump(mode="json"),
        "default_for_artifact_classes": default_for_artifact_classes,
    }


def find_artifact_classes(
    extensions: ExtensionRegistryData,
    *,
    mode: str | None = None,
    capability: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    mode_id = resolve_analysis_mode(extensions, mode).id if mode else None
    capability_id = resolve_capability(extensions, capability).id if capability else None
    results = []
    for item in extensions.artifact_classes:
        if mode_id and mode_id not in item.suitable_mode_ids:
            continue
        if capability_id and capability_id not in {
            *item.required_capability_ids,
            *item.optional_capability_ids,
        }:
            continue
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.summary,
                    item.default_expression_mode,
                    *item.audience_modes,
                    *item.suitable_mode_ids,
                    *item.required_evidence_partitions,
                    *item.required_capability_ids,
                    *item.optional_capability_ids,
                    *item.typical_forms,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def artifact_class_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_artifact_class(extensions, ref)
    default_expression_profile = next(
        (
            profile.model_dump(mode="json")
            for profile in extensions.expression_profiles
            if profile.expression_mode == item.default_expression_mode
        ),
        None,
    )
    return {
        "artifact_class": item.model_dump(mode="json"),
        "default_expression_profile": default_expression_profile,
    }


def find_actualization_protocols(
    extensions: ExtensionRegistryData,
    *,
    run_mode: str | None = None,
    artifact_class: str | None = None,
    capability: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    mode_id = resolve_analysis_mode(extensions, run_mode).id if run_mode else None
    artifact_id = resolve_artifact_class(extensions, artifact_class).id if artifact_class else None
    capability_id = resolve_capability(extensions, capability).id if capability else None
    results = []
    for item in extensions.actualization_protocols:
        if mode_id and mode_id not in item.run_mode_ids:
            continue
        if artifact_id and artifact_id not in item.target_artifact_class_ids:
            continue
        if capability_id and capability_id not in {
            *item.required_capability_ids,
            *item.optional_capability_ids,
        }:
            continue
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.summary,
                    *item.run_mode_ids,
                    *item.protocol_ids,
                    *item.target_artifact_class_ids,
                    *item.required_capability_ids,
                    *item.optional_capability_ids,
                    *item.steps,
                    *item.cautions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def actualization_protocol_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_actualization_protocol(extensions, ref)
    return {"actualization_protocol": item.model_dump(mode="json")}


def find_workflow_recipes(
    extensions: ExtensionRegistryData,
    *,
    run_mode: str | None = None,
    artifact_class: str | None = None,
    actualization_protocol: str | None = None,
    expression_profile: str | None = None,
    capability: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    mode_id = resolve_analysis_mode(extensions, run_mode).id if run_mode else None
    artifact_id = resolve_artifact_class(extensions, artifact_class).id if artifact_class else None
    actualization_id = (
        resolve_actualization_protocol(extensions, actualization_protocol).id
        if actualization_protocol
        else None
    )
    expression_id = (
        resolve_expression_profile(extensions, expression_profile).id
        if expression_profile
        else None
    )
    capability_id = resolve_capability(extensions, capability).id if capability else None
    results = []
    for item in extensions.workflow_recipes:
        if mode_id and mode_id not in item.run_mode_ids:
            continue
        if artifact_id and item.artifact_class_id != artifact_id:
            continue
        if actualization_id and item.actualization_protocol_id != actualization_id:
            continue
        if expression_id and item.expression_profile_id != expression_id:
            continue
        if capability_id and capability_id not in item.required_capability_ids:
            continue
        if text:
            blob = "\n".join(
                [
                    item.id,
                    item.name,
                    item.summary,
                    item.artifact_class_id,
                    item.expression_profile_id,
                    item.actualization_protocol_id,
                    *item.run_mode_ids,
                    *item.required_capability_ids,
                    *(block.label for block in item.realization_blocks),
                    *(block.summary for block in item.realization_blocks),
                    *item.recipe_steps,
                    *item.deliverables,
                    *item.cautions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(item.model_dump(mode="json"))
    return sorted(results, key=lambda entry: entry["name"].lower())


def workflow_recipe_record(extensions: ExtensionRegistryData, ref: str) -> dict[str, Any]:
    item = resolve_workflow_recipe(extensions, ref)
    artifact = resolve_artifact_class(extensions, item.artifact_class_id)
    expression = resolve_expression_profile(extensions, item.expression_profile_id)
    actualization = resolve_actualization_protocol(extensions, item.actualization_protocol_id)
    return {
        "workflow_recipe": item.model_dump(mode="json"),
        "artifact_class": artifact.model_dump(mode="json"),
        "expression_profile": expression.model_dump(mode="json"),
        "actualization_protocol": actualization.model_dump(mode="json"),
    }


def _select_realization_form(
    artifact: ArtifactClass,
    recipe: WorkflowRecipe,
    capability_ids: set[str],
) -> str | None:
    candidate_forms: list[str] = []
    for value in [*recipe.deliverables, *artifact.typical_forms]:
        if value not in candidate_forms:
            candidate_forms.append(value)

    def _first_matching(*needles: str) -> str | None:
        for item in candidate_forms:
            normalized = _normalize(item)
            if any(needle in normalized for needle in needles):
                return item
        return None

    if "cap_json_emit" in capability_ids:
        match = _first_matching("json", "bundle")
        if match:
            return match
    if "cap_spreadsheet_render" in capability_ids:
        match = _first_matching("spreadsheet")
        if match:
            return match
    if "cap_pdf_render" in capability_ids:
        match = _first_matching("pdf")
        if match:
            return match
    if "cap_table_render" in capability_ids:
        match = _first_matching("table", "matrix", "sheet")
        if match:
            return match
    if "cap_file_write" in capability_ids:
        match = _first_matching("handoff", "repo artifact", "markdown handoff")
        if match:
            return match
    if "cap_markdown_write" in capability_ids:
        match = _first_matching("markdown", "memo", "card")
        if match:
            return match
    return candidate_forms[0] if candidate_forms else None


def prepare_artifact_realization(
    extensions: ExtensionRegistryData,
    *,
    workflow_recipe: str,
    capability_refs: Iterable[str] | None = None,
    host_profile_refs: Iterable[str] | None = None,
) -> dict[str, Any]:
    recipe = resolve_workflow_recipe(extensions, workflow_recipe)
    artifact = resolve_artifact_class(extensions, recipe.artifact_class_id)
    expression = resolve_expression_profile(extensions, recipe.expression_profile_id)
    actualization = resolve_actualization_protocol(extensions, recipe.actualization_protocol_id)
    host_profile_items, capability_items = _resolve_declared_host_context(
        extensions,
        capability_refs=capability_refs,
        host_profile_refs=host_profile_refs,
    )
    capability_id_set = {item.id for item in capability_items}
    missing_required_capability_ids = sorted(
        capability_id
        for capability_id in recipe.required_capability_ids
        if capability_id not in capability_id_set
    )
    if not capability_items:
        readiness_status = "needs_capabilities"
    elif missing_required_capability_ids:
        readiness_status = "partial"
    else:
        readiness_status = "ready"

    selected_realization_form = _select_realization_form(artifact, recipe, capability_id_set)
    next_steps: list[str] = []
    if missing_required_capability_ids:
        missing_labels = ", ".join(
            resolve_capability(extensions, capability_id).name
            for capability_id in missing_required_capability_ids
        )
        next_steps.append(
            f"Declare or acquire the missing workflow capabilities before full realization: {missing_labels}."
        )
    else:
        next_steps.append("Populate the required realization blocks in order before polishing the final output.")
    if selected_realization_form:
        next_steps.append(f"Use {selected_realization_form} as the primary realization form in this host.")

    return {
        "workflow_recipe": recipe.model_dump(mode="json"),
        "artifact_class": artifact.model_dump(mode="json"),
        "expression_profile": expression.model_dump(mode="json"),
        "actualization_protocol": actualization.model_dump(mode="json"),
        "declared_host_profiles": [item.model_dump(mode="json") for item in host_profile_items],
        "declared_capabilities": [item.model_dump(mode="json") for item in capability_items],
        "readiness_status": readiness_status,
        "missing_required_capability_ids": missing_required_capability_ids,
        "selected_realization_form": selected_realization_form,
        "realization_blocks": [block.model_dump(mode="json") for block in recipe.realization_blocks],
        "required_evidence_partitions": artifact.required_evidence_partitions,
        "deliverables": recipe.deliverables,
        "recommended_tools": [
            "fetch_workflow_recipe",
            "fetch_artifact_class",
            "fetch_expression_profile",
            "fetch_actualization_protocol",
            "prepare_artifact_template",
        ],
        "recommended_resources": [
            "registry://workflow-recipes",
            "registry://artifact-realization",
            "registry://artifact-templates",
            "registry://expression-and-artifacts",
            "registry://actualization-protocols",
        ],
        "next_steps": next_steps,
    }


def _template_kind_for_form(selected_realization_form: str | None) -> str:
    normalized = _normalize(selected_realization_form or "")
    if "json" in normalized or "bundle" in normalized:
        return "json_object"
    return "markdown_document"


def _template_filename_hint(recipe: WorkflowRecipe, template_kind: str) -> str:
    stem = re.sub(r"[^a-z0-9]+", "_", recipe.name.lower()).strip("_")
    if template_kind == "json_object":
        return f"{stem}.json"
    return f"{stem}.md"


def _markdown_block_template(
    block: dict[str, Any],
    *,
    required_evidence_partitions: list[str],
) -> str:
    label = block["label"]
    summary = block["summary"]
    block_kind = block["block_kind"]
    lines = [f"## {label}", f"<!-- {summary} -->"]
    if block_kind == "metadata":
        lines.extend(
            [
                "- TODO: scope",
                "- TODO: intended use",
                "- TODO: key declarations or labels",
            ]
        )
    elif block_kind == "narrative":
        lines.append("[Write the grounded narrative for this block here.]")
    elif block_kind == "list":
        lines.extend(
            [
                "- TODO: item 1",
                "- TODO: item 2",
                "- TODO: item 3",
            ]
        )
    elif block_kind == "caveat":
        lines.extend(
            [
                "- TODO: missingness",
                "- TODO: confidence limits",
                "- TODO: overread risk",
            ]
        )
    elif block_kind == "provenance":
        for partition in required_evidence_partitions:
            lines.append(f"- {partition}: []")
    elif block_kind == "matrix":
        lines.extend(
            [
                "| Comparative Axis | Slice A | Slice B | Notes |",
                "| --- | --- | --- | --- |",
                "| TODO | TODO | TODO | TODO |",
            ]
        )
    elif block_kind == "bundle":
        lines.extend(
            [
                "```json",
                "{",
                '  "TODO": "Add the structured machine-readable payload for this block."',
                "}",
                "```",
            ]
        )
    else:
        lines.append("[Populate this block here.]")
    return "\n".join(lines)


def _json_block_template(
    block: dict[str, Any],
    *,
    required_evidence_partitions: list[str],
) -> Any:
    block_kind = block["block_kind"]
    if block_kind == "metadata":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "value": None,
        }
    if block_kind == "narrative":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "content": "",
        }
    if block_kind == "list":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "items": [],
        }
    if block_kind == "caveat":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "items": [],
        }
    if block_kind == "provenance":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "partitions": {partition: [] for partition in required_evidence_partitions},
        }
    if block_kind == "matrix":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "columns": ["comparative_axis", "left", "right", "notes"],
            "rows": [],
        }
    if block_kind == "bundle":
        return {
            "label": block["label"],
            "summary": block["summary"],
            "content": {},
        }
    return {
        "label": block["label"],
        "summary": block["summary"],
        "content": None,
    }


def prepare_artifact_template(
    extensions: ExtensionRegistryData,
    *,
    workflow_recipe: str,
    capability_refs: Iterable[str] | None = None,
    host_profile_refs: Iterable[str] | None = None,
) -> dict[str, Any]:
    realization = prepare_artifact_realization(
        extensions,
        workflow_recipe=workflow_recipe,
        capability_refs=capability_refs,
        host_profile_refs=host_profile_refs,
    )
    recipe = realization["workflow_recipe"]
    template_kind = _template_kind_for_form(realization["selected_realization_form"])
    filename_hint = _template_filename_hint(
        resolve_workflow_recipe(extensions, workflow_recipe),
        template_kind,
    )
    template_sections = [
        {
            "id": block["id"],
            "label": block["label"],
            "block_kind": block["block_kind"],
            "required": block["required"],
            "summary": block["summary"],
        }
        for block in realization["realization_blocks"]
    ]

    template_text = None
    template_object = None
    if template_kind == "markdown_document":
        section_text = [
            f"# {recipe['name']}",
            "",
            f"<!-- Selected realization form: {realization['selected_realization_form'] or 'markdown'} -->",
            f"<!-- Artifact class: {realization['artifact_class']['name']} -->",
            "",
        ]
        for block in realization["realization_blocks"]:
            section_text.append(
                _markdown_block_template(
                    block,
                    required_evidence_partitions=realization["required_evidence_partitions"],
                )
            )
            section_text.append("")
        template_text = "\n".join(section_text).rstrip() + "\n"
    else:
        template_object = {
            "template_meta": {
                "workflow_recipe_id": recipe["id"],
                "workflow_recipe_name": recipe["name"],
                "artifact_class_id": realization["artifact_class"]["id"],
                "expression_profile_id": realization["expression_profile"]["id"],
                "actualization_protocol_id": realization["actualization_protocol"]["id"],
                "selected_realization_form": realization["selected_realization_form"],
            },
            "required_evidence_partitions": realization["required_evidence_partitions"],
            "block_order": [block["id"] for block in realization["realization_blocks"]],
            "blocks": {
                block["id"]: _json_block_template(
                    block,
                    required_evidence_partitions=realization["required_evidence_partitions"],
                )
                for block in realization["realization_blocks"]
            },
        }

    next_steps = list(realization["next_steps"])
    next_steps.append("Replace placeholders with grounded comparative content before final delivery.")

    return {
        **realization,
        "template_kind": template_kind,
        "template_filename_hint": filename_hint,
        "template_sections": template_sections,
        "template_text": template_text,
        "template_object": template_object,
        "recommended_tools": [
            "prepare_artifact_realization",
            "fetch_workflow_recipe",
            "fetch_artifact_class",
        ],
        "recommended_resources": [
            "registry://artifact-realization",
            "registry://artifact-templates",
            "registry://expression-and-artifacts",
        ],
        "next_steps": next_steps,
    }


def _text_signal_score(text: str, parts: Iterable[str]) -> int:
    normalized_text = _normalize(text)
    text_tokens = _tokenize_search_terms(text)
    score = 0
    for raw_part in parts:
        part = raw_part.strip()
        if not part:
            continue
        normalized_part = _normalize(part)
        if not normalized_part:
            continue
        if normalized_part in normalized_text or normalized_text in normalized_part:
            score += 100
            continue
        part_tokens = _tokenize_search_terms(part)
        overlap = text_tokens & part_tokens
        if overlap:
            score += len(overlap) * 10
    return score


def _recommended_mode_candidates(
    extensions: ExtensionRegistryData,
    text: str,
) -> list[dict[str, Any]]:
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in extensions.analysis_modes:
        score = _text_signal_score(
            text,
            [
                item.name,
                item.summary,
                item.purpose,
                *item.intent_signals,
                *item.typical_outputs,
            ],
        )
        if score <= 0:
            continue
        scored.append((score, item.model_dump(mode="json")))
    scored.sort(key=lambda entry: (-entry[0], entry[1]["name"].lower()))
    return [item for _, item in scored]


def _recommended_comparison_shape_candidates(
    extensions: ExtensionRegistryData,
    mode_id: str,
    text: str,
) -> list[dict[str, Any]]:
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in extensions.comparison_shapes:
        if mode_id not in item.mode_ids:
            continue
        score = _text_signal_score(
            text,
            [
                item.name,
                item.summary,
                item.purpose,
                *item.intent_signals,
                *(field.label for field in item.declaration_fields),
                *(field.summary for field in item.declaration_fields),
                *(example for field in item.declaration_fields for example in field.examples),
                *item.required_declarations,
            ],
        )
        if score <= 0:
            continue
        scored.append((score, item.model_dump(mode="json")))
    scored.sort(key=lambda entry: (-entry[0], entry[1]["name"].lower()))
    return [item for _, item in scored]


def recommend_next_path(
    extensions: ExtensionRegistryData,
    *,
    run_mode: str | None = None,
    comparison_shape: str | None = None,
    capability_refs: Iterable[str] | None = None,
    host_profile_refs: Iterable[str] | None = None,
    artifact_class: str | None = None,
    text: str | None = None,
) -> dict[str, Any]:
    host_profile_items, capability_items = _resolve_declared_host_context(
        extensions,
        capability_refs=capability_refs,
        host_profile_refs=host_profile_refs,
    )
    capability_id_set = {item.id for item in capability_items}

    notes: list[str] = []
    inferred_mode = False
    inferred_comparison_shape = False
    mode_item = None
    mode_candidates: list[dict[str, Any]] = []
    explicit_comparison_shape = (
        resolve_comparison_shape(extensions, comparison_shape)
        if comparison_shape
        else None
    )
    if run_mode:
        mode_item = resolve_analysis_mode(extensions, run_mode)
        mode_candidates = [mode_item.model_dump(mode="json")]
    elif explicit_comparison_shape and explicit_comparison_shape.mode_ids:
        mode_item = resolve_analysis_mode(extensions, explicit_comparison_shape.mode_ids[0])
        mode_candidates = [mode_item.model_dump(mode="json")]
        inferred_mode = True
        notes.append("Run mode was derived from the declared comparison shape.")
    elif text:
        mode_candidates = _recommended_mode_candidates(extensions, text)
        if mode_candidates:
            mode_item = resolve_analysis_mode(extensions, mode_candidates[0]["id"])
            inferred_mode = True
            notes.append("Run mode was inferred from the provided text rather than explicitly declared.")
    if mode_item is None:
        mode_item = resolve_analysis_mode(extensions, "Run Planning")
        inferred_mode = True
        notes.append("No run mode was provided, so the recommendation defaults to Run Planning.")

    comparison_shape_candidates: list[dict[str, Any]] = []
    comparison_shape_item = None
    if explicit_comparison_shape is not None:
        comparison_shape_item = explicit_comparison_shape
        comparison_shape_candidates = [comparison_shape_item.model_dump(mode="json")]
    elif text and mode_item.id == "mode_contextual_comparison":
        comparison_shape_candidates = _recommended_comparison_shape_candidates(
            extensions,
            mode_item.id,
            text,
        )
        if comparison_shape_candidates:
            comparison_shape_item = resolve_comparison_shape(extensions, comparison_shape_candidates[0]["id"])
            inferred_comparison_shape = True
            notes.append("Comparison shape was inferred from the provided text.")

    explicit_artifact = resolve_artifact_class(extensions, artifact_class) if artifact_class else None

    artifact_candidates = []
    for item in extensions.artifact_classes:
        if mode_item.id not in item.suitable_mode_ids:
            continue
        if comparison_shape_item and item.id not in comparison_shape_item.suitable_artifact_class_ids:
            continue
        if explicit_artifact and item.id != explicit_artifact.id:
            continue
        if text:
            text_bonus = _text_signal_score(
                text,
                [
                    item.id,
                    item.name,
                    item.summary,
                    *item.typical_forms,
                    *((item.notes or "").splitlines()),
                ],
            )
        else:
            text_bonus = 0
        missing_required = sorted(set(item.required_capability_ids) - capability_id_set)
        satisfied_required = sorted(set(item.required_capability_ids) & capability_id_set)
        satisfied_optional = sorted(set(item.optional_capability_ids) & capability_id_set)
        score = (
            (100 if not missing_required else 0)
            + len(satisfied_required) * 10
            + len(satisfied_optional) * 3
            + text_bonus
            + (25 if explicit_artifact and item.id == explicit_artifact.id else 0)
        )
        artifact_candidates.append(
            {
                "artifact_class": item.model_dump(mode="json"),
                "fit_status": "ready" if not missing_required else "partial",
                "missing_required_capability_ids": missing_required,
                "satisfied_capability_ids": satisfied_required,
                "satisfied_optional_capability_ids": satisfied_optional,
                "score": score,
            }
        )
    artifact_candidates.sort(
        key=lambda item: (
            0 if item["fit_status"] == "ready" else 1,
            len(item["missing_required_capability_ids"]),
            -item["score"],
            item["artifact_class"]["name"].lower(),
        )
    )
    recommended_artifact = artifact_candidates[0] if artifact_candidates else None
    expression_candidates = []
    if recommended_artifact is not None:
        expression_candidates = find_expression_profiles(
            extensions,
            mode=recommended_artifact["artifact_class"]["default_expression_mode"],
        )

    actualization_candidates = []
    if recommended_artifact is not None:
        for item in extensions.actualization_protocols:
            if mode_item.id not in item.run_mode_ids:
                continue
            if comparison_shape_item and not (
                set(item.protocol_ids) & set(comparison_shape_item.recommended_protocol_ids)
            ):
                continue
            if recommended_artifact["artifact_class"]["id"] not in item.target_artifact_class_ids:
                continue
            missing_required = sorted(set(item.required_capability_ids) - capability_id_set)
            satisfied_required = sorted(set(item.required_capability_ids) & capability_id_set)
            satisfied_optional = sorted(set(item.optional_capability_ids) & capability_id_set)
            score = (
                (100 if not missing_required else 0)
                + len(satisfied_required) * 10
                + len(satisfied_optional) * 3
            )
            actualization_candidates.append(
                {
                    "actualization_protocol": item.model_dump(mode="json"),
                    "fit_status": "ready" if not missing_required else "partial",
                    "missing_required_capability_ids": missing_required,
                    "satisfied_capability_ids": satisfied_required,
                    "satisfied_optional_capability_ids": satisfied_optional,
                    "score": score,
                }
            )
        actualization_candidates.sort(
            key=lambda item: (
                0 if item["fit_status"] == "ready" else 1,
                len(item["missing_required_capability_ids"]),
                -item["score"],
                item["actualization_protocol"]["name"].lower(),
            )
        )

    recommended_expression = expression_candidates[0] if expression_candidates else None
    recommended_actualization = actualization_candidates[0] if actualization_candidates else None
    workflow_candidates = []
    if (
        recommended_artifact is not None
        and recommended_expression is not None
        and recommended_actualization is not None
    ):
        for item in extensions.workflow_recipes:
            if mode_item.id not in item.run_mode_ids:
                continue
            if item.artifact_class_id != recommended_artifact["artifact_class"]["id"]:
                continue
            if item.expression_profile_id != recommended_expression["id"]:
                continue
            if item.actualization_protocol_id != recommended_actualization["actualization_protocol"]["id"]:
                continue
            missing_required = sorted(set(item.required_capability_ids) - capability_id_set)
            satisfied_required = sorted(set(item.required_capability_ids) & capability_id_set)
            score = (100 if not missing_required else 0) + len(satisfied_required) * 10
            workflow_candidates.append(
                {
                    "workflow_recipe": item.model_dump(mode="json"),
                    "fit_status": "ready" if not missing_required else "partial",
                    "missing_required_capability_ids": missing_required,
                    "satisfied_capability_ids": satisfied_required,
                    "score": score,
                }
            )
        workflow_candidates.sort(
            key=lambda item: (
                0 if item["fit_status"] == "ready" else 1,
                len(item["missing_required_capability_ids"]),
                -item["score"],
                item["workflow_recipe"]["name"].lower(),
            )
        )

    if host_profile_items:
        notes.append("Capabilities were expanded from the declared host profile set.")
    if not capability_items:
        notes.append("No capabilities were declared, so readiness is conservative.")
    elif recommended_artifact and recommended_artifact["missing_required_capability_ids"]:
        notes.append("The top artifact recommendation is only partial with the currently declared capabilities.")
    if comparison_shape_item and mode_item.id not in comparison_shape_item.mode_ids:
        notes.append("The declared comparison shape does not naturally fit the current run mode.")

    recommended_tools = []
    if inferred_mode:
        recommended_tools.append("fetch_analysis_mode")
    if (
        not capability_items
        or recommended_artifact is None
        or (recommended_artifact and recommended_artifact["missing_required_capability_ids"])
        or not actualization_candidates
    ):
        recommended_tools.append("list_capabilities")
    if recommended_artifact is not None:
        recommended_tools.append("fetch_artifact_class")
    if comparison_shape_candidates:
        recommended_tools.append("fetch_comparison_shape")
        recommended_tools.append("prepare_comparison_run")
    if expression_candidates:
        recommended_tools.append("fetch_expression_profile")
    if actualization_candidates:
        recommended_tools.append("fetch_actualization_protocol")
    if workflow_candidates:
        recommended_tools.append("fetch_workflow_recipe")
        recommended_tools.append("prepare_artifact_realization")
        recommended_tools.append("prepare_artifact_template")

    recommended_resources = [
        "registry://advanced-modes",
        "registry://comparison-shapes",
        "registry://capability-model",
        "registry://expression-model",
        "registry://workflow-recipes",
    ]
    if comparison_shape_item is not None:
        recommended_resources.append("registry://comparison-preflight")
    if recommended_artifact is not None:
        recommended_resources.append("registry://actualization-protocols")
    if workflow_candidates:
        recommended_resources.append("registry://artifact-realization")
        recommended_resources.append("registry://artifact-templates")

    return {
        "run_mode": mode_item.model_dump(mode="json"),
        "run_mode_inferred": inferred_mode,
        "mode_candidates": mode_candidates[:3],
        "recommended_comparison_shape": comparison_shape_item.model_dump(mode="json") if comparison_shape_item else None,
        "comparison_shape_inferred": inferred_comparison_shape,
        "comparison_shape_candidates": comparison_shape_candidates[:3],
        "declared_host_profiles": [item.model_dump(mode="json") for item in host_profile_items],
        "declared_capabilities": [item.model_dump(mode="json") for item in capability_items],
        "recommended_artifact": recommended_artifact,
        "artifact_candidates": artifact_candidates[:3],
        "recommended_expression_profile": expression_candidates[0] if expression_candidates else None,
        "expression_candidates": expression_candidates[:3],
        "recommended_actualization_protocol": actualization_candidates[0] if actualization_candidates else None,
        "actualization_candidates": actualization_candidates[:3],
        "recommended_workflow_recipe": workflow_candidates[0] if workflow_candidates else None,
        "workflow_candidates": workflow_candidates[:3],
        "recommended_tools": recommended_tools,
        "recommended_resources": recommended_resources,
        "notes": notes,
    }


def _related_interaction_entity_ids(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    ref: str,
) -> set[str]:
    try:
        motif = resolve_motif(extensions, ref)
        return {motif.id}
    except KeyError:
        pass

    entity = resolve_entity_reference(repository, ref)
    related_ids = {entity["entity_id"]}
    if entity["entity_type"] == "instrument":
        bundle = resolve_instrument(repository, ref)
        related_ids.update(construct.id for construct in bundle.constructs)
    trace_payload = trace_entity_to_motifs(repository, extensions, ref)
    related_ids.update(item["motif"]["id"] for item in trace_payload["motif_summary"])
    return related_ids


def _interaction_payload(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    interaction,
) -> dict[str, Any]:
    left = _extended_entity_ref(
        repository,
        extensions,
        interaction.left_entity_type,
        interaction.left_entity_id,
    )
    right = _extended_entity_ref(
        repository,
        extensions,
        interaction.right_entity_type,
        interaction.right_entity_id,
    )
    return {
        "id": interaction.id,
        "left": left,
        "right": right,
        "interaction_type": interaction.interaction_type,
        "confidence": interaction.confidence,
        "status": interaction.status,
        "summary": interaction.summary,
        "rationale": interaction.rationale,
        "protocol_relevance": interaction.protocol_relevance,
        "conditions": interaction.conditions,
        "notes": interaction.notes,
    }


def find_interaction_hypotheses(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    *,
    related_to: str | None = None,
    interaction_type: str | None = None,
    protocol: str | None = None,
    text: str | None = None,
) -> list[dict[str, Any]]:
    related_ids: set[str] | None = None
    if related_to:
        related_ids = _related_interaction_entity_ids(repository, extensions, related_to)

    results = []
    for interaction in extensions.interaction_hypotheses:
        if interaction_type and interaction.interaction_type != interaction_type:
            continue
        if protocol and protocol not in interaction.protocol_relevance:
            continue
        if related_ids is not None and not (
            interaction.left_entity_id in related_ids or interaction.right_entity_id in related_ids
        ):
            continue
        if text:
            blob = "\n".join(
                [
                    interaction.id,
                    interaction.summary,
                    interaction.rationale,
                    interaction.interaction_type,
                    *interaction.protocol_relevance,
                    *interaction.conditions,
                ]
            )
            if _normalize(text) not in _normalize(blob):
                continue
        results.append(_interaction_payload(repository, extensions, interaction))
    return sorted(results, key=lambda item: item["id"])


def interaction_hypothesis_record(
    repository: RepositoryData,
    extensions: ExtensionRegistryData,
    ref: str,
) -> dict[str, Any]:
    interaction = resolve_interaction_hypothesis(extensions, ref)
    return {"interaction_hypothesis": _interaction_payload(repository, extensions, interaction)}


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

    suggested_next_queries = [
        {
            "tool": "trace_to_motifs",
            "args": {"ref": left_bundle.slug},
            "purpose": f"Trace {left_bundle.instrument.canonical_name} into the motif layer.",
        },
        {
            "tool": "trace_to_motifs",
            "args": {"ref": right_bundle.slug},
            "purpose": f"Trace {right_bundle.instrument.canonical_name} into the motif layer.",
        },
        {
            "tool": "list_interaction_hypotheses",
            "args": {"related_to": left_bundle.slug},
            "purpose": f"Inspect interaction hypotheses related to {left_bundle.instrument.canonical_name}.",
        },
        {
            "tool": "list_interaction_hypotheses",
            "args": {"related_to": right_bundle.slug},
            "purpose": f"Inspect interaction hypotheses related to {right_bundle.instrument.canonical_name}.",
        },
    ]

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
        "suggested_next_queries": suggested_next_queries,
    }


def load_repository_for_query(root: Path) -> RepositoryData:
    return load_repository_strict(root)


def load_extensions_for_query(root: Path) -> ExtensionRegistryData:
    return load_extensions_strict(root)


def dumps_json(payload: object) -> str:
    return json.dumps(payload, indent=2)
