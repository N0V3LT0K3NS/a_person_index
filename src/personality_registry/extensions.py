from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import Field, ValidationError, field_validator

from personality_registry.models import StrictModel


EXTENSION_FILE_MODELS = {
    "motifs/registry.yaml": "motifs",
    "mappings/construct_to_motif.yaml": "mappings",
    "techniques/registry.yaml": "techniques",
    "protocols/registry.yaml": "protocols",
    "research/contribution_models.yaml": "contribution_models",
}


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
    purpose: str
    summary: str
    downstream_consumers: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    optional_inputs: list[str] = Field(default_factory=list)
    technique_ids: list[str] = Field(default_factory=list)
    primary_outputs: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ProtocolsDocument(StrictModel):
    protocols: list[Protocol]


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


DOCUMENT_MODEL_BY_FILE = {
    "motifs/registry.yaml": MotifsDocument,
    "mappings/construct_to_motif.yaml": ConstructMappingsDocument,
    "techniques/registry.yaml": TechniquesDocument,
    "protocols/registry.yaml": ProtocolsDocument,
    "research/contribution_models.yaml": ContributionModelsDocument,
}


@dataclass
class ExtensionRegistryData:
    motifs: list[Motif]
    mappings: list[ConstructMapping]
    techniques: list[Technique]
    protocols: list[Protocol]
    contribution_models: list[ContributionModel]


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

    motifs_doc = documents["motifs/registry.yaml"]
    mappings_doc = documents["mappings/construct_to_motif.yaml"]
    techniques_doc = documents["techniques/registry.yaml"]
    protocols_doc = documents["protocols/registry.yaml"]
    contribution_models_doc = documents["research/contribution_models.yaml"]

    data = ExtensionRegistryData(
        motifs=motifs_doc.motifs,
        mappings=mappings_doc.mappings,
        techniques=techniques_doc.techniques,
        protocols=protocols_doc.protocols,
        contribution_models=contribution_models_doc.contribution_models,
    )
    return ExtensionLoadResult(data=data, errors=errors)


def load_extensions_strict(root: Path) -> ExtensionRegistryData:
    result = load_extensions(root)
    if result.errors:
        raise ValueError("\n".join(result.errors))
    if result.data is None:
        raise ValueError("Extension registries could not be loaded.")
    return result.data
