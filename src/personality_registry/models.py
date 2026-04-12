from __future__ import annotations

from datetime import date
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from personality_registry.constants import (
    ANNOTATION_STATUSES,
    CARDINALITIES,
    CONFIDENCE_LEVELS,
    CROSSWALK_RELATIONSHIP_TYPES,
    ENTITY_TYPES,
    RELATIONSHIP_STRENGTHS,
    SEVERITY_LEVELS,
    SUITABILITY_LEVELS,
    TARGETABLE_ENTITY_TYPES,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class OntologyRegistry(StrictModel):
    id: str
    title: str
    status: str
    version: str
    description: str
    principles: list[str] = Field(default_factory=list)


class OntologyRegistryDocument(StrictModel):
    ontology: OntologyRegistry


class OntologyDimension(StrictModel):
    id: str
    cardinality: Literal["one", "many"]
    description: str
    enum_file: str

    @field_validator("cardinality")
    @classmethod
    def validate_cardinality(cls, value: str) -> str:
        if value not in CARDINALITIES:
            raise ValueError(f"Unsupported cardinality: {value}")
        return value


class OntologyDimensionsDocument(StrictModel):
    dimensions: list[OntologyDimension]


class EnumValuesDocument(StrictModel):
    values: list[str]

    @field_validator("values")
    @classmethod
    def validate_values(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("Enum file must declare at least one value.")
        return value


class Instrument(StrictModel):
    id: str
    canonical_name: str
    short_names: list[str] = Field(default_factory=list)
    aliases: list[str] = Field(default_factory=list)
    status: str
    family: list[str] = Field(default_factory=list)
    short_description: str
    creators: list[str] = Field(default_factory=list)
    publisher_or_owner: Optional[str] = None
    original_release_year: Optional[int] = None
    official_websites: list[Optional[str]] = Field(default_factory=list)
    licensing_model: Optional[str] = None
    primary_domain: Optional[str] = None
    country_or_origin_context: list[str] = Field(default_factory=list)
    notes: Optional[str] = None


class InstrumentDocument(StrictModel):
    instrument: Instrument


class InstrumentVersion(StrictModel):
    id: str
    instrument_id: str
    version_label: str
    release_date: Optional[date] = None
    retired_date: Optional[date] = None
    current: bool
    change_summary: str
    scoring_changes: Optional[str] = None
    construct_changes: Optional[str] = None
    norming_changes: Optional[str] = None
    administration_changes: Optional[str] = None


class VersionsDocument(StrictModel):
    versions: list[InstrumentVersion]


class ConstructPolarity(StrictModel):
    low_label: Optional[str] = None
    high_label: Optional[str] = None


class ConstructValueRange(StrictModel):
    type: str
    min: Optional[float] = None
    max: Optional[float] = None


class Construct(StrictModel):
    id: str
    instrument_id: str
    version_ids: list[str] = Field(default_factory=list)
    name: str
    short_name: Optional[str] = None
    construct_kind: list[str] = Field(default_factory=list)
    official_definition: Optional[str] = None
    scoring_type: str
    polarity: Optional[ConstructPolarity] = None
    value_range: Optional[ConstructValueRange] = None
    parent_construct_id: Optional[str] = None


class ConstructsDocument(StrictModel):
    constructs: list[Construct]


class Claim(StrictModel):
    id: str
    instrument_id: str
    version_id: Optional[str] = None
    claim_type: str
    claim_text: str
    source_resource_ids: list[str] = Field(default_factory=list)
    quotation_status: str


class ClaimsDocument(StrictModel):
    claims: list[Claim]


class Resource(StrictModel):
    id: str
    instrument_id: str
    version_id: Optional[str] = None
    resource_type: str
    title: str
    url: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    access_status: str
    officiality: str
    notes: Optional[str] = None


class ResourcesDocument(StrictModel):
    resources: list[Resource]


class Annotation(StrictModel):
    id: str
    target_entity_type: Literal["instrument", "version", "construct"]
    target_entity_id: str
    ontology_dimension: str
    ontology_values: list[str]
    annotation_status: Literal["explicit", "implicit", "inferred", "comparative", "contested"]
    confidence: Literal["low", "medium", "high"]
    rationale: str
    evidence_links: list[str] = Field(default_factory=list)

    @field_validator("ontology_values")
    @classmethod
    def validate_ontology_values(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("Annotation must contain at least one ontology value.")
        return value


class AnnotationsDocument(StrictModel):
    annotations: list[Annotation]


class Inference(StrictModel):
    id: str
    target_entity_type: Literal["instrument", "version", "construct"]
    target_entity_id: str
    inference_type: str
    text: str
    confidence: Literal["low", "medium", "high"]
    linked_entities: list[str] = Field(default_factory=list)
    author: str
    timestamp: date


class InferencesDocument(StrictModel):
    inferences: list[Inference]


class Crosswalk(StrictModel):
    id: str
    source_entity_type: Literal["instrument", "version", "construct"]
    source_entity_id: str
    target_entity_type: Literal["instrument", "version", "construct"]
    target_entity_id: str
    relationship_type: str
    relationship_strength: Literal["low", "medium", "high"]
    rationale: str
    confidence: Literal["low", "medium", "high"]
    notes: Optional[str] = None

    @field_validator("relationship_type")
    @classmethod
    def validate_relationship_type(cls, value: str) -> str:
        if value not in CROSSWALK_RELATIONSHIP_TYPES:
            raise ValueError(f"Unsupported relationship_type: {value}")
        return value


class CrosswalksDocument(StrictModel):
    crosswalks: list[Crosswalk]


class Risk(StrictModel):
    id: str
    instrument_id: str
    risk_type: str
    severity: Literal["low", "medium", "high", "very_high", "critical"]
    description: str
    mitigation: Optional[str] = None


class RisksDocument(StrictModel):
    risks: list[Risk]


class UseCase(StrictModel):
    id: str
    instrument_id: str
    use_context: str
    utility_type: str
    suitability_level: Literal["low", "medium", "high", "mixed"]
    cautions: Optional[str] = None


class UseCasesDocument(StrictModel):
    use_cases: list[UseCase]


DOCUMENT_MODEL_BY_FILE = {
    "instrument.yaml": InstrumentDocument,
    "versions.yaml": VersionsDocument,
    "constructs.yaml": ConstructsDocument,
    "claims.yaml": ClaimsDocument,
    "resources.yaml": ResourcesDocument,
    "annotations.yaml": AnnotationsDocument,
    "inferences.yaml": InferencesDocument,
    "crosswalks.yaml": CrosswalksDocument,
    "risks.yaml": RisksDocument,
    "use_cases.yaml": UseCasesDocument,
}


def serialize_for_json(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    return value
