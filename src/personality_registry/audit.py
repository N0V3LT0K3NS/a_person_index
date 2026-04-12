from __future__ import annotations

from personality_registry.loader import InstrumentBundle


def bundle_audit_entry(bundle: InstrumentBundle) -> dict:
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
    coverage = {
        "has_crosswalks": counts["crosswalks"] > 0,
        "has_multiple_resources": counts["resources"] > 1,
        "has_multiple_constructs": counts["constructs"] > 1,
        "has_multiple_claims": counts["claims"] > 1,
        "has_multiple_inferences": counts["inferences"] > 1,
        "has_multiple_risks": counts["risks"] > 1,
        "has_multiple_use_cases": counts["use_cases"] > 1,
        "has_official_or_semi_official_resource": any(
            resource.officiality in {"official", "semi_official"} for resource in bundle.resources
        ),
    }

    return {
        "slug": bundle.slug,
        "instrument_id": bundle.instrument.id,
        "canonical_name": bundle.instrument.canonical_name,
        "counts": counts,
        "resource_officiality": dict(sorted(officiality_counts.items())),
        "coverage": coverage,
    }


def audit_summary(audit_entries: list[dict]) -> dict:
    return {
        "instrument_count": len(audit_entries),
        "instruments_with_crosswalks": sum(1 for entry in audit_entries if entry["coverage"]["has_crosswalks"]),
        "instruments_with_multiple_resources": sum(
            1 for entry in audit_entries if entry["coverage"]["has_multiple_resources"]
        ),
        "instruments_with_multiple_constructs": sum(
            1 for entry in audit_entries if entry["coverage"]["has_multiple_constructs"]
        ),
        "instruments_with_multiple_claims": sum(
            1 for entry in audit_entries if entry["coverage"]["has_multiple_claims"]
        ),
        "instruments_with_multiple_inferences": sum(
            1 for entry in audit_entries if entry["coverage"]["has_multiple_inferences"]
        ),
        "instruments_with_multiple_risks": sum(
            1 for entry in audit_entries if entry["coverage"]["has_multiple_risks"]
        ),
        "instruments_with_multiple_use_cases": sum(
            1 for entry in audit_entries if entry["coverage"]["has_multiple_use_cases"]
        ),
        "instruments_with_official_or_semi_official_resource": sum(
            1
            for entry in audit_entries
            if entry["coverage"]["has_official_or_semi_official_resource"]
        ),
    }
