from __future__ import annotations

from personality_registry.builder import build_docs, build_outputs


def test_build_docs_renders_audit_and_registry_sections(repo_root):
    build_outputs(repo_root)
    build_docs(repo_root)

    index_path = repo_root / "site" / "index.html"
    audit_path = repo_root / "site" / "audit.html"
    search_path = repo_root / "site" / "search.html"
    compare_index_path = repo_root / "site" / "compare.html"
    motifs_path = repo_root / "site" / "motifs.html"
    interactions_path = repo_root / "site" / "interactions.html"
    protocols_path = repo_root / "site" / "protocols.html"
    protocol_packs_path = repo_root / "site" / "protocol-packs.html"
    research_path = repo_root / "site" / "research.html"
    favicon_path = repo_root / "site" / "favicon.svg"
    landing_css_path = repo_root / "site" / "landing.css"
    landing_options_path = repo_root / "site" / "landing-options.html"
    landing_atlas_path = repo_root / "site" / "landing-atlas.html"
    landing_signal_path = repo_root / "site" / "landing-signal.html"
    landing_field_guide_path = repo_root / "site" / "landing-field-guide.html"
    search_data_path = repo_root / "site" / "data" / "search.json"
    comparisons_data_path = repo_root / "site" / "data" / "comparisons.json"
    extensions_data_path = repo_root / "site" / "data" / "extensions.json"
    manifest_data_path = repo_root / "site" / "data" / "manifest.json"
    site_variants_data_path = repo_root / "site" / "data" / "site_variants.json"
    protocol_pack_grammar_data_path = repo_root / "site" / "data" / "protocol_pack_grammar.json"
    protocol_pack_index_data_path = repo_root / "site" / "data" / "protocol_packs" / "index.json"
    research_promotion_data_path = repo_root / "site" / "data" / "research_promotion.json"
    instrument_path = repo_root / "site" / "instruments" / "enneagram.html"
    hexaco_path = repo_root / "site" / "instruments" / "hexaco.html"
    compare_path = repo_root / "site" / "comparisons" / "big-five--mbti.html"

    assert index_path.exists()
    assert audit_path.exists()
    assert search_path.exists()
    assert compare_index_path.exists()
    assert motifs_path.exists()
    assert interactions_path.exists()
    assert protocols_path.exists()
    assert protocol_packs_path.exists()
    assert research_path.exists()
    assert favicon_path.exists()
    assert landing_css_path.exists()
    assert landing_options_path.exists()
    assert landing_atlas_path.exists()
    assert landing_signal_path.exists()
    assert landing_field_guide_path.exists()
    assert search_data_path.exists()
    assert comparisons_data_path.exists()
    assert extensions_data_path.exists()
    assert manifest_data_path.exists()
    assert site_variants_data_path.exists()
    assert protocol_pack_grammar_data_path.exists()
    assert protocol_pack_index_data_path.exists()
    assert research_promotion_data_path.exists()
    assert instrument_path.exists()
    assert hexaco_path.exists()
    assert compare_path.exists()

    index_html = index_path.read_text(encoding="utf-8")
    audit_html = audit_path.read_text(encoding="utf-8")
    search_html = search_path.read_text(encoding="utf-8")
    compare_index_html = compare_index_path.read_text(encoding="utf-8")
    motifs_html = motifs_path.read_text(encoding="utf-8")
    interactions_html = interactions_path.read_text(encoding="utf-8")
    protocols_html = protocols_path.read_text(encoding="utf-8")
    protocol_packs_html = protocol_packs_path.read_text(encoding="utf-8")
    research_html = research_path.read_text(encoding="utf-8")
    landing_options_html = landing_options_path.read_text(encoding="utf-8")
    landing_atlas_html = landing_atlas_path.read_text(encoding="utf-8")
    landing_signal_html = landing_signal_path.read_text(encoding="utf-8")
    landing_field_guide_html = landing_field_guide_path.read_text(encoding="utf-8")
    instrument_html = instrument_path.read_text(encoding="utf-8")
    hexaco_html = hexaco_path.read_text(encoding="utf-8")
    compare_html = compare_path.read_text(encoding="utf-8")

    assert "Finally, a map where personhood frameworks can talk." in index_html
    assert "landing.css" in index_html
    assert "Atlas / flagship direction" in index_html
    assert 'meta name="viewport" content="width=device-width, initial-scale=1"' in index_html
    assert 'link rel="icon" href="favicon.svg" type="image/svg+xml"' in index_html
    assert "Three ways to present the same substrate." in landing_options_html
    assert "Atlas of Personhood Systems" in landing_options_html
    assert "From frameworks to circuitry." in landing_signal_html
    assert "A field guide to systems that describe a person." in landing_field_guide_html
    assert "curator and research audiences" in landing_options_html
    assert "The job is not to flatten these systems into one bucket." in landing_atlas_html
    assert "Index Audit" in audit_html
    assert "With 2+ claims" in audit_html
    assert "<th>Claims</th>" in audit_html
    assert "Index Search" in search_html
    assert 'fetch("data/search.json")' in search_html
    assert "Comparison Index" in compare_index_html
    assert "House Motifs" in motifs_html
    assert "Interaction Hypotheses" in interactions_html
    assert "Index Programs" in protocols_html
    assert "Curated Program Packs" in protocol_packs_html
    assert "Stable, reviewed runtime bundles" in protocol_packs_html
    assert "Research Contribution Models" in research_html
    assert "Promotion Pathways" in research_html
    assert "promotion policy" in research_html.lower()
    assert "Result Atom Schema" in research_html
    assert "Resources" in instrument_html
    assert "Crosswalks" in instrument_html
    assert "Risks" in instrument_html
    assert "Use Cases" in instrument_html
    assert 'link rel="icon" href="../favicon.svg" type="image/svg+xml"' in instrument_html
    assert 'href="big-five.html#con_big_five_openness"' in hexaco_html
    assert "Shared Ontology Annotations" in compare_html
    assert "Recorded Crosswalks" in compare_html
