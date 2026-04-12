from __future__ import annotations

import json

from personality_registry.builder import build_outputs


def test_build_outputs_creates_expected_payloads(repo_root):
    export_payload = build_outputs(repo_root)

    index_path = repo_root / "generated" / "index.json"
    search_path = repo_root / "generated" / "search.json"
    audit_path = repo_root / "generated" / "audit.json"
    registry_path = repo_root / "generated" / "registry.json"

    assert index_path.exists()
    assert search_path.exists()
    assert audit_path.exists()
    assert registry_path.exists()

    index_payload = json.loads(index_path.read_text(encoding="utf-8"))
    search_payload = json.loads(search_path.read_text(encoding="utf-8"))
    audit_payload = json.loads(audit_path.read_text(encoding="utf-8"))

    assert len(index_payload["instruments"]) == len(export_payload["instruments"])
    assert len(search_payload["entries"]) == len(export_payload["instruments"])
    assert audit_payload["summary"]["instrument_count"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_constructs"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_claims"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_inferences"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_risks"] == len(export_payload["instruments"])
    assert audit_payload["summary"]["instruments_with_multiple_use_cases"] == len(export_payload["instruments"])

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
