from __future__ import annotations

import subprocess
import sys

from personality_registry.extensions import load_extensions_strict
from personality_registry.loader import load_repository_strict
from personality_registry.query import (
    agent_orientation,
    audit_repository,
    compare_instruments,
    find_contribution_models,
    find_interaction_hypotheses,
    find_motifs,
    find_promotion_pathways,
    find_protocol_packs,
    find_protocols,
    find_techniques,
    find_instruments,
    curated_protocol_pack_record,
    interaction_hypothesis_record,
    instrument_record,
    motif_record,
    protocol_pack,
    protocol_pack_summary,
    protocol_pack_grammar,
    protocol_record,
    query_results,
    promotion_pathway_record,
    research_promotion_registry_record,
    result_atom_schema_record,
    resolve_instrument,
    show_instrument,
    trace_entity_to_motifs,
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


def test_query_text_matches_common_natural_variants(repo_root):
    repository = load_repository_strict(repo_root)
    results = query_results(repository, text="astrology natal chart love language")
    result_ids = {result.instrument_id for result in results}
    assert "instr_natal_astrology" in result_ids
    assert "instr_love_languages" in result_ids


def test_query_text_can_recover_frameworks_from_mixed_assessment_blob(repo_root):
    repository = load_repository_strict(repo_root)
    results = query_results(
        repository,
        text="Human Design Enneagram MBTI Big Five OCEAN StrengthsFinder DISC KOLBE Dark Triad Love Language natal birth chart astrology",
    )
    result_ids = {result.instrument_id for result in results}
    assert "instr_human_design" in result_ids
    assert "instr_big_five" in result_ids
    assert "instr_mbti" in result_ids
    assert "instr_enneagram" in result_ids
    assert "instr_love_languages" in result_ids
    assert "instr_natal_astrology" in result_ids


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
    next_query_tools = {item["tool"] for item in payload["suggested_next_queries"]}
    assert "trace_to_motifs" in next_query_tools
    assert "list_interaction_hypotheses" in next_query_tools


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
    assert payload["summary"]["instruments_with_multiple_claims"] == 15
    assert payload["summary"]["instruments_with_multiple_inferences"] == 15
    assert payload["summary"]["instruments_with_multiple_risks"] == 15
    assert payload["summary"]["instruments_with_multiple_use_cases"] == 15


def test_audit_filter_surfaces_missing_official_resources(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository, needs_official_or_semi_official_resource=True)
    result_ids = {entry["instrument_id"] for entry in payload["instruments"]}
    assert {"instr_attachment_styles", "instr_dark_triad", "instr_natal_astrology"}.issubset(result_ids)


def test_audit_filter_surfaces_thin_claim_layers(repo_root):
    repository = load_repository_strict(repo_root)
    payload = audit_repository(repository, needs_multiple_claims=True)
    assert payload["instruments"] == []


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


def test_find_motifs_related_to_mbti(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = find_motifs(repository, extensions, related_to="MBTI")
    motif_ids = {item["id"] for item in payload}
    assert "mtf_social_energy_orientation" in motif_ids
    assert "mtf_pattern_abstraction_preference" in motif_ids


def test_trace_entity_to_motifs_surfaces_construct_and_direct_links(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = trace_entity_to_motifs(repository, extensions, "MBTI")
    motif_ids = {item["motif"]["id"] for item in payload["motif_summary"]}
    assert "mtf_identity_adhesion" in motif_ids
    assert "mtf_structure_and_closure_preference" in motif_ids
    assert payload["construct_mappings"]


def test_motif_record_includes_linked_mappings(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = motif_record(repository, extensions, "Social Energy Orientation")
    assert payload["motif"]["id"] == "mtf_social_energy_orientation"
    assert payload["linked_mappings"]


def test_protocol_record_expands_techniques(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = protocol_record(extensions, "ILENS")
    assert payload["protocol"]["id"] == "proto_ilens"
    assert len(payload["techniques"]) >= 3
    component_ids = {item["id"] for item in payload["component_programs"]}
    assert {"proto_paradox_finder", "proto_translation_memo"} <= component_ids


def test_agent_orientation_surfaces_featured_packs_and_resources(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = agent_orientation(repository, extensions)
    pack_ids = {item["id"] for item in payload["featured_program_packs"]}
    assert "ppk_ilens_core_trait_motive_stack" in pack_ids
    assert "registry://quickstart" in payload["recommended_resources"]
    assert "registry://ilens-walkthrough" in payload["recommended_resources"]
    assert "assessment-results-intake" in payload["recommended_prompts"]
    assert "ilens-walkthrough" in payload["recommended_prompts"]


def test_protocol_pack_summary_is_compact_and_scoped(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = protocol_pack_summary(
        repository,
        extensions,
        "ILENS",
        framework_refs=["Big Five", "MBTI", "Enneagram"],
    )
    assert payload["pack"]["protocol_id"] == "proto_ilens"
    assert payload["summary"]["protocol_name"] == "ILENS"
    assert "Cross-Framework Translation" in payload["summary"]["technique_names"]
    assert payload["summary"]["motif_count"] >= 1
    assert payload["summary"]["result_atom_schema_id"] == "ras_result_atom_v0_1"


def test_extension_finders_return_expected_records(repo_root):
    extensions = load_extensions_strict(repo_root)
    protocol_ids = {item["id"] for item in find_protocols(extensions, consumer="GNOMY")}
    technique_ids = {item["id"] for item in find_techniques(extensions, text="paradox")}
    contribution_ids = {item["id"] for item in find_contribution_models(extensions, text="normalized")}
    assert "proto_ilens" in protocol_ids
    assert "proto_paradox_finder" in protocol_ids
    assert "tech_paradox_scan" in technique_ids
    assert "rcm_result_atom_bundle" in contribution_ids


def test_find_interaction_hypotheses_related_to_attachment(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = find_interaction_hypotheses(
        repository,
        extensions,
        related_to="Attachment Style Frameworks",
    )
    interaction_ids = {item["id"] for item in payload}
    assert "ihp_attachment_anxiety_words_affirmation" in interaction_ids
    assert "ihp_social_energy_attachment_regulation" in interaction_ids


def test_interaction_hypothesis_record_expands_entity_refs(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = interaction_hypothesis_record(
        repository,
        extensions,
        "ihp_identity_adhesion_symbolic_meaning",
    )
    interaction = payload["interaction_hypothesis"]
    assert interaction["left"]["label"] == "Identity Adhesion"
    assert interaction["right"]["label"] == "Symbolic Meaning Load"


def test_result_atom_schema_record_is_available(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = result_atom_schema_record(extensions)
    assert payload["result_atom_schema"]["id"] == "ras_result_atom_v0_1"
    required_fields = {field["name"] for field in payload["result_atom_schema"]["required_fields"]}
    assert {"framework_id", "construct_id", "output_type", "output_value"} <= required_fields


def test_query_cli_returns_concise_error_for_unknown_program(repo_root):
    completed = subprocess.run(
        [sys.executable, "scripts/query_registry.py", "program-pack", "novel"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 1
    assert "Traceback" not in completed.stderr
    assert "No extension record found for 'novel'" in completed.stderr


def test_protocol_pack_expands_scope_for_ilens(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = protocol_pack(
        repository,
        extensions,
        "ILENS",
        framework_refs=["MBTI", "Enneagram"],
    )
    assert payload["pack"]["protocol_id"] == "proto_ilens"
    assert {"instr_mbti", "instr_enneagram"} <= set(payload["pack"]["target_framework_ids"])
    assert payload["techniques"]
    component_ids = {item["id"] for item in payload["component_programs"]}
    assert "proto_paradox_finder" in component_ids
    assert payload["motif_summary"]
    assert payload["interaction_hypotheses"]
    assert payload["return_contract"]["preferred_contribution_model_ids"]
    assert payload["return_contract"]["result_atom_schema"]["id"] == "ras_result_atom_v0_1"


def test_find_protocol_packs_surfaces_featured_catalog_entries(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = find_protocol_packs(repository, extensions, featured_only=True)
    pack_ids = {item["id"] for item in payload}
    assert "ppk_ilens_core_trait_motive_stack" in pack_ids
    assert "ppk_translation_attachment_and_care" in pack_ids


def test_research_promotion_registry_record_is_available(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = research_promotion_registry_record(extensions)
    assert payload["promotion_registry"]["id"] == "research_promotion_v0_1"
    assert payload["promotion_pathway_count"] >= 5


def test_find_promotion_pathways_for_mapping_vote(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = find_promotion_pathways(extensions, contribution_model="Mapping Vote")
    pathway_ids = {item["id"] for item in payload}
    assert "rpp_mapping_vote_to_house_mapping" in pathway_ids


def test_promotion_pathway_record_expands_contribution_model(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = promotion_pathway_record(extensions, "rpp_protocol_feedback_to_protocol_revision")
    assert payload["promotion_pathway"]["target_outcome_type"] == "protocol_revision"
    assert payload["contribution_model"]["id"] == "rcm_protocol_feedback"
    assert payload["stages"][-1]["id"] == "protocol_revision"


def test_curated_protocol_pack_record_expands_catalog_entry(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    payload = curated_protocol_pack_record(
        repository,
        extensions,
        "ppk_ilens_core_trait_motive_stack",
    )
    assert payload["catalog_entry"]["protocol_id"] == "proto_ilens"
    assert payload["protocol_pack"]["pack"]["protocol_id"] == "proto_ilens"
    assert {"instr_big_five", "instr_mbti", "instr_enneagram"} <= set(
        payload["protocol_pack"]["pack"]["target_framework_ids"]
    )


def test_protocol_pack_grammar_has_required_sections():
    payload = protocol_pack_grammar()
    section_names = {section["section"] for section in payload["required_sections"]}
    assert payload["id"] == "protocol_pack_grammar_v0_1"
    assert {"pack", "protocol", "techniques", "return_contract"} <= section_names
