from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import Field, ValidationError, field_validator

from personality_registry.models import StrictModel


EXTENSION_FILE_MODELS = {
    "modes/registry.yaml": "analysis_modes",
    "comparison_shapes/registry.yaml": "comparison_shapes",
    "capabilities/registry.yaml": "capabilities",
    "expression/registry.yaml": "expression_profiles",
    "artifacts/registry.yaml": "artifact_classes",
    "actualization/registry.yaml": "actualization_protocols",
    "workflow_recipes/registry.yaml": "workflow_recipes",
    "motifs/registry.yaml": "motifs",
    "mappings/construct_to_motif.yaml": "mappings",
    "interactions/registry.yaml": "interaction_hypotheses",
    "techniques/registry.yaml": "techniques",
    "protocols/registry.yaml": "protocols",
    "protocol_packs/catalog.yaml": "protocol_packs",
    "research/promotion_registry.yaml": "promotion_registry",
    "research/contribution_models.yaml": "contribution_models",
    "research/result_atom_schema.yaml": "result_atom_schema",
}


class AnalysisMode(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    summary: str
    purpose: str
    intent_signals: list[str] = Field(default_factory=list)
    preferred_entrypoints: list[str] = Field(default_factory=list)
    typical_outputs: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class AnalysisModesDocument(StrictModel):
    analysis_modes: list[AnalysisMode]


class ComparisonDeclarationField(StrictModel):
    id: str
    label: str
    value_kind: Literal["string", "string_list"]
    required: bool
    summary: str
    examples: list[str] = Field(default_factory=list)


class ComparisonShape(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    summary: str
    purpose: str
    mode_ids: list[str] = Field(default_factory=list)
    intent_signals: list[str] = Field(default_factory=list)
    declaration_fields: list[ComparisonDeclarationField] = Field(default_factory=list)
    required_declarations: list[str] = Field(default_factory=list)
    optional_declarations: list[str] = Field(default_factory=list)
    suitable_artifact_class_ids: list[str] = Field(default_factory=list)
    recommended_protocol_ids: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ComparisonShapesDocument(StrictModel):
    comparison_shapes: list[ComparisonShape]


class Capability(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    capability_kind: Literal[
        "input",
        "execution",
        "rendering",
        "visualization",
        "network",
        "persistence",
        "packaging",
    ]
    summary: str
    purpose: str
    detection_questions: list[str] = Field(default_factory=list)
    typical_tool_signals: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class CapabilitiesDocument(StrictModel):
    capabilities: list[Capability]


class ExpressionProfile(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    expression_mode: Literal["tacit", "explanatory", "technical", "mixed"]
    summary: str
    purpose: str
    audience_modes: list[str] = Field(default_factory=list)
    visible_by_default: list[str] = Field(default_factory=list)
    keep_implicit_by_default: list[str] = Field(default_factory=list)
    good_for: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ExpressionProfilesDocument(StrictModel):
    expression_profiles: list[ExpressionProfile]


class ArtifactClass(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    summary: str
    audience_modes: list[str] = Field(default_factory=list)
    default_expression_mode: Literal["tacit", "explanatory", "technical", "mixed"]
    suitable_mode_ids: list[str] = Field(default_factory=list)
    required_evidence_partitions: list[str] = Field(default_factory=list)
    required_capability_ids: list[str] = Field(default_factory=list)
    optional_capability_ids: list[str] = Field(default_factory=list)
    typical_forms: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ArtifactClassesDocument(StrictModel):
    artifact_classes: list[ArtifactClass]


class ActualizationProtocol(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    summary: str
    run_mode_ids: list[str] = Field(default_factory=list)
    protocol_ids: list[str] = Field(default_factory=list)
    target_artifact_class_ids: list[str] = Field(default_factory=list)
    required_capability_ids: list[str] = Field(default_factory=list)
    optional_capability_ids: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ActualizationProtocolsDocument(StrictModel):
    actualization_protocols: list[ActualizationProtocol]


class WorkflowRecipe(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    summary: str
    run_mode_ids: list[str] = Field(default_factory=list)
    artifact_class_id: str
    expression_profile_id: str
    actualization_protocol_id: str
    required_capability_ids: list[str] = Field(default_factory=list)
    recipe_steps: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class WorkflowRecipesDocument(StrictModel):
    workflow_recipes: list[WorkflowRecipe]


class Motif(StrictModel):
    id: str
    name: str
    status: Literal["provisional", "active", "experimental"]
    motif_kind: Literal["translation_axis", "circuit_motif", "social_function"]
    summary: str
    description: str
    tags: list[str] = Field(default_factory=list)
    related_dimensions: list[str] = Field(default_factory=list)


class MotifsDocument(StrictModel):
    motifs: list[Motif]


class ConstructMapping(StrictModel):
    id: str
    source_entity_type: Literal["instrument", "construct", "motif"]
    source_entity_id: str
    target_entity_type: Literal["instrument", "construct", "motif"]
    target_entity_id: str
    relationship_type: Literal[
        "direct_signal",
        "partial_signal",
        "inverse_signal",
        "symbolic_analogue",
        "different_layer",
        "incommensurable",
    ]
    relationship_strength: Literal["low", "medium", "high"]
    confidence: Literal["low", "medium", "high"]
    status: Literal["provisional", "active", "contested"]
    rationale: str
    notes: Optional[str] = None

    @field_validator("target_entity_type")
    @classmethod
    def validate_target_entity_type(cls, value: str) -> str:
        if value != "motif":
            raise ValueError("Construct-to-motif mappings must target a motif.")
        return value


class ConstructMappingsDocument(StrictModel):
    mappings: list[ConstructMapping]


class InteractionHypothesis(StrictModel):
    id: str
    left_entity_type: Literal["instrument", "construct", "motif"]
    left_entity_id: str
    right_entity_type: Literal["instrument", "construct", "motif"]
    right_entity_id: str
    interaction_type: Literal[
        "reinforcing",
        "compensatory",
        "orthogonal",
        "masking",
        "tension_producing",
        "context_dependent",
    ]
    confidence: Literal["low", "medium", "high"]
    status: Literal["provisional", "active", "contested"]
    summary: str
    rationale: str
    protocol_relevance: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("right_entity_id")
    @classmethod
    def validate_not_self_link(
        cls,
        value: str,
        info,
    ) -> str:
        left_entity_id = info.data.get("left_entity_id")
        left_entity_type = info.data.get("left_entity_type")
        right_entity_type = info.data.get("right_entity_type")
        if left_entity_id == value and left_entity_type == right_entity_type:
            raise ValueError("Interaction hypothesis must connect two distinct entities.")
        return value


class InteractionHypothesesDocument(StrictModel):
    interaction_hypotheses: list[InteractionHypothesis]


class Technique(StrictModel):
    id: str
    name: str
    purpose: str
    summary: str
    input_types: list[str] = Field(default_factory=list)
    output_types: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class TechniquesDocument(StrictModel):
    techniques: list[Technique]


class Protocol(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    program_kind: Literal[
        "micro_program",
        "comparison_program",
        "translation_program",
        "synthesis_program",
        "artifact_program",
        "research_program",
    ]
    purpose: str
    summary: str
    downstream_consumers: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    optional_inputs: list[str] = Field(default_factory=list)
    technique_ids: list[str] = Field(default_factory=list)
    component_program_ids: list[str] = Field(default_factory=list)
    primary_outputs: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ProtocolsDocument(StrictModel):
    protocols: list[Protocol]


class ProtocolPackSpec(StrictModel):
    id: str
    protocol_id: str
    status: Literal["draft", "experimental", "active"]
    title: str
    summary: str
    intended_consumers: list[str] = Field(default_factory=list)
    target_framework_ids: list[str] = Field(default_factory=list)
    target_construct_ids: list[str] = Field(default_factory=list)
    featured: bool = False
    notes: Optional[str] = None

    @field_validator("target_construct_ids")
    @classmethod
    def validate_scoped_targets(
        cls,
        value: list[str],
        info,
    ) -> list[str]:
        framework_ids = info.data.get("target_framework_ids", [])
        if not framework_ids and not value:
            raise ValueError("Protocol pack spec must target at least one framework or construct.")
        return value


class ProtocolPacksDocument(StrictModel):
    protocol_packs: list[ProtocolPackSpec]


class PromotionStage(StrictModel):
    id: str
    name: str
    summary: str
    stage_kind: Literal["collection", "aggregation", "review", "promotion", "revision"]
    entry_criteria: list[str] = Field(default_factory=list)
    exit_criteria: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class PromotionPathway(StrictModel):
    id: str
    contribution_model_id: str
    target_outcome_type: Literal[
        "mapping_revision",
        "interaction_hypothesis",
        "house_inference",
        "protocol_revision",
        "comparative_analysis",
    ]
    target_layer: Literal["house_synthesis", "protocol_library", "research_stream"]
    summary: str
    stages: list[str] = Field(default_factory=list)
    evidence_requirements: list[str] = Field(default_factory=list)
    reviewer_questions: list[str] = Field(default_factory=list)
    output_artifacts: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class PromotionRegistry(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    summary: str
    principles: list[str] = Field(default_factory=list)
    stages: list[PromotionStage] = Field(default_factory=list)
    promotion_pathways: list[PromotionPathway] = Field(default_factory=list)
    notes: Optional[str] = None


class PromotionRegistryDocument(StrictModel):
    promotion_registry: PromotionRegistry


class ContributionModel(StrictModel):
    id: str
    name: str
    purpose: str
    privacy_posture: str
    required_fields: list[str] = Field(default_factory=list)
    optional_fields: list[str] = Field(default_factory=list)
    promotion_path: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ContributionModelsDocument(StrictModel):
    contribution_models: list[ContributionModel]


class ResultAtomField(StrictModel):
    name: str
    field_kind: Literal["identifier", "categorical", "numeric", "text", "timestamp", "confidence", "provenance"]
    description: str
    examples: list[str] = Field(default_factory=list)


class ResultAtomSchema(StrictModel):
    id: str
    name: str
    status: Literal["draft", "experimental", "active"]
    purpose: str
    summary: str
    required_fields: list[ResultAtomField] = Field(default_factory=list)
    optional_fields: list[ResultAtomField] = Field(default_factory=list)
    normalization_rules: list[str] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ResultAtomSchemaDocument(StrictModel):
    result_atom_schema: ResultAtomSchema


DOCUMENT_MODEL_BY_FILE = {
    "modes/registry.yaml": AnalysisModesDocument,
    "comparison_shapes/registry.yaml": ComparisonShapesDocument,
    "capabilities/registry.yaml": CapabilitiesDocument,
    "expression/registry.yaml": ExpressionProfilesDocument,
    "artifacts/registry.yaml": ArtifactClassesDocument,
    "actualization/registry.yaml": ActualizationProtocolsDocument,
    "workflow_recipes/registry.yaml": WorkflowRecipesDocument,
    "motifs/registry.yaml": MotifsDocument,
    "mappings/construct_to_motif.yaml": ConstructMappingsDocument,
    "interactions/registry.yaml": InteractionHypothesesDocument,
    "techniques/registry.yaml": TechniquesDocument,
    "protocols/registry.yaml": ProtocolsDocument,
    "protocol_packs/catalog.yaml": ProtocolPacksDocument,
    "research/promotion_registry.yaml": PromotionRegistryDocument,
    "research/contribution_models.yaml": ContributionModelsDocument,
    "research/result_atom_schema.yaml": ResultAtomSchemaDocument,
}


@dataclass
class ExtensionRegistryData:
    analysis_modes: list[AnalysisMode]
    comparison_shapes: list[ComparisonShape]
    capabilities: list[Capability]
    expression_profiles: list[ExpressionProfile]
    artifact_classes: list[ArtifactClass]
    actualization_protocols: list[ActualizationProtocol]
    workflow_recipes: list[WorkflowRecipe]
    motifs: list[Motif]
    mappings: list[ConstructMapping]
    interaction_hypotheses: list[InteractionHypothesis]
    techniques: list[Technique]
    protocols: list[Protocol]
    protocol_packs: list[ProtocolPackSpec]
    promotion_registry: PromotionRegistry
    contribution_models: list[ContributionModel]
    result_atom_schema: ResultAtomSchema


@dataclass
class ExtensionLoadResult:
    data: Optional[ExtensionRegistryData]
    errors: list[str]


def _format_validation_error(path: Path, error: ValidationError) -> list[str]:
    formatted: list[str] = []
    for item in error.errors():
        location = ".".join(str(part) for part in item["loc"])
        formatted.append(f"{path}: {location}: {item['msg']}")
    return formatted


def _read_yaml_file(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_extensions(root: Path) -> ExtensionLoadResult:
    errors: list[str] = []
    documents: dict[str, object] = {}

    for relative_path, document_model in DOCUMENT_MODEL_BY_FILE.items():
        path = root / relative_path
        try:
            documents[relative_path] = document_model.model_validate(_read_yaml_file(path))
        except FileNotFoundError:
            errors.append(f"{path}: missing required extension registry file")
        except ValidationError as exc:
            errors.extend(_format_validation_error(path, exc))
        except yaml.YAMLError as exc:
            errors.append(f"{path}: invalid YAML: {exc}")

    if errors:
        return ExtensionLoadResult(data=None, errors=errors)

    analysis_modes_doc = documents["modes/registry.yaml"]
    comparison_shapes_doc = documents["comparison_shapes/registry.yaml"]
    capabilities_doc = documents["capabilities/registry.yaml"]
    expression_profiles_doc = documents["expression/registry.yaml"]
    artifact_classes_doc = documents["artifacts/registry.yaml"]
    actualization_protocols_doc = documents["actualization/registry.yaml"]
    workflow_recipes_doc = documents["workflow_recipes/registry.yaml"]
    motifs_doc = documents["motifs/registry.yaml"]
    mappings_doc = documents["mappings/construct_to_motif.yaml"]
    interaction_hypotheses_doc = documents["interactions/registry.yaml"]
    techniques_doc = documents["techniques/registry.yaml"]
    protocols_doc = documents["protocols/registry.yaml"]
    protocol_packs_doc = documents["protocol_packs/catalog.yaml"]
    promotion_registry_doc = documents["research/promotion_registry.yaml"]
    contribution_models_doc = documents["research/contribution_models.yaml"]
    result_atom_schema_doc = documents["research/result_atom_schema.yaml"]

    data = ExtensionRegistryData(
        analysis_modes=analysis_modes_doc.analysis_modes,
        comparison_shapes=comparison_shapes_doc.comparison_shapes,
        capabilities=capabilities_doc.capabilities,
        expression_profiles=expression_profiles_doc.expression_profiles,
        artifact_classes=artifact_classes_doc.artifact_classes,
        actualization_protocols=actualization_protocols_doc.actualization_protocols,
        workflow_recipes=workflow_recipes_doc.workflow_recipes,
        motifs=motifs_doc.motifs,
        mappings=mappings_doc.mappings,
        interaction_hypotheses=interaction_hypotheses_doc.interaction_hypotheses,
        techniques=techniques_doc.techniques,
        protocols=protocols_doc.protocols,
        protocol_packs=protocol_packs_doc.protocol_packs,
        promotion_registry=promotion_registry_doc.promotion_registry,
        contribution_models=contribution_models_doc.contribution_models,
        result_atom_schema=result_atom_schema_doc.result_atom_schema,
    )
    return ExtensionLoadResult(data=data, errors=errors)


def load_extensions_strict(root: Path) -> ExtensionRegistryData:
    result = load_extensions(root)
    if result.errors:
        raise ValueError("\n".join(result.errors))
    if result.data is None:
        raise ValueError("Extension registries could not be loaded.")
    return result.data
