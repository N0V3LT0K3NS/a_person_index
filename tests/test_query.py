from __future__ import annotations

import subprocess
import sys

from personality_registry.extensions import load_extensions_strict
from personality_registry.loader import load_repository_strict
from personality_registry.query import (
    actualization_protocol_record,
    agent_orientation,
    analysis_mode_record,
    artifact_class_record,
    audit_repository,
    capability_record,
    compare_instruments,
    find_contribution_models,
    find_actualization_protocols,
    find_analysis_modes,
    find_artifact_classes,
    find_capabilities,
    find_host_profiles,
    find_comparison_shapes,
    find_expression_profiles,
    find_interaction_hypotheses,
    find_motifs,
    find_promotion_pathways,
    find_protocol_packs,
    find_protocols,
    find_techniques,
    find_instruments,
    find_workflow_recipes,
    curated_protocol_pack_record,
    comparison_shape_record,
    expression_profile_record,
    interaction_hypothesis_record,
    instrument_record,
    motif_record,
    protocol_pack,
    protocol_pack_summary,
    protocol_pack_grammar,
    protocol_record,
    prepare_comparison_run,
    prepare_artifact_realization,
    prepare_artifact_template,
    query_results,
    promotion_pathway_record,
    recommend_next_path,
    research_promotion_registry_record,
    result_atom_schema_record,
    resolve_instrument,
    show_instrument,
    trace_entity_to_motifs,
    host_profile_record,
    workflow_recipe_record,
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
    assert payload["summary"]["instrument_count"] == 16
    assert payload["summary"]["instruments_with_crosswalks"] == 16
    assert payload["summary"]["instruments_with_multiple_resources"] == 16
    assert payload["summary"]["instruments_with_multiple_constructs"] == 16
    assert payload["summary"]["instruments_with_multiple_claims"] == 16
    assert payload["summary"]["instruments_with_multiple_inferences"] == 16
    assert payload["summary"]["instruments_with_multiple_risks"] == 16
    assert payload["summary"]["instruments_with_multiple_use_cases"] == 16


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


def test_contextual_and_pairwise_protocol_records_are_available(repo_root):
    extensions = load_extensions_strict(repo_root)
    contextual_payload = protocol_record(extensions, "Contextual Comparison Memo")
    pairwise_payload = protocol_record(extensions, "Pairwise Relational Comparison")
    assert contextual_payload["protocol"]["program_kind"] == "comparison_program"
    assert pairwise_payload["protocol"]["program_kind"] == "comparison_program"
    contextual_component_ids = {item["id"] for item in contextual_payload["component_programs"]}
    pairwise_component_ids = {item["id"] for item in pairwise_payload["component_programs"]}
    assert "proto_paradox_finder" in contextual_component_ids
    assert {"proto_translation_memo", "proto_paradox_finder"} <= pairwise_component_ids


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


def test_contextual_and_pairwise_packs_are_discoverable(repo_root):
    repository = load_repository_strict(repo_root)
    extensions = load_extensions_strict(repo_root)
    pack_ids = {
        item["id"] for item in find_protocol_packs(
            repository,
            extensions,
            protocol="Contextual Comparison Memo",
        )
    }
    assert "ppk_contextual_core_trait_motive_stack" in pack_ids
    pairwise_pack_ids = {
        item["id"]
        for item in find_protocol_packs(
            repository,
            extensions,
            protocol="Pairwise Relational Comparison",
        )
    }
    assert "ppk_pairwise_relational_baseline" in pairwise_pack_ids


def test_extension_finders_return_expected_records(repo_root):
    extensions = load_extensions_strict(repo_root)
    mode_ids = {item["id"] for item in find_analysis_modes(extensions, text="plan")}
    comparison_shape_ids = {
        item["id"]
        for item in find_comparison_shapes(
            extensions,
            artifact_class="Context Matrix",
            text="compare me across time",
        )
    }
    capability_ids = {
        item["id"]
        for item in find_capabilities(
            extensions,
            artifact_class="Context Matrix",
            include_optional=False,
            text="render",
        )
    }
    host_profile_ids = {
        item["id"]
        for item in find_host_profiles(
            extensions,
            capability="Markdown Write",
            text="codex",
        )
    }
    artifact_ids = {
        item["id"]
        for item in find_artifact_classes(
            extensions,
            capability="Markdown Write",
            text="markdown",
        )
    }
    actualization_ids = {
        item["id"]
        for item in find_actualization_protocols(
            extensions,
            artifact_class="Comparative Memo",
            capability="Structured Text Render",
        )
    }
    protocol_ids = {item["id"] for item in find_protocols(extensions, consumer="GNOMY")}
    technique_ids = {item["id"] for item in find_techniques(extensions, text="paradox")}
    contribution_ids = {item["id"] for item in find_contribution_models(extensions, text="normalized")}
    assert "mode_run_planning" in mode_ids
    assert "cmp_contextual_time_slices" in comparison_shape_ids
    assert "host_codex_desktop" in host_profile_ids
    assert {"cap_table_render", "cap_markdown_write"} <= capability_ids
    assert "art_agent_markdown_handoff" in artifact_ids
    assert "actx_single_subject_comparative_memo" in actualization_ids
    assert "proto_ilens" in protocol_ids
    assert "proto_paradox_finder" in protocol_ids
    assert "tech_paradox_scan" in technique_ids
    assert "rcm_result_atom_bundle" in contribution_ids


def test_analysis_mode_and_artifact_records_are_available(repo_root):
    extensions = load_extensions_strict(repo_root)
    mode_payload = analysis_mode_record(extensions, "Run Planning")
    comparison_shape_payload = comparison_shape_record(extensions, "Contextual Time Slices")
    host_payload = host_profile_record(extensions, "Codex Desktop")
    capability_payload = capability_record(extensions, "Markdown Write")
    expression_payload = expression_profile_record(extensions, "Explanatory Scaffolded")
    artifact_payload = artifact_class_record(extensions, "Context Matrix")
    actualization_payload = actualization_protocol_record(extensions, "Pairwise Relational Sheet")
    assert mode_payload["analysis_mode"]["id"] == "mode_run_planning"
    assert comparison_shape_payload["comparison_shape"]["id"] == "cmp_contextual_time_slices"
    assert host_payload["host_profile"]["id"] == "host_codex_desktop"
    host_capability_ids = {item["id"] for item in host_payload["capabilities"]}
    assert {"cap_markdown_write", "cap_file_write"} <= host_capability_ids
    assert capability_payload["capability"]["id"] == "cap_markdown_write"
    assert expression_payload["expression_profile"]["id"] == "expr_explanatory"
    used_by_artifact_ids = {item["id"] for item in capability_payload["used_by_artifact_classes"]}
    used_by_host_ids = {item["id"] for item in capability_payload["used_by_host_profiles"]}
    assert "art_comparative_memo" in used_by_artifact_ids
    assert "host_codex_desktop" in used_by_host_ids
    assert artifact_payload["artifact_class"]["id"] == "art_context_matrix"
    assert artifact_payload["default_expression_profile"]["id"] == "expr_explanatory"
    assert "cap_spreadsheet_render" in artifact_payload["artifact_class"]["optional_capability_ids"]
    assert actualization_payload["actualization_protocol"]["id"] == "actx_pairwise_relational_sheet"
    assert "cap_diagram_render" in actualization_payload["actualization_protocol"]["optional_capability_ids"]
    related_artifact_ids = {item["id"] for item in comparison_shape_payload["suitable_artifact_classes"]}
    assert "art_context_matrix" in related_artifact_ids
    declaration_field_ids = {
        item["id"] for item in comparison_shape_payload["comparison_shape"]["declaration_fields"]
    }
    assert {"slice_labels", "comparison_question"} <= declaration_field_ids


def test_find_expression_profiles_for_artifact(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = find_expression_profiles(
        extensions,
        artifact_class="Agent Markdown Handoff",
    )
    profile_ids = {item["id"] for item in payload}
    assert profile_ids == {"expr_technical"}


def test_find_workflow_recipes_for_context_matrix(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = find_workflow_recipes(
        extensions,
        artifact_class="Context Matrix",
    )
    recipe_ids = {item["id"] for item in payload}
    assert recipe_ids == {"wfr_context_matrix_explanatory"}


def test_find_workflow_recipes_for_human_model_card(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = find_workflow_recipes(
        extensions,
        artifact_class="Human Model Card",
    )
    recipe_ids = {item["id"] for item in payload}
    assert "wfr_human_model_card_mixed" in recipe_ids


def test_find_workflow_recipes_for_result_bundle(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = find_workflow_recipes(
        extensions,
        artifact_class="Structured Result Bundle",
    )
    recipe_ids = {item["id"] for item in payload}
    assert "wfr_structured_result_bundle_technical" in recipe_ids
    assert "wfr_comparison_result_bundle_technical" in recipe_ids


def test_recommend_next_path_prefers_context_matrix_when_capabilities_fit(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Contextual and Multi-Subject Comparison",
        capability_refs=["Markdown Write", "Table Render"],
        text="compare me across time and make a matrix",
    )
    assert payload["run_mode"]["id"] == "mode_contextual_comparison"
    assert payload["recommended_comparison_shape"]["id"] == "cmp_contextual_time_slices"
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_context_matrix"
    assert payload["recommended_expression_profile"]["id"] == "expr_explanatory"
    assert payload["recommended_workflow_recipe"]["workflow_recipe"]["id"] == "wfr_context_matrix_explanatory"
    assert payload["recommended_actualization_protocol"]["actualization_protocol"]["id"] == "actx_context_matrix_render"
    assert payload["recommended_artifact"]["fit_status"] == "ready"
    assert "fetch_comparison_shape" in payload["recommended_tools"]
    assert "prepare_comparison_run" in payload["recommended_tools"]
    assert "registry://comparison-preflight" in payload["recommended_resources"]


def test_prepare_comparison_run_surfaces_missing_time_slice_fields(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_comparison_run(
        extensions,
        comparison_shape="Contextual Time Slices",
        declarations={"comparison_question": "What changed in a meaningful way?"},
    )
    assert payload["readiness_status"] == "needs_declarations"
    missing_ids = {item["id"] for item in payload["missing_required_fields"]}
    assert "slice_labels" in missing_ids
    assert payload["path_recommendation"] is None


def test_prepare_comparison_run_returns_ready_path_when_declared(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_comparison_run(
        extensions,
        comparison_shape="Contextual Time Slices",
        declarations={
            "slice_labels": ["2013 self", "2020 self"],
            "comparison_question": "What changed in a meaningful way?",
        },
        capability_refs=["Markdown Write", "Table Render"],
    )
    assert payload["readiness_status"] == "ready"
    assert payload["path_recommendation"]["recommended_comparison_shape"]["id"] == "cmp_contextual_time_slices"
    assert payload["path_recommendation"]["recommended_artifact"]["artifact_class"]["id"] == "art_context_matrix"


def test_prepare_comparison_run_can_expand_host_profile_context(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_comparison_run(
        extensions,
        comparison_shape="Contextual Time Slices",
        declarations={
            "slice_labels": ["earlier self", "later self"],
            "comparison_question": "What meaningfully changed?",
        },
        host_profile_refs=["Claude Code"],
    )
    assert payload["readiness_status"] == "ready"
    declared_host_ids = {item["id"] for item in payload["declared_host_profiles"]}
    declared_capability_ids = {item["id"] for item in payload["declared_capabilities"]}
    assert declared_host_ids == {"host_claude_code"}
    assert {"cap_markdown_write", "cap_file_write"} <= declared_capability_ids
    assert payload["path_recommendation"]["recommended_comparison_shape"]["id"] == "cmp_contextual_time_slices"
    assert payload["path_recommendation"]["recommended_artifact"]["artifact_class"]["id"] in {
        "art_comparative_memo",
        "art_context_matrix",
    }


def test_find_pairwise_comparison_shapes_from_relational_text(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = find_comparison_shapes(
        extensions,
        text="compare us in relationship and show where the seams are",
    )
    shape_ids = {item["id"] for item in payload}
    assert "cmp_pairwise_relational_question" in shape_ids


def test_workflow_recipe_record_expands_related_surfaces(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = workflow_recipe_record(extensions, "Context Matrix Explanatory")
    assert payload["workflow_recipe"]["id"] == "wfr_context_matrix_explanatory"
    assert payload["artifact_class"]["id"] == "art_context_matrix"
    assert payload["expression_profile"]["id"] == "expr_explanatory"
    assert payload["actualization_protocol"]["id"] == "actx_context_matrix_render"
    block_ids = {item["id"] for item in payload["workflow_recipe"]["realization_blocks"]}
    assert {"slice_declaration", "context_matrix"} <= block_ids


def test_prepare_artifact_realization_returns_context_matrix_scaffold(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_realization(
        extensions,
        workflow_recipe="Context Matrix Explanatory",
        capability_refs=["Markdown Write", "Table Render"],
    )
    assert payload["readiness_status"] == "ready"
    assert payload["selected_realization_form"] == "markdown table"
    block_ids = {item["id"] for item in payload["realization_blocks"]}
    assert {"slice_declaration", "comparison_axes", "context_matrix"} <= block_ids


def test_prepare_artifact_realization_can_expand_host_profile_context(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_realization(
        extensions,
        workflow_recipe="Human Model Card Mixed",
        host_profile_refs=["Codex Desktop"],
    )
    assert payload["readiness_status"] == "ready"
    declared_host_ids = {item["id"] for item in payload["declared_host_profiles"]}
    assert declared_host_ids == {"host_codex_desktop"}
    assert payload["selected_realization_form"] == "markdown card"


def test_prepare_artifact_realization_surfaces_missing_capabilities(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_realization(
        extensions,
        workflow_recipe="Agent Markdown Handoff Technical",
        capability_refs=["Markdown Write"],
    )
    assert payload["readiness_status"] == "partial"
    assert payload["missing_required_capability_ids"] == ["cap_file_write"]


def test_prepare_artifact_realization_returns_result_bundle_scaffold(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_realization(
        extensions,
        workflow_recipe="Structured Result Bundle Technical",
        capability_refs=["JSON Emit", "File Write"],
    )
    assert payload["readiness_status"] == "ready"
    assert payload["selected_realization_form"] == "JSON bundle"
    block_ids = {item["id"] for item in payload["realization_blocks"]}
    assert {"bundle_header", "structured_findings", "provenance_partitions"} <= block_ids


def test_prepare_artifact_realization_returns_comparison_result_bundle_scaffold(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_realization(
        extensions,
        workflow_recipe="Comparison Result Bundle Technical",
        capability_refs=["JSON Emit", "File Write"],
    )
    assert payload["readiness_status"] == "ready"
    assert payload["selected_realization_form"] == "JSON bundle"
    block_ids = {item["id"] for item in payload["realization_blocks"]}
    assert {"comparison_bundle_header", "structured_comparison_findings", "provenance_partitions"} <= block_ids


def test_prepare_artifact_template_returns_markdown_card_stub(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_template(
        extensions,
        workflow_recipe="Human Model Card Mixed",
        host_profile_refs=["Codex Desktop"],
    )
    assert payload["template_kind"] == "markdown_document"
    assert payload["template_filename_hint"].endswith(".md")
    assert payload["template_text"].startswith("# Human Model Card Mixed")
    assert "## Card Header" in payload["template_text"]
    assert "## Provenance and Inputs" in payload["template_text"]
    assert payload["template_object"] is None


def test_prepare_artifact_template_returns_json_bundle_stub(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = prepare_artifact_template(
        extensions,
        workflow_recipe="Structured Result Bundle Technical",
        host_profile_refs=["Codex Desktop"],
    )
    assert payload["template_kind"] == "json_object"
    assert payload["template_filename_hint"].endswith(".json")
    assert payload["template_text"] is None
    assert (
        payload["template_object"]["template_meta"]["workflow_recipe_id"]
        == "wfr_structured_result_bundle_technical"
    )
    assert "structured_findings" in payload["template_object"]["blocks"]
    assert (
        payload["template_object"]["blocks"]["provenance_partitions"]["partitions"]["canonical_framework_content"]
        == []
    )


def test_recommend_next_path_infers_contextual_mode_from_text(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        capability_refs=["Markdown Write", "Table Render"],
        text="compare me across time and make a matrix",
    )
    assert payload["run_mode"]["id"] == "mode_contextual_comparison"
    assert payload["run_mode_inferred"] is True
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_context_matrix"
    assert payload["recommended_actualization_protocol"]["actualization_protocol"]["id"] == "actx_context_matrix_render"
    assert "list_capabilities" not in payload["recommended_tools"]
    assert "prepare_artifact_realization" in payload["recommended_tools"]
    assert "prepare_artifact_template" in payload["recommended_tools"]


def test_recommend_next_path_respects_explicit_pairwise_shape(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Contextual and Multi-Subject Comparison",
        comparison_shape="Pairwise Relational Question",
        capability_refs=["Markdown Write", "Table Render"],
    )
    assert payload["recommended_comparison_shape"]["id"] == "cmp_pairwise_relational_question"
    assert payload["comparison_shape_inferred"] is False
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_pairwise_relational_sheet"
    assert (
        payload["recommended_actualization_protocol"]["actualization_protocol"]["id"]
        == "actx_pairwise_relational_sheet"
    )


def test_recommend_next_path_can_target_human_model_card(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Artifact Actualization",
        capability_refs=["Markdown Write", "Structured Text Render"],
        text="make a human model card",
    )
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_human_model_card"
    assert payload["recommended_workflow_recipe"]["workflow_recipe"]["id"] == "wfr_human_model_card_mixed"


def test_recommend_next_path_can_expand_host_profile_context(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Artifact Actualization",
        host_profile_refs=["Codex Desktop"],
        text="make a human model card",
    )
    declared_host_ids = {item["id"] for item in payload["declared_host_profiles"]}
    declared_capability_ids = {item["id"] for item in payload["declared_capabilities"]}
    assert declared_host_ids == {"host_codex_desktop"}
    assert {"cap_markdown_write", "cap_structured_text_render"} <= declared_capability_ids
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_human_model_card"
    assert payload["recommended_workflow_recipe"]["workflow_recipe"]["id"] == "wfr_human_model_card_mixed"
    assert "Capabilities were expanded from the declared host profile set." in payload["notes"]


def test_recommend_next_path_can_target_structured_result_bundle(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Bounded Single-Subject Mixed Stack",
        capability_refs=["JSON Emit", "File Write"],
        artifact_class="Structured Result Bundle",
    )
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_result_bundle"
    assert payload["recommended_expression_profile"]["id"] == "expr_technical"
    assert (
        payload["recommended_actualization_protocol"]["actualization_protocol"]["id"]
        == "actx_structured_result_bundle_packaging"
    )
    assert (
        payload["recommended_workflow_recipe"]["workflow_recipe"]["id"]
        == "wfr_structured_result_bundle_technical"
    )
    assert "prepare_artifact_realization" in payload["recommended_tools"]
    assert "prepare_artifact_template" in payload["recommended_tools"]


def test_recommend_next_path_can_target_contextual_result_bundle(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Contextual and Multi-Subject Comparison",
        comparison_shape="Contextual Time Slices",
        capability_refs=["JSON Emit", "File Write"],
        artifact_class="Structured Result Bundle",
    )
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_result_bundle"
    assert payload["recommended_expression_profile"]["id"] == "expr_technical"
    assert (
        payload["recommended_actualization_protocol"]["actualization_protocol"]["id"]
        == "actx_comparison_result_bundle_packaging"
    )
    assert (
        payload["recommended_workflow_recipe"]["workflow_recipe"]["id"]
        == "wfr_comparison_result_bundle_technical"
    )


def test_recommend_next_path_can_target_pairwise_result_bundle_without_matrix_fallback(repo_root):
    extensions = load_extensions_strict(repo_root)
    payload = recommend_next_path(
        extensions,
        run_mode="Contextual and Multi-Subject Comparison",
        comparison_shape="Pairwise Relational Question",
        capability_refs=["JSON Emit", "File Write"],
        artifact_class="Structured Result Bundle",
    )
    assert payload["recommended_artifact"]["artifact_class"]["id"] == "art_result_bundle"
    assert (
        payload["recommended_actualization_protocol"]["actualization_protocol"]["id"]
        == "actx_comparison_result_bundle_packaging"
    )
    assert (
        payload["recommended_workflow_recipe"]["workflow_recipe"]["id"]
        == "wfr_comparison_result_bundle_technical"
    )


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
