from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import ValidationError

from personality_registry.constants import REQUIRED_INSTRUMENT_FILES
from personality_registry.models import (
    DOCUMENT_MODEL_BY_FILE,
    Annotation,
    AnnotationsDocument,
    Claim,
    ClaimsDocument,
    Construct,
    ConstructsDocument,
    Crosswalk,
    CrosswalksDocument,
    EnumValuesDocument,
    Inference,
    InferencesDocument,
    Instrument,
    InstrumentDocument,
    InstrumentVersion,
    OntologyDimensionsDocument,
    OntologyRegistryDocument,
    Resource,
    ResourcesDocument,
    Risk,
    RisksDocument,
    UseCase,
    UseCasesDocument,
)


@dataclass
class InstrumentBundle:
    slug: str
    path: Path
    instrument: Instrument
    versions: list[InstrumentVersion]
    constructs: list[Construct]
    claims: list[Claim]
    resources: list[Resource]
    annotations: list[Annotation]
    inferences: list[Inference]
    crosswalks: list[Crosswalk]
    risks: list[Risk]
    use_cases: list[UseCase]
    notes: str


@dataclass
class RepositoryData:
    root: Path
    ontology_registry: OntologyRegistryDocument
    ontology_dimensions: OntologyDimensionsDocument
    ontology_enums: dict[str, list[str]]
    instruments: dict[str, InstrumentBundle]


@dataclass
class LoadResult:
    repository: Optional[RepositoryData]
    errors: list[str]


def _format_validation_error(path: Path, error: ValidationError) -> list[str]:
    formatted: list[str] = []
    for item in error.errors():
        location = ".".join(str(part) for part in item["loc"])
        formatted.append(f"{path}: {location}: {item['msg']}")
    return formatted


def read_yaml_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def instrument_directories(root: Path) -> list[Path]:
    instruments_root = root / "instruments"
    if not instruments_root.exists():
        return []
    return sorted(path for path in instruments_root.iterdir() if path.is_dir())


def load_repository(root: Path, continue_on_error: bool = False) -> LoadResult:
    errors: list[str] = []

    ontology_registry_path = root / "ontology" / "registry.yaml"
    ontology_dimensions_path = root / "ontology" / "dimensions.yaml"

    ontology_registry_doc: Optional[OntologyRegistryDocument] = None
    ontology_dimensions_doc: Optional[OntologyDimensionsDocument] = None
    ontology_enums: dict[str, list[str]] = {}

    try:
        ontology_registry_doc = OntologyRegistryDocument.model_validate(read_yaml_file(ontology_registry_path))
    except FileNotFoundError:
        errors.append(f"{ontology_registry_path}: missing required file")
    except ValidationError as exc:
        errors.extend(_format_validation_error(ontology_registry_path, exc))

    try:
        ontology_dimensions_doc = OntologyDimensionsDocument.model_validate(read_yaml_file(ontology_dimensions_path))
    except FileNotFoundError:
        errors.append(f"{ontology_dimensions_path}: missing required file")
    except ValidationError as exc:
        errors.extend(_format_validation_error(ontology_dimensions_path, exc))

    if ontology_dimensions_doc is not None:
        for dimension in ontology_dimensions_doc.dimensions:
            enum_path = root / "ontology" / dimension.enum_file
            try:
                enum_doc = EnumValuesDocument.model_validate(read_yaml_file(enum_path))
            except FileNotFoundError:
                errors.append(f"{enum_path}: missing enum file referenced by ontology dimension '{dimension.id}'")
                continue
            except ValidationError as exc:
                errors.extend(_format_validation_error(enum_path, exc))
                continue
            ontology_enums[dimension.id] = enum_doc.values

    bundles: dict[str, InstrumentBundle] = {}
    for directory in instrument_directories(root):
        missing = [name for name in REQUIRED_INSTRUMENT_FILES if not (directory / name).exists()]
        for filename in missing:
            errors.append(f"{directory / filename}: missing required file")
        if missing and not continue_on_error:
            continue

        documents: dict[str, Any] = {}
        bundle_failed = False
        for filename, document_model in DOCUMENT_MODEL_BY_FILE.items():
            path = directory / filename
            if not path.exists():
                bundle_failed = True
                continue
            try:
                raw = read_yaml_file(path)
                documents[filename] = document_model.model_validate(raw)
            except ValidationError as exc:
                errors.extend(_format_validation_error(path, exc))
                bundle_failed = True
            except FileNotFoundError:
                errors.append(f"{path}: missing required file")
                bundle_failed = True
            except yaml.YAMLError as exc:
                errors.append(f"{path}: invalid YAML: {exc}")
                bundle_failed = True

        notes_path = directory / "notes.md"
        notes = ""
        if notes_path.exists():
            notes = read_text_file(notes_path)
        else:
            errors.append(f"{notes_path}: missing required file")
            bundle_failed = True

        if bundle_failed and not continue_on_error:
            continue
        if bundle_failed and continue_on_error:
            continue

        instrument_doc = documents["instrument.yaml"]
        versions_doc = documents["versions.yaml"]
        constructs_doc = documents["constructs.yaml"]
        claims_doc = documents["claims.yaml"]
        resources_doc = documents["resources.yaml"]
        annotations_doc = documents["annotations.yaml"]
        inferences_doc = documents["inferences.yaml"]
        crosswalks_doc = documents["crosswalks.yaml"]
        risks_doc = documents["risks.yaml"]
        use_cases_doc = documents["use_cases.yaml"]

        bundles[directory.name] = InstrumentBundle(
            slug=directory.name,
            path=directory,
            instrument=instrument_doc.instrument,
            versions=versions_doc.versions,
            constructs=constructs_doc.constructs,
            claims=claims_doc.claims,
            resources=resources_doc.resources,
            annotations=annotations_doc.annotations,
            inferences=inferences_doc.inferences,
            crosswalks=crosswalks_doc.crosswalks,
            risks=risks_doc.risks,
            use_cases=use_cases_doc.use_cases,
            notes=notes,
        )

    if errors and not continue_on_error:
        return LoadResult(repository=None, errors=errors)

    if ontology_registry_doc is None or ontology_dimensions_doc is None:
        return LoadResult(repository=None, errors=errors)

    repository = RepositoryData(
        root=root,
        ontology_registry=ontology_registry_doc,
        ontology_dimensions=ontology_dimensions_doc,
        ontology_enums=ontology_enums,
        instruments=bundles,
    )
    return LoadResult(repository=repository, errors=errors)


def load_repository_strict(root: Path) -> RepositoryData:
    result = load_repository(root)
    if result.errors:
        raise ValueError("\n".join(result.errors))
    if result.repository is None:
        raise ValueError("Repository could not be loaded.")
    return result.repository
