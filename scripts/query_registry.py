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
                f"resources={entry['counts']['resources']} crosswalks={entry['counts']['crosswalks']} "
                f"officiality={entry['resource_officiality']}"
            )
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
            needs_official_or_semi_official_resource=args.needs_official_resource,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_audit_text(payload))
        return 0

    payload = compare_instruments(repository, args.left, args.right)
    if args.format == "json":
        print(dumps_json(payload))
    else:
        print(_render_compare_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
