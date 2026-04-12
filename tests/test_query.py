from __future__ import annotations

from personality_registry.loader import load_repository_strict
from personality_registry.query import (
    audit_repository,
    compare_instruments,
    find_instruments,
    instrument_record,
    query_results,
    resolve_instrument,
    show_instrument,
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


def test_compare_hexaco_and_big_five_includes_multiple_construct_crosswalks(repo_root):
    repository = load_repository_strict(repo_root)
    payload = compare_instruments(repository, "HEXACO", "Big Five")
    assert len(payload["crosswalks"]) >= 5


def test_compare_disc_and_culture_index_includes_construct_crosswalks(repo_root):
    repository = load_repository_strict(repo_root)
    payload = compare_instruments(repository, "DISC", "Culture Index")
    assert len(payload["crosswalks"]) >= 5


def test_audit_summary_reflects_seed_coverage(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository)
    assert payload["summary"]["instrument_count"] == 15
    assert payload["summary"]["instruments_with_crosswalks"] == 15
    assert payload["summary"]["instruments_with_multiple_resources"] == 15
    assert payload["summary"]["instruments_with_multiple_constructs"] == 15
    assert payload["summary"]["instruments_with_multiple_claims"] >= 7
    assert payload["summary"]["instruments_with_multiple_inferences"] >= 7
    assert payload["summary"]["instruments_with_multiple_risks"] >= 7
    assert payload["summary"]["instruments_with_multiple_use_cases"] >= 7


def test_audit_filter_surfaces_missing_official_resources(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository, needs_official_or_semi_official_resource=True)
    result_ids = {entry["instrument_id"] for entry in payload["instruments"]}
    assert {"instr_attachment_styles", "instr_dark_triad", "instr_natal_astrology"}.issubset(result_ids)


def test_audit_filter_surfaces_thin_claim_layers(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository, needs_multiple_claims=True)
    result_ids = {entry["instrument_id"] for entry in payload["instruments"]}
    assert "instr_attachment_styles" not in result_ids
    assert "instr_cliftonstrengths" not in result_ids
    assert {"instr_cqs", "instr_disc", "instr_human_design"}.issubset(result_ids)


def test_show_instrument_returns_full_record(repo_root):
    repository = load_repository_strict(repo_root)
    bundle = resolve_instrument(repository, "MBTI")
    payload = show_instrument(repository, "MBTI")
    assert payload["instrument"]["id"] == "instr_mbti"
    assert payload["annotation_index"] == instrument_record(bundle)["annotation_index"]


def test_show_instrument_section_returns_constructs(repo_root):
    repository = load_repository_strict(repo_root)
    payload = show_instrument(repository, "HEXACO", section="constructs")
    assert len(payload) == 6
