from __future__ import annotations

import json

from personality_registry.builder import build_outputs


def test_build_outputs_creates_expected_payloads(repo_root):
    export_payload = build_outputs(repo_root)

    index_path = repo_root / "generated" / "index.json"
    search_path = repo_root / "generated" / "search.json"
    audit_path = repo_root / "generated" / "audit.json"
    manifest_path = repo_root / "generated" / "manifest.json"
    site_variants_path = repo_root / "generated" / "site_variants.json"
    protocol_pack_grammar_path = repo_root / "generated" / "protocol_pack_grammar.json"
    protocol_pack_index_path = repo_root / "generated" / "protocol_packs" / "index.json"
    curated_protocol_pack_path = (
        repo_root / "generated" / "protocol_packs" / "ppk_ilens_core_trait_motive_stack.json"
    )
    research_promotion_path = repo_root / "generated" / "research_promotion.json"
    registry_path = repo_root / "generated" / "registry.json"

    assert index_path.exists()
    assert search_path.exists()
    assert audit_path.exists()
    assert manifest_path.exists()
    assert site_variants_path.exists()
    assert protocol_pack_grammar_path.exists()
    assert protocol_pack_index_path.exists()
    assert curated_protocol_pack_path.exists()
    assert research_promotion_path.exists()
    assert registry_path.exists()

    index_payload = json.loads(index_path.read_text(encoding="utf-8"))
    search_payload = json.loads(search_path.read_text(encoding="utf-8"))
    audit_payload = json.loads(audit_path.read_text(encoding="utf-8"))
    manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    site_variants_payload = json.loads(site_variants_path.read_text(encoding="utf-8"))
    protocol_pack_grammar_payload = json.loads(protocol_pack_grammar_path.read_text(encoding="utf-8"))
    protocol_pack_index_payload = json.loads(protocol_pack_index_path.read_text(encoding="utf-8"))
    research_promotion_payload = json.loads(research_promotion_path.read_text(encoding="utf-8"))

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
    assert index_payload["product_layers"]["protocol_library"]["protocol_pack_count"] == len(
        export_payload["protocol_library"]["protocol_packs"]
    )
    assert manifest_payload["composition_model"]["index_programs"]["count"] == len(
        export_payload["protocol_library"]["protocols"]
    )
    assert index_payload["product_layers"]["research_stream"]["contribution_model_count"] == len(
        export_payload["research_stream"]["contribution_models"]
    )
    assert index_payload["product_layers"]["research_stream"]["promotion_pathway_count"] == len(
        export_payload["research_stream"]["promotion_registry"]["promotion_pathways"]
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
    assert any(item["id"] == "proto_paradox_finder" for item in export_payload["protocol_library"]["protocols"])
    assert manifest_payload["repository"]["name"] == "a-person-index"
    assert manifest_payload["repository"]["title"] == "A Person Index (API)"
    assert manifest_payload["repository"]["github_url"] == "https://github.com/N0V3LT0K3NS/a_person_index"
    assert manifest_payload["repository"]["homepage_url"] == "https://a-person-index.netlify.app"
    assert manifest_payload["repository"]["current_phase"] == "phase_3_downstream_consumer_integration"
    assert len(manifest_payload["site_variants"]) == 3
    assert any(item["id"] == "atlas" and item["recommended"] for item in manifest_payload["site_variants"])
    assert manifest_payload["downstream_contract"]["result_atom_schema_id"] == "ras_result_atom_v0_1"
    assert manifest_payload["consumer_model"]["lead_example_consumer"] == "GNOMY"
    assert manifest_payload["consumer_model"]["consumer_agnostic"] is True
    assert manifest_payload["agent_companion_skill"]["name"] == "a-person-index"
    assert manifest_payload["agent_companion_skill"]["host"] == "codex"
    assert manifest_payload["compatibility_surfaces"]["uri_scheme"] == "registry://"
    assert manifest_payload["governance"]["contributing_doc"] == "CONTRIBUTING.md"
    assert manifest_payload["governance"]["security_doc"] == "SECURITY.md"
    assert manifest_payload["governance"]["codeowners"] == ".github/CODEOWNERS"
    assert manifest_payload["governance"]["codex_automation_doc"] == "docs/codex_automation.md"
    assert ".github/workflows/codex-task.yml" in manifest_payload["governance"]["automation_workflows"]
    assert manifest_payload["next_priorities"]
    assert manifest_payload["service_primitives"]
    assert any(item["id"] == "list_protocol_packs" for item in manifest_payload["service_primitives"])
    assert any(item["id"] == "fetch_curated_protocol_pack" for item in manifest_payload["service_primitives"])
    assert any(item["id"] == "fetch_protocol_pack" for item in manifest_payload["service_primitives"])
    assert any(item["id"] == "fetch_research_promotion_policy" for item in manifest_payload["service_primitives"])
    assert manifest_payload["interfaces"]["mcp"]["status"] == "active_read_only"
    assert "list_protocol_packs" in manifest_payload["interfaces"]["mcp"]["tool_ids"]
    assert "fetch_curated_protocol_pack" in manifest_payload["interfaces"]["mcp"]["tool_ids"]
    assert "fetch_protocol_pack" in manifest_payload["interfaces"]["mcp"]["tool_ids"]
    assert "fetch_research_promotion_policy" in manifest_payload["interfaces"]["mcp"]["tool_ids"]
    assert protocol_pack_index_payload["protocol_packs"]
    assert protocol_pack_index_payload["protocol_packs"][0]["id"].startswith("ppk_")
    assert len(site_variants_payload["variants"]) == 3
    assert {item["id"] for item in site_variants_payload["variants"]} == {"atlas", "signal", "field-guide"}
    assert research_promotion_payload["id"] == "research_promotion_v0_1"
    assert protocol_pack_grammar_payload["id"] == "protocol_pack_grammar_v0_1"
