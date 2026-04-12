from __future__ import annotations

from personality_registry.builder import build_docs, build_outputs


def test_build_docs_renders_audit_and_registry_sections(repo_root):
    build_outputs(repo_root)
    build_docs(repo_root)

    index_path = repo_root / "site" / "index.html"
    audit_path = repo_root / "site" / "audit.html"
    instrument_path = repo_root / "site" / "instruments" / "enneagram.html"
    hexaco_path = repo_root / "site" / "instruments" / "hexaco.html"

    assert index_path.exists()
    assert audit_path.exists()
    assert instrument_path.exists()
    assert hexaco_path.exists()

    index_html = index_path.read_text(encoding="utf-8")
    audit_html = audit_path.read_text(encoding="utf-8")
    instrument_html = instrument_path.read_text(encoding="utf-8")
    hexaco_html = hexaco_path.read_text(encoding="utf-8")

    assert "View registry audit" in index_html
    assert "Registry Audit" in audit_html
    assert "With 2+ claims" in audit_html
    assert "<th>Claims</th>" in audit_html
    assert "Resources" in instrument_html
    assert "Crosswalks" in instrument_html
    assert "Risks" in instrument_html
    assert "Use Cases" in instrument_html
    assert 'href="big-five.html#con_big_five_openness"' in hexaco_html
