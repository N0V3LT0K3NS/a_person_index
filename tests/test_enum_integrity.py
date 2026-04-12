from __future__ import annotations

from personality_registry.constants import REQUIRED_ANNOTATION_DIMENSIONS
from personality_registry.loader import load_repository_strict


def test_ontology_enum_files_cover_dimensions(repo_root):
    repository = load_repository_strict(repo_root)
    dimension_ids = {dimension.id for dimension in repository.ontology_dimensions.dimensions}
    assert set(REQUIRED_ANNOTATION_DIMENSIONS).issubset(dimension_ids)
    for dimension in repository.ontology_dimensions.dimensions:
        assert dimension.id in repository.ontology_enums
        assert repository.ontology_enums[dimension.id]


def test_instruments_cover_required_annotation_dimensions(repo_root):
    repository = load_repository_strict(repo_root)
    for bundle in repository.instruments.values():
        covered = {
            annotation.ontology_dimension
            for annotation in bundle.annotations
            if annotation.target_entity_type == "instrument" and annotation.target_entity_id == bundle.instrument.id
        }
        assert set(REQUIRED_ANNOTATION_DIMENSIONS).issubset(covered)
