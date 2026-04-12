from __future__ import annotations

import argparse

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.query import (
    audit_repository,
    compare_instruments,
    contribution_model_record,
    dumps_json,
    find_contribution_models,
    find_interaction_hypotheses,
    find_motifs,
    find_protocols,
    find_techniques,
    interaction_hypothesis_record,
    load_extensions_for_query,
    load_repository_for_query,
    motif_record,
    protocol_record,
    query_results,
    resolve_instrument,
    result_atom_schema_record,
    show_instrument,
    technique_record,
    trace_entity_to_motifs,
)


def _render_find_text(results):
    if not results:
        return "No matching instruments."
    lines = []
    for result in results:
        lines.append(f"{result.canonical_name} ({result.instrument_id})")
        lines.append(f"  slug: {result.slug}")
        if result.annotation_index:
            summary = ", ".join(
                f"{dimension}={','.join(values)}"
                for dimension, values in sorted(result.annotation_index.items())
            )
            lines.append(f"  annotations: {summary}")
    return "\n".join(lines)


def _render_compare_text(payload):
    lines = [
        f"{payload['left']['canonical_name']} ({payload['left']['id']})",
        f"{payload['right']['canonical_name']} ({payload['right']['id']})",
        "",
        "Shared annotation values:",
    ]
    if payload["shared_annotation_values"]:
        for dimension, values in sorted(payload["shared_annotation_values"].items()):
            lines.append(f"  {dimension}: {', '.join(values)}")
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Crosswalks:")
    if payload["crosswalks"]:
        for crosswalk in payload["crosswalks"]:
            lines.append(
                f"  {crosswalk['relationship_type']} ({crosswalk['relationship_strength']}): {crosswalk['rationale']}"
            )
    else:
        lines.append("  none")
    return "\n".join(lines)


def _render_audit_text(payload):
    lines = [
        "Coverage summary:",
        f"  instruments: {payload['summary']['instrument_count']}",
        f"  with crosswalks: {payload['summary']['instruments_with_crosswalks']}",
        f"  with 2+ resources: {payload['summary']['instruments_with_multiple_resources']}",
        f"  with 2+ constructs: {payload['summary']['instruments_with_multiple_constructs']}",
        f"  with 2+ claims: {payload['summary']['instruments_with_multiple_claims']}",
        f"  with 2+ inferences: {payload['summary']['instruments_with_multiple_inferences']}",
        f"  with 2+ risks: {payload['summary']['instruments_with_multiple_risks']}",
        f"  with 2+ use cases: {payload['summary']['instruments_with_multiple_use_cases']}",
        (
            "  with official/semi-official resource: "
            f"{payload['summary']['instruments_with_official_or_semi_official_resource']}"
        ),
    ]
    if payload["instruments"]:
        lines.append("")
        lines.append("Filtered instruments:")
        for entry in payload["instruments"]:
            lines.append(f"  {entry['canonical_name']} ({entry['instrument_id']})")
            lines.append(
                "    "
                f"resources={entry['counts']['resources']} constructs={entry['counts']['constructs']} "
                f"claims={entry['counts']['claims']} inferences={entry['counts']['inferences']} "
                f"crosswalks={entry['counts']['crosswalks']} risks={entry['counts']['risks']} "
                f"use_cases={entry['counts']['use_cases']} "
                f"officiality={entry['resource_officiality']}"
            )
    return "\n".join(lines)


def _render_show_text(bundle, section, payload):
    if section is None:
        lines = [
            f"{bundle.instrument.canonical_name} ({bundle.instrument.id})",
            f"slug: {bundle.slug}",
            bundle.instrument.short_description,
            "",
            "Section counts:",
            f"  versions: {len(bundle.versions)}",
            f"  constructs: {len(bundle.constructs)}",
            f"  claims: {len(bundle.claims)}",
            f"  resources: {len(bundle.resources)}",
            f"  annotations: {len(bundle.annotations)}",
            f"  inferences: {len(bundle.inferences)}",
            f"  crosswalks: {len(bundle.crosswalks)}",
            f"  risks: {len(bundle.risks)}",
            f"  use_cases: {len(bundle.use_cases)}",
        ]
        return "\n".join(lines)

    if section == "notes":
        return str(payload)

    if section == "instrument":
        instrument = payload
        lines = [
            f"{instrument['canonical_name']} ({instrument['id']})",
            f"status: {instrument['status']}",
            f"family: {', '.join(instrument['family'])}",
        ]
        if instrument.get("aliases"):
            lines.append(f"aliases: {', '.join(instrument['aliases'])}")
        if instrument.get("creators"):
            lines.append(f"creators: {', '.join(instrument['creators'])}")
        return "\n".join(lines)

    if section == "annotation_index":
        lines = ["Annotation index:"]
        for dimension, values in sorted(payload.items()):
            lines.append(f"  {dimension}: {', '.join(values)}")
        return "\n".join(lines)

    if not isinstance(payload, list):
        return dumps_json(payload)

    if not payload:
        return "No records."

    lines = [f"{section}:"]
    for item in payload:
        label = item.get("id", "(no id)")
        summary = item.get("name") or item.get("title") or item.get("claim_text") or item.get("text") or item.get("description") or item.get("use_context") or item.get("ontology_dimension") or ""
        lines.append(f"  {label}: {summary}")
    return "\n".join(lines)


def _render_motifs_text(results):
    if not results:
        return "No matching motifs."
    lines = []
    for result in results:
        lines.append(f"{result['name']} ({result['id']})")
        lines.append(
            f"  kind={result['motif_kind']} status={result['status']} mappings={result['mapping_count']}"
        )
        if result.get("tags"):
            lines.append(f"  tags: {', '.join(result['tags'])}")
        lines.append(f"  {result['summary']}")
    return "\n".join(lines)


def _render_motif_record_text(payload):
    motif = payload["motif"]
    lines = [
        f"{motif['name']} ({motif['id']})",
        f"kind: {motif['motif_kind']}",
        f"status: {motif['status']}",
        f"mappings: {payload['mapping_count']}",
        motif["summary"],
        "",
        "Linked mappings:",
    ]
    if payload["linked_mappings"]:
        for item in payload["linked_mappings"]:
            lines.append(
                f"  {item['source_label']} -> {item['target_label']} [{item['relationship_type']} / {item['relationship_strength']}]"
            )
    else:
        lines.append("  none")
    return "\n".join(lines)


def _render_trace_text(payload):
    entity = payload["entity"]
    lines = [
        f"{entity['label']} ({entity['entity_id']})",
        f"type: {entity['entity_type']}",
        f"instrument: {entity['instrument_label']}",
        "",
        "Motif summary:",
    ]
    if payload["motif_summary"]:
        for item in payload["motif_summary"]:
            motif = item["motif"]
            lines.append(
                f"  {motif['name']} ({motif['id']}): mappings={item['mapping_count']} via {', '.join(item['source_labels'])}"
            )
    else:
        lines.append("  none")
    if payload["construct_mappings"]:
        lines.append("")
        lines.append("Construct mappings:")
        for entry in payload["construct_mappings"]:
            lines.append(f"  {entry['construct']['label']} ({entry['construct']['entity_id']})")
            for mapping in entry["mappings"]:
                lines.append(
                    f"    -> {mapping['target_label']} [{mapping['relationship_type']} / {mapping['relationship_strength']}]"
                )
    return "\n".join(lines)


def _render_protocols_text(results):
    if not results:
        return "No matching protocols."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(
            f"  status={item['status']} consumers={', '.join(item['downstream_consumers']) or 'none'}"
        )
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_protocol_record_text(payload):
    protocol = payload["protocol"]
    lines = [
        f"{protocol['name']} ({protocol['id']})",
        f"status: {protocol['status']}",
        f"consumers: {', '.join(protocol['downstream_consumers']) or 'none'}",
        protocol["summary"],
        "",
        "Required inputs:",
    ]
    for item in protocol["required_inputs"]:
        lines.append(f"  - {item}")
    lines.append("")
    lines.append("Techniques:")
    for technique in payload["techniques"]:
        lines.append(f"  {technique['name']} ({technique['id']})")
    return "\n".join(lines)


def _render_techniques_text(results):
    if not results:
        return "No matching techniques."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_technique_record_text(payload):
    technique = payload["technique"]
    lines = [
        f"{technique['name']} ({technique['id']})",
        technique["summary"],
        "",
        "Used by protocols:",
    ]
    if payload["used_by_protocol_ids"]:
        for protocol_id in payload["used_by_protocol_ids"]:
            lines.append(f"  - {protocol_id}")
    else:
        lines.append("  none")
    return "\n".join(lines)


def _render_contribution_models_text(results):
    if not results:
        return "No matching contribution models."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  {item['purpose']}")
    return "\n".join(lines)


def _render_contribution_model_record_text(payload):
    model = payload["contribution_model"]
    lines = [
        f"{model['name']} ({model['id']})",
        model["purpose"],
        f"privacy: {model['privacy_posture']}",
        "",
        "Promotion path:",
    ]
    for item in model["promotion_path"]:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def _render_interactions_text(results):
    if not results:
        return "No matching interaction hypotheses."
    lines = []
    for item in results:
        lines.append(f"{item['id']}: {item['left']['label']} <> {item['right']['label']}")
        lines.append(
            f"  type={item['interaction_type']} status={item['status']} confidence={item['confidence']}"
        )
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_interaction_record_text(payload):
    item = payload["interaction_hypothesis"]
    lines = [
        f"{item['id']}",
        f"left: {item['left']['label']} ({item['left']['entity_id']})",
        f"right: {item['right']['label']} ({item['right']['entity_id']})",
        f"type: {item['interaction_type']}",
        f"status: {item['status']}",
        f"confidence: {item['confidence']}",
        item["summary"],
        "",
        "Protocol relevance:",
    ]
    if item["protocol_relevance"]:
        for protocol_id in item["protocol_relevance"]:
            lines.append(f"  - {protocol_id}")
    else:
        lines.append("  none")
    if item["conditions"]:
        lines.append("")
        lines.append("Conditions:")
        for condition in item["conditions"]:
            lines.append(f"  - {condition}")
    return "\n".join(lines)


def _render_result_atom_schema_text(payload):
    schema = payload["result_atom_schema"]
    lines = [
        f"{schema['name']} ({schema['id']})",
        f"status: {schema['status']}",
        schema["summary"],
        "",
        "Required fields:",
    ]
    for field in schema["required_fields"]:
        lines.append(f"  - {field['name']} [{field['field_kind']}]")
    lines.append("")
    lines.append("Optional fields:")
    for field in schema["optional_fields"]:
        lines.append(f"  - {field['name']} [{field['field_kind']}]")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the Personality Instrument Registry.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    find_parser = subparsers.add_parser("find", help="Find instruments by ID, name, alias, filters, or text.")
    find_parser.add_argument("--ref", action="append", help="Instrument ID, slug, canonical name, or alias.")
    find_parser.add_argument("--family", action="append", help="Family filter. Repeatable.")
    find_parser.add_argument(
        "--filter",
        action="append",
        help="Ontology filter in dimension=value format. Repeatable.",
    )
    find_parser.add_argument("--text", help="Substring search across notes, claims, inferences, and constructs.")
    find_parser.add_argument("--related-to", help="Return instruments related by crosswalk to this instrument.")
    find_parser.add_argument("--format", choices=("text", "json"), default="text")

    compare_parser = subparsers.add_parser("compare", help="Compare two instruments.")
    compare_parser.add_argument("left", help="Left instrument reference.")
    compare_parser.add_argument("right", help="Right instrument reference.")
    compare_parser.add_argument("--format", choices=("text", "json"), default="text")

    show_parser = subparsers.add_parser("show", help="Show a full instrument record or one section.")
    show_parser.add_argument("ref", help="Instrument ID, slug, canonical name, or alias.")
    show_parser.add_argument(
        "--section",
        choices=(
            "instrument",
            "versions",
            "constructs",
            "claims",
            "resources",
            "annotations",
            "annotation_index",
            "inferences",
            "crosswalks",
            "risks",
            "use_cases",
            "notes",
        ),
    )
    show_parser.add_argument("--format", choices=("text", "json"), default="text")

    audit_parser = subparsers.add_parser("audit", help="Inspect corpus coverage and curation gaps.")
    audit_parser.add_argument("--needs-crosswalks", action="store_true", help="Show only instruments missing crosswalks.")
    audit_parser.add_argument(
        "--needs-multiple-resources",
        action="store_true",
        help="Show only instruments with fewer than two resources.",
    )
    audit_parser.add_argument(
        "--needs-official-resource",
        action="store_true",
        help="Show only instruments missing an official or semi-official resource.",
    )
    audit_parser.add_argument(
        "--needs-multiple-claims",
        action="store_true",
        help="Show only instruments with fewer than two source claims.",
    )
    audit_parser.add_argument(
        "--needs-multiple-inferences",
        action="store_true",
        help="Show only instruments with fewer than two house inferences.",
    )
    audit_parser.add_argument(
        "--needs-multiple-risks",
        action="store_true",
        help="Show only instruments with fewer than two risk records.",
    )
    audit_parser.add_argument(
        "--needs-multiple-use-cases",
        action="store_true",
        help="Show only instruments with fewer than two use cases.",
    )
    audit_parser.add_argument("--format", choices=("text", "json"), default="text")

    motifs_parser = subparsers.add_parser("motifs", help="List or show house motifs.")
    motifs_parser.add_argument("ref", nargs="?", help="Optional motif ID or name for a detailed record.")
    motifs_parser.add_argument("--text", help="Substring search across motif IDs, names, summaries, and tags.")
    motifs_parser.add_argument("--tag", help="Filter motifs by tag.")
    motifs_parser.add_argument("--related-to", help="Return motifs linked to an instrument or construct.")
    motifs_parser.add_argument("--format", choices=("text", "json"), default="text")

    trace_parser = subparsers.add_parser(
        "trace", help="Trace an instrument or construct through the house motif layer."
    )
    trace_parser.add_argument("ref", help="Instrument or construct reference.")
    trace_parser.add_argument("--format", choices=("text", "json"), default="text")

    protocols_parser = subparsers.add_parser("protocols", help="List or show protocol specs.")
    protocols_parser.add_argument("ref", nargs="?", help="Optional protocol ID or name for a detailed record.")
    protocols_parser.add_argument("--text", help="Substring search across protocol fields.")
    protocols_parser.add_argument("--consumer", help="Filter protocols by downstream consumer label.")
    protocols_parser.add_argument("--format", choices=("text", "json"), default="text")

    techniques_parser = subparsers.add_parser("techniques", help="List or show technique records.")
    techniques_parser.add_argument("ref", nargs="?", help="Optional technique ID or name for a detailed record.")
    techniques_parser.add_argument("--text", help="Substring search across technique fields.")
    techniques_parser.add_argument("--format", choices=("text", "json"), default="text")

    research_parser = subparsers.add_parser(
        "research-models", help="List or show research contribution model records."
    )
    research_parser.add_argument(
        "ref", nargs="?", help="Optional contribution model ID or name for a detailed record."
    )
    research_parser.add_argument("--text", help="Substring search across contribution model fields.")
    research_parser.add_argument("--format", choices=("text", "json"), default="text")

    interactions_parser = subparsers.add_parser(
        "interactions", help="List or show house interaction hypotheses."
    )
    interactions_parser.add_argument(
        "ref", nargs="?", help="Optional interaction hypothesis ID for a detailed record."
    )
    interactions_parser.add_argument("--related-to", help="Return interaction hypotheses related to an entity or motif.")
    interactions_parser.add_argument("--type", help="Filter by interaction type.")
    interactions_parser.add_argument("--protocol", help="Filter by protocol ID.")
    interactions_parser.add_argument("--text", help="Substring search across interaction summaries and rationale.")
    interactions_parser.add_argument("--format", choices=("text", "json"), default="text")

    result_atom_parser = subparsers.add_parser(
        "result-atom-schema", help="Show the downstream result atom contract."
    )
    result_atom_parser.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args()
    repository = load_repository_for_query(root)
    extensions = load_extensions_for_query(root)

    if args.command == "find":
        annotation_filters = {}
        for raw_filter in args.filter or []:
            if "=" not in raw_filter:
                raise SystemExit(f"Invalid --filter '{raw_filter}'. Expected dimension=value.")
            dimension, value = raw_filter.split("=", 1)
            annotation_filters.setdefault(dimension.strip(), set()).add(value.strip())
        results = query_results(
            repository,
            refs=args.ref,
            families=args.family,
            annotation_filters=annotation_filters,
            text=args.text,
            related_to=args.related_to,
        )
        if args.format == "json":
            print(dumps_json([result.to_dict() for result in results]))
        else:
            print(_render_find_text(results))
        return 0

    if args.command == "audit":
        payload = audit_repository(
            repository,
            needs_crosswalks=args.needs_crosswalks,
            needs_multiple_resources=args.needs_multiple_resources,
            needs_multiple_claims=args.needs_multiple_claims,
            needs_multiple_inferences=args.needs_multiple_inferences,
            needs_multiple_risks=args.needs_multiple_risks,
            needs_multiple_use_cases=args.needs_multiple_use_cases,
            needs_official_or_semi_official_resource=args.needs_official_resource,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_audit_text(payload))
        return 0

    if args.command == "show":
        bundle = resolve_instrument(repository, args.ref)
        payload = show_instrument(repository, args.ref, section=args.section)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_show_text(bundle, args.section, payload))
        return 0

    if args.command == "motifs":
        if args.ref:
            payload = motif_record(repository, extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_motif_record_text(payload))
            return 0
        payload = find_motifs(
            repository,
            extensions,
            text=args.text,
            tag=args.tag,
            related_to=args.related_to,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_motifs_text(payload))
        return 0

    if args.command == "trace":
        payload = trace_entity_to_motifs(repository, extensions, args.ref)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_trace_text(payload))
        return 0

    if args.command == "protocols":
        if args.ref:
            payload = protocol_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_protocol_record_text(payload))
            return 0
        payload = find_protocols(extensions, text=args.text, consumer=args.consumer)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_protocols_text(payload))
        return 0

    if args.command == "techniques":
        if args.ref:
            payload = technique_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_technique_record_text(payload))
            return 0
        payload = find_techniques(extensions, text=args.text)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_techniques_text(payload))
        return 0

    if args.command == "research-models":
        if args.ref:
            payload = contribution_model_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_contribution_model_record_text(payload))
            return 0
        payload = find_contribution_models(extensions, text=args.text)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_contribution_models_text(payload))
        return 0

    if args.command == "interactions":
        if args.ref:
            payload = interaction_hypothesis_record(repository, extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_interaction_record_text(payload))
            return 0
        payload = find_interaction_hypotheses(
            repository,
            extensions,
            related_to=args.related_to,
            interaction_type=args.type,
            protocol=args.protocol,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_interactions_text(payload))
        return 0

    if args.command == "result-atom-schema":
        payload = result_atom_schema_record(extensions)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_result_atom_schema_text(payload))
        return 0

    payload = compare_instruments(repository, args.left, args.right)
    if args.format == "json":
        print(dumps_json(payload))
    else:
        print(_render_compare_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
