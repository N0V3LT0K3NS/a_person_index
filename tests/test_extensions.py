from __future__ import annotations

from personality_registry.extensions import load_extensions_strict


def test_extension_registries_load_and_cross_reference(repo_root):
    extensions = load_extensions_strict(repo_root)

    assert len(extensions.motifs) >= 10
    assert len(extensions.mappings) >= 10
    assert len(extensions.techniques) >= 5
    assert len(extensions.protocols) >= 3
    assert len(extensions.contribution_models) >= 4

    motif_ids = {motif.id for motif in extensions.motifs}
    technique_ids = {technique.id for technique in extensions.techniques}

    assert "mtf_social_energy_orientation" in motif_ids
    assert "tech_paradox_scan" in technique_ids

    for mapping in extensions.mappings:
        assert mapping.target_entity_id in motif_ids

    for protocol in extensions.protocols:
        assert set(protocol.technique_ids).issubset(technique_ids)
