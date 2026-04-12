from __future__ import annotations

from personality_registry.builder import build_docs, build_outputs


def test_build_docs_renders_audit_and_registry_sections(repo_root):
    build_outputs(repo_root)
    build_docs(repo_root)

    index_path = repo_root / "site" / "index.html"
    audit_path = repo_root / "site" / "audit.html"
    instrument_path = repo_root / "site" / "instruments" / "enneagram.html"

    assert index_path.exists()
    assert audit_path.exists()
    assert instrument_path.exists()

    index_html = index_path.read_text(encoding="utf-8")
    audit_html = audit_path.read_text(encoding="utf-8")
    instrument_html = instrument_path.read_text(encoding="utf-8")

    assert "View registry audit" in index_html
    assert "Registry Audit" in audit_html
    assert "Resources" in instrument_html
    assert "Crosswalks" in instrument_html
    assert "Risks" in instrument_html
    assert "Use Cases" in instrument_html
