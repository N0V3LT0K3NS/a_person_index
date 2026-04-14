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
        analysis_mode_ids = {mode.id for mode in extensions.analysis_modes}
        capability_ids = {capability.id for capability in extensions.capabilities}
        artifact_class_ids = {artifact.id for artifact in extensions.artifact_classes}
        motif_ids = {motif.id for motif in extensions.motifs}
        technique_ids = {technique.id for technique in extensions.techniques}
        dimension_ids = {dimension.id for dimension in repository.ontology_dimensions.dimensions}

        extension_groups = {
            "analysis_mode": extensions.analysis_modes,
            "capability": extensions.capabilities,
            "artifact_class": extensions.artifact_classes,
            "actualization_protocol": extensions.actualization_protocols,
            "motif": extensions.motifs,
            "mapping": extensions.mappings,
            "interaction_hypothesis": extensions.interaction_hypotheses,
            "technique": extensions.techniques,
            "protocol": extensions.protocols,
            "protocol_pack": extensions.protocol_packs,
            "promotion_pathway": extensions.promotion_registry.promotion_pathways,
            "contribution_model": extensions.contribution_models,
            "result_atom_schema": [extensions.result_atom_schema],
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

        for artifact_class in extensions.artifact_classes:
            for mode_id in artifact_class.suitable_mode_ids:
                if mode_id not in analysis_mode_ids:
                    errors.append(
                        f"artifacts/registry.yaml: artifact class '{artifact_class.id}' references missing analysis mode '{mode_id}'"
                    )
            for capability_id in artifact_class.required_capability_ids:
                if capability_id not in capability_ids:
                    errors.append(
                        f"artifacts/registry.yaml: artifact class '{artifact_class.id}' references missing required capability '{capability_id}'"
                    )
            for capability_id in artifact_class.optional_capability_ids:
                if capability_id not in capability_ids:
                    errors.append(
                        f"artifacts/registry.yaml: artifact class '{artifact_class.id}' references missing optional capability '{capability_id}'"
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

        protocol_ids = {protocol.id for protocol in extensions.protocols}
        for protocol in extensions.protocols:
            for technique_id in protocol.technique_ids:
                if technique_id not in technique_ids:
                    errors.append(
                        f"protocols/registry.yaml: protocol '{protocol.id}' references missing technique '{technique_id}'"
                    )
            for component_program_id in protocol.component_program_ids:
                if component_program_id == protocol.id:
                    errors.append(
                        f"protocols/registry.yaml: protocol '{protocol.id}' cannot compose itself as a component program"
                    )
                elif component_program_id not in protocol_ids:
                    errors.append(
                        f"protocols/registry.yaml: protocol '{protocol.id}' references missing component program "
                        f"'{component_program_id}'"
                    )

        for actualization_protocol in extensions.actualization_protocols:
            for mode_id in actualization_protocol.run_mode_ids:
                if mode_id not in analysis_mode_ids:
                    errors.append(
                        f"actualization/registry.yaml: actualization protocol '{actualization_protocol.id}' references missing analysis mode '{mode_id}'"
                    )
            for protocol_id in actualization_protocol.protocol_ids:
                if protocol_id not in protocol_ids:
                    errors.append(
                        f"actualization/registry.yaml: actualization protocol '{actualization_protocol.id}' references missing protocol '{protocol_id}'"
                    )
            for artifact_id in actualization_protocol.target_artifact_class_ids:
                if artifact_id not in artifact_class_ids:
                    errors.append(
                        f"actualization/registry.yaml: actualization protocol '{actualization_protocol.id}' references missing artifact class '{artifact_id}'"
                    )
            for capability_id in actualization_protocol.required_capability_ids:
                if capability_id not in capability_ids:
                    errors.append(
                        f"actualization/registry.yaml: actualization protocol '{actualization_protocol.id}' references missing required capability '{capability_id}'"
                    )
            for capability_id in actualization_protocol.optional_capability_ids:
                if capability_id not in capability_ids:
                    errors.append(
                        f"actualization/registry.yaml: actualization protocol '{actualization_protocol.id}' references missing optional capability '{capability_id}'"
                    )

        contribution_model_ids = {item.id for item in extensions.contribution_models}
        stage_ids = [stage.id for stage in extensions.promotion_registry.stages]
        stage_id_set = set(stage_ids)
        if len(stage_ids) != len(stage_id_set):
            errors.append("research/promotion_registry.yaml: duplicate promotion stage IDs detected")

        for protocol_pack in extensions.protocol_packs:
            if protocol_pack.protocol_id not in protocol_ids:
                errors.append(
                    f"protocol_packs/catalog.yaml: protocol pack '{protocol_pack.id}' references missing protocol "
                    f"'{protocol_pack.protocol_id}'"
                )
            for framework_id in protocol_pack.target_framework_ids:
                framework_entity = entities.get(framework_id)
                if framework_entity is None:
                    errors.append(
                        f"protocol_packs/catalog.yaml: protocol pack '{protocol_pack.id}' references missing framework "
                        f"'{framework_id}'"
                    )
                elif framework_entity[0] != "instrument":
                    errors.append(
                        f"protocol_packs/catalog.yaml: protocol pack '{protocol_pack.id}' framework target "
                        f"'{framework_id}' is a {framework_entity[0]}, not an instrument"
                    )
            for construct_id in protocol_pack.target_construct_ids:
                construct_entity = entities.get(construct_id)
                if construct_entity is None:
                    errors.append(
                        f"protocol_packs/catalog.yaml: protocol pack '{protocol_pack.id}' references missing construct "
                        f"'{construct_id}'"
                    )
                elif construct_entity[0] != "construct":
                    errors.append(
                        f"protocol_packs/catalog.yaml: protocol pack '{protocol_pack.id}' construct target "
                        f"'{construct_id}' is a {construct_entity[0]}, not a construct"
                    )

        for contribution_model in extensions.contribution_models:
            for stage_id in contribution_model.promotion_path:
                if stage_id not in stage_id_set:
                    errors.append(
                        f"research/contribution_models.yaml: contribution model '{contribution_model.id}' references "
                        f"unknown promotion stage '{stage_id}'"
                    )

        target_stage_by_outcome = {
            "mapping_revision": "promoted_to_house_mapping",
            "interaction_hypothesis": "promoted_to_interaction_hypothesis",
            "house_inference": "promoted_to_house_inference",
            "protocol_revision": "protocol_revision",
            "comparative_analysis": "comparative_analysis",
        }
        for pathway in extensions.promotion_registry.promotion_pathways:
            if pathway.contribution_model_id not in contribution_model_ids:
                errors.append(
                    f"research/promotion_registry.yaml: promotion pathway '{pathway.id}' references missing "
                    f"contribution model '{pathway.contribution_model_id}'"
                )
            for stage_id in pathway.stages:
                if stage_id not in stage_id_set:
                    errors.append(
                        f"research/promotion_registry.yaml: promotion pathway '{pathway.id}' references unknown "
                        f"stage '{stage_id}'"
                    )
            if pathway.target_layer in {"house_synthesis", "protocol_library"} and "reviewed" not in pathway.stages:
                errors.append(
                    f"research/promotion_registry.yaml: promotion pathway '{pathway.id}' must include 'reviewed' "
                    f"before changing {pathway.target_layer}"
                )
            expected_terminal_stage = target_stage_by_outcome[pathway.target_outcome_type]
            if not pathway.stages or pathway.stages[-1] != expected_terminal_stage:
                errors.append(
                    f"research/promotion_registry.yaml: promotion pathway '{pathway.id}' must end with "
                    f"'{expected_terminal_stage}' for outcome '{pathway.target_outcome_type}'"
                )

        for interaction in extensions.interaction_hypotheses:
            for side, entity_type, entity_id in (
                ("left", interaction.left_entity_type, interaction.left_entity_id),
                ("right", interaction.right_entity_type, interaction.right_entity_id),
            ):
                if entity_type == "motif":
                    if entity_id not in motif_ids:
                        errors.append(
                            f"interactions/registry.yaml: interaction '{interaction.id}' references missing {side} motif '{entity_id}'"
                        )
                else:
                    entity = entities.get(entity_id)
                    if entity is None:
                        errors.append(
                            f"interactions/registry.yaml: interaction '{interaction.id}' references missing {side} entity '{entity_id}'"
                        )
                    elif entity[0] != entity_type:
                        errors.append(
                            f"interactions/registry.yaml: interaction '{interaction.id}' {side} entity '{entity_id}' "
                            f"is a {entity[0]}, not a {entity_type}"
                        )
            for protocol_id in interaction.protocol_relevance:
                if protocol_id not in protocol_ids:
                    errors.append(
                        f"interactions/registry.yaml: interaction '{interaction.id}' references missing protocol '{protocol_id}'"
                    )

        for entity_id, locations in duplicate_tracker.items():
            if len(locations) > 1:
                errors.append(f"duplicate ID '{entity_id}' appears in {', '.join(sorted(locations))}")

    return sorted(set(errors))


def validate_repository(root: Path) -> None:
    errors = collect_validation_errors(root)
    if errors:
        raise ValueError("\n".join(errors))
