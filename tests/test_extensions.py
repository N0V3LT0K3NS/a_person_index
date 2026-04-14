from __future__ import annotations

from personality_registry.extensions import load_extensions_strict


def test_extension_registries_load_and_cross_reference(repo_root):
    extensions = load_extensions_strict(repo_root)

    assert len(extensions.analysis_modes) >= 5
    assert len(extensions.artifact_classes) >= 4
    assert len(extensions.actualization_protocols) >= 3
    assert len(extensions.motifs) >= 10
    assert len(extensions.mappings) >= 10
    assert len(extensions.interaction_hypotheses) >= 5
    assert len(extensions.techniques) >= 5
    assert len(extensions.protocols) >= 6
    assert len(extensions.protocol_packs) >= 6
    assert len(extensions.contribution_models) >= 4
    assert len(extensions.promotion_registry.promotion_pathways) >= 5

    analysis_mode_ids = {mode.id for mode in extensions.analysis_modes}
    artifact_class_ids = {artifact.id for artifact in extensions.artifact_classes}
    motif_ids = {motif.id for motif in extensions.motifs}
    technique_ids = {technique.id for technique in extensions.techniques}
    protocol_ids = {protocol.id for protocol in extensions.protocols}
    protocol_pack_ids = {protocol_pack.id for protocol_pack in extensions.protocol_packs}
    stage_ids = {stage.id for stage in extensions.promotion_registry.stages}

    assert "mode_bounded_single_subject" in analysis_mode_ids
    assert "art_comparative_memo" in artifact_class_ids
    assert "mtf_social_energy_orientation" in motif_ids
    assert "tech_paradox_scan" in technique_ids
    assert "proto_paradox_finder" in protocol_ids
    assert "ppk_ilens_core_trait_motive_stack" in protocol_pack_ids
    assert "proto_contextual_comparison" in protocol_ids
    assert "proto_pairwise_relational_comparison" in protocol_ids
    assert "ppk_contextual_core_trait_motive_stack" in protocol_pack_ids
    assert "ppk_pairwise_relational_baseline" in protocol_pack_ids
    assert extensions.result_atom_schema.id == "ras_result_atom_v0_1"
    assert extensions.promotion_registry.id == "research_promotion_v0_1"
    assert "reviewed" in stage_ids

    for artifact_class in extensions.artifact_classes:
        assert set(artifact_class.suitable_mode_ids).issubset(analysis_mode_ids)

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

    for contribution_model in extensions.contribution_models:
        assert set(contribution_model.promotion_path).issubset(stage_ids)

    for interaction in extensions.interaction_hypotheses:
        assert set(interaction.protocol_relevance).issubset(protocol_ids)
