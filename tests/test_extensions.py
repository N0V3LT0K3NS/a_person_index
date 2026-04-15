from __future__ import annotations

from personality_registry.extensions import load_extensions_strict


def test_extension_registries_load_and_cross_reference(repo_root):
    extensions = load_extensions_strict(repo_root)

    assert len(extensions.analysis_modes) >= 5
    assert len(extensions.comparison_shapes) >= 4
    assert len(extensions.capabilities) >= 8
    assert len(extensions.expression_profiles) >= 4
    assert len(extensions.artifact_classes) >= 4
    assert len(extensions.actualization_protocols) >= 5
    assert len(extensions.workflow_recipes) >= 6
    assert len(extensions.motifs) >= 10
    assert len(extensions.mappings) >= 10
    assert len(extensions.interaction_hypotheses) >= 5
    assert len(extensions.techniques) >= 5
    assert len(extensions.protocols) >= 6
    assert len(extensions.protocol_packs) >= 6
    assert len(extensions.contribution_models) >= 4
    assert len(extensions.promotion_registry.promotion_pathways) >= 5

    analysis_mode_ids = {mode.id for mode in extensions.analysis_modes}
    comparison_shape_ids = {shape.id for shape in extensions.comparison_shapes}
    capability_ids = {capability.id for capability in extensions.capabilities}
    expression_profile_ids = {profile.id for profile in extensions.expression_profiles}
    artifact_class_ids = {artifact.id for artifact in extensions.artifact_classes}
    workflow_recipe_ids = {recipe.id for recipe in extensions.workflow_recipes}
    motif_ids = {motif.id for motif in extensions.motifs}
    technique_ids = {technique.id for technique in extensions.techniques}
    protocol_ids = {protocol.id for protocol in extensions.protocols}
    protocol_pack_ids = {protocol_pack.id for protocol_pack in extensions.protocol_packs}
    stage_ids = {stage.id for stage in extensions.promotion_registry.stages}

    assert "mode_bounded_single_subject" in analysis_mode_ids
    assert "cmp_contextual_time_slices" in comparison_shape_ids
    assert "cap_markdown_write" in capability_ids
    assert "expr_explanatory" in expression_profile_ids
    assert "art_comparative_memo" in artifact_class_ids
    assert "wfr_context_matrix_explanatory" in workflow_recipe_ids
    assert "wfr_human_model_card_mixed" in workflow_recipe_ids
    assert "wfr_structured_result_bundle_technical" in workflow_recipe_ids
    assert "mtf_social_energy_orientation" in motif_ids
    assert "tech_paradox_scan" in technique_ids
    assert "proto_paradox_finder" in protocol_ids
    assert "ppk_ilens_core_trait_motive_stack" in protocol_pack_ids
    assert "proto_contextual_comparison" in protocol_ids
    assert "proto_pairwise_relational_comparison" in protocol_ids
    assert "ppk_contextual_core_trait_motive_stack" in protocol_pack_ids
    assert "ppk_pairwise_relational_baseline" in protocol_pack_ids
    assert "actx_structured_result_bundle_packaging" in {protocol.id for protocol in extensions.actualization_protocols}
    assert extensions.result_atom_schema.id == "ras_result_atom_v0_1"
    assert extensions.promotion_registry.id == "research_promotion_v0_1"
    assert "reviewed" in stage_ids

    for artifact_class in extensions.artifact_classes:
        assert set(artifact_class.suitable_mode_ids).issubset(analysis_mode_ids)
        assert set(artifact_class.required_capability_ids).issubset(capability_ids)
        assert set(artifact_class.optional_capability_ids).issubset(capability_ids)

    for comparison_shape in extensions.comparison_shapes:
        assert set(comparison_shape.mode_ids).issubset(analysis_mode_ids)
        assert set(comparison_shape.suitable_artifact_class_ids).issubset(artifact_class_ids)
        assert set(comparison_shape.recommended_protocol_ids).issubset(protocol_ids)
        assert comparison_shape.declaration_fields

    for mapping in extensions.mappings:
        assert mapping.target_entity_id in motif_ids

    for protocol in extensions.protocols:
        assert set(protocol.technique_ids).issubset(technique_ids)
        assert set(protocol.component_program_ids).issubset(protocol_ids)

    for protocol_pack in extensions.protocol_packs:
        assert protocol_pack.protocol_id in protocol_ids

    for actualization_protocol in extensions.actualization_protocols:
        assert set(actualization_protocol.run_mode_ids).issubset(analysis_mode_ids)
        assert set(actualization_protocol.protocol_ids).issubset(protocol_ids)
        assert set(actualization_protocol.target_artifact_class_ids).issubset(artifact_class_ids)
        assert set(actualization_protocol.required_capability_ids).issubset(capability_ids)
        assert set(actualization_protocol.optional_capability_ids).issubset(capability_ids)

    for workflow_recipe in extensions.workflow_recipes:
        assert set(workflow_recipe.run_mode_ids).issubset(analysis_mode_ids)
        assert workflow_recipe.artifact_class_id in artifact_class_ids
        assert workflow_recipe.expression_profile_id in expression_profile_ids
        assert workflow_recipe.actualization_protocol_id in {
            protocol.id for protocol in extensions.actualization_protocols
        }
        assert set(workflow_recipe.required_capability_ids).issubset(capability_ids)
        assert workflow_recipe.realization_blocks

    for contribution_model in extensions.contribution_models:
        assert set(contribution_model.promotion_path).issubset(stage_ids)

    for interaction in extensions.interaction_hypotheses:
        assert set(interaction.protocol_relevance).issubset(protocol_ids)
