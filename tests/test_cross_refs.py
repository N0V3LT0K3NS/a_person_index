from __future__ import annotations

from personality_registry.loader import load_repository_strict


def test_crosswalk_targets_resolve(repo_root):
    repository = load_repository_strict(repo_root)
    entity_ids = set()
    for bundle in repository.instruments.values():
        entity_ids.add(bundle.instrument.id)
        entity_ids.update(item.id for item in bundle.versions)
        entity_ids.update(item.id for item in bundle.constructs)

    for bundle in repository.instruments.values():
        for crosswalk in bundle.crosswalks:
            assert crosswalk.source_entity_id in entity_ids
            assert crosswalk.target_entity_id in entity_ids


def test_inference_links_resolve(repo_root):
    repository = load_repository_strict(repo_root)
    entity_ids = set()
    for bundle in repository.instruments.values():
        entity_ids.add(bundle.instrument.id)
        entity_ids.update(item.id for item in bundle.versions)
        entity_ids.update(item.id for item in bundle.constructs)

    for bundle in repository.instruments.values():
        for inference in bundle.inferences:
            assert inference.target_entity_id in entity_ids
            for linked_id in inference.linked_entities:
                assert linked_id in entity_ids
