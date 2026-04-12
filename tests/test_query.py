from __future__ import annotations

from personality_registry.loader import load_repository_strict
from personality_registry.query import (
    audit_repository,
    compare_instruments,
    find_instruments,
    query_results,
    resolve_instrument,
)


def test_resolve_instrument_by_alias(repo_root):
    repository = load_repository_strict(repo_root)
    bundle = resolve_instrument(repository, "OCEAN")
    assert bundle.instrument.id == "instr_big_five"


def test_query_by_family_and_text(repo_root):
    repository = load_repository_strict(repo_root)
    results = query_results(repository, families=["typology"], text="identity narrative")
    result_ids = {result.instrument_id for result in results}
    assert "instr_enneagram" in result_ids


def test_compare_surfaces_shared_values(repo_root):
    repository = load_repository_strict(repo_root)
    payload = compare_instruments(repository, "MBTI", "Enneagram")
    assert payload["left"]["id"] == "instr_mbti"
    assert payload["right"]["id"] == "instr_enneagram"
    assert "deployment_context" in payload["shared_annotation_values"]


def test_related_lookup_includes_construct_crosswalks(repo_root):
    repository = load_repository_strict(repo_root)
    related = find_instruments(repository, related_to="MBTI")
    related_ids = {bundle.instrument.id for bundle in related}
    assert "instr_big_five" in related_ids


def test_compare_includes_construct_crosswalks(repo_root):
    repository = load_repository_strict(repo_root)
    payload = compare_instruments(repository, "Big Five", "MBTI")
    assert payload["crosswalks"]


def test_audit_summary_reflects_seed_coverage(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository)
    assert payload["summary"]["instrument_count"] == 15
    assert payload["summary"]["instruments_with_crosswalks"] == 15
    assert payload["summary"]["instruments_with_multiple_resources"] == 15
    assert payload["summary"]["instruments_with_multiple_constructs"] == 15


def test_audit_filter_surfaces_missing_official_resources(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository, needs_official_or_semi_official_resource=True)
    result_ids = {entry["instrument_id"] for entry in payload["instruments"]}
    assert {"instr_attachment_styles", "instr_dark_triad", "instr_natal_astrology"}.issubset(result_ids)
