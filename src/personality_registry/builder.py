from __future__ import annotations

import json
from html import escape
from pathlib import Path

from personality_registry.audit import audit_summary, bundle_audit_entry
from personality_registry.loader import InstrumentBundle, load_repository_strict
from personality_registry.query import compare_instruments
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


def _nav_html(prefix: str, current: str) -> str:
    links = [
        ("index.html", "registry", "Registry"),
        ("search.html", "search", "Search"),
        ("compare.html", "compare", "Compare"),
        ("audit.html", "audit", "Audit"),
    ]
    items = []
    for href, key, label in links:
        class_name = "active" if key == current else ""
        class_attr = f' class="{class_name}"' if class_name else ""
        items.append(f'<a href="{escape(prefix + href)}"{class_attr}>{escape(label)}</a>')
    return '<nav class="site-nav">' + "".join(items) + "</nav>"


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
      {_nav_html("../", "instrument")}
      <section class="hero-panel">
        <p class="eyebrow">Instrument Record</p>
        <h1>{escape(bundle.instrument.canonical_name)}</h1>
        <p class="page-lead">{escape(bundle.instrument.short_description)}</p>
        <div class="action-row">
          <a class="action-link" href="../index.html">Browse registry</a>
          <a class="action-link" href="../search.html">Search records</a>
          <a class="action-link" href="../compare.html">Compare systems</a>
        </div>
      </section>
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
      {_nav_html("", "audit")}
      <section class="hero-panel">
        <p class="eyebrow">Registry Audit</p>
        <h1>Coverage Snapshot</h1>
        <p class="page-lead">Structural and curation coverage for the shipped seed corpus.</p>
      </section>
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


def _build_entity_refs(repository, instrument_prefix: str) -> dict[str, dict[str, str]]:
    refs: dict[str, dict[str, str]] = {}
    for _, bundle in sorted(repository.instruments.items()):
        refs[bundle.instrument.id] = {
            "label": bundle.instrument.canonical_name,
            "href": f"{instrument_prefix}{bundle.slug}.html",
        }
        for version in bundle.versions:
            refs[version.id] = {
                "label": version.version_label,
                "href": f"{instrument_prefix}{bundle.slug}.html",
            }
        for construct in bundle.constructs:
            refs[construct.id] = {
                "label": construct.name,
                "href": f"{instrument_prefix}{bundle.slug}.html#{construct.id}",
            }
    return refs


def _entity_to_instrument_ids(repository) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for bundle in repository.instruments.values():
        instrument_id = bundle.instrument.id
        mapping[instrument_id] = instrument_id
        for collection in (
            bundle.versions,
            bundle.constructs,
            bundle.resources,
            bundle.claims,
            bundle.annotations,
            bundle.inferences,
            bundle.crosswalks,
            bundle.risks,
            bundle.use_cases,
        ):
            for item in collection:
                mapping[item.id] = instrument_id
    return mapping


def _comparison_slug(left_slug: str, right_slug: str) -> str:
    return f"{left_slug}--{right_slug}"


def _comparison_entries(repository) -> list[dict]:
    instrument_by_id = {bundle.instrument.id: bundle for bundle in repository.instruments.values()}
    entity_to_instrument = _entity_to_instrument_ids(repository)
    seen_pairs: set[tuple[str, str]] = set()

    for bundle in repository.instruments.values():
        for crosswalk in bundle.crosswalks:
            left_id = entity_to_instrument.get(crosswalk.source_entity_id)
            right_id = entity_to_instrument.get(crosswalk.target_entity_id)
            if left_id is None or right_id is None or left_id == right_id:
                continue
            ordered_pair = tuple(
                sorted((left_id, right_id), key=lambda instrument_id: instrument_by_id[instrument_id].slug)
            )
            seen_pairs.add(ordered_pair)

    entries: list[dict] = []
    for left_id, right_id in sorted(
        seen_pairs,
        key=lambda pair: (
            instrument_by_id[pair[0]].instrument.canonical_name.lower(),
            instrument_by_id[pair[1]].instrument.canonical_name.lower(),
        ),
    ):
        left_bundle = instrument_by_id[left_id]
        right_bundle = instrument_by_id[right_id]
        payload = compare_instruments(repository, left_id, right_id)
        entries.append(
            {
                "slug": _comparison_slug(left_bundle.slug, right_bundle.slug),
                "left": {
                    "slug": left_bundle.slug,
                    "id": left_bundle.instrument.id,
                    "canonical_name": left_bundle.instrument.canonical_name,
                    "family": left_bundle.instrument.family,
                },
                "right": {
                    "slug": right_bundle.slug,
                    "id": right_bundle.instrument.id,
                    "canonical_name": right_bundle.instrument.canonical_name,
                    "family": right_bundle.instrument.family,
                },
                "crosswalk_count": len(payload["crosswalks"]),
                "shared_dimension_count": len(payload["shared_annotation_values"]),
                "payload": payload,
            }
        )
    return entries


def _comparison_card(entry: dict) -> str:
    family_tags = entry["left"]["family"] + entry["right"]["family"]
    tag_html = "".join(f'<span class="tag">{escape(value)}</span>' for value in sorted(set(family_tags)))
    return f"""
<article class="instrument-card compare-card">
  <p class="eyebrow">Comparison</p>
  <h2><a href="comparisons/{escape(entry['slug'])}.html">{escape(entry['left']['canonical_name'])} vs {escape(entry['right']['canonical_name'])}</a></h2>
  <p class="muted">{escape(entry['left']['id'])} <> {escape(entry['right']['id'])}</p>
  <div class="tag-row">{tag_html}</div>
  <p class="coverage-line">{escape(_count_label(entry['crosswalk_count'], 'crosswalk'))} | {escape(_count_label(entry['shared_dimension_count'], 'shared ontology dimension'))}</p>
</article>
"""


def _linked_entity(entity_id: str, refs: dict[str, dict[str, str]]) -> str:
    ref = refs.get(entity_id)
    if ref is None:
        return escape(entity_id)
    return f'<a href="{escape(ref["href"])}">{escape(ref["label"])}</a>'


def _comparison_crosswalk_lines(payload: dict, entity_refs: dict[str, dict[str, str]]) -> list[str]:
    lines: list[str] = []
    for crosswalk in payload["crosswalks"]:
        source = _linked_entity(crosswalk["source_entity_id"], entity_refs)
        target = _linked_entity(crosswalk["target_entity_id"], entity_refs)
        line = (
            f"{source} -> {target} <span class=\"muted\">[{escape(crosswalk['relationship_type'])} / "
            f"{escape(crosswalk['relationship_strength'])} / {escape(crosswalk['confidence'])}]</span><br />"
            f"{escape(crosswalk['rationale'])}"
        )
        if crosswalk.get("notes"):
            line += f"<br />{escape(crosswalk['notes'])}"
        lines.append(line)
    return lines


def _comparison_overlap_lines(payload: dict) -> list[str]:
    if not payload["shared_annotation_values"]:
        return ["No shared ontology values recorded yet."]
    return [
        f"<strong>{escape(dimension)}</strong>: {escape(', '.join(values))}"
        for dimension, values in sorted(payload["shared_annotation_values"].items())
    ]


def _comparison_html(entry: dict, entity_refs: dict[str, dict[str, str]]) -> str:
    payload = entry["payload"]
    left = payload["left"]
    right = payload["right"]
    left_constructs = _render_list([escape(name) for name in left["constructs"]])
    right_constructs = _render_list([escape(name) for name in right["constructs"]])
    shared = _render_list(_comparison_overlap_lines(payload))
    crosswalks = _render_list(_comparison_crosswalk_lines(payload, entity_refs))
    left_tags = "".join(f'<span class="tag">{escape(value)}</span>' for value in left["family"])
    right_tags = "".join(f'<span class="tag">{escape(value)}</span>' for value in right["family"])

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{escape(left['canonical_name'])} vs {escape(right['canonical_name'])}</title>
    <link rel="stylesheet" href="../style.css" />
  </head>
  <body>
    <main>
      {_nav_html("../", "compare")}
      <section class="hero-panel">
        <p class="eyebrow">Comparison</p>
        <h1>{escape(left['canonical_name'])} vs {escape(right['canonical_name'])}</h1>
        <p class="page-lead">Shared ontology values and recorded crosswalks across the two instrument records.</p>
        <div class="action-row">
          <a class="action-link" href="../compare.html">All comparisons</a>
          <a class="action-link" href="../instruments/{escape(entry['left']['slug'])}.html">{escape(left['canonical_name'])}</a>
          <a class="action-link" href="../instruments/{escape(entry['right']['slug'])}.html">{escape(right['canonical_name'])}</a>
        </div>
      </section>
      <section class="comparison-columns">
        <article class="instrument-card">
          <p class="eyebrow">Left instrument</p>
          <h2>{escape(left['canonical_name'])}</h2>
          <div class="tag-row">{left_tags}</div>
          {left_constructs}
        </article>
        <article class="instrument-card">
          <p class="eyebrow">Right instrument</p>
          <h2>{escape(right['canonical_name'])}</h2>
          <div class="tag-row">{right_tags}</div>
          {right_constructs}
        </article>
      </section>
      <section>
        <h2>Shared Ontology Annotations</h2>
        {shared}
      </section>
      <section>
        <h2>Recorded Crosswalks</h2>
        {crosswalks}
      </section>
    </main>
  </body>
</html>
"""


def _search_html() -> str:
    nav = _nav_html("", "search")
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Registry Search</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main>
      __NAV__
      <section class="hero-panel">
        <p class="eyebrow">Registry Search</p>
        <h1>Find instruments by name, alias, ontology, or notes</h1>
        <p class="page-lead">Client-side search across the shipped static corpus. Results are backed by data published with the site.</p>
      </section>
      <section class="search-shell">
        <div class="search-controls">
          <label>
            Query
            <input id="search-query" type="search" placeholder="Big Five, attachment, identity narrative, hiring..." />
          </label>
          <label>
            Family
            <select id="family-filter">
              <option value="">All families</option>
            </select>
          </label>
        </div>
        <p id="search-meta" class="muted">Loading registry data…</p>
        <div id="search-results" class="card-grid search-results"></div>
      </section>
    </main>
    <script>
      (async function () {
        const queryInput = document.getElementById("search-query");
        const familyFilter = document.getElementById("family-filter");
        const meta = document.getElementById("search-meta");
        const resultsNode = document.getElementById("search-results");

        const response = await fetch("data/search.json");
        const payload = await response.json();
        const entries = payload.entries.map((entry) => ({
          ...entry,
          families: (entry.annotation_index.instrument_family || []).slice().sort(),
        }));

        const families = Array.from(new Set(entries.flatMap((entry) => entry.families))).sort();
        for (const family of families) {
          const option = document.createElement("option");
          option.value = family;
          option.textContent = family;
          familyFilter.appendChild(option);
        }

        function render() {
          const query = queryInput.value.trim().toLowerCase();
          const family = familyFilter.value;
          const matches = entries.filter((entry) => {
            const familyMatch = !family || entry.families.includes(family);
            const textMatch =
              !query ||
              entry.canonical_name.toLowerCase().includes(query) ||
              entry.instrument_id.toLowerCase().includes(query) ||
              entry.slug.toLowerCase().includes(query) ||
              entry.short_names.some((item) => item.toLowerCase().includes(query)) ||
              entry.aliases.some((item) => item.toLowerCase().includes(query)) ||
              entry.text.toLowerCase().includes(query);
            return familyMatch && textMatch;
          });

          meta.textContent = `${matches.length} result${matches.length === 1 ? "" : "s"} across ${entries.length} shipped records`;
          resultsNode.innerHTML = matches
            .map((entry) => {
              const tags = entry.families.map((family) => `<span class="tag">${family}</span>`).join("");
              return `
                <article class="instrument-card search-card">
                  <p class="eyebrow">Instrument</p>
                  <h2><a href="instruments/${entry.slug}.html">${entry.canonical_name}</a></h2>
                  <p class="muted">${entry.instrument_id}</p>
                  <div class="tag-row">${tags}</div>
                </article>
              `;
            })
            .join("");

          if (!matches.length) {
            resultsNode.innerHTML = '<p class="empty">No matching instruments.</p>';
          }
        }

        queryInput.addEventListener("input", render);
        familyFilter.addEventListener("change", render);
        render();
      })();
    </script>
  </body>
</html>
""".replace("__NAV__", nav)


def _compare_index_html(comparison_entries: list[dict]) -> str:
    nav = _nav_html("", "compare")
    cards = "\n".join(_comparison_card(entry) for entry in comparison_entries)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Registry Comparisons</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main>
      {nav}
      <section class="hero-panel">
        <p class="eyebrow">Comparison Index</p>
        <h1>Recorded instrument comparisons</h1>
        <p class="page-lead">Static comparison pages generated from crosswalks and shared ontology values across the registry.</p>
      </section>
      <section class="stats">
        <article class="stat-card"><strong>{len(comparison_entries)}</strong> comparison pages</article>
        <article class="stat-card"><strong>{sum(entry['crosswalk_count'] for entry in comparison_entries)}</strong> total crosswalk records</article>
      </section>
      <section>
        <div class="card-grid">{cards}</div>
      </section>
    </main>
  </body>
</html>
"""


def build_docs(root: Path) -> None:
    repository = load_repository_strict(root)
    site_root = root / "site"
    site_data_root = site_root / "data"
    site_instruments_root = site_root / "instruments"
    site_comparisons_root = site_root / "comparisons"
    site_data_root.mkdir(parents=True, exist_ok=True)
    site_instruments_root.mkdir(parents=True, exist_ok=True)
    site_comparisons_root.mkdir(parents=True, exist_ok=True)
    audit_entries = [bundle_audit_entry(bundle) for _, bundle in sorted(repository.instruments.items())]
    audit_snapshot = audit_summary(audit_entries)
    audit_by_slug = {entry["slug"]: entry for entry in audit_entries}
    instrument_entity_refs = _build_entity_refs(repository, "")
    comparison_entity_refs = _build_entity_refs(repository, "../instruments/")
    comparison_entries = _comparison_entries(repository)
    search_payload = {
        "entries": [_search_entry(bundle) for _, bundle in sorted(repository.instruments.items())],
    }
    comparison_payload = {
        "comparisons": [
            {
                "slug": entry["slug"],
                "left": entry["left"],
                "right": entry["right"],
                "crosswalk_count": entry["crosswalk_count"],
                "shared_dimension_count": entry["shared_dimension_count"],
            }
            for entry in comparison_entries
        ]
    }

    style = """body { font-family: Georgia, serif; margin: 0; background:
radial-gradient(circle at top, rgba(255, 244, 218, 0.8), transparent 38%),
linear-gradient(180deg, #f3ecdf 0%, #eadfcd 100%); color: #1f1a14; }
main { max-width: 1120px; margin: 0 auto; padding: 28px 24px 88px; }
a { color: #7d321d; text-decoration-thickness: 0.08em; text-underline-offset: 0.14em; }
h1, h2 { font-family: 'Palatino Linotype', 'Book Antiqua', serif; letter-spacing: -0.02em; }
section { margin-top: 32px; }
.site-nav { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
.site-nav a { padding: 10px 14px; border: 1px solid #d5b88f; border-radius: 999px; background: rgba(255, 249, 240, 0.78); text-decoration: none; color: #5c2c19; }
.site-nav a.active { background: #7d321d; color: #fff7ed; border-color: #7d321d; }
.hero-panel { background: linear-gradient(135deg, rgba(255, 250, 242, 0.94), rgba(246, 231, 204, 0.92)); border: 1px solid #d8bf97; border-radius: 22px; padding: 24px 26px; box-shadow: 0 18px 40px rgba(85, 57, 24, 0.08); }
.eyebrow { margin: 0 0 8px; text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.78rem; color: #8b5b2b; }
.page-lead { max-width: 62ch; font-size: 1.05rem; color: #4d3f30; }
.action-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 18px; }
.action-link { display: inline-flex; align-items: center; justify-content: center; padding: 10px 14px; border-radius: 999px; background: #f5e4c5; border: 1px solid #d8bf97; text-decoration: none; }
.muted { color: #6f6352; font-size: 0.95rem; }
.empty { color: #6f6352; font-style: italic; }
.notes-block { white-space: pre-wrap; background: #fffaf3; padding: 16px; border: 1px solid #d9c9ae; border-radius: 12px; }
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.tag { background: #ead8bb; border: 1px solid #d1b78d; border-radius: 999px; padding: 4px 10px; font-size: 0.9rem; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 20px; }
.stat-card, .instrument-card { background: rgba(255, 250, 243, 0.94); border: 1px solid #d9c9ae; border-radius: 16px; padding: 18px 20px; box-shadow: 0 12px 30px rgba(72, 49, 24, 0.06); }
.stat-card strong { display: block; font-size: 1.8rem; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.compare-card h2, .search-card h2 { font-size: 1.15rem; }
.coverage-line { margin-top: 12px; color: #6f6352; font-size: 0.95rem; }
.item-list { padding-left: 20px; line-height: 1.58; }
.audit-table { width: 100%; border-collapse: collapse; background: rgba(255, 250, 243, 0.94); border: 1px solid #d9c9ae; border-radius: 16px; overflow: hidden; }
.audit-table th, .audit-table td { text-align: left; padding: 12px 14px; border-bottom: 1px solid #e7d8c0; vertical-align: top; }
.audit-table th { background: #ead8bb; }
.comparison-columns { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
.search-shell { background: rgba(255, 250, 243, 0.9); border: 1px solid #d9c9ae; border-radius: 18px; padding: 20px; box-shadow: 0 12px 30px rgba(72, 49, 24, 0.05); }
.search-controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.search-controls label { display: grid; gap: 8px; font-weight: 600; color: #4f3a27; }
.search-controls input, .search-controls select { width: 100%; padding: 12px 14px; border-radius: 12px; border: 1px solid #cfb693; background: #fffdf9; font: inherit; }
.search-results { margin-top: 20px; }
@media (max-width: 720px) { main { padding: 22px 16px 72px; } .hero-panel { padding: 20px 18px; } }
"""
    (site_root / "style.css").write_text(style, encoding="utf-8")
    (site_data_root / "search.json").write_text(json.dumps(search_payload, indent=2), encoding="utf-8")
    (site_data_root / "audit.json").write_text(
        json.dumps({"summary": audit_snapshot, "instruments": audit_entries}, indent=2),
        encoding="utf-8",
    )
    (site_data_root / "comparisons.json").write_text(json.dumps(comparison_payload, indent=2), encoding="utf-8")

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
      {_nav_html("", "registry")}
      <section class="hero-panel">
        <p class="eyebrow">Registry</p>
        <h1>Personality Instrument Registry</h1>
        <p class="page-lead">Versioned corpus for personality and typology systems, with source claims, ontology labels, and house comparison kept separate.</p>
        <div class="action-row">
          <a class="action-link" href="search.html">Search the corpus</a>
          <a class="action-link" href="compare.html">Browse comparisons</a>
          <a class="action-link" href="audit.html">View audit</a>
        </div>
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
    (site_root / "search.html").write_text(_search_html(), encoding="utf-8")
    (site_root / "compare.html").write_text(_compare_index_html(comparison_entries), encoding="utf-8")

    for slug, bundle in repository.instruments.items():
        (site_instruments_root / f"{slug}.html").write_text(
            _bundle_html(bundle, instrument_entity_refs),
            encoding="utf-8",
        )
    for entry in comparison_entries:
        (site_comparisons_root / f"{entry['slug']}.html").write_text(
            _comparison_html(entry, comparison_entity_refs),
            encoding="utf-8",
        )
