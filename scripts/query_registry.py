from __future__ import annotations

import argparse

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.query import (
    audit_repository,
    compare_instruments,
    dumps_json,
    load_repository_for_query,
    query_results,
    resolve_instrument,
    show_instrument,
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

    args = parser.parse_args()
    repository = load_repository_for_query(root)

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

    payload = compare_instruments(repository, args.left, args.right)
    if args.format == "json":
        print(dumps_json(payload))
    else:
        print(_render_compare_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
