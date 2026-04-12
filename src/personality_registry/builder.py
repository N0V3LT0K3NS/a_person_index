from __future__ import annotations

import json
from html import escape
from pathlib import Path

from personality_registry.loader import InstrumentBundle, load_repository_strict
from personality_registry.validation import validate_repository


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


def _audit_entry(bundle: InstrumentBundle) -> dict:
    officiality_counts: dict[str, int] = {}
    for resource in bundle.resources:
        officiality_counts[resource.officiality] = officiality_counts.get(resource.officiality, 0) + 1

    counts = {
        "versions": len(bundle.versions),
        "constructs": len(bundle.constructs),
        "claims": len(bundle.claims),
        "resources": len(bundle.resources),
        "annotations": len(bundle.annotations),
        "inferences": len(bundle.inferences),
        "crosswalks": len(bundle.crosswalks),
        "risks": len(bundle.risks),
        "use_cases": len(bundle.use_cases),
    }

    return {
        "slug": bundle.slug,
        "instrument_id": bundle.instrument.id,
        "canonical_name": bundle.instrument.canonical_name,
        "counts": counts,
        "resource_officiality": dict(sorted(officiality_counts.items())),
        "coverage": {
            "has_crosswalks": counts["crosswalks"] > 0,
            "has_multiple_resources": counts["resources"] > 1,
            "has_official_or_semi_official_resource": any(
                resource.officiality in {"official", "semi_official"} for resource in bundle.resources
            ),
        },
    }


def _docs_index_entry(bundle: InstrumentBundle) -> str:
    return (
        f"<li><a href=\"instruments/{escape(bundle.slug)}.html\">{escape(bundle.instrument.canonical_name)}</a> "
        f"({escape(bundle.instrument.id)})</li>"
    )


def _bundle_html(bundle: InstrumentBundle) -> str:
    def render_items(items: list[str]) -> str:
        if not items:
            return "<p>None recorded.</p>"
        return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"

    annotation_lines = [
        f"{annotation.ontology_dimension}: {', '.join(annotation.ontology_values)}"
        for annotation in bundle.annotations
        if annotation.target_entity_type == "instrument"
    ]
    claim_lines = [claim.claim_text for claim in bundle.claims]
    inference_lines = [inference.text for inference in bundle.inferences]
    construct_lines = [construct.name for construct in bundle.constructs]

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{escape(bundle.instrument.canonical_name)}</title>
    <link rel="stylesheet" href="../style.css" />
  </head>
  <body>
    <main>
      <p><a href="../index.html">Back to registry</a></p>
      <h1>{escape(bundle.instrument.canonical_name)}</h1>
      <p>{escape(bundle.instrument.short_description)}</p>
      <section>
        <h2>Constructs</h2>
        {render_items(construct_lines)}
      </section>
      <section>
        <h2>Source claims</h2>
        {render_items(claim_lines)}
      </section>
      <section>
        <h2>Ontology annotations</h2>
        {render_items(annotation_lines)}
      </section>
      <section>
        <h2>House inferences</h2>
        {render_items(inference_lines)}
      </section>
      <section>
        <h2>Notes</h2>
        <pre>{escape(bundle.notes)}</pre>
      </section>
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
    audit_entries = [_audit_entry(bundle) for _, bundle in sorted(repository.instruments.items())]
    audit_payload = {
        "summary": {
            "instrument_count": len(audit_entries),
            "instruments_with_crosswalks": sum(1 for entry in audit_entries if entry["coverage"]["has_crosswalks"]),
            "instruments_with_multiple_resources": sum(
                1 for entry in audit_entries if entry["coverage"]["has_multiple_resources"]
            ),
            "instruments_with_official_or_semi_official_resource": sum(
                1
                for entry in audit_entries
                if entry["coverage"]["has_official_or_semi_official_resource"]
            ),
        },
        "instruments": audit_entries,
    }
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

    style = """body { font-family: Georgia, serif; margin: 0; background: #f6f1e8; color: #1c1a16; }
main { max-width: 920px; margin: 0 auto; padding: 48px 24px 80px; }
a { color: #7a2f18; }
h1, h2 { font-family: 'Palatino Linotype', serif; }
pre { white-space: pre-wrap; background: #fffaf3; padding: 16px; border: 1px solid #d9c9ae; }
section { margin-top: 32px; }"""
    (site_root / "style.css").write_text(style, encoding="utf-8")

    index_items = "\n".join(_docs_index_entry(bundle) for _, bundle in sorted(repository.instruments.items()))
    index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Personality Instrument Registry</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main>
      <h1>Personality Instrument Registry</h1>
      <p>Versioned corpus for personality and typology instruments.</p>
      <ul>{index_items}</ul>
    </main>
  </body>
</html>
"""
    (site_root / "index.html").write_text(index_html, encoding="utf-8")

    for slug, bundle in repository.instruments.items():
        (site_instruments_root / f"{slug}.html").write_text(_bundle_html(bundle), encoding="utf-8")
