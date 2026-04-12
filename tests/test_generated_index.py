from __future__ import annotations

import json

from personality_registry.builder import build_outputs


def test_build_outputs_creates_expected_payloads(repo_root):
    export_payload = build_outputs(repo_root)

    index_path = repo_root / "generated" / "index.json"
    search_path = repo_root / "generated" / "search.json"
    registry_path = repo_root / "generated" / "registry.json"

    assert index_path.exists()
    assert search_path.exists()
    assert registry_path.exists()

    index_payload = json.loads(index_path.read_text(encoding="utf-8"))
    search_payload = json.loads(search_path.read_text(encoding="utf-8"))

    assert len(index_payload["instruments"]) == len(export_payload["instruments"])
    assert len(search_payload["entries"]) == len(export_payload["instruments"])

    instrument_ids = {entry["id"] for entry in index_payload["instruments"]}
    assert {"instr_big_five", "instr_enneagram", "instr_mbti"}.issubset(instrument_ids)
