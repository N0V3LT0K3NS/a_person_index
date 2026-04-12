from __future__ import annotations

import json
from html import escape
from pathlib import Path

from personality_registry.audit import audit_summary, bundle_audit_entry
from personality_registry.loader import InstrumentBundle, load_repository_strict
from personality_registry.validation import validate_repository


def _count_label(count: int, singular: str, plural: str | None = None) -> str:
    plural = plural or f"{singular}s"
    word = singular if count == 1 else plural
    return f"{count} {word}"


def _bundle_to_dict(bundle: InstrumentBundle) -> dict:
    annotation_map: dict[str, list[str]] = {}
    for annotation in bundle.annotations:
        annotation_map.setdefault(annotation.ontology_dimension, []).extend(annotation.ontology_values)

    return {
        "slug": bundle.slug,
        "instrument": bundle.instrument.model_dump(mode="json"),
        "versions": [item.model_dump(mode="json") for item in bundle.versions],
        "constructs": [item.model_dump(mode="json") for item in bundle.constructs],
        "claims": [item.model_dump(mode="json") for item in bundle.claims],
        "resources": [item.model_dump(mode="json") for item in bundle.resources],
        "annotations": [item.model_dump(mode="json") for item in bundle.annotations],
        "annotation_index": {key: sorted(set(values)) for key, values in annotation_map.items()},
        "inferences": [item.model_dump(mode="json") for item in bundle.inferences],
        "crosswalks": [item.model_dump(mode="json") for item in bundle.crosswalks],
        "risks": [item.model_dump(mode="json") for item in bundle.risks],
        "use_cases": [item.model_dump(mode="json") for item in bundle.use_cases],
        "notes": bundle.notes,
    }


def _search_entry(bundle: InstrumentBundle) -> dict:
    annotation_index: dict[str, list[str]] = {}
    for annotation in bundle.annotations:
        annotation_index.setdefault(annotation.ontology_dimension, []).extend(annotation.ontology_values)

    text_parts = [
        bundle.instrument.canonical_name,
        *bundle.instrument.short_names,
        *bundle.instrument.aliases,
        bundle.instrument.short_description,
        bundle.notes,
        *(claim.claim_text for claim in bundle.claims),
        *(inference.text for inference in bundle.inferences),
        *(construct.official_definition or "" for construct in bundle.constructs),
    ]

    related_instruments = sorted(
        {
            crosswalk.target_entity_id
            for crosswalk in bundle.crosswalks
            if crosswalk.target_entity_type == "instrument"
        }
    )

    return {
        "slug": bundle.slug,
        "instrument_id": bundle.instrument.id,
        "canonical_name": bundle.instrument.canonical_name,
        "short_names": bundle.instrument.short_names,
        "aliases": bundle.instrument.aliases,
        "annotation_index": {key: sorted(set(values)) for key, values in annotation_index.items()},
        "related_instruments": related_instruments,
        "text": "\n".join(part for part in text_parts if part).strip(),
    }


def _render_tag_list(values: list[str]) -> str:
    if not values:
        return "<p class=\"empty\">None recorded.</p>"
    return (
        "<div class=\"tag-row\">"
        + "".join(f"<span class=\"tag\">{escape(value)}</span>" for value in values)
        + "</div>"
    )


def _render_list(items: list[str]) -> str:
    if not items:
        return "<p class=\"empty\">None recorded.</p>"
    return "<ul class=\"item-list\">" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def _docs_index_entry(bundle: InstrumentBundle, audit_entry: dict) -> str:
    family_tags = "".join(f"<span class=\"tag\">{escape(value)}</span>" for value in bundle.instrument.family)
    coverage_bits = [
        _count_label(audit_entry["counts"]["resources"], "resource"),
        _count_label(audit_entry["counts"]["constructs"], "construct"),
        _count_label(audit_entry["counts"]["crosswalks"], "crosswalk"),
    ]
    return f"""
<article class="instrument-card">
  <h2><a href="instruments/{escape(bundle.slug)}.html">{escape(bundle.instrument.canonical_name)}</a></h2>
  <p class="muted">{escape(bundle.instrument.id)}</p>
  <p>{escape(bundle.instrument.short_description)}</p>
  <div class="tag-row">{family_tags}</div>
  <p class="coverage-line">{escape(" | ".join(coverage_bits))}</p>
</article>
"""


def _metadata_lines(bundle: InstrumentBundle) -> list[str]:
    lines = [
        f"<strong>ID:</strong> {escape(bundle.instrument.id)}",
        f"<strong>Status:</strong> {escape(bundle.instrument.status)}",
    ]
    if bundle.instrument.aliases:
        lines.append(f"<strong>Aliases:</strong> {escape(', '.join(bundle.instrument.aliases))}")
    if bundle.instrument.creators:
        lines.append(f"<strong>Creators:</strong> {escape(', '.join(bundle.instrument.creators))}")
    if bundle.instrument.publisher_or_owner:
        lines.append(f"<strong>Publisher / Owner:</strong> {escape(bundle.instrument.publisher_or_owner)}")
    if bundle.instrument.official_websites:
        links = ", ".join(
            f'<a href="{escape(url)}">{escape(url)}</a>' for url in bundle.instrument.official_websites if url
        )
        if links:
            lines.append(f"<strong>Official websites:</strong> {links}")
    return lines


def _resource_lines(bundle: InstrumentBundle) -> list[str]:
    lines: list[str] = []
    for resource in bundle.resources:
        title = escape(resource.title)
        if resource.url:
            title = f'<a href="{escape(resource.url)}">{title}</a>'
        meta_parts = [resource.resource_type, resource.officiality]
        if resource.publisher:
            meta_parts.append(resource.publisher)
        if resource.publication_date:
            meta_parts.append(str(resource.publication_date))
        description = f"{title} <span class=\"muted\">({' | '.join(escape(part) for part in meta_parts)})</span>"
        if resource.notes:
            description += f"<br />{escape(resource.notes)}"
        lines.append(description)
    return lines


def _annotation_lines(bundle: InstrumentBundle) -> list[str]:
    return [
        (
            f"<strong>{escape(annotation.ontology_dimension)}</strong>: "
            f"{escape(', '.join(annotation.ontology_values))} "
            f"<span class=\"muted\">[{escape(annotation.annotation_status)} / {escape(annotation.confidence)}]</span><br />"
            f"{escape(annotation.rationale)}"
        )
        for annotation in bundle.annotations
        if annotation.target_entity_type == "instrument"
    ]


def _claim_lines(bundle: InstrumentBundle) -> list[str]:
    return [escape(claim.claim_text) for claim in bundle.claims]


def _inference_lines(bundle: InstrumentBundle) -> list[str]:
    return [
        (
            f"{escape(inference.text)} "
            f"<span class=\"muted\">[{escape(inference.inference_type)} / {escape(inference.confidence)}]</span>"
        )
        for inference in bundle.inferences
    ]


def _render_construct_list(bundle: InstrumentBundle) -> str:
    if not bundle.constructs:
        return "<p class=\"empty\">None recorded.</p>"
    items: list[str] = []
    for construct in bundle.constructs:
        line = f"<li id=\"{escape(construct.id)}\"><strong>{escape(construct.name)}</strong>"
        if construct.official_definition:
            line += f"<br />{escape(construct.official_definition)}"
        line += "</li>"
        items.append(line)
    return "<ul class=\"item-list\">" + "".join(items) + "</ul>"


def _crosswalk_lines(bundle: InstrumentBundle, entity_refs: dict[str, dict[str, str]]) -> list[str]:
    lines: list[str] = []
    for crosswalk in bundle.crosswalks:
        target_ref = entity_refs.get(crosswalk.target_entity_id)
        if target_ref is None:
            target_label = escape(crosswalk.target_entity_id)
        else:
            target_label = f'<a href="{escape(target_ref["href"])}">{escape(target_ref["label"])}</a>'
        lines.append(
            (
                f"{target_label} <span class=\"muted\">[{escape(crosswalk.relationship_type)} / "
                f"{escape(crosswalk.relationship_strength)} / {escape(crosswalk.confidence)}]</span><br />"
                f"{escape(crosswalk.rationale)}"
            )
        )
    return lines


def _risk_lines(bundle: InstrumentBundle) -> list[str]:
    lines: list[str] = []
    for risk in bundle.risks:
        line = (
            f"<strong>{escape(risk.risk_type)}</strong> <span class=\"muted\">[{escape(risk.severity)}]</span><br />"
            f"{escape(risk.description)}"
        )
        if risk.mitigation:
            line += f"<br /><em>Mitigation:</em> {escape(risk.mitigation)}"
        lines.append(line)
    return lines


def _use_case_lines(bundle: InstrumentBundle) -> list[str]:
    lines: list[str] = []
    for use_case in bundle.use_cases:
        line = (
            f"<strong>{escape(use_case.use_context)}</strong> -> {escape(use_case.utility_type)} "
            f"<span class=\"muted\">[{escape(use_case.suitability_level)}]</span>"
        )
        if use_case.cautions:
            line += f"<br />{escape(use_case.cautions)}"
        lines.append(line)
    return lines


def _bundle_html(bundle: InstrumentBundle, entity_refs: dict[str, dict[str, str]]) -> str:
    metadata = _render_list(_metadata_lines(bundle))
    constructs = _render_construct_list(bundle)
    claims = _render_list(_claim_lines(bundle))
    resources = _render_list(_resource_lines(bundle))
    annotations = _render_list(_annotation_lines(bundle))
    inferences = _render_list(_inference_lines(bundle))
    crosswalks = _render_list(_crosswalk_lines(bundle, entity_refs))
    risks = _render_list(_risk_lines(bundle))
    use_cases = _render_list(_use_case_lines(bundle))

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{escape(bundle.instrument.canonical_name)}</title>
    <link rel="stylesheet" href="../style.css" />
  </head>
  <body>
    <main>
      <p><a href="../index.html">Back to registry</a> | <a href="../audit.html">Audit</a></p>
      <h1>{escape(bundle.instrument.canonical_name)}</h1>
      <p>{escape(bundle.instrument.short_description)}</p>
      <section>
        <h2>Metadata</h2>
        {metadata}
      </section>
      <section>
        <h2>Families</h2>
        {_render_tag_list(bundle.instrument.family)}
      </section>
      <section>
        <h2>Constructs</h2>
        {constructs}
      </section>
      <section>
        <h2>Source claims</h2>
        {claims}
      </section>
      <section>
        <h2>Resources</h2>
        {resources}
      </section>
      <section>
        <h2>Ontology annotations</h2>
        {annotations}
      </section>
      <section>
        <h2>House inferences</h2>
        {inferences}
      </section>
      <section>
        <h2>Crosswalks</h2>
        {crosswalks}
      </section>
      <section>
        <h2>Risks</h2>
        {risks}
      </section>
      <section>
        <h2>Use Cases</h2>
        {use_cases}
      </section>
      <section>
        <h2>Notes</h2>
        <pre class="notes-block">{escape(bundle.notes)}</pre>
      </section>
    </main>
  </body>
</html>
"""


def _audit_html(audit_entries: list[dict], summary: dict) -> str:
    rows = []
    for entry in audit_entries:
        rows.append(
            "<tr>"
            f"<td><a href=\"instruments/{escape(entry['slug'])}.html\">{escape(entry['canonical_name'])}</a></td>"
            f"<td>{entry['counts']['resources']}</td>"
            f"<td>{entry['counts']['constructs']}</td>"
            f"<td>{entry['counts']['claims']}</td>"
            f"<td>{entry['counts']['inferences']}</td>"
            f"<td>{entry['counts']['crosswalks']}</td>"
            f"<td>{entry['counts']['risks']}</td>"
            f"<td>{entry['counts']['use_cases']}</td>"
            f"<td>{'yes' if entry['coverage']['has_official_or_semi_official_resource'] else 'no'}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Registry Audit</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main>
      <p><a href="index.html">Back to registry</a></p>
      <h1>Registry Audit</h1>
      <p>Coverage snapshot for the seeded corpus.</p>
      <section class="stats">
        <article class="stat-card"><strong>{summary['instrument_count']}</strong><span>Instruments</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_multiple_resources']}</strong><span>With 2+ resources</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_multiple_constructs']}</strong><span>With 2+ constructs</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_multiple_claims']}</strong><span>With 2+ claims</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_multiple_inferences']}</strong><span>With 2+ inferences</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_multiple_risks']}</strong><span>With 2+ risks</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_multiple_use_cases']}</strong><span>With 2+ use cases</span></article>
        <article class="stat-card"><strong>{summary['instruments_with_official_or_semi_official_resource']}</strong><span>With official/semi source</span></article>
      </section>
      <table class="audit-table">
        <thead>
          <tr>
            <th>Instrument</th>
            <th>Resources</th>
            <th>Constructs</th>
            <th>Claims</th>
            <th>Inferences</th>
            <th>Crosswalks</th>
            <th>Risks</th>
            <th>Use Cases</th>
            <th>Official / Semi</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </main>
  </body>
</html>
"""


def build_outputs(root: Path) -> dict:
    validate_repository(root)
    repository = load_repository_strict(root)
    generated_root = root / "generated"
    instrument_output_root = generated_root / "instruments"
    instrument_output_root.mkdir(parents=True, exist_ok=True)

    bundle_payloads = {slug: _bundle_to_dict(bundle) for slug, bundle in repository.instruments.items()}
    index_payload = {
        "ontology": {
            "registry": repository.ontology_registry.model_dump(mode="json"),
            "dimensions": repository.ontology_dimensions.model_dump(mode="json"),
            "enums": repository.ontology_enums,
        },
        "instruments": [
            {
                "slug": slug,
                "id": payload["instrument"]["id"],
                "canonical_name": payload["instrument"]["canonical_name"],
                "short_names": payload["instrument"]["short_names"],
                "aliases": payload["instrument"]["aliases"],
                "family": payload["instrument"]["family"],
                "annotation_index": payload["annotation_index"],
            }
            for slug, payload in sorted(bundle_payloads.items())
        ],
    }
    search_payload = {
        "entries": [_search_entry(bundle) for _, bundle in sorted(repository.instruments.items())],
    }
    audit_entries = [bundle_audit_entry(bundle) for _, bundle in sorted(repository.instruments.items())]
    audit_payload = {"summary": audit_summary(audit_entries), "instruments": audit_entries}
    export_payload = {
        "ontology": index_payload["ontology"],
        "instruments": bundle_payloads,
    }

    (generated_root / "index.json").write_text(json.dumps(index_payload, indent=2), encoding="utf-8")
    (generated_root / "search.json").write_text(json.dumps(search_payload, indent=2), encoding="utf-8")
    (generated_root / "audit.json").write_text(json.dumps(audit_payload, indent=2), encoding="utf-8")
    (generated_root / "registry.json").write_text(json.dumps(export_payload, indent=2), encoding="utf-8")

    for slug, payload in bundle_payloads.items():
        (instrument_output_root / f"{slug}.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    return export_payload


def build_docs(root: Path) -> None:
    repository = load_repository_strict(root)
    site_root = root / "site"
    site_instruments_root = site_root / "instruments"
    site_instruments_root.mkdir(parents=True, exist_ok=True)
    audit_entries = [bundle_audit_entry(bundle) for _, bundle in sorted(repository.instruments.items())]
    audit_snapshot = audit_summary(audit_entries)
    audit_by_slug = {entry["slug"]: entry for entry in audit_entries}
    entity_refs: dict[str, dict[str, str]] = {}
    for _, bundle in sorted(repository.instruments.items()):
        entity_refs[bundle.instrument.id] = {
            "label": bundle.instrument.canonical_name,
            "href": f"{bundle.slug}.html",
        }
        for version in bundle.versions:
            entity_refs[version.id] = {
                "label": version.version_label,
                "href": f"{bundle.slug}.html",
            }
        for construct in bundle.constructs:
            entity_refs[construct.id] = {
                "label": construct.name,
                "href": f"{bundle.slug}.html#{construct.id}",
            }

    style = """body { font-family: Georgia, serif; margin: 0; background: linear-gradient(180deg, #f7f1e8 0%, #efe5d6 100%); color: #1c1a16; }
main { max-width: 1040px; margin: 0 auto; padding: 48px 24px 80px; }
a { color: #7a2f18; }
h1, h2 { font-family: 'Palatino Linotype', serif; }
section { margin-top: 32px; }
.muted { color: #6f6352; font-size: 0.95rem; }
.empty { color: #6f6352; font-style: italic; }
.notes-block { white-space: pre-wrap; background: #fffaf3; padding: 16px; border: 1px solid #d9c9ae; border-radius: 10px; }
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.tag { background: #ead8bb; border: 1px solid #d1b78d; border-radius: 999px; padding: 4px 10px; font-size: 0.9rem; }
.hero { display: grid; gap: 16px; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 20px; }
.stat-card, .instrument-card { background: rgba(255, 250, 243, 0.92); border: 1px solid #d9c9ae; border-radius: 14px; padding: 16px 18px; box-shadow: 0 12px 30px rgba(72, 49, 24, 0.06); }
.stat-card strong { display: block; font-size: 1.8rem; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.coverage-line { margin-top: 12px; color: #6f6352; font-size: 0.95rem; }
.item-list { padding-left: 20px; line-height: 1.55; }
.audit-table { width: 100%; border-collapse: collapse; background: rgba(255, 250, 243, 0.92); border: 1px solid #d9c9ae; border-radius: 14px; overflow: hidden; }
.audit-table th, .audit-table td { text-align: left; padding: 12px 14px; border-bottom: 1px solid #e7d8c0; }
.audit-table th { background: #ead8bb; }
"""
    (site_root / "style.css").write_text(style, encoding="utf-8")

    index_items = "\n".join(
        _docs_index_entry(bundle, audit_by_slug[bundle.slug])
        for _, bundle in sorted(repository.instruments.items())
    )
    index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Personality Instrument Registry</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main>
      <section class="hero">
        <h1>Personality Instrument Registry</h1>
        <p>Versioned corpus for personality and typology instruments, with source claims, ontology labels, and house comparison kept separate.</p>
        <p><a href="audit.html">View registry audit</a></p>
      </section>
      <section class="stats">
        <article class="stat-card"><strong>{audit_snapshot['instrument_count']}</strong> seeded instruments</article>
        <article class="stat-card"><strong>{audit_snapshot['instruments_with_multiple_resources']}</strong> with 2+ resources</article>
        <article class="stat-card"><strong>{audit_snapshot['instruments_with_multiple_constructs']}</strong> with 2+ constructs</article>
        <article class="stat-card"><strong>{audit_snapshot['instruments_with_crosswalks']}</strong> with outgoing crosswalks</article>
      </section>
      <section>
        <h2>Instrument Index</h2>
        <div class="card-grid">{index_items}</div>
      </section>
    </main>
  </body>
</html>
"""
    (site_root / "index.html").write_text(index_html, encoding="utf-8")
    (site_root / "audit.html").write_text(_audit_html(audit_entries, audit_snapshot), encoding="utf-8")

    for slug, bundle in repository.instruments.items():
        (site_instruments_root / f"{slug}.html").write_text(
            _bundle_html(bundle, entity_refs),
            encoding="utf-8",
        )
