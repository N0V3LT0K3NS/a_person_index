from __future__ import annotations

from personality_registry.builder import build_docs, build_outputs


def test_build_docs_renders_audit_and_registry_sections(repo_root):
    build_outputs(repo_root)
    build_docs(repo_root)

    index_path = repo_root / "site" / "index.html"
    audit_path = repo_root / "site" / "audit.html"
    search_path = repo_root / "site" / "search.html"
    compare_index_path = repo_root / "site" / "compare.html"
    search_data_path = repo_root / "site" / "data" / "search.json"
    comparisons_data_path = repo_root / "site" / "data" / "comparisons.json"
    instrument_path = repo_root / "site" / "instruments" / "enneagram.html"
    hexaco_path = repo_root / "site" / "instruments" / "hexaco.html"
    compare_path = repo_root / "site" / "comparisons" / "big-five--mbti.html"

    assert index_path.exists()
    assert audit_path.exists()
    assert search_path.exists()
    assert compare_index_path.exists()
    assert search_data_path.exists()
    assert comparisons_data_path.exists()
    assert instrument_path.exists()
    assert hexaco_path.exists()
    assert compare_path.exists()

    index_html = index_path.read_text(encoding="utf-8")
    audit_html = audit_path.read_text(encoding="utf-8")
    search_html = search_path.read_text(encoding="utf-8")
    compare_index_html = compare_index_path.read_text(encoding="utf-8")
    instrument_html = instrument_path.read_text(encoding="utf-8")
    hexaco_html = hexaco_path.read_text(encoding="utf-8")
    compare_html = compare_path.read_text(encoding="utf-8")

    assert "Search the corpus" in index_html
    assert "Browse comparisons" in index_html
    assert "Registry Audit" in audit_html
    assert "With 2+ claims" in audit_html
    assert "<th>Claims</th>" in audit_html
    assert "Registry Search" in search_html
    assert 'fetch("data/search.json")' in search_html
    assert "Comparison Index" in compare_index_html
    assert "Resources" in instrument_html
    assert "Crosswalks" in instrument_html
    assert "Risks" in instrument_html
    assert "Use Cases" in instrument_html
    assert 'href="big-five.html#con_big_five_openness"' in hexaco_html
    assert "Shared Ontology Annotations" in compare_html
    assert "Recorded Crosswalks" in compare_html
