from __future__ import annotations

import json

from personality_registry.builder import build_outputs


def test_build_outputs_creates_expected_payloads(repo_root):
    export_payload = build_outputs(repo_root)

    index_path = repo_root / "generated" / "index.json"
    search_path = repo_root / "generated" / "search.json"
    audit_path = repo_root / "generated" / "audit.json"
    manifest_path = repo_root / "generated" / "manifest.json"
    registry_path = repo_root / "generated" / "registry.json"

    assert index_path.exists()
    assert search_path.exists()
    assert audit_path.exists()
    assert manifest_path.exists()
    assert registry_path.exists()

    index_payload = json.loads(index_path.read_text(encoding="utf-8"))
    search_payload = json.loads(search_path.read_text(encoding="utf-8"))
    audit_payload = json.loads(audit_path.read_text(encoding="utf-8"))
    manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert len(index_payload["instruments"]) == len(export_payload["instruments"])
    assert len(search_payload["entries"]) == len(export_payload["instruments"])
    assert audit_payload["summary"]["instrument_count"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_constructs"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_claims"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_inferences"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_risks"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_use_cases"] == len(export_payload["instruments"])
    assert index_payload["product_layers"]["house_synthesis"]["motif_count"] == len(
        export_payload["house_synthesis"]["motifs"]
    )
    assert index_payload["product_layers"]["house_synthesis"]["interaction_hypothesis_count"] == len(
        export_payload["house_synthesis"]["interaction_hypotheses"]
    )
    assert index_payload["product_layers"]["protocol_library"]["protocol_count"] == len(
        export_payload["protocol_library"]["protocols"]
    )
    assert index_payload["product_layers"]["research_stream"]["contribution_model_count"] == len(
        export_payload["research_stream"]["contribution_models"]
    )
    assert index_payload["product_layers"]["research_stream"]["result_atom_schema_id"] == export_payload[
        "research_stream"
    ]["result_atom_schema"]["id"]

    instrument_ids = {entry["id"] for entry in index_payload["instruments"]}
    assert {"instr_big_five", "instr_enneagram", "instr_mbti"}.issubset(instrument_ids)

    audit_ids = {entry["instrument_id"] for entry in audit_payload["instruments"]}
    assert {"instr_big_five", "instr_enneagram", "instr_mbti"}.issubset(audit_ids)

    attachment_entry = next(
        entry for entry in audit_payload["instruments"] if entry["instrument_id"] == "instr_attachment_styles"
    )
    assert attachment_entry["coverage"]["has_multiple_claims"]
    assert attachment_entry["coverage"]["has_multiple_inferences"]
    assert attachment_entry["coverage"]["has_multiple_risks"]
    assert attachment_entry["coverage"]["has_multiple_use_cases"]
    assert export_payload["protocol_library"]["protocols"][0]["id"].startswith("proto_")
    assert manifest_payload["repository"]["name"] == "personality-instrument-registry"
    assert manifest_payload["downstream_contract"]["result_atom_schema_id"] == "ras_result_atom_v0_1"
    assert manifest_payload["service_primitives"]
