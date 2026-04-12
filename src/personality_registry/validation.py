from __future__ import annotations

import re
from pathlib import Path

from personality_registry.constants import (
    ANNOTATION_STATUSES,
    CONFIDENCE_LEVELS,
    CROSSWALK_RELATIONSHIP_TYPES,
    ENTITY_PREFIXES,
    ENTITY_TYPES,
    REQUIRED_ANNOTATION_DIMENSIONS,
)
from personality_registry.extensions import load_extensions
from personality_registry.loader import RepositoryData, load_repository

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def _expected_prefix_for_id(entity_id: str) -> str | None:
    for prefix in ENTITY_PREFIXES.values():
        if entity_id.startswith(prefix):
            return prefix
    return None


def _collect_entities(repository: RepositoryData) -> dict[str, tuple[str, str]]:
    entities: dict[str, tuple[str, str]] = {}
    for slug, bundle in repository.instruments.items():
        entities[bundle.instrument.id] = ("instrument", slug)
        for version in bundle.versions:
            entities[version.id] = ("version", slug)
        for construct in bundle.constructs:
            entities[construct.id] = ("construct", slug)
        for resource in bundle.resources:
            entities[resource.id] = ("resource", slug)
        for claim in bundle.claims:
            entities[claim.id] = ("claim", slug)
        for annotation in bundle.annotations:
            entities[annotation.id] = ("annotation", slug)
        for inference in bundle.inferences:
            entities[inference.id] = ("inference", slug)
        for crosswalk in bundle.crosswalks:
            entities[crosswalk.id] = ("crosswalk", slug)
        for risk in bundle.risks:
            entities[risk.id] = ("risk", slug)
        for use_case in bundle.use_cases:
            entities[use_case.id] = ("use_case", slug)
    return entities


def collect_validation_errors(root: Path) -> list[str]:
    result = load_repository(root, continue_on_error=True)
    errors = list(result.errors)
    repository = result.repository
    if repository is None:
        return sorted(set(errors))

    extension_result = load_extensions(root)
    errors.extend(extension_result.errors)
    extensions = extension_result.data

    entities = _collect_entities(repository)
    duplicate_tracker: dict[str, list[str]] = {}

    for slug, bundle in repository.instruments.items():
        object_groups = {
            "instrument": [bundle.instrument],
            "version": bundle.versions,
            "construct": bundle.constructs,
            "resource": bundle.resources,
            "claim": bundle.claims,
            "annotation": bundle.annotations,
            "inference": bundle.inferences,
            "crosswalk": bundle.crosswalks,
            "risk": bundle.risks,
            "use_case": bundle.use_cases,
        }

        for entity_type, items in object_groups.items():
            expected_prefix = ENTITY_PREFIXES[entity_type]
            for item in items:
                entity_id = item.id
                duplicate_tracker.setdefault(entity_id, []).append(f"{slug}:{entity_type}")
                if not ID_PATTERN.match(entity_id):
                    errors.append(f"instruments/{slug}: invalid ID format '{entity_id}'")
                if not entity_id.startswith(expected_prefix):
                    errors.append(
                        f"instruments/{slug}: ID '{entity_id}' must start with prefix '{expected_prefix}'"
                    )

        if bundle.instrument.family:
            allowed_family_values = set(repository.ontology_enums.get("instrument_family", []))
            for family_value in bundle.instrument.family:
                if family_value not in allowed_family_values:
                    errors.append(
                        f"instruments/{slug}/instrument.yaml: family value '{family_value}' is not in instrument_family enum"
                    )

        version_ids = {version.id for version in bundle.versions}
        construct_ids = {construct.id for construct in bundle.constructs}
        resource_ids = {resource.id for resource in bundle.resources}

        if not bundle.versions:
            errors.append(f"instruments/{slug}/versions.yaml: at least one version is required")
        if not bundle.resources:
            errors.append(f"instruments/{slug}/resources.yaml: at least one resource is required")

        for version in bundle.versions:
            if version.instrument_id != bundle.instrument.id:
                errors.append(
                    f"instruments/{slug}/versions.yaml: version '{version.id}' references instrument_id "
                    f"'{version.instrument_id}' but folder instrument is '{bundle.instrument.id}'"
                )

        for construct in bundle.constructs:
            if construct.instrument_id != bundle.instrument.id:
                errors.append(
                    f"instruments/{slug}/constructs.yaml: construct '{construct.id}' references instrument_id "
                    f"'{construct.instrument_id}' but folder instrument is '{bundle.instrument.id}'"
                )
            for version_id in construct.version_ids:
                if version_id not in version_ids:
                    errors.append(
                        f"instruments/{slug}/constructs.yaml: construct '{construct.id}' references missing version '{version_id}'"
                    )
            if construct.parent_construct_id and construct.parent_construct_id not in construct_ids:
                errors.append(
                    f"instruments/{slug}/constructs.yaml: construct '{construct.id}' has missing parent_construct_id "
                    f"'{construct.parent_construct_id}'"
                )

        for resource in bundle.resources:
            if resource.instrument_id != bundle.instrument.id:
                errors.append(
                    f"instruments/{slug}/resources.yaml: resource '{resource.id}' references instrument_id "
                    f"'{resource.instrument_id}' but folder instrument is '{bundle.instrument.id}'"
                )
            if resource.version_id and resource.version_id not in version_ids:
                errors.append(
                    f"instruments/{slug}/resources.yaml: resource '{resource.id}' references missing version '{resource.version_id}'"
                )

        for claim in bundle.claims:
            if claim.instrument_id != bundle.instrument.id:
                errors.append(
                    f"instruments/{slug}/claims.yaml: claim '{claim.id}' references instrument_id "
                    f"'{claim.instrument_id}' but folder instrument is '{bundle.instrument.id}'"
                )
            if claim.version_id and claim.version_id not in version_ids:
                errors.append(
                    f"instruments/{slug}/claims.yaml: claim '{claim.id}' references missing version '{claim.version_id}'"
                )
            for resource_id in claim.source_resource_ids:
                if resource_id not in resource_ids:
                    errors.append(
                        f"instruments/{slug}/claims.yaml: claim '{claim.id}' references missing resource '{resource_id}'"
                    )

        for annotation in bundle.annotations:
            if annotation.annotation_status not in ANNOTATION_STATUSES:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' has invalid status '{annotation.annotation_status}'"
                )
            if annotation.confidence not in CONFIDENCE_LEVELS:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' has invalid confidence '{annotation.confidence}'"
                )
            if annotation.target_entity_type not in ENTITY_TYPES:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' has invalid target_entity_type "
                    f"'{annotation.target_entity_type}'"
                )
            if annotation.target_entity_id not in entities:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' references missing target '{annotation.target_entity_id}'"
                )
            dimension = annotation.ontology_dimension
            dimension_def = next(
                (item for item in repository.ontology_dimensions.dimensions if item.id == dimension),
                None,
            )
            if dimension_def is None:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' uses unknown ontology dimension '{dimension}'"
                )
                continue
            allowed_values = set(repository.ontology_enums.get(dimension, []))
            for value in annotation.ontology_values:
                if value not in allowed_values:
                    errors.append(
                        f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' uses invalid ontology value "
                        f"'{value}' for dimension '{dimension}'"
                    )
            if dimension_def.cardinality == "one" and len(annotation.ontology_values) != 1:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' must have exactly one value for "
                    f"single-cardinality dimension '{dimension}'"
                )
            if len(annotation.ontology_values) != len(set(annotation.ontology_values)):
                errors.append(
                    f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' contains duplicate ontology values"
                )
            for resource_id in annotation.evidence_links:
                if resource_id not in resource_ids:
                    errors.append(
                        f"instruments/{slug}/annotations.yaml: annotation '{annotation.id}' references missing evidence link '{resource_id}'"
                    )

        instrument_annotation_dimensions = {
            annotation.ontology_dimension
            for annotation in bundle.annotations
            if annotation.target_entity_type == "instrument" and annotation.target_entity_id == bundle.instrument.id
        }
        for required_dimension in REQUIRED_ANNOTATION_DIMENSIONS:
            if required_dimension not in instrument_annotation_dimensions:
                errors.append(
                    f"instruments/{slug}/annotations.yaml: missing required instrument-level annotation for dimension "
                    f"'{required_dimension}'"
                )

        for inference in bundle.inferences:
            if inference.target_entity_id not in entities:
                errors.append(
                    f"instruments/{slug}/inferences.yaml: inference '{inference.id}' references missing target '{inference.target_entity_id}'"
                )
            for linked_id in inference.linked_entities:
                if linked_id not in entities:
                    errors.append(
                        f"instruments/{slug}/inferences.yaml: inference '{inference.id}' references missing linked entity '{linked_id}'"
                    )

        for crosswalk in bundle.crosswalks:
            if crosswalk.relationship_type not in CROSSWALK_RELATIONSHIP_TYPES:
                errors.append(
                    f"instruments/{slug}/crosswalks.yaml: crosswalk '{crosswalk.id}' has invalid relationship_type "
                    f"'{crosswalk.relationship_type}'"
                )
            if crosswalk.source_entity_id not in entities:
                errors.append(
                    f"instruments/{slug}/crosswalks.yaml: crosswalk '{crosswalk.id}' references missing source '{crosswalk.source_entity_id}'"
                )
            if crosswalk.target_entity_id not in entities:
                errors.append(
                    f"instruments/{slug}/crosswalks.yaml: crosswalk '{crosswalk.id}' references missing target '{crosswalk.target_entity_id}'"
                )

        for risk in bundle.risks:
            if risk.instrument_id != bundle.instrument.id:
                errors.append(
                    f"instruments/{slug}/risks.yaml: risk '{risk.id}' references instrument_id "
                    f"'{risk.instrument_id}' but folder instrument is '{bundle.instrument.id}'"
                )

        for use_case in bundle.use_cases:
            if use_case.instrument_id != bundle.instrument.id:
                errors.append(
                    f"instruments/{slug}/use_cases.yaml: use case '{use_case.id}' references instrument_id "
                    f"'{use_case.instrument_id}' but folder instrument is '{bundle.instrument.id}'"
                )

    for entity_id, locations in duplicate_tracker.items():
        if len(locations) > 1:
            errors.append(f"duplicate ID '{entity_id}' appears in {', '.join(sorted(locations))}")

    if extensions is not None:
        motif_ids = {motif.id for motif in extensions.motifs}
        technique_ids = {technique.id for technique in extensions.techniques}
        dimension_ids = {dimension.id for dimension in repository.ontology_dimensions.dimensions}

        extension_groups = {
            "motif": extensions.motifs,
            "mapping": extensions.mappings,
            "technique": extensions.techniques,
            "protocol": extensions.protocols,
            "contribution_model": extensions.contribution_models,
        }

        for entity_type, items in extension_groups.items():
            expected_prefix = ENTITY_PREFIXES[entity_type]
            for item in items:
                entity_id = item.id
                duplicate_tracker.setdefault(entity_id, []).append(f"extensions:{entity_type}")
                if not ID_PATTERN.match(entity_id):
                    errors.append(f"extensions/{entity_type}: invalid ID format '{entity_id}'")
                if not entity_id.startswith(expected_prefix):
                    errors.append(
                        f"extensions/{entity_type}: ID '{entity_id}' must start with prefix '{expected_prefix}'"
                    )

        for motif in extensions.motifs:
            for dimension in motif.related_dimensions:
                if dimension not in dimension_ids:
                    errors.append(
                        f"motifs/registry.yaml: motif '{motif.id}' references unknown ontology dimension '{dimension}'"
                    )

        for mapping in extensions.mappings:
            source_type = mapping.source_entity_type
            target_type = mapping.target_entity_type

            if source_type == "motif":
                if mapping.source_entity_id not in motif_ids:
                    errors.append(
                        f"mappings/construct_to_motif.yaml: mapping '{mapping.id}' references missing source motif '{mapping.source_entity_id}'"
                    )
            else:
                source_entity = entities.get(mapping.source_entity_id)
                if source_entity is None:
                    errors.append(
                        f"mappings/construct_to_motif.yaml: mapping '{mapping.id}' references missing source '{mapping.source_entity_id}'"
                    )
                elif source_entity[0] != source_type:
                    errors.append(
                        f"mappings/construct_to_motif.yaml: mapping '{mapping.id}' source '{mapping.source_entity_id}' "
                        f"is a {source_entity[0]}, not a {source_type}"
                    )

            if target_type == "motif":
                if mapping.target_entity_id not in motif_ids:
                    errors.append(
                        f"mappings/construct_to_motif.yaml: mapping '{mapping.id}' references missing target motif '{mapping.target_entity_id}'"
                    )
            else:
                target_entity = entities.get(mapping.target_entity_id)
                if target_entity is None:
                    errors.append(
                        f"mappings/construct_to_motif.yaml: mapping '{mapping.id}' references missing target '{mapping.target_entity_id}'"
                    )
                elif target_entity[0] != target_type:
                    errors.append(
                        f"mappings/construct_to_motif.yaml: mapping '{mapping.id}' target '{mapping.target_entity_id}' "
                        f"is a {target_entity[0]}, not a {target_type}"
                    )

        for protocol in extensions.protocols:
            for technique_id in protocol.technique_ids:
                if technique_id not in technique_ids:
                    errors.append(
                        f"protocols/registry.yaml: protocol '{protocol.id}' references missing technique '{technique_id}'"
                    )

        for entity_id, locations in duplicate_tracker.items():
            if len(locations) > 1:
                errors.append(f"duplicate ID '{entity_id}' appears in {', '.join(sorted(locations))}")

    return sorted(set(errors))


def validate_repository(root: Path) -> None:
    errors = collect_validation_errors(root)
    if errors:
        raise ValueError("\n".join(errors))
