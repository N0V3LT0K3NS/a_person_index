from __future__ import annotations

import argparse
import sys

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.query import (
    actualization_protocol_record,
    agent_orientation,
    analysis_mode_record,
    artifact_class_record,
    audit_repository,
    capability_record,
    comparison_shape_record,
    compare_instruments,
    contribution_model_record,
    curated_protocol_pack_record,
    dumps_json,
    expression_profile_record,
    find_actualization_protocols,
    find_analysis_modes,
    find_artifact_classes,
    find_capabilities,
    find_comparison_shapes,
    find_contribution_models,
    find_expression_profiles,
    find_interaction_hypotheses,
    find_motifs,
    find_promotion_pathways,
    find_protocol_packs,
    find_protocols,
    find_techniques,
    find_workflow_recipes,
    interaction_hypothesis_record,
    load_extensions_for_query,
    load_repository_for_query,
    motif_record,
    prepare_comparison_run,
    promotion_pathway_record,
    protocol_pack,
    protocol_pack_summary,
    protocol_pack_grammar,
    protocol_record,
    query_results,
    recommend_next_path,
    research_promotion_registry_record,
    resolve_instrument,
    result_atom_schema_record,
    show_instrument,
    technique_record,
    trace_entity_to_motifs,
    workflow_recipe_record,
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
    if payload.get("suggested_next_queries"):
        lines.append("")
        lines.append("Suggested next queries:")
        for item in payload["suggested_next_queries"]:
            lines.append(f"  - {item['tool']}: {item['purpose']}")
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
        return "No matching index programs."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(
            "  "
            f"kind={item['program_kind']} status={item['status']} "
            f"consumers={', '.join(item['downstream_consumers']) or 'none'}"
        )
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_protocol_record_text(payload):
    protocol = payload["protocol"]
    lines = [
        f"{protocol['name']} ({protocol['id']})",
        f"kind: {protocol['program_kind']}",
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
    lines.append("")
    lines.append("Component programs:")
    if payload["component_programs"]:
        for program in payload["component_programs"]:
            lines.append(f"  {program['name']} ({program['id']})")
    else:
        lines.append("  none")
    return "\n".join(lines)


def _render_protocol_pack_text(payload):
    pack = payload["pack"]
    lines = [
        f"{pack['protocol_name']} pack ({pack['id']})",
        f"grammar: {pack['grammar_id']}",
        f"targets: {', '.join(pack['target_labels']) or 'protocol-only'}",
        "",
        "Component programs:",
    ]
    if payload["component_programs"]:
        for program in payload["component_programs"]:
            lines.append(f"  - {program['name']} ({program['id']})")
    else:
        lines.append("  none")
    lines.extend(
        [
            "",
        "Techniques:",
        ]
    )
    for technique in payload["techniques"]:
        lines.append(f"  - {technique['name']} ({technique['id']})")
    lines.append("")
    lines.append("Motifs:")
    if payload["motif_summary"]:
        for item in payload["motif_summary"]:
            lines.append(
                f"  - {item['motif']['name']} ({item['motif']['id']}): "
                f"mappings={item['mapping_count']} via {', '.join(item['source_labels'])}"
            )
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Interaction hypotheses:")
    if payload["interaction_hypotheses"]:
        for item in payload["interaction_hypotheses"]:
            lines.append(
                f"  - {item['id']}: {item['left']['label']} <> {item['right']['label']} [{item['interaction_type']}]"
            )
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Execution order:")
    for step in payload["execution_order"]:
        lines.append(f"  - {step}")
    lines.append("")
    lines.append("Preferred return models:")
    for item in payload["return_contract"]["preferred_contribution_model_ids"]:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def _render_protocol_packs_text(results):
    if not results:
        return "No matching curated protocol packs."
    lines = []
    for item in results:
        lines.append(f"{item['title']} ({item['id']})")
        lines.append(
            "  "
            f"protocol={item['protocol_name']} status={item['status']} featured={'yes' if item['featured'] else 'no'}"
        )
        lines.append(f"  targets: {', '.join(item['target_labels'])}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_curated_protocol_pack_record_text(payload):
    catalog_entry = payload["catalog_entry"]
    lines = [
        f"{catalog_entry['title']} ({catalog_entry['id']})",
        f"protocol: {catalog_entry['protocol_name']} ({catalog_entry['protocol_id']})",
        f"status: {catalog_entry['status']}",
        f"featured: {'yes' if catalog_entry['featured'] else 'no'}",
        f"targets: {', '.join(catalog_entry['target_labels'])}",
        catalog_entry["summary"],
        "",
        _render_protocol_pack_text(payload["protocol_pack"]),
    ]
    return "\n".join(lines)


def _render_protocol_pack_grammar_text(payload):
    lines = [
        f"{payload['id']}",
        payload["summary"],
        "",
        "Required sections:",
    ]
    for section in payload["required_sections"]:
        lines.append(f"  - {section['section']}: {', '.join(section['required_keys'])}")
    lines.append("")
    lines.append("Construction rules:")
    for rule in payload["construction_rules"]:
        lines.append(f"  - {rule}")
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
        "Used by programs:",
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


def _render_research_promotion_registry_text(payload):
    registry = payload["promotion_registry"]
    lines = [
        f"{registry['name']} ({registry['id']})",
        f"status: {registry['status']}",
        registry["summary"],
        "",
        "Stages:",
    ]
    for stage in registry["stages"]:
        lines.append(f"  - {stage['id']}: {stage['name']}")
    lines.append("")
    lines.append("Promotion pathways:")
    for pathway in registry["promotion_pathways"]:
        lines.append(
            f"  - {pathway['id']}: {pathway['contribution_model_id']} -> {pathway['target_outcome_type']}"
        )
    return "\n".join(lines)


def _render_promotion_pathways_text(results):
    if not results:
        return "No matching promotion pathways."
    lines = []
    for item in results:
        lines.append(f"{item['id']}: {item['contribution_model_name']} -> {item['target_outcome_type']}")
        lines.append(f"  layer={item['target_layer']} stages={', '.join(item['stages'])}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_promotion_pathway_record_text(payload):
    pathway = payload["promotion_pathway"]
    contribution_model = payload["contribution_model"]
    lines = [
        f"{pathway['id']}",
        f"contribution model: {contribution_model['name']} ({contribution_model['id']})",
        f"target layer: {pathway['target_layer']}",
        f"target outcome: {pathway['target_outcome_type']}",
        pathway["summary"],
        "",
        "Stages:",
    ]
    for stage in payload["stages"]:
        lines.append(f"  - {stage['id']}: {stage['name']}")
    lines.append("")
    lines.append("Evidence requirements:")
    for item in pathway["evidence_requirements"]:
        lines.append(f"  - {item}")
    lines.append("")
    lines.append("Reviewer questions:")
    for item in pathway["reviewer_questions"]:
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


def _render_orientation_text(payload):
    lines = [
        payload["summary"],
        "",
        "Recommended sequence:",
    ]
    for step in payload["recommended_sequence"]:
        lines.append(f"  - {step}")
    lines.append("")
    lines.append("Featured program packs:")
    for item in payload["featured_program_packs"]:
        lines.append(f"  - {item['id']}: {item['title']} [{item['status']}]")
    lines.append("")
    lines.append("Framework refs:")
    for item in payload["available_framework_refs"]:
        aliases = f" aliases: {', '.join(item['aliases'])}" if item["aliases"] else ""
        lines.append(f"  - {item['canonical_name']} ({item['slug']}){aliases}")
    return "\n".join(lines)


def _render_protocol_pack_summary_text(payload):
    summary = payload["summary"]
    lines = [
        f"{summary['protocol_name']} [{payload['pack']['id']}]",
        f"targets: {', '.join(summary['target_labels']) if summary['target_labels'] else '(none)'}",
        f"techniques: {', '.join(summary['technique_names']) if summary['technique_names'] else '(none)'}",
        f"components: {', '.join(summary['component_program_names']) if summary['component_program_names'] else '(none)'}",
        f"motifs: {summary['motif_count']}",
        f"interaction hypotheses: {summary['interaction_hypothesis_count']}",
        "",
        "Execution order:",
    ]
    for step in summary["execution_order"]:
        lines.append(f"  - {step}")
    lines.append("")
    lines.append("Primary outputs:")
    for item in summary["primary_outputs"]:
        lines.append(f"  - {item}")
    return "\n".join(lines)


def _render_analysis_modes_text(results):
    if not results:
        return "No matching analysis modes."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  status={item['status']}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_analysis_mode_record_text(payload):
    item = payload["analysis_mode"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        item["summary"],
        "",
        "Intent signals:",
    ]
    for signal in item["intent_signals"]:
        lines.append(f"  - {signal}")
    lines.append("")
    lines.append("Preferred entrypoints:")
    for entry in item["preferred_entrypoints"]:
        lines.append(f"  - {entry}")
    return "\n".join(lines)


def _render_capabilities_text(results):
    if not results:
        return "No matching capabilities."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  status={item['status']} kind={item['capability_kind']}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_capability_record_text(payload):
    item = payload["capability"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        f"kind: {item['capability_kind']}",
        item["summary"],
        "",
        "Detection questions:",
    ]
    for question in item["detection_questions"]:
        lines.append(f"  - {question}")
    lines.append("")
    lines.append("Typical tool signals:")
    for signal in item["typical_tool_signals"]:
        lines.append(f"  - {signal}")
    lines.append("")
    lines.append("Used by artifact classes:")
    if payload["used_by_artifact_classes"]:
        for artifact in payload["used_by_artifact_classes"]:
            lines.append(f"  - {artifact['name']} ({artifact['id']})")
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Used by actualization protocols:")
    if payload["used_by_actualization_protocols"]:
        for protocol in payload["used_by_actualization_protocols"]:
            lines.append(f"  - {protocol['name']} ({protocol['id']})")
    else:
        lines.append("  none")
    return "\n".join(lines)


def _render_comparison_shapes_text(results):
    if not results:
        return "No matching comparison shapes."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  status={item['status']} modes={', '.join(item['mode_ids'])}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_comparison_shape_record_text(payload):
    item = payload["comparison_shape"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        item["summary"],
        "",
        "Declaration fields:",
    ]
    if item["declaration_fields"]:
        for field in item["declaration_fields"]:
            requirement = "required" if field["required"] else "optional"
            lines.append(
                f"  - {field['label']} ({field['id']}) [{field['value_kind']}; {requirement}]"
            )
            lines.append(f"    {field['summary']}")
    else:
        lines.append("  none")
    lines.extend([
        "",
        "Required declarations:",
    ])
    for entry in item["required_declarations"]:
        lines.append(f"  - {entry}")
    if item["optional_declarations"]:
        lines.append("")
        lines.append("Optional declarations:")
        for entry in item["optional_declarations"]:
            lines.append(f"  - {entry}")
    lines.append("")
    lines.append("Suitable artifact classes:")
    for artifact in payload["suitable_artifact_classes"]:
        lines.append(f"  - {artifact['name']} ({artifact['id']})")
    lines.append("")
    lines.append("Recommended protocols:")
    for protocol in payload["recommended_protocols"]:
        lines.append(f"  - {protocol['name']} ({protocol['id']})")
    return "\n".join(lines)


def _render_comparison_preflight_text(payload):
    shape = payload["comparison_shape"]
    lines = [
        f"Comparison shape: {shape['name']} ({shape['id']})",
        f"Readiness: {payload['readiness_status']}",
        "",
        "Provided declarations:",
    ]
    if payload["provided_declarations"]:
        for key, value in payload["provided_declarations"].items():
            if isinstance(value, list):
                rendered = ", ".join(value)
            else:
                rendered = value
            lines.append(f"  - {key}: {rendered}")
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Missing required fields:")
    if payload["missing_required_fields"]:
        for field in payload["missing_required_fields"]:
            lines.append(f"  - {field['label']} ({field['id']})")
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Invalid fields:")
    if payload["invalid_fields"]:
        for field in payload["invalid_fields"]:
            lines.append(f"  - {field['label']} ({field['field_id']}): {field['reason']}")
    else:
        lines.append("  none")

    if payload["unexpected_fields"]:
        lines.append("")
        lines.append("Unexpected fields:")
        for field in payload["unexpected_fields"]:
            lines.append(f"  - {field}")

    if payload["path_recommendation"]:
        lines.append("")
        lines.append("Recommended path:")
        lines.append(_render_recommendation_text(payload["path_recommendation"]))

    if payload["next_steps"]:
        lines.append("")
        lines.append("Next steps:")
        for step in payload["next_steps"]:
            lines.append(f"  - {step}")
    return "\n".join(lines)


def _render_expression_profiles_text(results):
    if not results:
        return "No matching expression profiles."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(
            f"  status={item['status']} mode={item['expression_mode']} audience={', '.join(item['audience_modes'])}"
        )
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_expression_profile_record_text(payload):
    item = payload["expression_profile"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        f"expression mode: {item['expression_mode']}",
        item["summary"],
        "",
        "Visible by default:",
    ]
    for entry in item["visible_by_default"]:
        lines.append(f"  - {entry}")
    lines.append("")
    lines.append("Keep implicit by default:")
    if item["keep_implicit_by_default"]:
        for entry in item["keep_implicit_by_default"]:
            lines.append(f"  - {entry}")
    else:
        lines.append("  none")
    lines.append("")
    lines.append("Default for artifact classes:")
    if payload["default_for_artifact_classes"]:
        for artifact in payload["default_for_artifact_classes"]:
            lines.append(f"  - {artifact['name']} ({artifact['id']})")
    else:
        lines.append("  none")
    return "\n".join(lines)


def _render_artifact_classes_text(results):
    if not results:
        return "No matching artifact classes."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(
            f"  status={item['status']} expression={item['default_expression_mode']} audience={', '.join(item['audience_modes'])}"
        )
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_artifact_class_record_text(payload):
    item = payload["artifact_class"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        f"default expression: {item['default_expression_mode']}",
        item["summary"],
    ]
    if payload.get("default_expression_profile"):
        expression = payload["default_expression_profile"]
        lines.extend(
            [
                "",
                f"Default expression profile: {expression['name']} ({expression['id']})",
                f"  {expression['summary']}",
            ]
        )
    lines.extend(
        [
            "",
            "Required evidence partitions:",
        ]
    )
    for partition in item["required_evidence_partitions"]:
        lines.append(f"  - {partition}")
    lines.append("")
    lines.append("Required capabilities:")
    for capability_id in item["required_capability_ids"]:
        lines.append(f"  - {capability_id}")
    if item["optional_capability_ids"]:
        lines.append("")
        lines.append("Optional capabilities:")
        for capability_id in item["optional_capability_ids"]:
            lines.append(f"  - {capability_id}")
    return "\n".join(lines)


def _render_actualization_protocols_text(results):
    if not results:
        return "No matching actualization protocols."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  status={item['status']} modes={', '.join(item['run_mode_ids'])}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_actualization_protocol_record_text(payload):
    item = payload["actualization_protocol"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        item["summary"],
        "",
        "Run modes:",
    ]
    for mode_id in item["run_mode_ids"]:
        lines.append(f"  - {mode_id}")
    lines.append("")
    lines.append("Target artifact classes:")
    for artifact_id in item["target_artifact_class_ids"]:
        lines.append(f"  - {artifact_id}")
    lines.append("")
    lines.append("Required capabilities:")
    for capability in item["required_capability_ids"]:
        lines.append(f"  - {capability}")
    if item["optional_capability_ids"]:
        lines.append("")
        lines.append("Optional capabilities:")
        for capability in item["optional_capability_ids"]:
            lines.append(f"  - {capability}")
    lines.append("")
    lines.append("Steps:")
    for step in item["steps"]:
        lines.append(f"  - {step}")
    return "\n".join(lines)


def _render_workflow_recipes_text(results):
    if not results:
        return "No matching workflow recipes."
    lines = []
    for item in results:
        lines.append(f"{item['name']} ({item['id']})")
        lines.append(f"  status={item['status']} artifact={item['artifact_class_id']} expression={item['expression_profile_id']}")
        lines.append(f"  {item['summary']}")
    return "\n".join(lines)


def _render_workflow_recipe_record_text(payload):
    item = payload["workflow_recipe"]
    lines = [
        f"{item['name']} ({item['id']})",
        f"status: {item['status']}",
        item["summary"],
        "",
        f"Artifact class: {payload['artifact_class']['name']} ({payload['artifact_class']['id']})",
        f"Expression profile: {payload['expression_profile']['name']} ({payload['expression_profile']['id']})",
        f"Actualization protocol: {payload['actualization_protocol']['name']} ({payload['actualization_protocol']['id']})",
        "",
        "Required capabilities:",
    ]
    for capability in item["required_capability_ids"]:
        lines.append(f"  - {capability}")
    lines.append("")
    lines.append("Recipe steps:")
    for step in item["recipe_steps"]:
        lines.append(f"  - {step}")
    if item["deliverables"]:
        lines.append("")
        lines.append("Deliverables:")
        for deliverable in item["deliverables"]:
            lines.append(f"  - {deliverable}")
    return "\n".join(lines)


def _render_recommendation_text(payload):
    mode = payload["run_mode"]
    lines = [
        f"Run mode: {mode['name']} ({mode['id']})",
    ]
    if payload["run_mode_inferred"]:
        lines.append("Mode status: inferred")
    if payload["declared_capabilities"]:
        lines.append("Capabilities:")
        for item in payload["declared_capabilities"]:
            lines.append(f"  - {item['name']} ({item['id']})")
    else:
        lines.append("Capabilities: none declared")

    lines.append("")
    lines.append("Recommended comparison shape:")
    if payload.get("recommended_comparison_shape"):
        shape = payload["recommended_comparison_shape"]
        lines.append(f"  {shape['name']} ({shape['id']})")
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Recommended artifact:")
    if payload["recommended_artifact"]:
        artifact = payload["recommended_artifact"]
        lines.append(
            f"  {artifact['artifact_class']['name']} ({artifact['artifact_class']['id']}) [{artifact['fit_status']}]"
        )
        if artifact["missing_required_capability_ids"]:
            lines.append(
                f"  missing required capabilities: {', '.join(artifact['missing_required_capability_ids'])}"
            )
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Recommended expression profile:")
    if payload.get("recommended_expression_profile"):
        expression = payload["recommended_expression_profile"]
        lines.append(
            f"  {expression['name']} ({expression['id']}) [{expression['expression_mode']}]"
        )
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Recommended workflow recipe:")
    if payload.get("recommended_workflow_recipe"):
        workflow = payload["recommended_workflow_recipe"]
        lines.append(
            f"  {workflow['workflow_recipe']['name']} ({workflow['workflow_recipe']['id']}) [{workflow['fit_status']}]"
        )
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Recommended actualization protocol:")
    if payload["recommended_actualization_protocol"]:
        protocol = payload["recommended_actualization_protocol"]
        lines.append(
            f"  {protocol['actualization_protocol']['name']} ({protocol['actualization_protocol']['id']}) [{protocol['fit_status']}]"
        )
        if protocol["missing_required_capability_ids"]:
            lines.append(
                f"  missing required capabilities: {', '.join(protocol['missing_required_capability_ids'])}"
            )
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Recommended next tools:")
    for tool_name in payload["recommended_tools"]:
        lines.append(f"  - {tool_name}")
    if payload["recommended_resources"]:
        lines.append("")
        lines.append("Recommended resources:")
        for uri in payload["recommended_resources"]:
            lines.append(f"  - {uri}")
    if payload["notes"]:
        lines.append("")
        lines.append("Notes:")
        for note in payload["notes"]:
            lines.append(f"  - {note}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Query A Person Index.")
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

    protocols_parser = subparsers.add_parser(
        "protocols",
        aliases=["programs"],
        help="List or show index program specs.",
    )
    protocols_parser.add_argument("ref", nargs="?", help="Optional protocol ID or name for a detailed record.")
    protocols_parser.add_argument("--text", help="Substring search across protocol fields.")
    protocols_parser.add_argument("--consumer", help="Filter protocols by downstream consumer label.")
    protocols_parser.add_argument("--format", choices=("text", "json"), default="text")

    protocol_pack_parser = subparsers.add_parser(
        "protocol-pack",
        aliases=["program-pack"],
        help="Assemble a downstream-ready runtime pack from an index program, scope, and A Person Index primitives.",
    )
    protocol_pack_parser.add_argument("ref", help="Protocol ID or name.")
    protocol_pack_parser.add_argument(
        "--framework",
        action="append",
        help="Framework or instrument reference to scope the pack. Repeatable.",
    )
    protocol_pack_parser.add_argument(
        "--construct",
        action="append",
        help="Construct reference to scope the pack. Repeatable.",
    )
    protocol_pack_parser.add_argument("--format", choices=("text", "json"), default="text")

    protocol_pack_grammar_parser = subparsers.add_parser(
        "protocol-pack-grammar",
        aliases=["program-pack-grammar"],
        help="Show the canonical grammar for generated runtime packs.",
    )
    protocol_pack_grammar_parser.add_argument("--format", choices=("text", "json"), default="text")

    protocol_packs_parser = subparsers.add_parser(
        "protocol-packs",
        aliases=["program-packs"],
        help="List or show curated runtime-pack catalog entries and their generated bundles.",
    )
    protocol_packs_parser.add_argument(
        "ref",
        nargs="?",
        help="Optional curated protocol-pack ID or title for a detailed record.",
    )
    protocol_packs_parser.add_argument("--text", help="Substring search across protocol-pack fields.")
    protocol_packs_parser.add_argument("--consumer", help="Filter curated protocol packs by intended consumer.")
    protocol_packs_parser.add_argument("--protocol", help="Filter curated protocol packs by protocol ID or name.")
    protocol_packs_parser.add_argument(
        "--status",
        choices=("draft", "experimental", "active"),
        help="Filter curated protocol packs by status.",
    )
    protocol_packs_parser.add_argument(
        "--featured",
        action="store_true",
        help="Return only featured curated protocol packs.",
    )
    protocol_packs_parser.add_argument("--format", choices=("text", "json"), default="text")

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

    research_promotion_parser = subparsers.add_parser(
        "research-promotion",
        help="Show the research promotion registry or list/show promotion pathways.",
    )
    research_promotion_parser.add_argument(
        "ref",
        nargs="?",
        help="Optional promotion pathway ID for a detailed record.",
    )
    research_promotion_parser.add_argument(
        "--contribution-model",
        help="Filter promotion pathways by contribution model ID or name.",
    )
    research_promotion_parser.add_argument(
        "--target-layer",
        choices=("house_synthesis", "protocol_library", "research_stream"),
        help="Filter promotion pathways by target layer.",
    )
    research_promotion_parser.add_argument(
        "--outcome",
        choices=(
            "mapping_revision",
            "interaction_hypothesis",
            "house_inference",
            "protocol_revision",
            "comparative_analysis",
        ),
        help="Filter promotion pathways by target outcome type.",
    )
    research_promotion_parser.add_argument("--text", help="Substring search across promotion pathway fields.")
    research_promotion_parser.add_argument("--format", choices=("text", "json"), default="text")

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

    orient_parser = subparsers.add_parser(
        "orient", help="Return a compact onboarding payload for agents arriving cold."
    )
    orient_parser.add_argument("--format", choices=("text", "json"), default="text")

    protocol_pack_summary_parser = subparsers.add_parser(
        "protocol-pack-summary",
        aliases=["program-pack-summary"],
        help="Return a compact summary of a runtime pack before fetching the full pack.",
    )
    protocol_pack_summary_parser.add_argument("ref", help="Protocol ID or name.")
    protocol_pack_summary_parser.add_argument(
        "--framework",
        action="append",
        help="Framework or instrument reference to scope the pack. Repeatable.",
    )
    protocol_pack_summary_parser.add_argument(
        "--construct",
        action="append",
        help="Construct reference to scope the pack. Repeatable.",
    )
    protocol_pack_summary_parser.add_argument("--format", choices=("text", "json"), default="text")

    modes_parser = subparsers.add_parser("modes", help="List or show advanced analysis modes.")
    modes_parser.add_argument("ref", nargs="?", help="Optional analysis mode ID or name for a detailed record.")
    modes_parser.add_argument("--text", help="Substring search across analysis mode fields.")
    modes_parser.add_argument("--format", choices=("text", "json"), default="text")

    capabilities_parser = subparsers.add_parser(
        "capabilities",
        help="List or show host capabilities used by the meta-skill and actualization layer.",
    )
    capabilities_parser.add_argument("ref", nargs="?", help="Optional capability ID or name for a detailed record.")
    capabilities_parser.add_argument(
        "--kind",
        choices=("input", "execution", "rendering", "visualization", "network", "persistence", "packaging"),
        help="Filter capabilities by capability kind.",
    )
    capabilities_parser.add_argument("--artifact", help="Filter capabilities by artifact class.")
    capabilities_parser.add_argument("--actualization", help="Filter capabilities by actualization protocol.")
    capabilities_parser.add_argument(
        "--required-only",
        action="store_true",
        help="When filtering by artifact or actualization protocol, exclude optional capabilities.",
    )
    capabilities_parser.add_argument("--text", help="Substring search across capability fields.")
    capabilities_parser.add_argument("--format", choices=("text", "json"), default="text")

    comparison_shapes_parser = subparsers.add_parser(
        "comparison-shapes",
        help="List or show structured comparison shapes for contextual or pairwise work.",
    )
    comparison_shapes_parser.add_argument(
        "ref", nargs="?", help="Optional comparison shape ID or name for a detailed record."
    )
    comparison_shapes_parser.add_argument("--mode", help="Filter comparison shapes by analysis mode.")
    comparison_shapes_parser.add_argument("--artifact", help="Filter comparison shapes by artifact class.")
    comparison_shapes_parser.add_argument("--protocol", help="Filter comparison shapes by protocol.")
    comparison_shapes_parser.add_argument("--text", help="Substring search across comparison shape fields.")
    comparison_shapes_parser.add_argument("--format", choices=("text", "json"), default="text")

    comparison_preflight_parser = subparsers.add_parser(
        "comparison-preflight",
        help="Validate whether a contextual or pairwise comparison run is ready from a named comparison shape and declared fields.",
    )
    comparison_preflight_parser.add_argument("shape", help="Comparison shape ID or name.")
    comparison_preflight_parser.add_argument(
        "--declare",
        action="append",
        help="Declaration field as key=value. Repeatable. For list fields, use comma-separated values.",
    )
    comparison_preflight_parser.add_argument(
        "--declarations-json",
        help="Optional JSON object of declarations for the comparison shape.",
    )
    comparison_preflight_parser.add_argument(
        "--capability",
        action="append",
        help="Declared host capability ID or name. Repeatable.",
    )
    comparison_preflight_parser.add_argument("--format", choices=("text", "json"), default="text")

    expressions_parser = subparsers.add_parser("expressions", help="List or show expression profiles.")
    expressions_parser.add_argument(
        "ref", nargs="?", help="Optional expression profile ID or name for a detailed record."
    )
    expressions_parser.add_argument("--mode", help="Filter expression profiles by expression mode.")
    expressions_parser.add_argument("--audience", help="Filter expression profiles by audience mode.")
    expressions_parser.add_argument("--artifact", help="Filter expression profiles by artifact class.")
    expressions_parser.add_argument("--text", help="Substring search across expression profile fields.")
    expressions_parser.add_argument("--format", choices=("text", "json"), default="text")

    artifacts_parser = subparsers.add_parser("artifacts", help="List or show artifact classes.")
    artifacts_parser.add_argument("ref", nargs="?", help="Optional artifact class ID or name for a detailed record.")
    artifacts_parser.add_argument("--mode", help="Filter artifact classes by analysis mode ID or name.")
    artifacts_parser.add_argument("--capability", help="Filter artifact classes by capability.")
    artifacts_parser.add_argument("--text", help="Substring search across artifact class fields.")
    artifacts_parser.add_argument("--format", choices=("text", "json"), default="text")

    actualization_parser = subparsers.add_parser(
        "actualization",
        help="List or show actualization protocols that turn comparative work into downstream artifacts.",
    )
    actualization_parser.add_argument(
        "ref", nargs="?", help="Optional actualization protocol ID or name for a detailed record."
    )
    actualization_parser.add_argument("--mode", help="Filter actualization protocols by analysis mode ID or name.")
    actualization_parser.add_argument("--artifact", help="Filter actualization protocols by artifact class.")
    actualization_parser.add_argument("--capability", help="Filter actualization protocols by capability.")
    actualization_parser.add_argument("--text", help="Substring search across actualization protocol fields.")
    actualization_parser.add_argument("--format", choices=("text", "json"), default="text")

    workflow_parser = subparsers.add_parser(
        "workflows",
        help="List or show workflow recipes that operationalize an artifact path in a host environment.",
    )
    workflow_parser.add_argument(
        "ref", nargs="?", help="Optional workflow recipe ID or name for a detailed record."
    )
    workflow_parser.add_argument("--mode", help="Filter workflow recipes by analysis mode.")
    workflow_parser.add_argument("--artifact", help="Filter workflow recipes by artifact class.")
    workflow_parser.add_argument("--actualization", help="Filter workflow recipes by actualization protocol.")
    workflow_parser.add_argument("--expression", help="Filter workflow recipes by expression profile.")
    workflow_parser.add_argument("--capability", help="Filter workflow recipes by required capability.")
    workflow_parser.add_argument("--text", help="Substring search across workflow recipe fields.")
    workflow_parser.add_argument("--format", choices=("text", "json"), default="text")

    recommend_parser = subparsers.add_parser(
        "recommend-path",
        help="Recommend the next A Person Index path from the current run shape and declared capabilities.",
    )
    recommend_parser.add_argument("--mode", help="Explicit run mode ID or name.")
    recommend_parser.add_argument("--comparison-shape", help="Optional comparison shape ID or name.")
    recommend_parser.add_argument(
        "--capability",
        action="append",
        help="Declared host capability ID or name. Repeatable.",
    )
    recommend_parser.add_argument("--artifact", help="Optional artifact class to target explicitly.")
    recommend_parser.add_argument("--text", help="Optional task hint for mode or artifact inference.")
    recommend_parser.add_argument("--format", choices=("text", "json"), default="text")

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

    if args.command in {"protocols", "programs"}:
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

    if args.command in {"protocol-pack", "program-pack"}:
        payload = protocol_pack(
            repository,
            extensions,
            args.ref,
            framework_refs=args.framework,
            construct_refs=args.construct,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_protocol_pack_text(payload))
        return 0

    if args.command in {"protocol-pack-grammar", "program-pack-grammar"}:
        payload = protocol_pack_grammar()
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_protocol_pack_grammar_text(payload))
        return 0

    if args.command in {"protocol-packs", "program-packs"}:
        if args.ref:
            payload = curated_protocol_pack_record(repository, extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_curated_protocol_pack_record_text(payload))
            return 0
        payload = find_protocol_packs(
            repository,
            extensions,
            text=args.text,
            consumer=args.consumer,
            protocol=args.protocol,
            status=args.status,
            featured_only=args.featured,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_protocol_packs_text(payload))
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

    if args.command == "research-promotion":
        if args.ref:
            payload = promotion_pathway_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_promotion_pathway_record_text(payload))
            return 0
        if args.contribution_model or args.target_layer or args.outcome or args.text:
            payload = find_promotion_pathways(
                extensions,
                contribution_model=args.contribution_model,
                target_layer=args.target_layer,
                target_outcome_type=args.outcome,
                text=args.text,
            )
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_promotion_pathways_text(payload))
            return 0
        payload = research_promotion_registry_record(extensions)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_research_promotion_registry_text(payload))
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

    if args.command == "orient":
        payload = agent_orientation(repository, extensions)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_orientation_text(payload))
        return 0

    if args.command == "modes":
        if args.ref:
            payload = analysis_mode_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_analysis_mode_record_text(payload))
            return 0
        payload = find_analysis_modes(extensions, text=args.text)
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_analysis_modes_text(payload))
        return 0

    if args.command == "capabilities":
        if args.ref:
            payload = capability_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_capability_record_text(payload))
            return 0
        payload = find_capabilities(
            extensions,
            kind=args.kind,
            artifact_class=args.artifact,
            actualization_protocol=args.actualization,
            include_optional=not args.required_only,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_capabilities_text(payload))
        return 0

    if args.command == "comparison-shapes":
        if args.ref:
            payload = comparison_shape_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_comparison_shape_record_text(payload))
            return 0
        payload = find_comparison_shapes(
            extensions,
            mode=args.mode,
            artifact_class=args.artifact,
            protocol=args.protocol,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_comparison_shapes_text(payload))
        return 0

    if args.command == "comparison-preflight":
        declarations: dict[str, str] = {}
        if args.declarations_json:
            import json

            loaded = json.loads(args.declarations_json)
            if not isinstance(loaded, dict):
                raise SystemExit("--declarations-json must decode to an object.")
            declarations.update(loaded)
        for raw_declaration in args.declare or []:
            if "=" not in raw_declaration:
                raise SystemExit(f"Invalid --declare '{raw_declaration}'. Expected key=value.")
            key, value = raw_declaration.split("=", 1)
            declarations[key.strip()] = value.strip()
        payload = prepare_comparison_run(
            extensions,
            comparison_shape=args.shape,
            declarations=declarations,
            capability_refs=args.capability,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_comparison_preflight_text(payload))
        return 0

    if args.command == "expressions":
        if args.ref:
            payload = expression_profile_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_expression_profile_record_text(payload))
            return 0
        payload = find_expression_profiles(
            extensions,
            mode=args.mode,
            audience=args.audience,
            artifact_class=args.artifact,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_expression_profiles_text(payload))
        return 0

    if args.command == "artifacts":
        if args.ref:
            payload = artifact_class_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_artifact_class_record_text(payload))
            return 0
        payload = find_artifact_classes(
            extensions,
            mode=args.mode,
            capability=args.capability,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_artifact_classes_text(payload))
        return 0

    if args.command == "actualization":
        if args.ref:
            payload = actualization_protocol_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_actualization_protocol_record_text(payload))
            return 0
        payload = find_actualization_protocols(
            extensions,
            run_mode=args.mode,
            artifact_class=args.artifact,
            capability=args.capability,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_actualization_protocols_text(payload))
        return 0

    if args.command == "workflows":
        if args.ref:
            payload = workflow_recipe_record(extensions, args.ref)
            if args.format == "json":
                print(dumps_json(payload))
            else:
                print(_render_workflow_recipe_record_text(payload))
            return 0
        payload = find_workflow_recipes(
            extensions,
            run_mode=args.mode,
            artifact_class=args.artifact,
            actualization_protocol=args.actualization,
            expression_profile=args.expression,
            capability=args.capability,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_workflow_recipes_text(payload))
        return 0

    if args.command == "recommend-path":
        payload = recommend_next_path(
            extensions,
            run_mode=args.mode,
            comparison_shape=args.comparison_shape,
            capability_refs=args.capability,
            artifact_class=args.artifact,
            text=args.text,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_recommendation_text(payload))
        return 0

    if args.command in {"protocol-pack-summary", "program-pack-summary"}:
        payload = protocol_pack_summary(
            repository,
            extensions,
            args.ref,
            framework_refs=args.framework,
            construct_refs=args.construct,
        )
        if args.format == "json":
            print(dumps_json(payload))
        else:
            print(_render_protocol_pack_summary_text(payload))
        return 0

    payload = compare_instruments(repository, args.left, args.right)
    if args.format == "json":
        print(dumps_json(payload))
    else:
        print(_render_compare_text(payload))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyError as error:
        message = error.args[0] if error.args else str(error)
        print(message, file=sys.stderr)
        raise SystemExit(1)
