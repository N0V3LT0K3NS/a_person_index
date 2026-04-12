from __future__ import annotations

from personality_registry.extensions import load_extensions_strict


def test_extension_registries_load_and_cross_reference(repo_root):
    extensions = load_extensions_strict(repo_root)

    assert len(extensions.motifs) >= 10
    assert len(extensions.mappings) >= 10
    assert len(extensions.interaction_hypotheses) >= 5
    assert len(extensions.techniques) >= 5
    assert len(extensions.protocols) >= 4
    assert len(extensions.protocol_packs) >= 4
    assert len(extensions.contribution_models) >= 4
    assert len(extensions.promotion_registry.promotion_pathways) >= 5

    motif_ids = {motif.id for motif in extensions.motifs}
    technique_ids = {technique.id for technique in extensions.techniques}
    protocol_ids = {protocol.id for protocol in extensions.protocols}
    protocol_pack_ids = {protocol_pack.id for protocol_pack in extensions.protocol_packs}
    stage_ids = {stage.id for stage in extensions.promotion_registry.stages}

    assert "mtf_social_energy_orientation" in motif_ids
    assert "tech_paradox_scan" in technique_ids
    assert "proto_paradox_finder" in protocol_ids
    assert "ppk_ilens_core_trait_motive_stack" in protocol_pack_ids
    assert extensions.result_atom_schema.id == "ras_result_atom_v0_1"
    assert extensions.promotion_registry.id == "research_promotion_v0_1"
    assert "reviewed" in stage_ids

    for mapping in extensions.mappings:
        assert mapping.target_entity_id in motif_ids

    for protocol in extensions.protocols:
        assert set(protocol.technique_ids).issubset(technique_ids)
        assert set(protocol.component_program_ids).issubset(protocol_ids)

    for protocol_pack in extensions.protocol_packs:
        assert protocol_pack.protocol_id in protocol_ids

    for contribution_model in extensions.contribution_models:
        assert set(contribution_model.promotion_path).issubset(stage_ids)

    for interaction in extensions.interaction_hypotheses:
        assert set(interaction.protocol_relevance).issubset(protocol_ids)
