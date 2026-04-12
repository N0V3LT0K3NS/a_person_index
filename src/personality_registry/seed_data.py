from __future__ import annotations

from typing import Any

from personality_registry.constants import REQUIRED_ANNOTATION_DIMENSIONS

ONTOLOGY_REGISTRY = {
    "ontology": {
        "id": "instrument_ontology_v0_1",
        "title": "Human Description Instrument Ontology",
        "status": "active",
        "version": "0.1.0",
        "description": (
            "A versioned ontology for describing and comparing personality tests, "
            "typology systems, psychometric instruments, symbolic self-description "
            "systems, and adjacent person-labeling frameworks."
        ),
        "principles": [
            "separate_source_claims_from_meta_annotations",
            "separate_explicit_from_implicit_from_inferred",
            "preserve_epistemic_differences",
            "keep_crosswalks_first_class",
            "support_incremental_growth",
        ],
    }
}

ONTOLOGY_DIMENSIONS = {
    "dimensions": [
        {
            "id": "instrument_family",
            "cardinality": "many",
            "description": "Top-level family membership for an instrument.",
            "enum_file": "enums/instrument_family.yaml",
        },
        {
            "id": "primary_measurement_target",
            "cardinality": "many",
            "description": "Primary things the instrument claims or appears to measure.",
            "enum_file": "enums/primary_measurement_target.yaml",
        },
        {
            "id": "representational_form",
            "cardinality": "many",
            "description": "How the instrument encodes a person.",
            "enum_file": "enums/representational_form.yaml",
        },
        {
            "id": "temporal_stance",
            "cardinality": "many",
            "description": "What kind of time-object the instrument assumes it captures.",
            "enum_file": "enums/temporal_stance.yaml",
        },
        {
            "id": "person_ontology",
            "cardinality": "many",
            "description": "What the instrument implicitly treats a person as.",
            "enum_file": "enums/person_ontology.yaml",
        },
        {
            "id": "administration_mode",
            "cardinality": "many",
            "description": "How the instrument gathers data.",
            "enum_file": "enums/administration_mode.yaml",
        },
        {
            "id": "scoring_logic",
            "cardinality": "many",
            "description": "How responses become outputs.",
            "enum_file": "enums/scoring_logic.yaml",
        },
        {
            "id": "epistemic_basis",
            "cardinality": "many",
            "description": "General evidence type or truth-claim basis.",
            "enum_file": "enums/epistemic_basis.yaml",
        },
        {
            "id": "evidence_profile",
            "cardinality": "many",
            "description": "More granular evidence annotations.",
            "enum_file": "enums/evidence_profile.yaml",
        },
        {
            "id": "interpretive_burden",
            "cardinality": "one",
            "description": "How much meaning depends on interpreter vs instrument.",
            "enum_file": "enums/interpretive_burden.yaml",
        },
        {
            "id": "granularity",
            "cardinality": "one",
            "description": "Resolution of the output model.",
            "enum_file": "enums/granularity.yaml",
        },
        {
            "id": "context_sensitivity",
            "cardinality": "one",
            "description": "How global vs context-sensitive the outputs are.",
            "enum_file": "enums/context_sensitivity.yaml",
        },
        {
            "id": "change_model",
            "cardinality": "many",
            "description": "What kind of change the instrument assumes is possible.",
            "enum_file": "enums/change_model.yaml",
        },
        {
            "id": "distortion_risk",
            "cardinality": "many",
            "description": "Likely distortions or misuse risks.",
            "enum_file": "enums/distortion_risk.yaml",
        },
        {
            "id": "deployment_context",
            "cardinality": "many",
            "description": "Common contexts where the instrument is used.",
            "enum_file": "enums/deployment_context.yaml",
        },
        {
            "id": "utility_profile",
            "cardinality": "many",
            "description": "What the instrument is actually useful for.",
            "enum_file": "enums/utility_profile.yaml",
        },
        {
            "id": "target_population",
            "cardinality": "many",
            "description": "Intended or normed user population.",
            "enum_file": "enums/target_population.yaml",
        },
        {
            "id": "norming_status",
            "cardinality": "one",
            "description": "Quality or presence of normative calibration.",
            "enum_file": "enums/norming_status.yaml",
        },
        {
            "id": "identity_adhesion_risk",
            "cardinality": "one",
            "description": "How likely users are to fuse output with identity.",
            "enum_file": "enums/identity_adhesion_risk.yaml",
        },
        {
            "id": "actionability_type",
            "cardinality": "many",
            "description": "What kind of actionability the instrument supports.",
            "enum_file": "enums/actionability_type.yaml",
        },
        {
            "id": "worldview_load",
            "cardinality": "one",
            "description": "Degree to which the instrument embeds a thick worldview.",
            "enum_file": "enums/worldview_load.yaml",
        },
        {
            "id": "cultural_symbolic_role",
            "cardinality": "many",
            "description": "Social and symbolic role beyond measurement.",
            "enum_file": "enums/cultural_symbolic_role.yaml",
        },
        {
            "id": "synthesis_value_for_ilens",
            "cardinality": "one",
            "description": "Estimated usefulness as an ILENS input layer.",
            "enum_file": "enums/synthesis_value_for_ilens.yaml",
        },
        {
            "id": "overlap_mode",
            "cardinality": "many",
            "description": "Typical overlap pattern with other instruments.",
            "enum_file": "enums/overlap_mode.yaml",
        },
    ]
}

ONTOLOGY_ENUMS = {
    "instrument_family": [
        "trait_personality",
        "typology",
        "motivational",
        "affective",
        "attachment_relational",
        "behavioral_interactional",
        "conative_action_style",
        "cognitive_style",
        "learning_style",
        "strengths_talent",
        "values_moral_orientation",
        "leadership_workplace",
        "developmental_stage",
        "clinical_symptom_pathology",
        "resilience_wellbeing",
        "cultural_intercultural",
        "identity_self_concept",
        "worldview_meaning_making",
        "symbolic_archetypal_spiritual",
        "hybrid_integrative",
        "projective",
        "observer_rating",
        "other",
    ],
    "primary_measurement_target": [
        "stable_traits",
        "interpersonal_style",
        "affect_emotion",
        "work_style",
        "motivation_drives",
        "defense_patterns",
        "attachment_patterns",
        "behavioral_style",
        "strengths_talents",
        "cultural_adaptation",
        "identity_narrative",
        "symbolic_archetypal_patterning",
        "moral_character",
        "dark_personality_features",
        "cognitive_preferences",
        "communication_preferences",
        "values_orientation",
        "relational_needs",
        "developmental_growth",
        "subjective_meaning",
    ],
    "representational_form": [
        "continuous_dimensional",
        "hierarchical_model",
        "categorical_typology",
        "hybrid_dimensional_typological",
        "narrative_description",
        "developmental_level",
        "profile_vector",
        "symbolic_chart",
        "rank_order_strengths",
        "binary_preferences",
    ],
    "temporal_stance": [
        "stable_traits",
        "semi_stable_patterns",
        "situational_state",
        "cyclical_temporal_pattern",
        "developmental_path",
        "identity_narrative_snapshot",
    ],
    "person_ontology": [
        "trait_container",
        "dynamic_strategy_system",
        "motivational_structure",
        "relational_attachment_system",
        "symbolic_cosmological_self",
        "strengths_expression_profile",
        "work_behavior_pattern",
        "hybrid_personhood_model",
        "cultural_competence_profile",
        "moral_character_profile",
    ],
    "administration_mode": [
        "self_report_questionnaire",
        "observer_report",
        "practitioner_interview",
        "practitioner_interpretation",
        "algorithmic_chart_calculation",
        "self_identification",
        "workshop_facilitation",
    ],
    "scoring_logic": [
        "sum_or_average_scale_scoring",
        "ipsative_preference_scoring",
        "type_assignment_rules",
        "interpretive_pattern_matching",
        "algorithmic_chart_rules",
        "rank_order_selection",
        "expert_interpretation",
        "factor_scoring",
    ],
    "epistemic_basis": [
        "strong_psychometric_validation",
        "mixed_psychometric_and_theoretical",
        "weak_or_contested_empirical_basis",
        "clinical_observation",
        "coaching_practice",
        "symbolic_tradition",
        "mixed_lineages",
        "proprietary_workplace_analytics",
        "cross_cultural_research",
        "popular_psychology",
        "narrative_interpretation",
    ],
    "evidence_profile": [
        "extensive_peer_review",
        "normative_data_available",
        "proprietary_or_limited_transparency",
        "cross_cultural_support",
        "mostly_anecdotal_or_practitioner_based",
        "contested_validity",
        "mixed_evidence",
        "open_question_bank_available",
    ],
    "interpretive_burden": ["low", "medium", "high", "very_high"],
    "granularity": ["low", "medium", "high", "very_high"],
    "context_sensitivity": ["low", "medium", "high", "very_high"],
    "change_model": [
        "trait_stability",
        "developmental_growth",
        "situational_expression",
        "skills_trainability",
        "cyclical_activation",
        "identity_revision",
        "subtype_refinement",
    ],
    "distortion_risk": [
        "self_report_distortion",
        "overinterpretation",
        "identity_capture",
        "barnum_effect",
        "practitioner_projection",
        "cultural_overgeneralization",
        "workplace_misuse",
        "reductionism",
        "reification",
        "confirmation_bias",
        "determinism",
        "false_precision",
    ],
    "deployment_context": [
        "self_reflection",
        "coaching",
        "therapy",
        "workplace",
        "hiring",
        "education",
        "team_design",
        "leadership_development",
        "relationship_support",
        "spiritual_community",
        "internet_identity_culture",
        "research",
        "intercultural_training",
    ],
    "utility_profile": [
        "self_understanding",
        "communication_adaptation",
        "team_alignment",
        "developmental_reflection",
        "selection_screening",
        "coaching_language",
        "cultural_navigation",
        "research_baseline",
        "symbolic_reflection",
        "motive_exploration",
        "strengths_identification",
        "relational_patterning",
    ],
    "target_population": [
        "general_adult_population",
        "workplace_teams",
        "students",
        "coaching_clients",
        "clinical_populations",
        "spiritual_seekers",
        "internet_communities",
        "leaders_managers",
        "couples_families",
        "multicultural_professionals",
    ],
    "norming_status": ["well_normed", "variant_dependent", "limited_norms", "not_normed", "unknown"],
    "identity_adhesion_risk": ["very_low", "low", "medium", "high", "very_high"],
    "actionability_type": [
        "descriptive_reflection",
        "coaching_intervention",
        "communication_adjustment",
        "selection_decision_support",
        "team_design_support",
        "developmental_planning",
        "relational_discussion",
        "symbolic_storytelling",
    ],
    "worldview_load": ["very_low", "low", "medium", "high", "very_high"],
    "cultural_symbolic_role": [
        "professional_shorthand",
        "internet_identity_language",
        "workplace_identity_language",
        "spiritual_symbolic_system",
        "coaching_identity_language",
        "research_anchor",
        "pop_psychology_meme",
        "community_belonging_language",
    ],
    "synthesis_value_for_ilens": ["low", "medium", "high", "very_high"],
    "overlap_mode": [
        "partial_construct_overlap",
        "shared_identity_space",
        "complementary_layers",
        "often_misread_as_equivalent",
        "weak_direct_mapping",
        "workplace_family_resemblance",
    ],
}


def _snake_slug(slug: str) -> str:
    return slug.replace("-", "_")


def _make_annotation(
    base: str,
    target_id: str,
    dimension: str,
    values: list[str],
    rationale: str,
    evidence_links: list[str],
    status: str = "inferred",
    confidence: str = "medium",
) -> dict[str, Any]:
    return {
        "id": f"ann_{base}_{dimension}",
        "target_entity_type": "instrument",
        "target_entity_id": target_id,
        "ontology_dimension": dimension,
        "ontology_values": values,
        "annotation_status": status,
        "confidence": confidence,
        "rationale": rationale,
        "evidence_links": evidence_links,
    }


def _default_annotation_rationale(canonical_name: str, dimension: str) -> str:
    return f"House annotation for {canonical_name} on the ontology dimension '{dimension}'."


def _build_annotations(
    base: str,
    canonical_name: str,
    instrument_id: str,
    resource_id: str,
    values_by_dimension: dict[str, list[str]],
    status_by_dimension: dict[str, str] | None = None,
    confidence_by_dimension: dict[str, str] | None = None,
    rationale_by_dimension: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    status_by_dimension = status_by_dimension or {}
    confidence_by_dimension = confidence_by_dimension or {}
    rationale_by_dimension = rationale_by_dimension or {}

    annotations: list[dict[str, Any]] = []
    for dimension, values in values_by_dimension.items():
        annotations.append(
            _make_annotation(
                base=base,
                target_id=instrument_id,
                dimension=dimension,
                values=values,
                rationale=rationale_by_dimension.get(
                    dimension,
                    _default_annotation_rationale(canonical_name, dimension),
                ),
                evidence_links=[resource_id],
                status=status_by_dimension.get(dimension, "inferred"),
                confidence=confidence_by_dimension.get(dimension, "medium"),
            )
        )
    return annotations


def default_placeholder_bundle(
    slug: str,
    canonical_name: str,
    instrument_id: str | None = None,
) -> dict[str, Any]:
    return placeholder_bundle(
        slug=slug,
        canonical_name=canonical_name,
        instrument_id=instrument_id,
        short_description="Starter scaffold entry for a person-description framework.",
        families=["other"],
        primary_measurement_target=["identity_narrative"],
        representational_form=["narrative_description"],
        temporal_stance=["semi_stable_patterns"],
        person_ontology=["hybrid_personhood_model"],
        administration_mode=["self_report_questionnaire"],
        scoring_logic=["interpretive_pattern_matching"],
        epistemic_basis=["mixed_lineages"],
        interpretive_burden="medium",
        granularity="medium",
        context_sensitivity="medium",
        change_model=["identity_revision"],
        distortion_risk=["overinterpretation"],
        deployment_context=["self_reflection"],
        utility_profile=["self_understanding"],
        identity_adhesion_risk="medium",
        worldview_load="medium",
        synthesis_value_for_ilens="medium",
        evidence_profile=["mixed_evidence"],
        target_population=["general_adult_population"],
        norming_status="unknown",
        actionability_type=["descriptive_reflection"],
        cultural_symbolic_role=["pop_psychology_meme"],
        overlap_mode=["weak_direct_mapping"],
        construct_name="Core profile",
        construct_definition="Placeholder construct for a newly scaffolded instrument entry.",
        claim_text=(
            "Starter placeholder claim. Replace with a source-backed statement about what the "
            "instrument says it measures or represents."
        ),
        inference_text=(
            "Starter scaffold entry requiring fuller source collection, ontology refinement, "
            "and cross-system analysis."
        ),
        risk_description="Placeholder risk entry. Replace with a concrete misuse mode or distortion hazard.",
        cautions="Replace starter caution text after source review.",
    )


def placeholder_bundle(
    *,
    slug: str,
    canonical_name: str,
    short_description: str,
    families: list[str],
    primary_measurement_target: list[str],
    representational_form: list[str],
    temporal_stance: list[str],
    person_ontology: list[str],
    administration_mode: list[str],
    scoring_logic: list[str],
    epistemic_basis: list[str],
    interpretive_burden: str,
    granularity: str,
    context_sensitivity: str,
    change_model: list[str],
    distortion_risk: list[str],
    deployment_context: list[str],
    utility_profile: list[str],
    identity_adhesion_risk: str,
    worldview_load: str,
    synthesis_value_for_ilens: str,
    evidence_profile: list[str] | None = None,
    target_population: list[str] | None = None,
    norming_status: str | None = None,
    actionability_type: list[str] | None = None,
    cultural_symbolic_role: list[str] | None = None,
    overlap_mode: list[str] | None = None,
    short_names: list[str] | None = None,
    aliases: list[str] | None = None,
    creators: list[str] | None = None,
    publisher_or_owner: str = "unknown",
    original_release_year: int | None = None,
    official_websites: list[str | None] | None = None,
    licensing_model: str = "mixed",
    primary_domain: str = "personality_framework",
    country_or_origin_context: list[str] | None = None,
    construct_name: str = "Core construct",
    construct_short_name: str | None = None,
    construct_kind: list[str] | None = None,
    construct_definition: str = "",
    scoring_type: str = "variant_dependent",
    include_primary_construct: bool = True,
    extra_constructs: list[dict[str, Any]] | None = None,
    claim_text: str = "",
    extra_claims: list[dict[str, Any]] | None = None,
    resource_type: str = "overview",
    resource_title: str | None = None,
    resource_url: str | None = None,
    resource_author: str | None = None,
    resource_publication_date: str | None = None,
    resource_publisher: str | None = None,
    resource_language: str = "en",
    resource_access_status: str = "public",
    resource_officiality: str = "secondary",
    resource_notes: str | None = "Starter source placeholder. Replace with a canonical source.",
    extra_resources: list[dict[str, Any]] | None = None,
    inference_id_suffix: str = "starter",
    inference_type: str = "starter_position",
    inference_confidence: str = "medium",
    inference_text: str | None = None,
    extra_inferences: list[dict[str, Any]] | None = None,
    crosswalks: list[dict[str, Any]] | None = None,
    risk_type: str = "overinterpretation",
    risk_severity: str = "medium",
    risk_description: str = "Outputs may be overread when context, method limits, or source quality are ignored.",
    risk_mitigation: str = "Treat the framework as one layer among several and preserve uncertainty.",
    extra_risks: list[dict[str, Any]] | None = None,
    use_context: str = "self_reflection",
    utility_type: str = "self_understanding",
    suitability_level: str = "medium",
    cautions: str = "Use as a descriptive aid, not a total account of the person.",
    extra_use_cases: list[dict[str, Any]] | None = None,
    notes: str | None = None,
    instrument_notes: str | None = None,
    instrument_id: str | None = None,
) -> dict[str, Any]:
    base = _snake_slug(slug)
    instrument_id = instrument_id or f"instr_{base}"
    version_id = f"ver_{base}_general"
    construct_id = f"con_{base}_core"
    resource_id = f"res_{base}_overview"
    claim_id = f"clm_{base}_overview"
    inference_id = f"inf_{base}_{inference_id_suffix}"
    risk_id = f"rsk_{base}_{risk_type}"
    use_case_id = f"use_{base}_{use_context}"

    values_by_dimension = {
        "instrument_family": families,
        "primary_measurement_target": primary_measurement_target,
        "representational_form": representational_form,
        "temporal_stance": temporal_stance,
        "person_ontology": person_ontology,
        "administration_mode": administration_mode,
        "scoring_logic": scoring_logic,
        "epistemic_basis": epistemic_basis,
        "interpretive_burden": [interpretive_burden],
        "granularity": [granularity],
        "context_sensitivity": [context_sensitivity],
        "change_model": change_model,
        "distortion_risk": distortion_risk,
        "deployment_context": deployment_context,
        "utility_profile": utility_profile,
        "identity_adhesion_risk": [identity_adhesion_risk],
        "worldview_load": [worldview_load],
        "synthesis_value_for_ilens": [synthesis_value_for_ilens],
    }
    if evidence_profile:
        values_by_dimension["evidence_profile"] = evidence_profile
    if target_population:
        values_by_dimension["target_population"] = target_population
    if norming_status:
        values_by_dimension["norming_status"] = [norming_status]
    if actionability_type:
        values_by_dimension["actionability_type"] = actionability_type
    if cultural_symbolic_role:
        values_by_dimension["cultural_symbolic_role"] = cultural_symbolic_role
    if overlap_mode:
        values_by_dimension["overlap_mode"] = overlap_mode

    annotations = _build_annotations(
        base=base,
        canonical_name=canonical_name,
        instrument_id=instrument_id,
        resource_id=resource_id,
        values_by_dimension=values_by_dimension,
    )
    missing_dimensions = [
        dimension for dimension in REQUIRED_ANNOTATION_DIMENSIONS if dimension not in values_by_dimension
    ]
    if missing_dimensions:
        raise ValueError(f"Placeholder bundle for {slug} is missing required dimensions: {missing_dimensions}")

    note_text = notes or f"""# {canonical_name}

## What it is
{short_description}

## Why it matters
This is a starter registry entry for {canonical_name}. It is structurally valid but should be deepened with better sources, richer claims, and more precise cross-system analysis.

## What it is good for
- placeholder registry coverage
- incremental source collection
- ontology refinement

## Common misuse
- treating a starter entry as fully researched
"""

    resources = [
        {
            "id": resource_id,
            "instrument_id": instrument_id,
            "version_id": version_id,
            "resource_type": resource_type,
            "title": resource_title or f"{canonical_name} overview source",
            "url": resource_url or f"https://example.org/{slug}",
            "author": resource_author,
            "publication_date": resource_publication_date,
            "publisher": resource_publisher,
            "language": resource_language,
            "access_status": resource_access_status,
            "officiality": resource_officiality,
            "notes": resource_notes,
        }
    ]
    for extra_resource in extra_resources or []:
        resources.append(
            {
                "instrument_id": instrument_id,
                "version_id": version_id,
                "language": resource_language,
                "access_status": resource_access_status,
                **extra_resource,
            }
        )

    constructs: list[dict[str, Any]] = []
    if include_primary_construct:
        constructs.append(
            {
                "id": construct_id,
                "instrument_id": instrument_id,
                "version_ids": [version_id],
                "name": construct_name,
                "short_name": construct_short_name or construct_name,
                "construct_kind": construct_kind or ["dimension"],
                "official_definition": construct_definition,
                "scoring_type": scoring_type,
                "polarity": {"low_label": None, "high_label": None},
                "value_range": {"type": "variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
            }
        )
    for extra_construct in extra_constructs or []:
        constructs.append(
            {
                "instrument_id": instrument_id,
                "version_ids": [version_id],
                "short_name": None,
                "construct_kind": ["dimension"],
                "scoring_type": scoring_type,
                "polarity": {"low_label": None, "high_label": None},
                "value_range": {"type": "variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
                **extra_construct,
            }
        )

    claims = [
        {
            "id": claim_id,
            "instrument_id": instrument_id,
            "version_id": version_id,
            "claim_type": "overview_claim",
            "claim_text": claim_text,
            "source_resource_ids": [resource_id],
            "quotation_status": "paraphrase",
        }
    ]
    for extra_claim in extra_claims or []:
        claims.append(
            {
                "instrument_id": instrument_id,
                "version_id": version_id,
                "source_resource_ids": [resource_id],
                "quotation_status": "paraphrase",
                **extra_claim,
            }
        )

    inferences = [
        {
            "id": inference_id,
            "target_entity_type": "instrument",
            "target_entity_id": instrument_id,
            "inference_type": inference_type,
            "text": inference_text
            or (
                f"{canonical_name} is included as a starter entry to preserve coverage across the instrument "
                "landscape while deeper source curation is still underway."
            ),
            "confidence": inference_confidence,
            "linked_entities": [],
            "author": "house",
            "timestamp": "2026-04-11",
        }
    ]
    for extra_inference in extra_inferences or []:
        inferences.append(
            {
                "target_entity_type": "instrument",
                "target_entity_id": instrument_id,
                "linked_entities": [],
                "author": "house",
                "timestamp": "2026-04-11",
                **extra_inference,
            }
        )

    risks = [
        {
            "id": risk_id,
            "instrument_id": instrument_id,
            "risk_type": risk_type,
            "severity": risk_severity,
            "description": risk_description,
            "mitigation": risk_mitigation,
        }
    ]
    for extra_risk in extra_risks or []:
        risks.append(
            {
                "instrument_id": instrument_id,
                **extra_risk,
            }
        )

    use_cases = [
        {
            "id": use_case_id,
            "instrument_id": instrument_id,
            "use_context": use_context,
            "utility_type": utility_type,
            "suitability_level": suitability_level,
            "cautions": cautions,
        }
    ]
    for extra_use_case in extra_use_cases or []:
        use_cases.append(
            {
                "instrument_id": instrument_id,
                **extra_use_case,
            }
        )

    return {
        "instrument.yaml": {
            "instrument": {
                "id": instrument_id,
                "canonical_name": canonical_name,
                "short_names": short_names or [],
                "aliases": aliases or [],
                "status": "active",
                "family": families,
                "short_description": short_description,
                "creators": creators or ["unknown"],
                "publisher_or_owner": publisher_or_owner,
                "original_release_year": original_release_year,
                "official_websites": official_websites or [],
                "licensing_model": licensing_model,
                "primary_domain": primary_domain,
                "country_or_origin_context": country_or_origin_context or ["mixed"],
                "notes": instrument_notes or f"Starter registry entry for {canonical_name}.",
            }
        },
        "versions.yaml": {
            "versions": [
                {
                    "id": version_id,
                    "instrument_id": instrument_id,
                    "version_label": "general_family_record",
                    "release_date": None,
                    "retired_date": None,
                    "current": True,
                    "change_summary": "Canonical general record for this instrument in the registry.",
                    "scoring_changes": None,
                    "construct_changes": None,
                    "norming_changes": None,
                    "administration_changes": None,
                }
            ]
        },
        "constructs.yaml": {"constructs": constructs},
        "claims.yaml": {"claims": claims},
        "resources.yaml": {"resources": resources},
        "annotations.yaml": {"annotations": annotations},
        "inferences.yaml": {"inferences": inferences},
        "crosswalks.yaml": {"crosswalks": crosswalks or []},
        "risks.yaml": {"risks": risks},
        "use_cases.yaml": {"use_cases": use_cases},
        "notes.md": note_text,
    }


BIG_FIVE_BUNDLE = {
    "instrument.yaml": {
        "instrument": {
            "id": "instr_big_five",
            "canonical_name": "Big Five Personality Model",
            "short_names": ["Big Five", "OCEAN", "Five-Factor Model"],
            "aliases": ["FFM"],
            "status": "active",
            "family": ["trait_personality"],
            "short_description": (
                "A dimensional trait personality framework typically organized around "
                "Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism."
            ),
            "creators": ["Lewis Goldberg", "multiple_contributors"],
            "publisher_or_owner": "none_decentralized",
            "original_release_year": 1981,
            "official_websites": [None],
            "licensing_model": "mixed_public_and_proprietary_variants",
            "primary_domain": "personality_trait_model",
            "country_or_origin_context": ["united_states"],
            "notes": (
                "This entry refers to the general Big Five / Five-Factor Model family rather "
                "than a single proprietary questionnaire instance."
            ),
        }
    },
    "versions.yaml": {
        "versions": [
            {
                "id": "ver_big_five_general",
                "instrument_id": "instr_big_five",
                "version_label": "general_family_record",
                "release_date": None,
                "retired_date": None,
                "current": True,
                "change_summary": "Generic umbrella record representing the broader Big Five family.",
                "scoring_changes": None,
                "construct_changes": None,
                "norming_changes": None,
                "administration_changes": None,
            },
            {
                "id": "ver_big_five_ipip_50",
                "instrument_id": "instr_big_five",
                "version_label": "IPIP_50_item_variant",
                "release_date": None,
                "retired_date": None,
                "current": True,
                "change_summary": "Common open-access short-form implementation.",
                "scoring_changes": "shorter_item_set",
                "construct_changes": "same_top_level_constructs",
                "norming_changes": "variant_specific",
                "administration_changes": "self_report_questionnaire",
            },
        ]
    },
    "constructs.yaml": {
        "constructs": [
            {
                "id": "con_big_five_openness",
                "instrument_id": "instr_big_five",
                "version_ids": ["ver_big_five_general", "ver_big_five_ipip_50"],
                "name": "Openness to Experience",
                "short_name": "Openness",
                "construct_kind": ["trait", "dimension"],
                "official_definition": (
                    "Broad tendency toward imagination, curiosity, aesthetic sensitivity, "
                    "intellectual exploration, and preference for novelty and complexity."
                ),
                "scoring_type": "continuous",
                "polarity": {"low_label": "low_openness", "high_label": "high_openness"},
                "value_range": {"type": "instrument_variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_big_five_conscientiousness",
                "instrument_id": "instr_big_five",
                "version_ids": ["ver_big_five_general", "ver_big_five_ipip_50"],
                "name": "Conscientiousness",
                "short_name": "Conscientiousness",
                "construct_kind": ["trait", "dimension"],
                "official_definition": (
                    "Broad tendency toward organization, self-discipline, reliability, and "
                    "goal-directed behavior."
                ),
                "scoring_type": "continuous",
                "polarity": {
                    "low_label": "low_conscientiousness",
                    "high_label": "high_conscientiousness",
                },
                "value_range": {"type": "instrument_variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_big_five_extraversion",
                "instrument_id": "instr_big_five",
                "version_ids": ["ver_big_five_general", "ver_big_five_ipip_50"],
                "name": "Extraversion",
                "short_name": "Extraversion",
                "construct_kind": ["trait", "dimension"],
                "official_definition": (
                    "Broad tendency toward sociability, energetic engagement, positive affect, "
                    "and stimulation seeking."
                ),
                "scoring_type": "continuous",
                "polarity": {"low_label": "low_extraversion", "high_label": "high_extraversion"},
                "value_range": {"type": "instrument_variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_big_five_agreeableness",
                "instrument_id": "instr_big_five",
                "version_ids": ["ver_big_five_general", "ver_big_five_ipip_50"],
                "name": "Agreeableness",
                "short_name": "Agreeableness",
                "construct_kind": ["trait", "dimension"],
                "official_definition": (
                    "Broad tendency toward compassion, cooperation, trust, and concern for social harmony."
                ),
                "scoring_type": "continuous",
                "polarity": {"low_label": "low_agreeableness", "high_label": "high_agreeableness"},
                "value_range": {"type": "instrument_variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_big_five_neuroticism",
                "instrument_id": "instr_big_five",
                "version_ids": ["ver_big_five_general", "ver_big_five_ipip_50"],
                "name": "Neuroticism",
                "short_name": "Neuroticism",
                "construct_kind": ["trait", "dimension"],
                "official_definition": (
                    "Broad tendency toward emotional volatility, stress reactivity, negative affect, and vulnerability."
                ),
                "scoring_type": "continuous",
                "polarity": {"low_label": "low_neuroticism", "high_label": "high_neuroticism"},
                "value_range": {"type": "instrument_variant_dependent", "min": None, "max": None},
                "parent_construct_id": None,
            },
        ]
    },
    "claims.yaml": {
        "claims": [
            {
                "id": "clm_big_five_describes_five_broad_traits",
                "instrument_id": "instr_big_five",
                "version_id": "ver_big_five_general",
                "claim_type": "construct_claim",
                "claim_text": "The model organizes personality variation into five broad trait domains.",
                "source_resource_ids": ["res_big_five_summary_source"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_big_five_trait_stability",
                "instrument_id": "instr_big_five",
                "version_id": "ver_big_five_general",
                "claim_type": "temporal_claim",
                "claim_text": (
                    "The framework is intended to describe relatively stable personality traits "
                    "rather than momentary emotional states."
                ),
                "source_resource_ids": ["res_big_five_summary_source"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_big_five_variant_ecosystem",
                "instrument_id": "instr_big_five",
                "version_id": "ver_big_five_ipip_50",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "The Big Five exists as a family of instruments with multiple public and proprietary implementations."
                ),
                "source_resource_ids": ["res_big_five_ipip"],
                "quotation_status": "paraphrase",
            },
        ]
    },
    "resources.yaml": {
        "resources": [
            {
                "id": "res_big_five_reference",
                "instrument_id": "instr_big_five",
                "version_id": "ver_big_five_general",
                "resource_type": "citation_guide",
                "title": "Citing IPIP Scales in Scientific Publications",
                "url": "https://www.ipip.ori.org/newCitation.htm",
                "author": "Lewis R. Goldberg",
                "publication_date": None,
                "publisher": "Oregon Research Institute",
                "language": "en",
                "access_status": "public",
                "officiality": "official",
                "notes": (
                    "Official IPIP citation guidance page linking the public-domain item pool to Goldberg (1992) "
                    "and Goldberg et al. (2006)."
                ),
            },
            {
                "id": "res_big_five_summary_source",
                "instrument_id": "instr_big_five",
                "version_id": "ver_big_five_general",
                "resource_type": "scoring_key",
                "title": "Big-Five Factor Markers",
                "url": "https://ipip.ori.org/newBigFive5broadKey.htm",
                "author": "Lewis R. Goldberg",
                "publication_date": None,
                "publisher": "Oregon Research Institute",
                "language": "en",
                "access_status": "public",
                "officiality": "semi_official",
                "notes": (
                    "IPIP page for the 50-item and 100-item Big-Five factor marker representations used as a public-domain "
                    "implementation of broad Big Five domains."
                ),
            },
            {
                "id": "res_big_five_ipip",
                "instrument_id": "instr_big_five",
                "version_id": "ver_big_five_ipip_50",
                "resource_type": "questionnaire_repository",
                "title": "International Personality Item Pool",
                "url": "https://ipip.ori.org/index.htm",
                "author": "Lewis R. Goldberg",
                "publication_date": None,
                "publisher": "Oregon Research Institute",
                "language": "en",
                "access_status": "public",
                "officiality": "official",
                "notes": (
                    "Official IPIP site describing the public-domain item pool and open-use terms for personality scales."
                ),
            },
        ]
    },
    "annotations.yaml": {
        "annotations": _build_annotations(
            base="big_five",
            canonical_name="Big Five Personality Model",
            instrument_id="instr_big_five",
            resource_id="res_big_five_reference",
            values_by_dimension={
                "instrument_family": ["trait_personality"],
                "primary_measurement_target": [
                    "stable_traits",
                    "interpersonal_style",
                    "affect_emotion",
                    "work_style",
                ],
                "representational_form": ["continuous_dimensional", "hierarchical_model"],
                "temporal_stance": ["stable_traits"],
                "person_ontology": ["trait_container"],
                "administration_mode": ["self_report_questionnaire", "observer_report"],
                "scoring_logic": ["sum_or_average_scale_scoring", "factor_scoring"],
                "epistemic_basis": ["strong_psychometric_validation"],
                "evidence_profile": [
                    "extensive_peer_review",
                    "normative_data_available",
                    "cross_cultural_support",
                ],
                "interpretive_burden": ["low"],
                "granularity": ["high"],
                "context_sensitivity": ["medium"],
                "change_model": ["trait_stability", "situational_expression", "developmental_growth"],
                "distortion_risk": ["self_report_distortion", "overinterpretation", "reductionism"],
                "deployment_context": ["self_reflection", "research", "workplace", "coaching", "team_design"],
                "utility_profile": ["self_understanding", "research_baseline", "communication_adaptation"],
                "target_population": ["general_adult_population", "workplace_teams"],
                "norming_status": ["variant_dependent"],
                "identity_adhesion_risk": ["low"],
                "actionability_type": ["descriptive_reflection", "communication_adjustment"],
                "worldview_load": ["very_low"],
                "cultural_symbolic_role": ["research_anchor", "professional_shorthand"],
                "synthesis_value_for_ilens": ["very_high"],
                "overlap_mode": ["partial_construct_overlap", "complementary_layers"],
            },
            status_by_dimension={
                "instrument_family": "explicit",
                "primary_measurement_target": "inferred",
                "representational_form": "inferred",
                "epistemic_basis": "inferred",
            },
            confidence_by_dimension={
                "instrument_family": "high",
                "primary_measurement_target": "high",
                "representational_form": "medium",
                "temporal_stance": "high",
                "person_ontology": "high",
                "administration_mode": "high",
                "scoring_logic": "high",
                "epistemic_basis": "high",
                "evidence_profile": "high",
                "interpretive_burden": "high",
                "granularity": "medium",
                "context_sensitivity": "medium",
                "change_model": "medium",
                "distortion_risk": "high",
                "deployment_context": "high",
                "utility_profile": "high",
                "identity_adhesion_risk": "medium",
                "worldview_load": "high",
                "synthesis_value_for_ilens": "high",
                "overlap_mode": "medium",
            },
            rationale_by_dimension={
                "instrument_family": "The Big Five is explicitly a trait personality framework.",
                "primary_measurement_target": (
                    "The model is trait-centered, but trait domains also bear on emotionality, "
                    "interpersonal style, and work-related behavior."
                ),
                "representational_form": (
                    "Most Big Five implementations are continuous dimensional models and many also organize "
                    "facets beneath broader domains."
                ),
                "temporal_stance": "The framework is designed to describe comparatively stable trait patterns.",
                "person_ontology": "The model treats the person primarily as a profile of broad dispositional traits.",
                "administration_mode": "Big Five instruments commonly use self-report and sometimes observer report.",
                "scoring_logic": "Questionnaire responses typically become continuous factor or scale scores.",
                "epistemic_basis": (
                    "Relative to many adjacent systems, the Big Five has a strong psychometric validation base."
                ),
                "interpretive_burden": "Interpretation is comparatively direct because the output model is trait-based.",
                "granularity": "The framework is broad at the top level but often enriched by facet-level resolution.",
                "context_sensitivity": (
                    "The model aims for cross-situational traits, but expression still varies with role and context."
                ),
                "change_model": "Trait stability is primary, but developmental and situational changes are still relevant.",
                "distortion_risk": (
                    "Self-report bias and overreading broad traits are persistent hazards in practical use."
                ),
                "deployment_context": "The Big Five is used across research, coaching, workplace, and self-reflection contexts.",
                "utility_profile": (
                    "Its strongest uses are baseline trait description, comparison, and synthesis anchoring."
                ),
                "identity_adhesion_risk": (
                    "The Big Five is less identity-sticky than more typological or symbolic systems."
                ),
                "worldview_load": "It carries relatively little metaphysical or worldview baggage.",
                "synthesis_value_for_ilens": (
                    "Big Five is an unusually strong baseline anchor for synthesis because it offers stable broad scaffolding."
                ),
                "overlap_mode": (
                    "Overlap with other systems is often partial or complementary rather than directly translatable."
                ),
            },
        )
    },
    "inferences.yaml": {
        "inferences": [
            {
                "id": "inf_big_five_foundational_anchor",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_big_five",
                "inference_type": "synthesis_position",
                "text": (
                    "Big Five is one of the best baseline anchor frameworks for a synthesis system because "
                    "it supplies relatively stable broad trait scaffolding without imposing a thick symbolic identity narrative."
                ),
                "confidence": "high",
                "linked_entities": ["instr_mbti", "instr_enneagram"],
                "author": "house",
                "timestamp": "2026-04-11",
            },
            {
                "id": "inf_big_five_limitations",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_big_five",
                "inference_type": "practical_limit",
                "text": (
                    "Big Five is weaker as a direct language of motive, defense strategy, or identity narrative "
                    "than systems like Enneagram, despite being stronger in psychometric grounding."
                ),
                "confidence": "high",
                "linked_entities": ["instr_enneagram"],
                "author": "house",
                "timestamp": "2026-04-11",
            },
        ]
    },
    "crosswalks.yaml": {
        "crosswalks": [
            {
                "id": "xwk_big_five_openness_mbti_intuition",
                "source_entity_type": "construct",
                "source_entity_id": "con_big_five_openness",
                "target_entity_type": "construct",
                "target_entity_id": "con_mbti_sensing_intuition",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "High openness often overlaps with constructs culturally associated with MBTI intuition, "
                    "but the mapping is partial and non-equivalent."
                ),
                "confidence": "medium",
                "notes": "This is not a one-to-one translation and should not be represented as such.",
            },
            {
                "id": "xwk_big_five_neuroticism_enneagram_reactivity",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_big_five",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_enneagram",
                "relationship_type": "complementary_non_equivalent",
                "relationship_strength": "medium",
                "rationale": (
                    "Big Five and Enneagram both capture meaningful aspects of emotional and behavioral patterning, "
                    "but they operate at different descriptive levels."
                ),
                "confidence": "medium",
                "notes": None,
            },
        ]
    },
    "risks.yaml": {
        "risks": [
            {
                "id": "rsk_big_five_self_report_distortion",
                "instrument_id": "instr_big_five",
                "risk_type": "self_report_distortion",
                "severity": "medium",
                "description": (
                    "Results can be affected by social desirability, self-deception, mood, or role-based answering."
                ),
                "mitigation": (
                    "Prefer repeated administration, observer reports, or triangulation with other evidence sources when possible."
                ),
            },
            {
                "id": "rsk_big_five_overinterpretation",
                "instrument_id": "instr_big_five",
                "risk_type": "overinterpretation",
                "severity": "medium",
                "description": (
                    "Broad trait scores are often treated as total explanations of a person, obscuring context, motive, and narrative structure."
                ),
                "mitigation": "Position Big Five as a baseline layer rather than a total person-model.",
            },
        ]
    },
    "use_cases.yaml": {
        "use_cases": [
            {
                "id": "use_big_five_self_reflection",
                "instrument_id": "instr_big_five",
                "use_context": "self_reflection",
                "utility_type": "self_understanding",
                "suitability_level": "high",
                "cautions": "Best used as broad descriptive scaffolding, not destiny language.",
            },
            {
                "id": "use_big_five_team_design",
                "instrument_id": "instr_big_five",
                "use_context": "team_design",
                "utility_type": "communication_adaptation",
                "suitability_level": "medium",
                "cautions": "Should not be used as the sole basis for team role assignment.",
            },
        ]
    },
    "notes.md": """# Big Five Personality Model

## What it is
A broad trait framework organizing personality variation into five major domains.

## Why it matters
In this registry, Big Five functions as one of the strongest empirical anchor layers for synthesis work. It is less thick as an identity language than systems like Enneagram or Human Design, but stronger as a baseline trait scaffold.

## What it is good for
- broad personality description
- baseline trait comparison
- self-reflection
- communication and work-style inference
- synthesis anchoring

## What it is weaker at
- motive language
- identity narrative
- defense strategy
- symbolic meaning
- thick developmental storytelling

## Common misuse
Treating broad traits as a total explanation of a person.
""",
}


ENNEAGRAM_BUNDLE = {
    "instrument.yaml": {
        "instrument": {
            "id": "instr_enneagram",
            "canonical_name": "Enneagram of Personality",
            "short_names": ["Enneagram"],
            "aliases": ["Enneagram of Personality Types"],
            "status": "active",
            "family": ["typology", "motivational", "identity_self_concept", "worldview_meaning_making"],
            "short_description": (
                "A typological framework centered on nine core personality strategies often described in terms "
                "of motivation, fear, desire, fixation, defense, and growth/stress patterns."
            ),
            "creators": ["multiple_historical_lineages"],
            "publisher_or_owner": "decentralized",
            "original_release_year": None,
            "official_websites": [],
            "licensing_model": "decentralized",
            "primary_domain": "personality_typology",
            "country_or_origin_context": ["mixed"],
            "notes": (
                "This record represents the broader Enneagram ecosystem rather than a single publisher-specific assessment."
            ),
        }
    },
    "versions.yaml": {
        "versions": [
            {
                "id": "ver_enneagram_general",
                "instrument_id": "instr_enneagram",
                "version_label": "general_family_record",
                "release_date": None,
                "retired_date": None,
                "current": True,
                "change_summary": "Umbrella record for the broader Enneagram ecosystem.",
                "scoring_changes": None,
                "construct_changes": None,
                "norming_changes": None,
                "administration_changes": "self_identification_and_practitioner_guidance",
            }
        ]
    },
    "constructs.yaml": {
        "constructs": [
                {
                    "id": "con_enneagram_type_one",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type One",
                    "short_name": "One",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "A reform-oriented strategy organized around restraint, improvement, and correctness.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_two",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Two",
                    "short_name": "Two",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "A relationship-oriented strategy organized around helpfulness, approval, and connection.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_three",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Three",
                    "short_name": "Three",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "An achievement-oriented strategy organized around performance, image, and adaptation.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_four",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Four",
                    "short_name": "Four",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "An identity-oriented strategy organized around depth, uniqueness, and longing.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_five",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Five",
                    "short_name": "Five",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "A withdrawal-oriented strategy organized around competence, privacy, and cognitive mastery.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_six",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Six",
                    "short_name": "Six",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "A security-oriented strategy organized around vigilance, loyalty, and threat management.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_seven",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Seven",
                    "short_name": "Seven",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "An expansive strategy organized around possibility, stimulation, and avoidance of constriction.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_eight",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Eight",
                    "short_name": "Eight",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "A force-oriented strategy organized around autonomy, intensity, and resistance to control.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
                {
                    "id": "con_enneagram_type_nine",
                    "instrument_id": "instr_enneagram",
                    "version_ids": ["ver_enneagram_general"],
                    "name": "Type Nine",
                    "short_name": "Nine",
                    "construct_kind": ["type", "motivation"],
                    "official_definition": "A harmony-oriented strategy organized around stability, merger, and conflict minimization.",
                    "scoring_type": "categorical_or_best_fit",
                    "polarity": {"low_label": None, "high_label": None},
                    "value_range": {"type": "categorical_typology", "min": None, "max": None},
                    "parent_construct_id": None,
                },
            ]
    },
    "claims.yaml": {
        "claims": [
            {
                "id": "clm_enneagram_nine_core_types",
                "instrument_id": "instr_enneagram",
                "version_id": "ver_enneagram_general",
                "claim_type": "construct_claim",
                "claim_text": "The system describes nine core personality strategies or types.",
                "source_resource_ids": ["res_enneagram_overview"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_enneagram_motivational_core",
                "instrument_id": "instr_enneagram",
                "version_id": "ver_enneagram_general",
                "claim_type": "motivational_claim",
                "claim_text": (
                    "Type descriptions are commonly framed through core motivations, fears, desires, and defensive patterns."
                ),
                "source_resource_ids": ["res_enneagram_overview"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_enneagram_growth_stress",
                "instrument_id": "instr_enneagram",
                "version_id": "ver_enneagram_general",
                "claim_type": "developmental_claim",
                "claim_text": (
                    "The framework often claims that each type has characteristic growth and stress dynamics."
                ),
                "source_resource_ids": ["res_enneagram_riso_hudson"],
                "quotation_status": "paraphrase",
            },
        ]
    },
    "resources.yaml": {
        "resources": [
            {
                "id": "res_enneagram_overview",
                "instrument_id": "instr_enneagram",
                "version_id": "ver_enneagram_general",
                "resource_type": "type_descriptions",
                "title": "The Nine Enneagram Type Descriptions",
                "url": "https://www.enneagraminstitute.com/type-descriptions/",
                "author": None,
                "publication_date": None,
                "publisher": "The Enneagram Institute",
                "language": "en",
                "access_status": "public",
                "officiality": "semi_official",
                "notes": (
                    "Lineage-specific Enneagram Institute overview page summarizing the nine type descriptions."
                ),
            },
            {
                "id": "res_enneagram_riso_hudson",
                "instrument_id": "instr_enneagram",
                "version_id": "ver_enneagram_general",
                "resource_type": "overview",
                "title": "How the Enneagram System Works",
                "url": "https://www.enneagraminstitute.com/how-the-enneagram-system-works/",
                "author": None,
                "publication_date": None,
                "publisher": "The Enneagram Institute",
                "language": "en",
                "access_status": "public",
                "officiality": "semi_official",
                "notes": (
                    "Lineage-specific overview covering nine basic types, wings, developmental levels, and growth/stress directions."
                ),
            },
        ]
    },
    "annotations.yaml": {
        "annotations": _build_annotations(
            base="enneagram",
            canonical_name="Enneagram of Personality",
            instrument_id="instr_enneagram",
            resource_id="res_enneagram_overview",
            values_by_dimension={
                "instrument_family": [
                    "typology",
                    "motivational",
                    "identity_self_concept",
                    "worldview_meaning_making",
                ],
                "primary_measurement_target": [
                    "motivation_drives",
                    "defense_patterns",
                    "identity_narrative",
                    "interpersonal_style",
                ],
                "representational_form": [
                    "categorical_typology",
                    "hybrid_dimensional_typological",
                    "narrative_description",
                    "developmental_level",
                ],
                "temporal_stance": ["semi_stable_patterns", "developmental_path"],
                "person_ontology": ["dynamic_strategy_system", "motivational_structure"],
                "administration_mode": ["self_identification", "practitioner_interview", "workshop_facilitation"],
                "scoring_logic": ["type_assignment_rules", "interpretive_pattern_matching", "expert_interpretation"],
                "epistemic_basis": [
                    "mixed_lineages",
                    "narrative_interpretation",
                    "weak_or_contested_empirical_basis",
                ],
                "evidence_profile": ["mostly_anecdotal_or_practitioner_based", "contested_validity"],
                "interpretive_burden": ["high"],
                "granularity": ["high"],
                "context_sensitivity": ["high"],
                "change_model": ["developmental_growth", "subtype_refinement", "identity_revision"],
                "distortion_risk": ["identity_capture", "practitioner_projection", "overinterpretation", "confirmation_bias"],
                "deployment_context": ["coaching", "self_reflection", "therapy", "spiritual_community", "internet_identity_culture"],
                "utility_profile": ["motive_exploration", "developmental_reflection", "coaching_language", "relational_patterning"],
                "target_population": ["general_adult_population", "coaching_clients", "spiritual_seekers"],
                "norming_status": ["limited_norms"],
                "identity_adhesion_risk": ["very_high"],
                "actionability_type": ["developmental_planning", "relational_discussion"],
                "worldview_load": ["high"],
                "cultural_symbolic_role": [
                    "coaching_identity_language",
                    "community_belonging_language",
                    "internet_identity_language",
                ],
                "synthesis_value_for_ilens": ["high"],
                "overlap_mode": ["shared_identity_space", "complementary_layers"],
            },
            confidence_by_dimension={
                "instrument_family": "high",
                "primary_measurement_target": "high",
                "representational_form": "high",
                "temporal_stance": "medium",
                "person_ontology": "high",
                "administration_mode": "high",
                "scoring_logic": "high",
                "epistemic_basis": "medium",
                "evidence_profile": "medium",
                "interpretive_burden": "high",
                "granularity": "high",
                "context_sensitivity": "high",
                "change_model": "medium",
                "distortion_risk": "high",
                "deployment_context": "high",
                "utility_profile": "high",
                "norming_status": "medium",
                "identity_adhesion_risk": "high",
                "worldview_load": "high",
                "synthesis_value_for_ilens": "medium",
                "overlap_mode": "medium",
            },
            rationale_by_dimension={
                "instrument_family": (
                    "The Enneagram is widely used as a typological and motivational system and often functions as an identity and meaning-making language."
                ),
                "representational_form": (
                    "The system is type-based but often includes wings, instincts, and developmental levels."
                ),
                "interpretive_burden": (
                    "Meaning often depends heavily on practitioner sophistication, user self-identification, and interpretive context."
                ),
                "identity_adhesion_risk": (
                    "Users frequently fuse with type identity or use type language as a durable self-narration frame."
                ),
                "epistemic_basis": (
                    "The Enneagram draws from mixed lineages and interpretive traditions and remains empirically contested."
                ),
                "synthesis_value_for_ilens": (
                    "The Enneagram is useful when motive, defense, and identity language matter, but it should not be treated as a psychometric anchor."
                ),
            },
        )
    },
    "inferences.yaml": {
        "inferences": [
            {
                "id": "inf_enneagram_motive_depth",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_enneagram",
                "inference_type": "comparative_strength",
                "text": (
                    "Enneagram is comparatively strong as a language of motive, defense strategy, and identity narrative even where psychometric grounding remains weak."
                ),
                "confidence": "high",
                "linked_entities": ["instr_big_five"],
                "author": "house",
                "timestamp": "2026-04-11",
            },
            {
                "id": "inf_enneagram_identity_risk",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_enneagram",
                "inference_type": "practical_risk",
                "text": (
                    "Its practical power is partly social and narrative, which also makes it unusually prone to identity capture and practitioner overreach."
                ),
                "confidence": "high",
                "linked_entities": [],
                "author": "house",
                "timestamp": "2026-04-11",
            },
        ]
    },
    "crosswalks.yaml": {
        "crosswalks": [
            {
                "id": "xwk_enneagram_big_five_person_layer",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_enneagram",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_big_five",
                "relationship_type": "different_layer_of_personhood",
                "relationship_strength": "high",
                "rationale": (
                    "Enneagram organizes motive, fixation, and identity strategy, while Big Five organizes broad trait variance. "
                    "They often complement each other in practice but do not describe the same layer of personhood."
                ),
                "confidence": "high",
                "notes": "House comparative mapping between motivational typology and broad trait scaffolding.",
            }
        ]
    },
    "risks.yaml": {
        "risks": [
            {
                "id": "rsk_enneagram_identity_capture",
                "instrument_id": "instr_enneagram",
                "risk_type": "identity_capture",
                "severity": "high",
                "description": (
                    "Users may fuse with a type identity and treat it as destiny, justification, or a durable self-explanation."
                ),
                "mitigation": "Frame type as a working hypothesis and revisit fit over time.",
            },
            {
                "id": "rsk_enneagram_practitioner_projection",
                "instrument_id": "instr_enneagram",
                "risk_type": "practitioner_projection",
                "severity": "high",
                "description": (
                    "Interpretation can become highly dependent on coach or teacher style, leading to confident but weakly grounded typing."
                ),
                "mitigation": "Prefer transparent rationale, multiple indicators, and explicit uncertainty.",
            },
        ]
    },
    "use_cases.yaml": {
        "use_cases": [
            {
                "id": "use_enneagram_self_reflection",
                "instrument_id": "instr_enneagram",
                "use_context": "self_reflection",
                "utility_type": "motive_exploration",
                "suitability_level": "high",
                "cautions": "Most useful when treated as exploratory language rather than fixed identity truth.",
            },
            {
                "id": "use_enneagram_coaching",
                "instrument_id": "instr_enneagram",
                "use_context": "coaching",
                "utility_type": "developmental_reflection",
                "suitability_level": "medium",
                "cautions": "Outcome quality varies sharply with practitioner rigor.",
            },
        ]
    },
    "notes.md": """# Enneagram of Personality

## What it is
A typological framework organized around nine core strategies often described through motives, fears, desires, and defenses.

## Why it matters
In this registry, Enneagram is valuable because it captures identity and motive language that many more psychometric frameworks describe only indirectly. It is also a strong example of a system that is culturally sticky despite a weaker evidence base.

## What it is good for
- motive exploration
- coaching language
- developmental reflection
- relational patterning
- identity narrative analysis

## What it is weaker at
- psychometric grounding
- standardized measurement
- low-interpretation administration
- clean construct commensurability

## Common misuse
Using type as destiny language or as an overconfident total explanation of the person.
""",
}


MBTI_BUNDLE = {
    "instrument.yaml": {
        "instrument": {
            "id": "instr_mbti",
            "canonical_name": "Myers-Briggs Type Indicator",
            "short_names": ["MBTI"],
            "aliases": ["Myers Briggs"],
            "status": "active",
            "family": ["typology", "cognitive_style", "identity_self_concept"],
            "short_description": (
                "A widely used typology framework built around four preference pairs that combine into sixteen type codes."
            ),
            "creators": ["Katherine Cook Briggs", "Isabel Briggs Myers"],
            "publisher_or_owner": "licensed_publishers",
            "original_release_year": 1943,
            "official_websites": [],
            "licensing_model": "proprietary",
            "primary_domain": "personality_typology",
            "country_or_origin_context": ["united_states"],
            "notes": (
                "This entry covers the broader MBTI ecosystem, not just a single publisher manual or training pathway."
            ),
        }
    },
    "versions.yaml": {
        "versions": [
            {
                "id": "ver_mbti_general",
                "instrument_id": "instr_mbti",
                "version_label": "general_family_record",
                "release_date": None,
                "retired_date": None,
                "current": True,
                "change_summary": "Umbrella record for the broader MBTI family.",
                "scoring_changes": None,
                "construct_changes": None,
                "norming_changes": None,
                "administration_changes": None,
            },
            {
                "id": "ver_mbti_step_i",
                "instrument_id": "instr_mbti",
                "version_label": "Step_I",
                "release_date": None,
                "retired_date": None,
                "current": True,
                "change_summary": "Representative step-based version for standard type assignment.",
                "scoring_changes": "preference_pair_scoring",
                "construct_changes": "four_preference_pairs",
                "norming_changes": "variant_specific",
                "administration_changes": "self_report_questionnaire",
            },
        ]
    },
    "constructs.yaml": {
        "constructs": [
            {
                "id": "con_mbti_extraversion_introversion",
                "instrument_id": "instr_mbti",
                "version_ids": ["ver_mbti_general", "ver_mbti_step_i"],
                "name": "Extraversion / Introversion",
                "short_name": "E/I",
                "construct_kind": ["preference_pair", "dimension"],
                "official_definition": "A preference pair describing orientation toward outer engagement or inner reflection.",
                "scoring_type": "bipolar_preference",
                "polarity": {"low_label": "introversion", "high_label": "extraversion"},
                "value_range": {"type": "preference_pair", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_mbti_sensing_intuition",
                "instrument_id": "instr_mbti",
                "version_ids": ["ver_mbti_general", "ver_mbti_step_i"],
                "name": "Sensing / Intuition",
                "short_name": "S/N",
                "construct_kind": ["preference_pair", "dimension"],
                "official_definition": "A preference pair describing attention to concrete detail or pattern-level possibility.",
                "scoring_type": "bipolar_preference",
                "polarity": {"low_label": "sensing", "high_label": "intuition"},
                "value_range": {"type": "preference_pair", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_mbti_thinking_feeling",
                "instrument_id": "instr_mbti",
                "version_ids": ["ver_mbti_general", "ver_mbti_step_i"],
                "name": "Thinking / Feeling",
                "short_name": "T/F",
                "construct_kind": ["preference_pair", "dimension"],
                "official_definition": "A preference pair describing decision style in terms of impersonal analysis or value-based consideration.",
                "scoring_type": "bipolar_preference",
                "polarity": {"low_label": "feeling", "high_label": "thinking"},
                "value_range": {"type": "preference_pair", "min": None, "max": None},
                "parent_construct_id": None,
            },
            {
                "id": "con_mbti_judging_perceiving",
                "instrument_id": "instr_mbti",
                "version_ids": ["ver_mbti_general", "ver_mbti_step_i"],
                "name": "Judging / Perceiving",
                "short_name": "J/P",
                "construct_kind": ["preference_pair", "dimension"],
                "official_definition": "A preference pair describing preference for structure and closure or openness and spontaneity.",
                "scoring_type": "bipolar_preference",
                "polarity": {"low_label": "perceiving", "high_label": "judging"},
                "value_range": {"type": "preference_pair", "min": None, "max": None},
                "parent_construct_id": None,
            },
        ]
    },
    "claims.yaml": {
        "claims": [
            {
                "id": "clm_mbti_sixteen_types",
                "instrument_id": "instr_mbti",
                "version_id": "ver_mbti_general",
                "claim_type": "typology_claim",
                "claim_text": "The framework organizes people into sixteen type combinations based on four preference pairs.",
                "source_resource_ids": ["res_mbti_overview"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_mbti_preferences_not_abilities",
                "instrument_id": "instr_mbti",
                "version_id": "ver_mbti_general",
                "claim_type": "construct_claim",
                "claim_text": "Type outputs are commonly framed as preferences rather than measures of ability or skill.",
                "source_resource_ids": ["res_mbti_overview"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_mbti_jungian_basis",
                "instrument_id": "instr_mbti",
                "version_id": "ver_mbti_general",
                "claim_type": "theoretical_claim",
                "claim_text": "The system is presented as deriving from Jungian ideas about psychological type.",
                "source_resource_ids": ["res_mbti_manual"],
                "quotation_status": "paraphrase",
            },
            {
                "id": "clm_mbti_not_for_hiring",
                "instrument_id": "instr_mbti",
                "version_id": "ver_mbti_general",
                "claim_type": "usage_claim",
                "claim_text": "The MBTI assessment is not intended for selection or hiring decisions.",
                "source_resource_ids": ["res_mbti_manual"],
                "quotation_status": "paraphrase",
            },
        ]
    },
    "resources.yaml": {
        "resources": [
            {
                "id": "res_mbti_overview",
                "instrument_id": "instr_mbti",
                "version_id": "ver_mbti_general",
                "resource_type": "overview",
                "title": "MBTI Assessment - Myers-Briggs Type Indicator Tool",
                "url": "https://www.themyersbriggs.com/en-US/Products-and-Services/Myers-Briggs",
                "author": None,
                "publication_date": None,
                "publisher": "The Myers-Briggs Company",
                "language": "en",
                "access_status": "public",
                "officiality": "official",
                "notes": "Official product overview page for the Myers-Briggs Type Indicator assessment.",
            },
            {
                "id": "res_mbti_manual",
                "instrument_id": "instr_mbti",
                "version_id": "ver_mbti_general",
                "resource_type": "faq",
                "title": "MBTI Facts",
                "url": "https://www.themyersbriggs.com/en-US/Support/MBTI-Facts",
                "author": None,
                "publication_date": "2020-04-24",
                "publisher": "The Myers-Briggs Company",
                "language": "en",
                "access_status": "public",
                "officiality": "official",
                "notes": (
                    "Official FAQ page covering MBTI history, intended uses, and explicit guidance against hiring use."
                ),
            },
        ]
    },
    "annotations.yaml": {
        "annotations": _build_annotations(
            base="mbti",
            canonical_name="Myers-Briggs Type Indicator",
            instrument_id="instr_mbti",
            resource_id="res_mbti_overview",
            values_by_dimension={
                "instrument_family": ["typology", "cognitive_style", "identity_self_concept"],
                "primary_measurement_target": [
                    "cognitive_preferences",
                    "interpersonal_style",
                    "work_style",
                    "communication_preferences",
                ],
                "representational_form": ["categorical_typology", "binary_preferences", "profile_vector"],
                "temporal_stance": ["semi_stable_patterns"],
                "person_ontology": ["hybrid_personhood_model", "work_behavior_pattern"],
                "administration_mode": ["self_report_questionnaire"],
                "scoring_logic": ["ipsative_preference_scoring", "type_assignment_rules"],
                "epistemic_basis": ["mixed_psychometric_and_theoretical"],
                "evidence_profile": ["mixed_evidence", "proprietary_or_limited_transparency", "contested_validity"],
                "interpretive_burden": ["medium"],
                "granularity": ["medium"],
                "context_sensitivity": ["medium"],
                "change_model": ["situational_expression", "identity_revision"],
                "distortion_risk": ["overinterpretation", "reification", "workplace_misuse", "self_report_distortion"],
                "deployment_context": ["workplace", "coaching", "self_reflection", "team_design", "leadership_development"],
                "utility_profile": ["communication_adaptation", "team_alignment", "self_understanding", "coaching_language"],
                "target_population": ["general_adult_population", "workplace_teams", "leaders_managers"],
                "norming_status": ["variant_dependent"],
                "identity_adhesion_risk": ["high"],
                "actionability_type": ["communication_adjustment", "team_design_support", "descriptive_reflection"],
                "worldview_load": ["medium"],
                "cultural_symbolic_role": [
                    "workplace_identity_language",
                    "pop_psychology_meme",
                    "professional_shorthand",
                ],
                "synthesis_value_for_ilens": ["medium"],
                "overlap_mode": ["often_misread_as_equivalent", "partial_construct_overlap"],
            },
            confidence_by_dimension={
                "instrument_family": "high",
                "primary_measurement_target": "medium",
                "representational_form": "high",
                "epistemic_basis": "medium",
                "evidence_profile": "medium",
                "distortion_risk": "high",
                "identity_adhesion_risk": "high",
            },
            rationale_by_dimension={
                "instrument_family": "MBTI is fundamentally a typology built around preference-based categories.",
                "representational_form": (
                    "The framework uses preference pairs that collapse into categorical type codes."
                ),
                "epistemic_basis": (
                    "MBTI combines questionnaire measurement with a strong theoretical inheritance and a contested evidence profile."
                ),
                "identity_adhesion_risk": (
                    "Users frequently adopt MBTI type as a durable social identity label."
                ),
                "overlap_mode": (
                    "MBTI is often loosely overlapped with trait models even when the underlying constructs are not equivalent."
                ),
            },
        )
    },
    "inferences.yaml": {
        "inferences": [
            {
                "id": "inf_mbti_shorthand_value",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_mbti",
                "inference_type": "practical_strength",
                "text": (
                    "MBTI persists because it offers an extremely portable social shorthand for communication and work-style differences."
                ),
                "confidence": "high",
                "linked_entities": ["instr_big_five"],
                "author": "house",
                "timestamp": "2026-04-11",
            },
            {
                "id": "inf_mbti_binary_limit",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_mbti",
                "inference_type": "practical_limit",
                "text": (
                    "Its type-coded outputs are often easier to remember than to justify, especially when they are treated as trait measures rather than interpretive preferences."
                ),
                "confidence": "high",
                "linked_entities": [],
                "author": "house",
                "timestamp": "2026-04-11",
            },
        ]
    },
    "crosswalks.yaml": {
        "crosswalks": [
            {
                "id": "xwk_mbti_intuition_big_five_openness",
                "source_entity_type": "construct",
                "source_entity_id": "con_mbti_sensing_intuition",
                "target_entity_type": "construct",
                "target_entity_id": "con_big_five_openness",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "MBTI intuition and Big Five openness often occupy nearby cultural territory, but they arise from different models and are not interchangeable."
                ),
                "confidence": "medium",
                "notes": "House comparison only; not an official translation.",
            }
        ]
    },
    "risks.yaml": {
        "risks": [
            {
                "id": "rsk_mbti_reification",
                "instrument_id": "instr_mbti",
                "risk_type": "reification",
                "severity": "high",
                "description": "Type codes can be reified into rigid identity boxes that obscure within-type variability.",
                "mitigation": "Treat type language as a conversational shorthand rather than a total explanatory model.",
            },
            {
                "id": "rsk_mbti_workplace_misuse",
                "instrument_id": "instr_mbti",
                "risk_type": "workplace_misuse",
                "severity": "medium",
                "description": "Organizations may overuse MBTI for role assignment, selection, or simplistic team narratives.",
                "mitigation": "Keep use limited to discussion and reflection rather than high-stakes decision making.",
            },
        ]
    },
    "use_cases.yaml": {
        "use_cases": [
            {
                "id": "use_mbti_team_design",
                "instrument_id": "instr_mbti",
                "use_context": "team_design",
                "utility_type": "communication_adaptation",
                "suitability_level": "medium",
                "cautions": "Useful as a discussion starter, weak as a personnel decision framework.",
            },
            {
                "id": "use_mbti_self_reflection",
                "instrument_id": "instr_mbti",
                "use_context": "self_reflection",
                "utility_type": "self_understanding",
                "suitability_level": "medium",
                "cautions": "Best treated as a preference-language heuristic rather than a fixed identity verdict.",
            },
        ]
    },
    "notes.md": """# Myers-Briggs Type Indicator

## What it is
A typological framework based on four preference pairs that combine into sixteen type codes.

## Why it matters
MBTI is culturally and organizationally important because it functions as a durable shorthand for personality difference, especially in workplace and coaching settings. Its practical stickiness matters even where evidence and construct commensurability remain contested.

## What it is good for
- communication shorthand
- lightweight team discussion
- reflective preference language
- coaching conversation

## What it is weaker at
- trait measurement
- clean construct comparability
- high-stakes decisions
- preserving nuance under binary labels

## Common misuse
Treating type as a hard box or using it for selection and assignment decisions.
""",
}


PLACEHOLDER_SPECS = [
    {
        "slug": "disc",
        "canonical_name": "DISC",
        "short_names": ["DISC"],
        "short_description": "A workplace-friendly behavioral style framework organized around four broad interaction styles.",
        "creators": ["William Moulton Marston", "multiple_commercial_publishers"],
        "publisher_or_owner": "multiple_commercial_publishers",
        "original_release_year": 1928,
        "licensing_model": "mixed_commercial_ecosystem",
        "country_or_origin_context": ["united_states"],
        "families": ["behavioral_interactional", "leadership_workplace"],
        "primary_measurement_target": ["behavioral_style", "interpersonal_style", "work_style"],
        "representational_form": ["profile_vector", "categorical_typology"],
        "temporal_stance": ["semi_stable_patterns"],
        "person_ontology": ["work_behavior_pattern"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["type_assignment_rules", "sum_or_average_scale_scoring"],
        "epistemic_basis": ["mixed_psychometric_and_theoretical", "proprietary_workplace_analytics"],
        "interpretive_burden": "medium",
        "granularity": "medium",
        "context_sensitivity": "medium",
        "change_model": ["situational_expression", "skills_trainability"],
        "distortion_risk": ["workplace_misuse", "overinterpretation"],
        "deployment_context": ["workplace", "team_design", "leadership_development", "coaching"],
        "utility_profile": ["communication_adaptation", "team_alignment"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "low",
        "synthesis_value_for_ilens": "medium",
        "evidence_profile": ["mixed_evidence", "proprietary_or_limited_transparency"],
        "target_population": ["workplace_teams", "leaders_managers"],
        "norming_status": "variant_dependent",
        "actionability_type": ["communication_adjustment", "team_design_support"],
        "cultural_symbolic_role": ["workplace_identity_language", "professional_shorthand"],
        "overlap_mode": ["workplace_family_resemblance"],
        "construct_name": "DISC style profile",
        "construct_definition": "Composite profile across dominance, influence, steadiness, and conscientiousness style dimensions.",
        "claim_text": (
            "DISC claims to describe observable behavior through four broad styles commonly labeled "
            "Dominance, Influence, Steadiness, and Conscientiousness."
        ),
        "resource_title": "About Everything DiSC",
        "resource_url": (
            "https://www.everythingdisc.com/EverythingDiSC/media/SiteFiles/Assets/History/"
            "Everything-DiSC-resources-aboutdisc.pdf"
        ),
        "resource_publisher": "Everything DiSC / John Wiley & Sons",
        "resource_officiality": "semi_official",
        "resource_notes": (
            "Modern commercial overview of the DiSC model and its four-style behavioral framing within the "
            "Everything DiSC product family."
        ),
        "inference_id_suffix": "workplace_shorthand",
        "inference_type": "practical_value",
        "inference_confidence": "high",
        "inference_text": (
            "DISC stays sticky in organizations because it offers a low-friction language for interpersonal style, "
            "even though the broader DISC ecosystem varies substantially in psychometric rigor and implementation."
        ),
        "risk_description": "DISC profiles are easy to overuse as simplified workplace identity boxes.",
        "cautions": "Useful for team language, weak for total personality explanation.",
        "instrument_notes": (
            "This entry refers to the broader DISC family rather than a single publisher-specific implementation."
        ),
        "notes": """# DISC

## What it is
A behavioral style family organized around four broad style labels: Dominance, Influence, Steadiness, and Conscientiousness.

## Why it matters
DISC matters because it remains one of the most portable workplace personality languages. It is easy to teach, easy to remember, and widely used in training and team settings, even though the broader DISC ecosystem is fragmented across implementations.

## What it is good for
- communication shorthand
- workplace training
- team discussion
- lightweight behavioral style reflection

## What it is weaker at
- deep motive language
- construct precision across vendors
- high-stakes personnel decisions
- whole-person modeling

## Common misuse
Using DISC profiles as rigid boxes for hiring, role assignment, or simplified judgments about capability.
""",
    },
    {
        "slug": "kolbe",
        "canonical_name": "Kolbe A Index",
        "short_names": ["Kolbe"],
        "short_description": "A conative action-style instrument describing instinctive modes of initiating work and solving problems.",
        "creators": ["Kathy Kolbe"],
        "publisher_or_owner": "kolbe_corp",
        "original_release_year": 1975,
        "official_websites": ["https://www.kolbe.com/"],
        "licensing_model": "proprietary",
        "country_or_origin_context": ["united_states"],
        "families": ["conative_action_style", "leadership_workplace"],
        "primary_measurement_target": ["work_style", "behavioral_style"],
        "representational_form": ["profile_vector"],
        "temporal_stance": ["semi_stable_patterns"],
        "person_ontology": ["work_behavior_pattern"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["sum_or_average_scale_scoring"],
        "epistemic_basis": ["proprietary_workplace_analytics", "mixed_psychometric_and_theoretical"],
        "interpretive_burden": "medium",
        "granularity": "medium",
        "context_sensitivity": "medium",
        "change_model": ["trait_stability", "situational_expression"],
        "distortion_risk": ["workplace_misuse", "overinterpretation"],
        "deployment_context": ["workplace", "coaching", "team_design"],
        "utility_profile": ["team_alignment", "communication_adaptation"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "low",
        "synthesis_value_for_ilens": "medium",
        "evidence_profile": ["proprietary_or_limited_transparency", "mixed_evidence"],
        "target_population": ["workplace_teams", "leaders_managers"],
        "norming_status": "variant_dependent",
        "actionability_type": ["team_design_support", "coaching_intervention"],
        "cultural_symbolic_role": ["professional_shorthand"],
        "overlap_mode": ["workplace_family_resemblance"],
        "construct_name": "MO profile",
        "construct_definition": (
            "A four-number Method of Operation profile summarizing instinctive action across Fact Finder, "
            "Follow Thru, Quick Start, and Implementor."
        ),
        "claim_text": (
            "Kolbe claims the Kolbe A Index measures the instinctive ways a person takes action when striving, "
            "producing a four-number Method of Operation profile across four Action Modes."
        ),
        "resource_title": "About The Kolbe A Index",
        "resource_url": "https://www.kolbe.com/kolbe-a-index/",
        "resource_publisher": "Kolbe Corp",
        "resource_officiality": "official",
        "resource_notes": (
            "Official Kolbe overview describing the Kolbe A Index as an instinct assessment measuring conative "
            "strengths and yielding a four-number MO result."
        ),
        "inference_id_suffix": "action_style_layer",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "Kolbe is most useful as a work-execution layer adjacent to trait and motivation systems: it frames how "
            "people instinctively organize and initiate action more than who they are globally."
        ),
        "risk_description": (
            "Its language of instinctive strengths can slide into essentialist hiring and role-fit claims, especially "
            "when stable action style is treated as a total capacity measure."
        ),
        "cautions": "Useful for workflow and task-fit discussion, weak as a total person model or unilateral hiring screen.",
        "instrument_notes": (
            "This entry centers the flagship Kolbe A Index within the broader Kolbe conative assessment ecosystem."
        ),
        "notes": """# Kolbe A Index

## What it is
A proprietary conative assessment that describes instinctive ways of taking action through a four-number Method of Operation profile.

## Why it matters
Kolbe matters because it occupies a distinct niche in the registry: it is neither a classic trait model nor a symbolic typology, but a branded action-style system focused on how people execute when they are free to be themselves.

## What it is good for
- workflow discussion
- team collaboration language
- coaching around task approach
- distinguishing action style from personality identity

## What it is weaker at
- whole-person description
- public psychometric transparency
- motive and identity language
- high-stakes selection decisions

## Common misuse
Treating a stable action-style profile as a definitive verdict on role fit, capability, or long-term hiring potential.
""",
    },
    {
        "slug": "cliftonstrengths",
        "canonical_name": "CliftonStrengths",
        "short_names": ["CliftonStrengths", "StrengthsFinder"],
        "aliases": ["StrengthsFinder"],
        "short_description": "A strengths and talent language that ranks recurring patterns of thought, feeling, and behavior into named themes.",
        "creators": ["Don Clifton", "Gallup"],
        "publisher_or_owner": "gallup",
        "official_websites": ["https://www.gallup.com/cliftonstrengths/"],
        "original_release_year": 1999,
        "licensing_model": "proprietary",
        "country_or_origin_context": ["united_states"],
        "families": ["strengths_talent", "leadership_workplace"],
        "primary_measurement_target": ["strengths_talents", "work_style", "interpersonal_style"],
        "representational_form": ["rank_order_strengths", "profile_vector", "narrative_description"],
        "temporal_stance": ["semi_stable_patterns"],
        "person_ontology": ["strengths_expression_profile"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["rank_order_selection"],
        "epistemic_basis": ["mixed_psychometric_and_theoretical", "proprietary_workplace_analytics"],
        "interpretive_burden": "medium",
        "granularity": "high",
        "context_sensitivity": "medium",
        "change_model": ["developmental_growth", "situational_expression"],
        "distortion_risk": ["overinterpretation", "workplace_misuse"],
        "deployment_context": ["workplace", "coaching", "leadership_development", "self_reflection"],
        "utility_profile": ["strengths_identification", "team_alignment", "coaching_language"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "medium",
        "synthesis_value_for_ilens": "medium",
        "evidence_profile": ["mixed_evidence", "proprietary_or_limited_transparency"],
        "target_population": ["workplace_teams", "leaders_managers", "general_adult_population"],
        "norming_status": "variant_dependent",
        "actionability_type": ["developmental_planning", "team_design_support"],
        "cultural_symbolic_role": ["workplace_identity_language", "coaching_identity_language"],
        "overlap_mode": ["workplace_family_resemblance"],
        "construct_name": "Talent theme profile",
        "construct_definition": "Rank-ordered strengths themes intended to highlight recurring talent patterns.",
        "claim_text": (
            "CliftonStrengths claims to identify and describe unique patterns of thought, feeling, and behavior "
            "through 34 research-validated talent themes."
        ),
        "resource_title": "What is the CliftonStrengths assessment?",
        "resource_url": "https://support.gallup.com/hc/en-us/articles/44814767818643-What-is-the-CliftonStrengths-assessment",
        "resource_publisher": "Gallup",
        "resource_officiality": "official",
        "resource_notes": (
            "Official Gallup overview describing CliftonStrengths as an online talent assessment grounded in 34 talent themes."
        ),
        "inference_id_suffix": "strengths_language",
        "inference_type": "practical_value",
        "inference_confidence": "high",
        "inference_text": (
            "CliftonStrengths is especially useful as a workplace and coaching language for talent development, but it is "
            "less suitable as a comprehensive ontology of personhood or as a selection instrument."
        ),
        "risk_description": "Users may confuse branded strengths language with total capability or role fit.",
        "cautions": "Strong for strengths framing, weak as a total ontology of personhood.",
        "instrument_notes": (
            "This entry centers the Gallup CliftonStrengths family as a branded strengths-and-talent assessment ecosystem."
        ),
        "notes": """# CliftonStrengths

## What it is
A Gallup strengths assessment that ranks 34 talent themes based on recurring patterns of thought, feeling, and behavior.

## Why it matters
CliftonStrengths matters because it is one of the most culturally sticky strengths vocabularies in workplaces and coaching. It functions less as a whole-person theory than as a branded language for talent development and self-description.

## What it is good for
- strengths language
- coaching and team development
- role reflection
- talent-focused development planning

## What it is weaker at
- psychometric transparency outside Gallup
- dark-side behavior
- motive and defense language
- non-work identity layers

## Common misuse
Treating top themes as fixed role entitlements or using them as hiring filters instead of development prompts.
""",
    },
    {
        "slug": "love-languages",
        "canonical_name": "The Five Love Languages",
        "short_names": ["Love Languages"],
        "short_description": "A relational preference framework describing preferred modes of expressing and receiving affection.",
        "creators": ["Gary Chapman"],
        "publisher_or_owner": "love_language_brand",
        "official_websites": ["https://5lovelanguages.com/"],
        "licensing_model": "proprietary_brand_ecosystem",
        "country_or_origin_context": ["united_states"],
        "families": ["attachment_relational", "identity_self_concept"],
        "primary_measurement_target": ["relational_needs", "communication_preferences", "interpersonal_style"],
        "representational_form": ["categorical_typology", "profile_vector", "narrative_description"],
        "temporal_stance": ["semi_stable_patterns"],
        "person_ontology": ["relational_attachment_system"],
        "administration_mode": ["self_report_questionnaire", "self_identification"],
        "scoring_logic": ["type_assignment_rules", "sum_or_average_scale_scoring"],
        "epistemic_basis": ["popular_psychology", "weak_or_contested_empirical_basis"],
        "interpretive_burden": "low",
        "granularity": "low",
        "context_sensitivity": "high",
        "change_model": ["situational_expression", "identity_revision"],
        "distortion_risk": ["overinterpretation", "reification"],
        "deployment_context": ["relationship_support", "self_reflection", "coaching"],
        "utility_profile": ["relational_patterning", "communication_adaptation"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "low",
        "synthesis_value_for_ilens": "low",
        "evidence_profile": ["mostly_anecdotal_or_practitioner_based", "contested_validity"],
        "target_population": ["couples_families", "general_adult_population"],
        "norming_status": "not_normed",
        "actionability_type": ["relational_discussion"],
        "cultural_symbolic_role": ["internet_identity_language", "pop_psychology_meme"],
        "overlap_mode": ["shared_identity_space"],
        "construct_name": "Preferred affection channel",
        "construct_definition": "A preferred mode of giving or receiving affection, such as words, time, gifts, service, or touch.",
        "claim_text": (
            "The Five Love Languages claims that people tend to give and receive love through five primary channels "
            "and that relationship quality improves when partners learn each other’s preferred channels."
        ),
        "resource_title": "What Are The 5 Love Languages?",
        "resource_url": "https://5lovelanguages.com/learn",
        "resource_publisher": "Love Language Brand",
        "resource_officiality": "official",
        "resource_notes": (
            "Official explainer page describing the five love languages as different ways people give and receive love."
        ),
        "inference_id_suffix": "relationship_shorthand",
        "inference_type": "practical_value",
        "inference_confidence": "high",
        "inference_text": (
            "Its value is mostly conversational and relational rather than psychometric: Love Languages persists because "
            "it gives people a low-complexity way to talk about care, preference, and disappointment."
        ),
        "risk_description": "Low-resolution categories can flatten complex relational dynamics into a single favorite language.",
        "cautions": "Useful as a conversation opener, not as a full relationship model.",
        "instrument_notes": (
            "This entry centers the branded Five Love Languages framework as a relational preference language."
        ),
        "notes": """# The Five Love Languages

## What it is
A five-category relational preference framework describing preferred ways of expressing and receiving affection.

## Why it matters
Love Languages matters because it is one of the most culturally sticky low-complexity relationship vocabularies in circulation. It is weak psychometrically but powerful as a conversational shorthand.

## What it is good for
- relationship conversations
- low-friction self-reflection
- identifying preferred expressions of care
- lightweight communication repair

## What it is weaker at
- psychometric rigor
- attachment and trauma dynamics
- whole-person relational modeling
- context sensitivity and change over time

## Common misuse
Reducing complex relational conflict to one fixed love language or treating the framework as a full theory of intimacy.
""",
    },
    {
        "slug": "dark-triad",
        "canonical_name": "Dark Triad",
        "short_names": ["Dark Triad"],
        "short_description": "A cluster of socially aversive personality constructs commonly organized around narcissism, Machiavellianism, and psychopathy.",
        "creators": ["Delroy L. Paulhus", "Kevin M. Williams"],
        "publisher_or_owner": "none_decentralized",
        "original_release_year": 2002,
        "licensing_model": "mixed_academic_and_derivative_measures",
        "country_or_origin_context": ["canada"],
        "families": ["trait_personality", "clinical_symptom_pathology"],
        "primary_measurement_target": ["dark_personality_features", "interpersonal_style"],
        "representational_form": ["continuous_dimensional", "profile_vector"],
        "temporal_stance": ["semi_stable_patterns"],
        "person_ontology": ["trait_container"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["sum_or_average_scale_scoring", "factor_scoring"],
        "epistemic_basis": ["strong_psychometric_validation"],
        "interpretive_burden": "medium",
        "granularity": "medium",
        "context_sensitivity": "medium",
        "change_model": ["trait_stability", "situational_expression"],
        "distortion_risk": ["self_report_distortion", "overinterpretation", "reification"],
        "deployment_context": ["research", "self_reflection"],
        "utility_profile": ["research_baseline"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "low",
        "synthesis_value_for_ilens": "medium",
        "evidence_profile": ["extensive_peer_review", "mixed_evidence"],
        "target_population": ["general_adult_population"],
        "norming_status": "variant_dependent",
        "actionability_type": ["descriptive_reflection"],
        "cultural_symbolic_role": ["professional_shorthand"],
        "overlap_mode": ["partial_construct_overlap"],
        "construct_name": "Dark trait profile",
        "construct_definition": "A profile across dark personality features such as narcissism, Machiavellianism, and psychopathy.",
        "claim_text": (
            "Dark Triad frameworks claim to measure three overlapping but distinct socially aversive personality "
            "constructs: narcissism, Machiavellianism, and psychopathy."
        ),
        "resource_title": "The Dark Triad of personality: Narcissism, Machiavellianism, and psychopathy",
        "resource_url": "https://www2.psych.ubc.ca/~dpaulhus/research/DARK_TRAITS/ARTICLES/JRP%20Paulhus%20%26%20Williams.2002.pdf",
        "resource_author": "Delroy L. Paulhus and Kevin M. Williams",
        "resource_publisher": "Journal of Research in Personality",
        "resource_officiality": "secondary",
        "resource_notes": (
            "Seminal paper introducing the Dark Triad as overlapping but distinct subclinical constructs."
        ),
        "inference_id_suffix": "aversive_trait_cluster",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "The Dark Triad is useful when the registry needs a compact aversive-traits layer, but it should be handled "
            "as a narrow construct cluster rather than a total account of personality or morality."
        ),
        "risk_description": "Scores can be moralized or used as total character judgments.",
        "cautions": "Treat as a narrow construct cluster, not a whole-person verdict.",
        "instrument_notes": (
            "This entry centers the Dark Triad as a construct family introduced in subclinical personality research."
        ),
        "notes": """# Dark Triad

## What it is
A construct cluster organized around narcissism, Machiavellianism, and psychopathy as overlapping but distinct socially aversive traits.

## Why it matters
Dark Triad matters because it captures a narrow but important slice of personality variation that broad positive or neutral trait models often understate: manipulativeness, grandiosity, callousness, and exploitative style.

## What it is good for
- research on aversive traits
- comparison to agreeableness and honesty-humility layers
- narrow interpersonal risk profiling

## What it is weaker at
- whole-person modeling
- developmental nuance
- context-rich interpretation
- non-pathologizing everyday self-understanding

## Common misuse
Using dark-trait shorthand as a moral diagnosis or total character verdict.
""",
    },
    {
        "slug": "cqs",
        "canonical_name": "Cultural Intelligence Scale",
        "short_names": ["CQS", "Cultural Intelligence Scale"],
        "short_description": "An intercultural capability instrument describing how effectively a person can function across cultural contexts.",
        "creators": ["Soon Ang", "Linn Van Dyne", "Christopher Koh", "K. Yee Ng"],
        "publisher_or_owner": "cultural_intelligence_center",
        "official_websites": ["https://culturalq.com/"],
        "original_release_year": 2007,
        "licensing_model": "mixed_commercial_and_research",
        "country_or_origin_context": ["mixed"],
        "families": ["cultural_intercultural"],
        "primary_measurement_target": ["cultural_adaptation", "behavioral_style"],
        "representational_form": ["continuous_dimensional", "profile_vector"],
        "temporal_stance": ["semi_stable_patterns", "developmental_path"],
        "person_ontology": ["cultural_competence_profile"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["sum_or_average_scale_scoring"],
        "epistemic_basis": ["cross_cultural_research", "strong_psychometric_validation"],
        "interpretive_burden": "medium",
        "granularity": "medium",
        "context_sensitivity": "high",
        "change_model": ["skills_trainability", "developmental_growth"],
        "distortion_risk": ["self_report_distortion", "false_precision"],
        "deployment_context": ["intercultural_training", "workplace", "education", "research"],
        "utility_profile": ["cultural_navigation", "developmental_reflection"],
        "identity_adhesion_risk": "low",
        "worldview_load": "low",
        "synthesis_value_for_ilens": "medium",
        "evidence_profile": ["extensive_peer_review", "cross_cultural_support"],
        "target_population": ["multicultural_professionals", "students", "general_adult_population"],
        "norming_status": "well_normed",
        "actionability_type": ["developmental_planning", "descriptive_reflection"],
        "cultural_symbolic_role": ["professional_shorthand"],
        "overlap_mode": ["complementary_layers"],
        "construct_name": "Cultural intelligence profile",
        "construct_definition": "A profile across cultural metacognitive, cognitive, motivational, and behavioral capabilities.",
        "claim_text": (
            "The Cultural Intelligence Scale claims to measure four capabilities relevant to functioning effectively "
            "across culturally diverse contexts: Drive, Knowledge, Strategy, and Action."
        ),
        "resource_type": "research_overview",
        "resource_title": "Cultural Intelligence (CQ): A Research Overview",
        "resource_url": "https://culturalq.com/wp-content/uploads/2024/03/CQ_Research_Summary_v.2.0.pdf",
        "resource_publisher": "Cultural Intelligence Center",
        "resource_officiality": "official",
        "resource_notes": (
            "Official CQ research summary describing the four-factor model, CQS development, and validity evidence."
        ),
        "inference_id_suffix": "contextual_capability_layer",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "CQS matters because it captures an intercultural capability layer that most personality systems ignore: "
            "how people make sense of and adapt in culturally diverse situations."
        ),
        "risk_description": "Self-report scores can be mistaken for demonstrated intercultural skill.",
        "cautions": "Use alongside behavioral evidence when possible.",
        "instrument_notes": (
            "This entry centers the four-factor Cultural Intelligence Scale as a theory-backed intercultural capability measure."
        ),
        "notes": """# Cultural Intelligence Scale

## What it is
An intercultural capability instrument organized around four factors: Drive, Knowledge, Strategy, and Action.

## Why it matters
CQS matters because it gives the registry a context-specific capability layer rather than another broad personality taxonomy. It is especially valuable when the question is whether someone can interpret and adapt across cultural settings.

## What it is good for
- intercultural training
- research on cross-cultural effectiveness
- global leadership development
- reflection on cultural adaptability

## What it is weaker at
- whole-person personality description
- symbolic or identity language
- trait anchoring outside intercultural contexts
- direct motive or attachment interpretation

## Common misuse
Treating self-report CQ as proof of real-world intercultural competence without behavioral evidence or situational context.
""",
    },
    {
        "slug": "culture-index",
        "canonical_name": "Culture Index",
        "short_names": ["Culture Index"],
        "short_description": "A workplace assessment framework focused on predictive patterns relevant to roles, performance, and organizational fit.",
        "creators": ["Gary Walstrom", "Cecilia Bruening-Walstrom", "Louis Janda"],
        "publisher_or_owner": "culture_index_llc",
        "original_release_year": 2004,
        "official_websites": ["https://www.cultureindex.com/"],
        "licensing_model": "proprietary",
        "country_or_origin_context": ["united_states"],
        "families": ["leadership_workplace", "trait_personality"],
        "primary_measurement_target": ["work_style", "behavioral_style"],
        "representational_form": ["profile_vector", "narrative_description"],
        "temporal_stance": ["semi_stable_patterns"],
        "person_ontology": ["work_behavior_pattern"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["sum_or_average_scale_scoring", "interpretive_pattern_matching"],
        "epistemic_basis": ["proprietary_workplace_analytics", "mixed_psychometric_and_theoretical"],
        "interpretive_burden": "medium",
        "granularity": "medium",
        "context_sensitivity": "medium",
        "change_model": ["situational_expression"],
        "distortion_risk": ["workplace_misuse", "false_precision"],
        "deployment_context": ["workplace", "hiring", "leadership_development"],
        "utility_profile": ["selection_screening", "team_alignment"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "medium",
        "synthesis_value_for_ilens": "low",
        "evidence_profile": ["proprietary_or_limited_transparency"],
        "target_population": ["workplace_teams", "leaders_managers"],
        "norming_status": "variant_dependent",
        "actionability_type": ["selection_decision_support", "team_design_support"],
        "cultural_symbolic_role": ["workplace_identity_language"],
        "overlap_mode": ["workplace_family_resemblance"],
        "construct_name": "Predictive workplace profile",
        "construct_definition": "A proprietary profile intended to support workplace fit and role-related discussion.",
        "claim_text": (
            "Culture Index claims to measure seven work-related traits through a quick survey and translate that data "
            "into hiring, management, and team-design decisions."
        ),
        "resource_title": "About Us | Culture Index Analytics",
        "resource_url": "https://www.cultureindex.com/about-us",
        "resource_publisher": "Culture Index, LLC",
        "resource_officiality": "official",
        "resource_notes": (
            "Official company history and methodology page describing Culture Index's 2004 launch, its founders, "
            "and its use of work-related trait measurement and free-choice adjective methodology."
        ),
        "inference_id_suffix": "high_stakes_workflow",
        "inference_type": "practical_risk",
        "inference_confidence": "high",
        "inference_text": (
            "Culture Index is oriented toward managerial action more than reflective self-understanding; because it is "
            "sold into hiring and role-fit workflows, evidence quality and interpretive limits matter more than its "
            "branding suggests."
        ),
        "risk_description": (
            "Using proprietary workplace outputs for hiring, filtering, or succession decisions can amplify false "
            "precision, bias, and overconfidence."
        ),
        "cautions": "Treat as a managerial heuristic with guardrails, not as an objective basis for high-stakes employment decisions.",
        "instrument_notes": (
            "This entry centers the modern Culture Index assessment ecosystem as a proprietary workplace analytics system."
        ),
        "notes": """# Culture Index

## What it is
A proprietary workplace assessment system that uses a brief survey to model work-related traits for hiring, management, and organizational decision-making.

## Why it matters
Culture Index matters because it sits at the high-stakes end of the workplace-assessment spectrum. It is designed less for personal reflection than for operational decisions about fit, performance, and team design.

## What it is good for
- managerial discussion of work-style patterns
- team planning language
- organizational role-fit conversations
- studying proprietary workplace assessment culture

## What it is weaker at
- transparent psychometric scrutiny
- whole-person description
- reflective self-understanding
- safe use in consequential employment decisions

## Common misuse
Treating a proprietary work-traits profile as objective truth in hiring or succession decisions without strong validity scrutiny and human oversight.
""",
    },
    {
        "slug": "human-design",
        "canonical_name": "Human Design",
        "short_names": ["Human Design"],
        "short_description": "A symbolic system combining astrology, I Ching, chakras, Kabbalah, and other traditions into a bodygraph-based self-description framework.",
        "creators": ["Ra Uru Hu"],
        "publisher_or_owner": "jovian_archive",
        "original_release_year": 1987,
        "official_websites": ["https://jovianarchive.com/"],
        "licensing_model": "mixed_proprietary_and_community_ecosystem",
        "country_or_origin_context": ["mixed"],
        "families": ["symbolic_archetypal_spiritual", "identity_self_concept", "worldview_meaning_making"],
        "primary_measurement_target": ["identity_narrative", "symbolic_archetypal_patterning", "subjective_meaning"],
        "representational_form": ["symbolic_chart", "narrative_description", "categorical_typology"],
        "temporal_stance": ["cyclical_temporal_pattern", "identity_narrative_snapshot"],
        "person_ontology": ["symbolic_cosmological_self"],
        "administration_mode": ["algorithmic_chart_calculation", "practitioner_interpretation"],
        "scoring_logic": ["algorithmic_chart_rules", "expert_interpretation"],
        "epistemic_basis": ["symbolic_tradition", "mixed_lineages"],
        "interpretive_burden": "very_high",
        "granularity": "very_high",
        "context_sensitivity": "medium",
        "change_model": ["identity_revision", "cyclical_activation"],
        "distortion_risk": ["identity_capture", "barnum_effect", "determinism", "practitioner_projection"],
        "deployment_context": ["self_reflection", "coaching", "spiritual_community", "internet_identity_culture"],
        "utility_profile": ["symbolic_reflection", "coaching_language"],
        "identity_adhesion_risk": "very_high",
        "worldview_load": "very_high",
        "synthesis_value_for_ilens": "low",
        "evidence_profile": ["mostly_anecdotal_or_practitioner_based"],
        "target_population": ["spiritual_seekers", "internet_communities"],
        "norming_status": "not_normed",
        "actionability_type": ["symbolic_storytelling"],
        "cultural_symbolic_role": ["spiritual_symbolic_system", "internet_identity_language", "community_belonging_language"],
        "overlap_mode": ["shared_identity_space", "weak_direct_mapping"],
        "construct_name": "Bodygraph profile",
        "construct_definition": "A chart-based symbolic profile derived from birth data and interpreted through Human Design rules.",
        "claim_text": (
            "Human Design claims that birth data can be used to generate a BodyGraph revealing a person's energetic "
            "blueprint, differentiation, and decision strategy."
        ),
        "resource_title": "Introduction to the Human Design System",
        "resource_url": "https://jovianarchive.com/blogs/human-design-basics/introduction-to-the-human-design-system",
        "resource_author": "Ra Uru Hu",
        "resource_publication_date": "2016-10-08",
        "resource_publisher": "Jovian Archive",
        "resource_officiality": "official",
        "resource_notes": (
            "Official founder-authored introduction describing Human Design as a synthesis of ancient wisdom and "
            "modern science expressed through the Rave Mandala and BodyGraph."
        ),
        "inference_id_suffix": "identity_engine",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "Human Design is important to the registry less as an assessment instrument than as a high-adhesion "
            "identity and decision language built around an internally coherent symbolic cosmology."
        ),
        "risk_description": (
            "Because the system presents itself as a precise bodygraph-based blueprint, users can externalize agency "
            "to chart mechanics, teachings, or practitioners."
        ),
        "cautions": "Treat as symbolic meaning language and community practice, not as empirical person measurement.",
        "instrument_notes": (
            "This entry centers the Ra Uru Hu and Jovian Archive lineage while recognizing the broader Human Design ecosystem."
        ),
        "notes": """# Human Design

## What it is
A birth-data-driven symbolic system that produces a BodyGraph and associated teachings about type, authority, definition, and differentiated life mechanics.

## Why it matters
Human Design matters because it is one of the most elaborate contemporary identity systems operating in online, coaching, and spiritual spaces. It is structurally rich, culturally sticky, and interpretively heavy.

## What it is good for
- symbolic self-reflection
- identity and decision language
- community belonging
- comparative study of modern spiritual person-models

## What it is weaker at
- empirical validation
- low-burden interpretation
- clean construct comparability
- maintaining distance between symbolic map and lived agency

## Common misuse
Treating the chart as a literal blueprint that overrides context, development, uncertainty, or practical judgment.
""",
    },
    {
        "slug": "natal-astrology",
        "canonical_name": "Natal Astrology",
        "short_names": ["Natal Astrology", "Birth Chart Astrology"],
        "aliases": ["Birth Chart"],
        "short_description": "A symbolic charting system that interprets birth time and place through zodiacal and planetary symbolism.",
        "creators": ["multiple_historical_lineages"],
        "publisher_or_owner": "decentralized",
        "official_websites": [],
        "licensing_model": "decentralized",
        "country_or_origin_context": ["mixed"],
        "families": ["symbolic_archetypal_spiritual", "worldview_meaning_making", "identity_self_concept"],
        "primary_measurement_target": ["symbolic_archetypal_patterning", "identity_narrative", "subjective_meaning"],
        "representational_form": ["symbolic_chart", "narrative_description"],
        "temporal_stance": ["cyclical_temporal_pattern", "identity_narrative_snapshot"],
        "person_ontology": ["symbolic_cosmological_self"],
        "administration_mode": ["algorithmic_chart_calculation", "practitioner_interpretation"],
        "scoring_logic": ["algorithmic_chart_rules", "expert_interpretation"],
        "epistemic_basis": ["symbolic_tradition"],
        "interpretive_burden": "very_high",
        "granularity": "very_high",
        "context_sensitivity": "high",
        "change_model": ["cyclical_activation", "identity_revision"],
        "distortion_risk": ["barnum_effect", "determinism", "identity_capture", "practitioner_projection"],
        "deployment_context": ["self_reflection", "spiritual_community", "coaching", "internet_identity_culture"],
        "utility_profile": ["symbolic_reflection", "coaching_language"],
        "identity_adhesion_risk": "very_high",
        "worldview_load": "very_high",
        "synthesis_value_for_ilens": "low",
        "evidence_profile": ["mostly_anecdotal_or_practitioner_based"],
        "target_population": ["spiritual_seekers", "internet_communities"],
        "norming_status": "not_normed",
        "actionability_type": ["symbolic_storytelling"],
        "cultural_symbolic_role": ["spiritual_symbolic_system", "internet_identity_language", "community_belonging_language"],
        "overlap_mode": ["shared_identity_space"],
        "construct_name": "Natal chart profile",
        "construct_definition": "A symbolic birth chart interpreted through astrological houses, planets, and signs.",
        "claim_text": (
            "Natal astrology claims that a birth chart is a snapshot of the sky at the exact moment of birth and can "
            "reveal personality, strengths, challenges, and life path."
        ),
        "resource_title": "Free Birth Chart Calculator",
        "resource_url": "https://www.astrology.com/birth-chart",
        "resource_publisher": "Astrology.com",
        "resource_officiality": "secondary",
        "resource_notes": (
            "Mainstream secondary explainer describing the natal chart as a snapshot of the sky at birth that reveals "
            "personality, strengths, challenges, and life path."
        ),
        "inference_id_suffix": "symbolic_identity_language",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "Natal astrology belongs in the registry because it is one of the most durable symbolic person-description "
            "systems in circulation, shaping identity, timing, and meaning-making despite lacking empirical measurement standing."
        ),
        "risk_description": (
            "Charts can be treated as destiny or diagnostic truth, inviting determinism, projection, and practitioner overreach."
        ),
        "cautions": "Keep empirical, symbolic, and interpretive layers clearly separated.",
        "instrument_notes": (
            "This entry represents natal astrology as a decentralized symbolic framework rather than any single school or publisher."
        ),
        "notes": """# Natal Astrology

## What it is
A symbolic birth-chart system that maps planets, signs, houses, and aspects at the moment of birth to interpret personality and life themes.

## Why it matters
Natal astrology matters because it remains one of the oldest and most persistent symbolic languages for personhood, identity, timing, and meaning. Its cultural reach is far larger than its empirical standing.

## What it is good for
- symbolic self-reflection
- narrative meaning-making
- archetypal language
- studying identity systems with strong cultural persistence

## What it is weaker at
- empirical measurement
- inter-rater consistency across practitioners
- construct commensurability with psychometric systems
- resisting destiny narratives

## Common misuse
Treating the birth chart as objective diagnosis or fate rather than an interpretive symbolic framework.
""",
    },
    {
        "slug": "attachment-styles",
        "canonical_name": "Attachment Style Frameworks",
        "short_names": ["Attachment Styles"],
        "short_description": "A family of relational frameworks describing recurring patterns of security, anxiety, avoidance, and closeness regulation.",
        "creators": ["John Bowlby", "Mary Ainsworth", "multiple_contributors"],
        "publisher_or_owner": "none_decentralized",
        "licensing_model": "mixed_academic_and_popular",
        "country_or_origin_context": ["mixed"],
        "families": ["attachment_relational"],
        "primary_measurement_target": ["attachment_patterns", "relational_needs", "interpersonal_style"],
        "representational_form": ["categorical_typology", "hybrid_dimensional_typological", "narrative_description"],
        "temporal_stance": ["semi_stable_patterns", "developmental_path"],
        "person_ontology": ["relational_attachment_system"],
        "administration_mode": ["self_report_questionnaire", "practitioner_interview"],
        "scoring_logic": ["type_assignment_rules", "sum_or_average_scale_scoring"],
        "epistemic_basis": ["strong_psychometric_validation", "clinical_observation"],
        "interpretive_burden": "medium",
        "granularity": "medium",
        "context_sensitivity": "high",
        "change_model": ["developmental_growth", "situational_expression"],
        "distortion_risk": ["overinterpretation", "identity_capture"],
        "deployment_context": ["therapy", "relationship_support", "self_reflection", "coaching"],
        "utility_profile": ["relational_patterning", "developmental_reflection", "self_understanding"],
        "identity_adhesion_risk": "high",
        "worldview_load": "low",
        "synthesis_value_for_ilens": "high",
        "evidence_profile": ["extensive_peer_review", "mixed_evidence"],
        "target_population": ["general_adult_population", "couples_families", "clinical_populations"],
        "norming_status": "variant_dependent",
        "actionability_type": ["developmental_planning", "relational_discussion"],
        "cultural_symbolic_role": ["internet_identity_language", "professional_shorthand"],
        "overlap_mode": ["complementary_layers", "shared_identity_space"],
        "construct_name": "Attachment pattern",
        "construct_definition": "A pattern of closeness regulation, security, anxiety, and avoidance in relational contexts.",
        "claim_text": (
            "Attachment frameworks claim that recurring differences in security, anxiety, and avoidance shape how "
            "people seek closeness, regulate distress, and navigate intimate relationships."
        ),
        "resource_title": "Adult Attachment Theory and Research",
        "resource_url": "https://labs.psychology.illinois.edu/~rcfraley/attachment.htm",
        "resource_author": "R. Chris Fraley",
        "resource_publisher": "University of Illinois Urbana-Champaign",
        "resource_officiality": "secondary",
        "resource_notes": (
            "Research overview summarizing Bowlby, Ainsworth, Hazan and Shaver, and dimensional adult attachment work."
        ),
        "inference_id_suffix": "relational_layer",
        "inference_type": "comparative_strength",
        "inference_confidence": "high",
        "inference_text": (
            "Attachment language is unusually useful when the question is relational security, dependency, or "
            "closeness regulation, but it is frequently overextended into a total personality label."
        ),
        "risk_description": "People may adopt an attachment label as a total identity instead of a relational pattern under specific conditions.",
        "cautions": "Preserve context and developmental nuance when using attachment labels.",
        "instrument_notes": (
            "This record covers the broader family of adult attachment-style frameworks rather than a single questionnaire."
        ),
        "notes": """# Attachment Style Frameworks

## What it is
A family of relational frameworks describing recurring patterns of security, anxiety, avoidance, and closeness regulation.

## Why it matters
Attachment frameworks matter because they capture a relational layer that broad trait models often blur: how people seek safety, proximity, reassurance, and distance in emotionally important relationships.

## What it is good for
- relational patterning
- therapy and coaching conversation
- understanding anxiety and avoidance dynamics
- contextual self-reflection in close relationships

## What it is weaker at
- whole-person personality modeling
- context-free labeling
- clean single-test standardization across the family
- explaining symbolic or motivational identity systems

## Common misuse
Treating an attachment style as a permanent identity instead of a relational pattern that can vary by context, relationship, and development.
""",
    },
    {
        "slug": "via-character-strengths",
        "canonical_name": "VIA Character Strengths",
        "short_names": ["VIA Character Strengths", "VIA"],
        "short_description": "A strengths framework organizing character strengths into a virtue-based taxonomy with questionnaire-driven profiles.",
        "creators": ["Christopher Peterson", "Martin E. P. Seligman", "multiple_contributors"],
        "publisher_or_owner": "via_institute_on_character",
        "official_websites": ["https://www.viacharacter.org/"],
        "licensing_model": "mixed_public_and_paid_reports",
        "country_or_origin_context": ["united_states"],
        "families": ["strengths_talent", "values_moral_orientation"],
        "primary_measurement_target": ["moral_character", "strengths_talents"],
        "representational_form": ["rank_order_strengths", "profile_vector"],
        "temporal_stance": ["semi_stable_patterns", "developmental_path"],
        "person_ontology": ["moral_character_profile", "strengths_expression_profile"],
        "administration_mode": ["self_report_questionnaire"],
        "scoring_logic": ["rank_order_selection", "sum_or_average_scale_scoring"],
        "epistemic_basis": ["strong_psychometric_validation"],
        "interpretive_burden": "medium",
        "granularity": "high",
        "context_sensitivity": "medium",
        "change_model": ["developmental_growth", "skills_trainability"],
        "distortion_risk": ["overinterpretation", "self_report_distortion"],
        "deployment_context": ["self_reflection", "coaching", "education", "research"],
        "utility_profile": ["strengths_identification", "developmental_reflection"],
        "identity_adhesion_risk": "medium",
        "worldview_load": "medium",
        "synthesis_value_for_ilens": "medium",
        "evidence_profile": ["extensive_peer_review", "normative_data_available"],
        "target_population": ["general_adult_population", "students"],
        "norming_status": "well_normed",
        "actionability_type": ["developmental_planning", "descriptive_reflection"],
        "cultural_symbolic_role": ["professional_shorthand"],
        "overlap_mode": ["complementary_layers"],
        "construct_name": "Character strengths profile",
        "construct_definition": "A ranked profile of character strengths organized within a virtue taxonomy.",
        "claim_text": (
            "VIA claims to classify 24 character strengths under six broad virtues and to measure those strengths "
            "through the VIA Survey."
        ),
        "resource_type": "classification",
        "resource_title": "VIA Classification of Character Strengths",
        "resource_url": "https://www.viacharacter.org/resources/activities/via-classification-of-character-strengths",
        "resource_publisher": "VIA Institute on Character",
        "resource_officiality": "official",
        "resource_notes": (
            "Official VIA page describing the 24 character strengths, six virtue categories, and the role of the VIA Survey."
        ),
        "inference_id_suffix": "strengths_layer",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "VIA is a strong positive-psychology layer for strengths-oriented description, especially when the corpus "
            "needs a moral-character and flourishing vocabulary rather than only trait or workplace language."
        ),
        "risk_description": "Strengths rankings can be taken as moral verdicts or fixed rankings of worth.",
        "cautions": "Treat strengths as developmental tendencies rather than moral badges.",
        "instrument_notes": (
            "This entry centers the VIA classification and survey family as a strengths-oriented moral character framework."
        ),
        "notes": """# VIA Character Strengths

## What it is
A strengths framework that organizes 24 character strengths under six virtue categories and measures them through the VIA Survey.

## Why it matters
VIA matters because it gives the registry a structured positive-personality and moral-character layer. It is one of the clearest alternatives to deficit-heavy or identity-heavy systems when the goal is strengths description and development.

## What it is good for
- strengths identification
- coaching and education
- positive psychology research
- developmental reflection

## What it is weaker at
- dark-side behavior
- motive conflict
- whole-person relational dynamics
- symbolic identity language

## Common misuse
Treating ranked strengths as moral rankings of the person rather than as tendencies that can be cultivated, overused, or context-dependent.
""",
    },
    {
        "slug": "hexaco",
        "canonical_name": "HEXACO Personality Inventory",
        "short_names": ["HEXACO"],
        "short_description": "A trait personality framework extending five-factor trait models with an additional Honesty-Humility domain.",
        "creators": ["Kibeom Lee", "Michael C. Ashton"],
        "publisher_or_owner": "hexaco_org",
        "official_websites": ["https://hexaco.org/"],
        "licensing_model": "free_for_nonprofit_academic_research_and_permissioned_other_use",
        "country_or_origin_context": ["canada"],
        "families": ["trait_personality"],
        "primary_measurement_target": ["stable_traits", "interpersonal_style", "affect_emotion", "moral_character"],
        "representational_form": ["continuous_dimensional", "hierarchical_model"],
        "temporal_stance": ["stable_traits"],
        "person_ontology": ["trait_container"],
        "administration_mode": ["self_report_questionnaire", "observer_report"],
        "scoring_logic": ["sum_or_average_scale_scoring", "factor_scoring"],
        "epistemic_basis": ["strong_psychometric_validation", "cross_cultural_research"],
        "interpretive_burden": "low",
        "granularity": "high",
        "context_sensitivity": "medium",
        "change_model": ["trait_stability", "developmental_growth"],
        "distortion_risk": ["self_report_distortion", "overinterpretation"],
        "deployment_context": ["research", "self_reflection", "workplace"],
        "utility_profile": ["research_baseline", "self_understanding"],
        "identity_adhesion_risk": "low",
        "worldview_load": "very_low",
        "synthesis_value_for_ilens": "high",
        "evidence_profile": ["extensive_peer_review", "cross_cultural_support", "normative_data_available"],
        "target_population": ["general_adult_population"],
        "norming_status": "well_normed",
        "actionability_type": ["descriptive_reflection"],
        "cultural_symbolic_role": ["research_anchor"],
        "overlap_mode": ["partial_construct_overlap", "complementary_layers"],
        "construct_name": "HEXACO trait profile",
        "construct_definition": "A dimensional profile across six broad personality factors including Honesty-Humility.",
        "claim_text": (
            "HEXACO claims to measure six broad personality dimensions, including Honesty-Humility, using a "
            "cross-culturally derived lexical model of personality structure."
        ),
        "resource_title": "The HEXACO Personality Inventory-Revised",
        "resource_url": "https://hexaco.org/hexaco-inventory",
        "resource_author": "Kibeom Lee and Michael C. Ashton",
        "resource_publisher": "HEXACO.org",
        "resource_officiality": "official",
        "resource_notes": (
            "Official instrument page describing the HEXACO-PI-R and its 60-, 100-, and 200-item self-report and observer versions."
        ),
        "inference_id_suffix": "honesty_humility_anchor",
        "inference_type": "synthesis_position",
        "inference_confidence": "high",
        "inference_text": (
            "HEXACO is especially valuable when the registry needs a trait anchor close to Big Five but with a clearer "
            "Honesty-Humility dimension and stronger cross-cultural lexical grounding."
        ),
        "risk_description": "Like other trait models, HEXACO can be overread as a total explanation of the person.",
        "cautions": "Useful as broad descriptive scaffolding, not as a complete model of motive or meaning.",
        "instrument_notes": (
            "This entry centers the HEXACO inventory family as a six-factor lexical trait framework."
        ),
        "notes": """# HEXACO Personality Inventory

## What it is
A six-factor trait personality framework that extends Big Five-like models with the additional domain of Honesty-Humility.

## Why it matters
HEXACO matters because it preserves the practical value of broad trait description while making room for a dimension that often matters in moral, interpersonal, and prosocial interpretation. It is one of the strongest neighboring anchor systems to Big Five in the registry.

## What it is good for
- broad trait description
- research comparison to Big Five
- honesty-humility analysis
- synthesis anchoring

## What it is weaker at
- motive language
- symbolic identity language
- deep developmental narrative
- context-rich relational interpretation

## Common misuse
Treating six-factor trait outputs as a full account of character, ethics, or relational behavior.
""",
    },
]


PLACEHOLDER_ENHANCEMENTS_BY_SLUG = {
    "attachment-styles": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_attachment_styles_dimensional_model",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Contemporary adult attachment measures often represent attachment variation along anxiety and "
                    "avoidance dimensions rather than only fixed style labels."
                ),
                "source_resource_ids": ["res_attachment_styles_ecrr"],
            },
            {
                "id": "clm_attachment_styles_relational_context",
                "claim_type": "theoretical_claim",
                "claim_text": (
                    "Attachment theory is intended to describe expectations of availability, closeness, and distress "
                    "regulation within emotionally significant relationships."
                ),
                "source_resource_ids": ["res_attachment_styles_overview"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_attachment_styles_anxiety",
                "name": "Attachment Anxiety",
                "short_name": "Anxiety",
                "construct_kind": ["dimension", "attachment_dimension"],
                "official_definition": "Sensitivity to rejection, abandonment, and uncertainty about the availability of close others.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_attachment_styles_avoidance",
                "name": "Attachment Avoidance",
                "short_name": "Avoidance",
                "construct_kind": ["dimension", "attachment_dimension"],
                "official_definition": "Discomfort with dependence, emotional intimacy, and closeness in attachment relationships.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_attachment_styles_not_total_personality",
                "inference_type": "practical_limit",
                "text": (
                    "Attachment language is strongest as a relationship-pattern layer and weakens when it is treated "
                    "as a global whole-person typology detached from context."
                ),
                "confidence": "high",
                "linked_entities": ["instr_love_languages", "instr_big_five"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_attachment_styles_ecrr",
                "resource_type": "questionnaire",
                "title": "Experiences in Close Relationships-Revised (ECR-R)",
                "url": "https://labs.psychology.illinois.edu/~rcfraley/measures/ecrr.htm",
                "author": "R. Chris Fraley",
                "publisher": "University of Illinois Urbana-Champaign",
                "officiality": "secondary",
                "notes": "Measurement page for the ECR-R, one of the most widely used adult attachment self-report instruments.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_attachment_styles_love_languages_relational",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_attachment_styles",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_love_languages",
                "relationship_type": "complementary_non_equivalent",
                "relationship_strength": "medium",
                "rationale": (
                    "Attachment styles and Love Languages both operate in relationship discourse, but attachment targets security "
                    "and regulation patterns while Love Languages targets preferred expressions of care."
                ),
                "confidence": "high",
                "notes": "Useful comparative link for relational frameworks that are often conflated in popular discourse.",
            },
            {
                "id": "xwk_attachment_styles_anxiety_words_of_affirmation",
                "source_entity_type": "construct",
                "source_entity_id": "con_attachment_styles_anxiety",
                "target_entity_type": "construct",
                "target_entity_id": "con_love_languages_words_of_affirmation",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "Higher attachment anxiety often heightens sensitivity to reassurance and verbal confirmation, which "
                    "can overlap with a felt importance of affirming language, though the constructs are not equivalent."
                ),
                "confidence": "medium",
                "notes": "This is a contextual overlap, not a translation between insecurity and preference.",
            },
            {
                "id": "xwk_attachment_styles_avoidance_physical_touch",
                "source_entity_type": "construct",
                "source_entity_id": "con_attachment_styles_avoidance",
                "target_entity_type": "construct",
                "target_entity_id": "con_love_languages_physical_touch",
                "relationship_type": "inverse_tendency",
                "relationship_strength": "medium",
                "rationale": (
                    "Attachment avoidance can coincide with reduced comfort around closeness and touch, but a lower "
                    "touch preference is neither necessary nor sufficient for avoidant attachment."
                ),
                "confidence": "medium",
                "notes": "Useful only as a cautionary comparative pattern, not as a diagnostic shortcut.",
            },
        ],
        "extra_risks": [
            {
                "id": "rsk_attachment_styles_partner_pathologizing",
                "risk_type": "partner_pathologizing",
                "severity": "medium",
                "description": (
                    "Popular attachment language is often used to diagnose partners or explain conflict unilaterally "
                    "without considering mutual dynamics, stress, or relationship history."
                ),
                "mitigation": "Use attachment labels to open inquiry into patterns, not to assign unilateral blame.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_attachment_styles_therapy",
                "use_context": "therapy",
                "utility_type": "relationship_pattern_reflection",
                "suitability_level": "high",
                "cautions": (
                    "Best used with developmental history and current relational context, not as a fixed diagnostic badge."
                ),
            }
        ],
    },
    "cliftonstrengths": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_cliftonstrengths_four_domains",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Gallup groups the 34 CliftonStrengths talent themes into four broader domains: Executing, "
                    "Influencing, Relationship Building, and Strategic Thinking."
                ),
                "source_resource_ids": ["res_cliftonstrengths_how_it_works"],
            },
            {
                "id": "clm_cliftonstrengths_ranked_output",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "CliftonStrengths reports an individual's pattern as a ranked profile of talent themes rather than "
                    "as a deficit-oriented pathology or symptom score."
                ),
                "source_resource_ids": ["res_cliftonstrengths_how_it_works"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_cliftonstrengths_executing",
                "name": "Executing",
                "short_name": "Executing",
                "construct_kind": ["domain", "strengths_domain"],
                "official_definition": "Themes that help a person turn ideas into action and reliably get work done.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_cliftonstrengths_influencing",
                "name": "Influencing",
                "short_name": "Influencing",
                "construct_kind": ["domain", "strengths_domain"],
                "official_definition": "Themes that help a person take charge, speak up, and move others to action.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_cliftonstrengths_relationship_building",
                "name": "Relationship Building",
                "short_name": "Relationship Building",
                "construct_kind": ["domain", "strengths_domain"],
                "official_definition": "Themes that help a person build trust, cohesion, and connection with others.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_cliftonstrengths_strategic_thinking",
                "name": "Strategic Thinking",
                "short_name": "Strategic Thinking",
                "construct_kind": ["domain", "strengths_domain"],
                "official_definition": "Themes that help a person absorb information, analyze situations, and envision possibilities.",
                "scoring_type": "rank_order_grouping",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_cliftonstrengths_branded_workplace_layer",
                "inference_type": "practical_limit",
                "text": (
                    "CliftonStrengths works best as a branded development language inside coaching and workplace "
                    "contexts, but it leaves motive, shadow, and non-work identity layers comparatively under-described."
                ),
                "confidence": "high",
                "linked_entities": ["instr_via_character_strengths", "instr_big_five"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_cliftonstrengths_how_it_works",
                "resource_type": "overview",
                "title": "How CliftonStrengths Works",
                "url": "https://www.gallup.com/cliftonstrengths/en/253676/how-cliftonstrengths-works.aspx",
                "publisher": "Gallup",
                "officiality": "official",
                "notes": "Official Gallup explainer of how the assessment ranks talent themes and produces strengths reports.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_cliftonstrengths_via_strengths",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_cliftonstrengths",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_via_character_strengths",
                "relationship_type": "same_layer_different_cut",
                "relationship_strength": "medium",
                "rationale": (
                    "CliftonStrengths and VIA both offer strengths-oriented vocabularies, but CliftonStrengths emphasizes talent and "
                    "performance themes while VIA emphasizes character strengths and virtues."
                ),
                "confidence": "high",
                "notes": "House comparison across two strengths-first systems with different normative framing.",
            },
            {
                "id": "xwk_cliftonstrengths_strategic_thinking_via_wisdom",
                "source_entity_type": "construct",
                "source_entity_id": "con_cliftonstrengths_strategic_thinking",
                "target_entity_type": "construct",
                "target_entity_id": "con_via_wisdom",
                "relationship_type": "same_layer_different_cut",
                "relationship_strength": "high",
                "rationale": (
                    "CliftonStrengths Strategic Thinking and VIA Wisdom both organize around learning, sense-making, "
                    "and using knowledge well, though one is talent-performance language and the other is virtue language."
                ),
                "confidence": "high",
                "notes": "A relatively strong bridge between workplace-strength and character-strength vocabularies.",
            },
            {
                "id": "xwk_cliftonstrengths_relationship_building_via_humanity",
                "source_entity_type": "construct",
                "source_entity_id": "con_cliftonstrengths_relationship_building",
                "target_entity_type": "construct",
                "target_entity_id": "con_via_humanity",
                "relationship_type": "loose_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "Relationship Building and Humanity both emphasize interpersonal warmth and connection, but "
                    "CliftonStrengths frames this as talent at building bonds while VIA frames it as character virtue."
                ),
                "confidence": "high",
                "notes": "Overlap is meaningful but still normatively different.",
            },
            {
                "id": "xwk_cliftonstrengths_influencing_via_courage",
                "source_entity_type": "construct",
                "source_entity_id": "con_cliftonstrengths_influencing",
                "target_entity_type": "construct",
                "target_entity_id": "con_via_courage",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "Influencing can overlap with courage-related themes of speaking up and acting publicly, but "
                    "CliftonStrengths highlights effectiveness and impact whereas VIA highlights virtue in the face of difficulty."
                ),
                "confidence": "medium",
                "notes": "Best treated as a partial bridge rather than a one-to-one mapping.",
            },
        ],
        "extra_risks": [
            {
                "id": "rsk_cliftonstrengths_workplace_misuse",
                "risk_type": "workplace_misuse",
                "severity": "high",
                "description": (
                    "Organizations may use top themes as hiring screens or fixed role assignments even though the "
                    "system is better suited to development, coaching, and team conversation."
                ),
                "mitigation": "Keep CliftonStrengths in development workflows and avoid treating theme rankings as selection criteria.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_cliftonstrengths_team_design",
                "use_context": "team_design",
                "utility_type": "communication_adaptation",
                "suitability_level": "high",
                "cautions": (
                    "Useful for role and collaboration discussion, but weak if it becomes the sole basis for staffing decisions."
                ),
            }
        ],
    },
    "cqs": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_cqs_predictive_validity",
                "claim_type": "usage_claim",
                "claim_text": (
                    "CQ materials present cultural intelligence as a measurable capability linked to effectiveness in "
                    "culturally diverse work, leadership, and collaboration contexts."
                ),
                "source_resource_ids": ["res_cqs_overview"],
            },
            {
                "id": "clm_cqs_developmental_reporting",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "The CQ Pro assessment is positioned as both a benchmark and a developmental report for improving "
                    "how a person functions in cross-cultural situations."
                ),
                "source_resource_ids": ["res_cqs_cq_pro_assessment"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_cqs_drive",
                "name": "CQ Drive",
                "short_name": "Drive",
                "construct_kind": ["dimension", "capability"],
                "official_definition": "Motivation, interest, and confidence for functioning effectively in culturally diverse settings.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_cqs_knowledge",
                "name": "CQ Knowledge",
                "short_name": "Knowledge",
                "construct_kind": ["dimension", "capability"],
                "official_definition": "Understanding of cultural similarities, differences, and norms that shape social interaction.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_cqs_strategy",
                "name": "CQ Strategy",
                "short_name": "Strategy",
                "construct_kind": ["dimension", "capability"],
                "official_definition": "Metacognitive capacity to plan for, interpret, and revise understanding in cross-cultural situations.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_cqs_action",
                "name": "CQ Action",
                "short_name": "Action",
                "construct_kind": ["dimension", "capability"],
                "official_definition": "Ability to adapt verbal and nonverbal behavior across culturally diverse contexts.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_cqs_behavior_gap_limit",
                "inference_type": "practical_limit",
                "text": (
                    "CQS is valuable because it names a context-specific capability layer, but self-report cultural "
                    "adaptability can diverge sharply from observed intercultural behavior under stress or ambiguity."
                ),
                "confidence": "high",
                "linked_entities": ["instr_big_five"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_cqs_cq_pro_assessment",
                "resource_type": "assessment_page",
                "title": "CQ Pro Assessment",
                "url": "https://culturalq.com/cq-store/assessments/cq-pro-assessment/",
                "publisher": "Cultural Intelligence Center",
                "officiality": "official",
                "notes": "Official product page describing the CQ Pro assessment and its use in development and benchmarking.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_cqs_self_report_inflation",
                "risk_type": "self_report_distortion",
                "severity": "medium",
                "description": (
                    "Respondents can overestimate intercultural skill, especially when social desirability and global-minded "
                    "self-image are in play."
                ),
                "mitigation": "Pair CQS with observed behavior, multisource feedback, or performance evidence in diverse contexts.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_cqs_coaching",
                "use_context": "coaching",
                "utility_type": "developmental_reflection",
                "suitability_level": "high",
                "cautions": "Best used with concrete cultural scenarios and feedback loops rather than abstract self-ratings alone.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_cqs_big_five_contextual_capability",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_cqs",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_big_five",
                "relationship_type": "different_layer_of_personhood",
                "relationship_strength": "medium",
                "rationale": (
                    "CQS measures context-specific intercultural capability, while Big Five measures broad trait tendencies. "
                    "Both matter for cross-cultural effectiveness, but they operate at different explanatory layers."
                ),
                "confidence": "high",
                "notes": "House comparison between capability and trait layers.",
            }
        ],
    },
    "culture-index": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_culture_index_free_choice_method",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "Culture Index materials describe the assessment as using a fast adjective-based, free-choice format "
                    "to infer stable work-related behavioral tendencies."
                ),
                "source_resource_ids": ["res_culture_index_overview"],
            },
            {
                "id": "clm_culture_index_role_fit_usage",
                "claim_type": "usage_claim",
                "claim_text": (
                    "Culture Index positions its flagship C-Analyst output for role fit, management, and hiring-related "
                    "decision support inside organizations."
                ),
                "source_resource_ids": ["res_culture_index_c_analyst"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_culture_index_autonomy",
                "name": "Autonomy",
                "short_name": "Autonomy",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "Assertive independence and willingness to initiate or direct activity without needing heavy external structure.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_culture_index_social_ability",
                "name": "Social Ability",
                "short_name": "Social Ability",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "Comfort with social interaction, networking, persuasion, and interpersonal contact.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_culture_index_patience",
                "name": "Patience",
                "short_name": "Patience",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "Preference for steadiness, consistency, and tolerating slower or more repetitive work rhythms.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_culture_index_conformity",
                "name": "Conformity",
                "short_name": "Conformity",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "Orientation toward structure, rules, precision, and disciplined adherence to standards.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_culture_index_energy_units",
                "name": "Energy Units",
                "short_name": "Energy Units",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "General energy level and stamina available for sustained work output.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_culture_index_logic",
                "name": "Logic",
                "short_name": "Logic",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "Preference for analytical reasoning, problem solving, and evidence-based judgment.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_culture_index_ingenuity",
                "name": "Ingenuity",
                "short_name": "Ingenuity",
                "construct_kind": ["trait", "work_trait"],
                "official_definition": "Tendency toward inventiveness, originality, and generating new approaches or solutions.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_culture_index_opacity_limit",
                "inference_type": "practical_limit",
                "text": (
                    "Culture Index is explicitly optimized for managerial action, but the proprietary and high-stakes nature "
                    "of its deployment makes opacity a bigger practical problem than in lower-stakes self-reflection tools."
                ),
                "confidence": "high",
                "linked_entities": ["instr_disc", "instr_cliftonstrengths"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_culture_index_c_analyst",
                "resource_type": "assessment_page",
                "title": "C-Analyst",
                "url": "https://www.cultureindex.com/c-analyst",
                "publisher": "Culture Index, LLC",
                "officiality": "official",
                "notes": "Official product page describing the flagship Culture Index assessment and its role in talent and fit decisions.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_culture_index_black_box_hiring",
                "risk_type": "workplace_misuse",
                "severity": "high",
                "description": (
                    "When proprietary profile outputs are treated as objective hiring truth, they can harden bias and "
                    "false precision inside employment decisions."
                ),
                "mitigation": "Keep Culture Index subordinate to structured interviews, job-relevant evidence, and explicit adverse-impact review.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_culture_index_team_design",
                "use_context": "team_design",
                "utility_type": "communication_adaptation",
                "suitability_level": "medium",
                "cautions": "Useful as a team heuristic only if the organization preserves uncertainty and avoids role essentialism.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_culture_index_disc_workplace",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_culture_index",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_disc",
                "relationship_type": "methodologically_similar",
                "relationship_strength": "medium",
                "rationale": (
                    "Culture Index and DISC are both used as brief workplace behavior-profiling tools, though Culture Index is more explicitly "
                    "positioned for hiring and role-fit workflows."
                ),
                "confidence": "medium",
                "notes": "Comparative workplace mapping based on deployment pattern rather than construct equivalence.",
            }
        ],
    },
    "dark-triad": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_dark_triad_construct_distinctness",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Dark Triad research treats narcissism, Machiavellianism, and psychopathy as related but distinct "
                    "socially aversive traits rather than as a single unitary construct."
                ),
                "source_resource_ids": ["res_dark_triad_overview"],
            },
            {
                "id": "clm_dark_triad_subclinical_scope",
                "claim_type": "theoretical_claim",
                "claim_text": (
                    "The Dark Triad is typically framed as a subclinical personality cluster, not as a substitute for "
                    "formal clinical diagnosis."
                ),
                "source_resource_ids": ["res_dark_triad_review"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_dark_triad_narcissism",
                "name": "Narcissism",
                "short_name": "Narcissism",
                "construct_kind": ["trait", "dark_trait"],
                "official_definition": "Grandiose self-focus, entitlement, and desire for admiration or status.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_dark_triad_machiavellianism",
                "name": "Machiavellianism",
                "short_name": "Machiavellianism",
                "construct_kind": ["trait", "dark_trait"],
                "official_definition": "Strategic manipulation, cynical social calculation, and willingness to use others instrumentally.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_dark_triad_psychopathy",
                "name": "Psychopathy",
                "short_name": "Psychopathy",
                "construct_kind": ["trait", "dark_trait"],
                "official_definition": "Callousness, impulsivity, low empathy, and diminished concern for harm to others.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_dark_triad_not_balanced_model",
                "inference_type": "practical_limit",
                "text": (
                    "The Dark Triad is valuable for aversive-trait and interpersonal-risk analysis, but it is too narrow "
                    "to function as a balanced developmental or whole-person framework."
                ),
                "confidence": "high",
                "linked_entities": ["instr_hexaco", "instr_big_five"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_dark_triad_review",
                "resource_type": "review",
                "title": "Dark Triad personality: At the heart of darkness",
                "url": "https://pubmed.ncbi.nlm.nih.gov/29106280/",
                "publisher": "PubMed",
                "officiality": "secondary",
                "notes": "Abstract page for a review article summarizing the structure, correlates, and interpretation of Dark Triad constructs.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_dark_triad_hexaco_inverse",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_dark_triad",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_hexaco",
                "relationship_type": "inverse_tendency",
                "relationship_strength": "medium",
                "rationale": (
                    "Dark Triad constructs frequently sit in inverse relation to prosociality-related HEXACO patterns, especially around "
                    "Honesty-Humility, but they are not reducible to a single HEXACO domain."
                ),
                "confidence": "high",
                "notes": "House comparison highlighting an important aversive-traits versus honesty-humility contrast.",
            },
            {
                "id": "xwk_dark_triad_narcissism_hexaco_honesty_humility",
                "source_entity_type": "construct",
                "source_entity_id": "con_dark_triad_narcissism",
                "target_entity_type": "construct",
                "target_entity_id": "con_hexaco_honesty_humility",
                "relationship_type": "inverse_tendency",
                "relationship_strength": "medium",
                "rationale": (
                    "Grandiose entitlement and self-importance often pull against the modesty and fairness facets central "
                    "to HEXACO Honesty-Humility, though narcissism also carries variance not captured by that single domain."
                ),
                "confidence": "medium",
                "notes": "A directional contrast, not a full reduction.",
            },
            {
                "id": "xwk_dark_triad_machiavellianism_hexaco_honesty_humility",
                "source_entity_type": "construct",
                "source_entity_id": "con_dark_triad_machiavellianism",
                "target_entity_type": "construct",
                "target_entity_id": "con_hexaco_honesty_humility",
                "relationship_type": "inverse_tendency",
                "relationship_strength": "high",
                "rationale": (
                    "Machiavellianism's manipulativeness and instrumental cynicism cut strongly against the sincerity and "
                    "fairness profile associated with HEXACO Honesty-Humility."
                ),
                "confidence": "high",
                "notes": "One of the clearest construct-level cross-system contrasts in the registry.",
            },
            {
                "id": "xwk_dark_triad_psychopathy_hexaco_agreeableness",
                "source_entity_type": "construct",
                "source_entity_id": "con_dark_triad_psychopathy",
                "target_entity_type": "construct",
                "target_entity_id": "con_hexaco_agreeableness",
                "relationship_type": "inverse_tendency",
                "relationship_strength": "high",
                "rationale": (
                    "Psychopathy's callousness and antagonism often sit opposite the forgiveness and gentleness "
                    "emphasized by HEXACO Agreeableness, while still extending beyond that domain in impulsivity and fearlessness."
                ),
                "confidence": "high",
                "notes": "Useful comparative anchor for aversive versus prosocial trait structure.",
            },
        ],
        "extra_risks": [
            {
                "id": "rsk_dark_triad_stigmatization",
                "risk_type": "stigmatization",
                "severity": "high",
                "description": (
                    "Dark Triad labels can be used as moral condemnation or amateur diagnosis, especially in online discourse "
                    "where subclinical constructs are flattened into villain labels."
                ),
                "mitigation": "Keep the framework tied to narrow construct interpretation and avoid using it as a total-person verdict.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_dark_triad_research",
                "use_context": "research",
                "utility_type": "aversive_trait_comparison",
                "suitability_level": "high",
                "cautions": (
                    "Most useful for research, comparative trait analysis, and narrow risk interpretation rather than everyday identity labeling."
                ),
            }
        ],
    },
    "disc": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_disc_style_patterns",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Contemporary DiSC materials frame behavior as patterned combinations of Dominance, Influence, "
                    "Steadiness, and Conscientiousness rather than as rigid one-box types."
                ),
                "source_resource_ids": ["res_disc_what_is_disc"],
            },
            {
                "id": "clm_disc_workplace_application",
                "claim_type": "usage_claim",
                "claim_text": (
                    "Everything DiSC positions the model as a tool for communication, teamwork, conflict discussion, "
                    "and other workplace interaction workflows."
                ),
                "source_resource_ids": ["res_disc_overview", "res_disc_what_is_disc"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_disc_dominance",
                "name": "Dominance",
                "short_name": "D",
                "construct_kind": ["dimension", "style"],
                "official_definition": "Direct, forceful, and results-focused behavioral style oriented toward challenge and control.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_disc_influence",
                "name": "Influence",
                "short_name": "I",
                "construct_kind": ["dimension", "style"],
                "official_definition": "Outgoing, persuasive, and socially expressive behavioral style oriented toward enthusiasm and interaction.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_disc_steadiness",
                "name": "Steadiness",
                "short_name": "S",
                "construct_kind": ["dimension", "style"],
                "official_definition": "Patient, accommodating, and cooperative behavioral style oriented toward consistency and support.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_disc_conscientiousness",
                "name": "Conscientiousness",
                "short_name": "C",
                "construct_kind": ["dimension", "style"],
                "official_definition": "Careful, systematic, and quality-focused behavioral style oriented toward standards and accuracy.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_disc_conversation_starter_limit",
                "inference_type": "practical_limit",
                "text": (
                    "DISC is strongest as a lightweight conversation starter about interaction style and weakest when it "
                    "is stretched into motive analysis, deep personality theory, or selection logic."
                ),
                "confidence": "high",
                "linked_entities": ["instr_culture_index", "instr_mbti"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_disc_what_is_disc",
                "resource_type": "overview",
                "title": "What Is DiSC?",
                "url": "https://www.everythingdisc.com/what-is-disc/",
                "publisher": "Everything DiSC / John Wiley & Sons",
                "officiality": "semi_official",
                "notes": "Commercial overview page describing the DiSC model and common workplace uses.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_disc_workplace_misuse",
                "risk_type": "workplace_misuse",
                "severity": "medium",
                "description": (
                    "DISC labels are often reified into stable workplace identities or used to justify simplistic assumptions "
                    "about collaboration, conflict, or role fit."
                ),
                "mitigation": "Use DiSC for communication prompts and avoid treating profile language as a full employment decision rule.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_disc_team_design",
                "use_context": "team_design",
                "utility_type": "communication_adaptation",
                "suitability_level": "high",
                "cautions": "Most useful for team communication norms, not for assigning fixed identities or career ceilings.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_disc_culture_index_workplace",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_disc",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_culture_index",
                "relationship_type": "methodologically_similar",
                "relationship_strength": "medium",
                "rationale": (
                    "DISC and Culture Index are often deployed as lightweight workplace behavior tools, even though their proprietary ecosystems "
                    "and interpretive claims differ."
                ),
                "confidence": "medium",
                "notes": "Comparative mapping based on shared organizational use patterns.",
            },
            {
                "id": "xwk_disc_dominance_culture_index_autonomy",
                "source_entity_type": "construct",
                "source_entity_id": "con_disc_dominance",
                "target_entity_type": "construct",
                "target_entity_id": "con_culture_index_autonomy",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "DISC Dominance and Culture Index Autonomy both point toward assertive, self-directed behavioral expression, "
                    "though they come from different workplace profiling systems."
                ),
                "confidence": "medium",
                "notes": "House construct mapping across adjacent workplace behavior models.",
            },
            {
                "id": "xwk_disc_influence_culture_index_social_ability",
                "source_entity_type": "construct",
                "source_entity_id": "con_disc_influence",
                "target_entity_type": "construct",
                "target_entity_id": "con_culture_index_social_ability",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "DISC Influence and Culture Index Social Ability both occupy an interpersonal expressiveness and persuasion zone."
                ),
                "confidence": "medium",
                "notes": "Useful but non-equivalent translation across workplace interaction constructs.",
            },
            {
                "id": "xwk_disc_steadiness_culture_index_patience",
                "source_entity_type": "construct",
                "source_entity_id": "con_disc_steadiness",
                "target_entity_type": "construct",
                "target_entity_id": "con_culture_index_patience",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "DISC Steadiness and Culture Index Patience both point toward consistency, stability, and tolerance for steadier rhythms."
                ),
                "confidence": "medium",
                "notes": "Construct-level overlap for slower-paced, stability-seeking work styles.",
            },
            {
                "id": "xwk_disc_conscientiousness_culture_index_conformity",
                "source_entity_type": "construct",
                "source_entity_id": "con_disc_conscientiousness",
                "target_entity_type": "construct",
                "target_entity_id": "con_culture_index_conformity",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "DISC Conscientiousness and Culture Index Conformity both describe orientation toward rules, quality, and structured standards."
                ),
                "confidence": "medium",
                "notes": "House construct mapping for order- and precision-oriented work behavior.",
            }
        ],
    },
    "hexaco": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_hexaco_form_variants",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "The HEXACO-PI-R is available in multiple questionnaire lengths and in both self-report and observer-report forms."
                ),
                "source_resource_ids": ["res_hexaco_overview"],
            },
            {
                "id": "clm_hexaco_facet_structure",
                "claim_type": "construct_claim",
                "claim_text": (
                    "HEXACO materials describe each of the six broad dimensions through a facet structure rather than only top-level trait scores."
                ),
                "source_resource_ids": ["res_hexaco_scale_descriptions"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_hexaco_honesty_humility",
                "name": "Honesty-Humility",
                "short_name": "Honesty-Humility",
                "construct_kind": ["trait", "dimension"],
                "official_definition": "Sincerity, fairness, modesty, and lack of entitlement or exploitation.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_hexaco_emotionality",
                "name": "Emotionality",
                "short_name": "Emotionality",
                "construct_kind": ["trait", "dimension"],
                "official_definition": "Fearfulness, anxiety, dependence, and emotional sensitivity.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_hexaco_extraversion",
                "name": "Extraversion",
                "short_name": "Extraversion",
                "construct_kind": ["trait", "dimension"],
                "official_definition": "Social self-confidence, sociability, liveliness, and positive engagement with others.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_hexaco_agreeableness",
                "name": "Agreeableness",
                "short_name": "Agreeableness",
                "construct_kind": ["trait", "dimension"],
                "official_definition": "Forgiveness, gentleness, flexibility, and tolerance in interpersonal conflict.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_hexaco_conscientiousness",
                "name": "Conscientiousness",
                "short_name": "Conscientiousness",
                "construct_kind": ["trait", "dimension"],
                "official_definition": "Organization, diligence, prudence, and disciplined goal-directedness.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_hexaco_openness",
                "name": "Openness to Experience",
                "short_name": "Openness",
                "construct_kind": ["trait", "dimension"],
                "official_definition": "Curiosity, aesthetic appreciation, creativity, and receptivity to novel ideas or experiences.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_hexaco_narrative_limit",
                "inference_type": "practical_limit",
                "text": (
                    "HEXACO is one of the strongest trait anchors in the registry, but like other lexical trait models it is "
                    "not optimized to name motive, defense, or narrative identity in thick terms."
                ),
                "confidence": "high",
                "linked_entities": ["instr_big_five", "instr_enneagram"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_hexaco_scale_descriptions",
                "resource_type": "reference",
                "title": "HEXACO Scale Descriptions",
                "url": "https://hexaco.org/scaledescriptions",
                "publisher": "HEXACO",
                "officiality": "official",
                "notes": "Official descriptions of the six HEXACO dimensions and their facet structure.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_hexaco_self_report_distortion",
                "risk_type": "self_report_distortion",
                "severity": "medium",
                "description": (
                    "HEXACO self-report results can still be shifted by impression management, self-deception, and situational answering."
                ),
                "mitigation": "Use observer reports, repeated administrations, or external behavioral evidence when the stakes are high.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_hexaco_research",
                "use_context": "research",
                "utility_type": "comparative_trait_analysis",
                "suitability_level": "high",
                "cautions": "Particularly strong for trait comparison and research synthesis, but still incomplete as a stand-alone person model.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_hexaco_big_five_trait_neighbor",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_hexaco",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_big_five",
                "relationship_type": "strong_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "HEXACO and Big Five are neighboring broad trait frameworks with substantial overlap, though HEXACO adds "
                    "Honesty-Humility and re-cuts some interpersonal-emotional variance."
                ),
                "confidence": "high",
                "notes": "One of the closest cross-framework trait comparisons in the registry.",
            },
            {
                "id": "xwk_hexaco_honesty_humility_dark_triad",
                "source_entity_type": "construct",
                "source_entity_id": "con_hexaco_honesty_humility",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_dark_triad",
                "relationship_type": "inverse_tendency",
                "relationship_strength": "high",
                "rationale": (
                    "Honesty-Humility often moves inversely to manipulative, exploitative, and entitled tendencies that cluster in Dark Triad measures."
                ),
                "confidence": "high",
                "notes": "Construct-to-instrument mapping because the inverse relation spans multiple dark-trait constructs.",
            },
            {
                "id": "xwk_hexaco_emotionality_big_five_neuroticism",
                "source_entity_type": "construct",
                "source_entity_id": "con_hexaco_emotionality",
                "target_entity_type": "construct",
                "target_entity_id": "con_big_five_neuroticism",
                "relationship_type": "strong_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "HEXACO Emotionality and Big Five Neuroticism share substantial variance around anxiety and emotional sensitivity, "
                    "even though HEXACO Emotionality also packages dependence and sentimentality somewhat differently."
                ),
                "confidence": "high",
                "notes": "Close neighboring trait constructs with non-identical composition.",
            },
            {
                "id": "xwk_hexaco_extraversion_big_five_extraversion",
                "source_entity_type": "construct",
                "source_entity_id": "con_hexaco_extraversion",
                "target_entity_type": "construct",
                "target_entity_id": "con_big_five_extraversion",
                "relationship_type": "strong_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "Extraversion is one of the cleanest overlap zones between HEXACO and Big Five, covering sociability, liveliness, and social confidence."
                ),
                "confidence": "high",
                "notes": "High-confidence neighboring trait mapping.",
            },
            {
                "id": "xwk_hexaco_agreeableness_big_five_agreeableness",
                "source_entity_type": "construct",
                "source_entity_id": "con_hexaco_agreeableness",
                "target_entity_type": "construct",
                "target_entity_id": "con_big_five_agreeableness",
                "relationship_type": "partial_translation",
                "relationship_strength": "medium",
                "rationale": (
                    "HEXACO Agreeableness and Big Five Agreeableness overlap around interpersonal softness and tolerance, "
                    "but the models cut some interpersonal content differently, especially alongside Honesty-Humility."
                ),
                "confidence": "high",
                "notes": "Related but not one-to-one because interpersonal variance is partitioned differently across the models.",
            },
            {
                "id": "xwk_hexaco_conscientiousness_big_five_conscientiousness",
                "source_entity_type": "construct",
                "source_entity_id": "con_hexaco_conscientiousness",
                "target_entity_type": "construct",
                "target_entity_id": "con_big_five_conscientiousness",
                "relationship_type": "strong_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "Conscientiousness is another close overlap zone between HEXACO and Big Five, centered on organization, diligence, and self-discipline."
                ),
                "confidence": "high",
                "notes": "High-confidence neighboring trait mapping.",
            },
            {
                "id": "xwk_hexaco_openness_big_five_openness",
                "source_entity_type": "construct",
                "source_entity_id": "con_hexaco_openness",
                "target_entity_type": "construct",
                "target_entity_id": "con_big_five_openness",
                "relationship_type": "strong_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "Openness to Experience is a major shared factor between HEXACO and Big Five, covering curiosity, aesthetics, and receptivity to novelty."
                ),
                "confidence": "high",
                "notes": "High-confidence neighboring trait mapping.",
            }
        ],
    },
    "human-design": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_human_design_lineage_synthesis",
                "claim_type": "theoretical_claim",
                "claim_text": (
                    "Human Design presents itself as a synthesis of multiple esoteric and scientific lineages rather "
                    "than as a standard psychometric personality inventory."
                ),
                "source_resource_ids": ["res_human_design_overview"],
            },
            {
                "id": "clm_human_design_chart_outputs",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "Official chart-generation materials position birth data as sufficient to generate a BodyGraph with "
                    "typed outputs such as Type, Authority, and Profile."
                ),
                "source_resource_ids": ["res_human_design_chart"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_human_design_generator",
                "name": "Generator",
                "short_name": "Generator",
                "construct_kind": ["type", "aura_type"],
                "official_definition": "A sacral energy type whose strategy is to respond and who carries the dominant life-force energy in the system.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_human_design_manifestor",
                "name": "Manifestor",
                "short_name": "Manifestor",
                "construct_kind": ["type", "aura_type"],
                "official_definition": "An initiating type whose strategy is to inform before acting and whose aura is described as closed and repelling.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_human_design_projector",
                "name": "Projector",
                "short_name": "Projector",
                "construct_kind": ["type", "aura_type"],
                "official_definition": "A non-sacral guiding type whose strategy is to wait for recognition and invitation.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_human_design_reflector",
                "name": "Reflector",
                "short_name": "Reflector",
                "construct_kind": ["type", "aura_type"],
                "official_definition": "A rare type with no fixed centers whose strategy is to wait through a lunar cycle before major decisions.",
                "scoring_type": "type_assignment",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_human_design_practitioner_burden",
                "inference_type": "practical_limit",
                "text": (
                    "Human Design carries a very high practitioner and community burden: meaning is often stabilized by "
                    "teachers, lineages, and ongoing interpretation rather than by a transparent measurement model."
                ),
                "confidence": "high",
                "linked_entities": ["instr_natal_astrology", "instr_enneagram"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_human_design_chart",
                "resource_type": "chart_generator",
                "title": "Get Your Chart",
                "url": "https://jovianarchive.com/Get_Your_Chart",
                "publisher": "Jovian Archive",
                "officiality": "official",
                "notes": "Official chart generator entry point used to produce a Human Design BodyGraph from birth data.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_human_design_identity_capture",
                "risk_type": "identity_capture",
                "severity": "high",
                "description": (
                    "Because Human Design offers a thick cosmology and precise chart language, users can fuse strongly "
                    "with type, authority, or profile labels and externalize agency to the system."
                ),
                "mitigation": "Use Human Design as symbolic reflection only if the user preserves agency, context, and the right to disagree with the chart.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_human_design_coaching",
                "use_context": "coaching",
                "utility_type": "symbolic_reflection",
                "suitability_level": "medium",
                "cautions": "Useful only when the symbolic frame is explicit and not confused with empirical measurement or fate.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_human_design_natal_astrology_derived",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_human_design",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_natal_astrology",
                "relationship_type": "derived_from",
                "relationship_strength": "high",
                "rationale": (
                    "Human Design explicitly incorporates astrology among its source lineages and depends on birth-chart style inputs "
                    "for BodyGraph generation."
                ),
                "confidence": "high",
                "notes": "Lineage-oriented mapping rather than an equivalence claim.",
            }
        ],
    },
    "kolbe": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_kolbe_action_modes",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Kolbe materials describe conative action through four Action Modes: Fact Finder, Follow Thru, "
                    "Quick Start, and Implementor."
                ),
                "source_resource_ids": ["res_kolbe_overview"],
            },
            {
                "id": "clm_kolbe_retest_stability",
                "claim_type": "evidence_claim",
                "claim_text": (
                    "Kolbe publishes test-retest evidence in support of the claim that Action Mode patterns are relatively stable over time."
                ),
                "source_resource_ids": ["res_kolbe_retest_reliability"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_kolbe_fact_finder",
                "name": "Fact Finder",
                "short_name": "Fact Finder",
                "construct_kind": ["action_mode", "dimension"],
                "official_definition": "Instinctive approach to probing, researching, and specifying details before acting.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_kolbe_follow_thru",
                "name": "Follow Thru",
                "short_name": "Follow Thru",
                "construct_kind": ["action_mode", "dimension"],
                "official_definition": "Instinctive approach to organizing, sequencing, and structuring work through systems and process.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_kolbe_quick_start",
                "name": "Quick Start",
                "short_name": "Quick Start",
                "construct_kind": ["action_mode", "dimension"],
                "official_definition": "Instinctive approach to dealing with risk, improvisation, and experimentation under uncertainty.",
                "scoring_type": "continuous",
            },
            {
                "id": "con_kolbe_implementor",
                "name": "Implementor",
                "short_name": "Implementor",
                "construct_kind": ["action_mode", "dimension"],
                "official_definition": "Instinctive approach to handling space, tangibles, and hands-on physical implementation.",
                "scoring_type": "continuous",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_kolbe_conative_limit",
                "inference_type": "practical_limit",
                "text": (
                    "Kolbe is best read as a narrow conative execution layer. It can clarify how someone tackles work, "
                    "but it says relatively little about motive, values, or broader personality structure."
                ),
                "confidence": "high",
                "linked_entities": ["instr_cliftonstrengths", "instr_big_five"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_kolbe_retest_reliability",
                "resource_type": "technical_report",
                "title": "Analysis of the Kolbe A Index: Test-Retest Reliability",
                "url": "https://assets.kolbe.com/wp-content/uploads/20250114180834/TestReTest_Kolbe-A-Index_October2018_FINAL-3.pdf",
                "publisher": "Kolbe Corp",
                "officiality": "official",
                "notes": "Official technical report focused on Kolbe A Index test-retest stability across Action Modes.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_kolbe_role_essentialism",
                "risk_type": "workplace_misuse",
                "severity": "medium",
                "description": (
                    "Stable action-style language can be overextended into claims about who should or should not hold a role, "
                    "especially in hiring or job-fit settings."
                ),
                "mitigation": "Treat Kolbe as workflow insight, not as a comprehensive talent or hiring screen.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_kolbe_team_design",
                "use_context": "team_design",
                "utility_type": "workflow_design",
                "suitability_level": "high",
                "cautions": "Useful for execution and handoff design, but weak when converted into fixed judgments about total capability.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_kolbe_cliftonstrengths_work_layers",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_kolbe",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_cliftonstrengths",
                "relationship_type": "complementary_non_equivalent",
                "relationship_strength": "medium",
                "rationale": (
                    "Kolbe and CliftonStrengths both circulate in work-development settings, but Kolbe emphasizes instinctive action style "
                    "while CliftonStrengths emphasizes talent themes and development language."
                ),
                "confidence": "high",
                "notes": "House mapping across adjacent workplace-development systems.",
            }
        ],
    },
    "love-languages": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_love_languages_five_categories",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Official Love Languages materials organize preferred expressions of care into five categories: Words of "
                    "Affirmation, Quality Time, Receiving Gifts, Acts of Service, and Physical Touch."
                ),
                "source_resource_ids": ["res_love_languages_overview"],
            },
            {
                "id": "clm_love_languages_relational_application",
                "claim_type": "usage_claim",
                "claim_text": (
                    "The Love Languages ecosystem positions the framework as a practical relationship tool for improving "
                    "understanding and communication in romantic and family settings."
                ),
                "source_resource_ids": ["res_love_languages_home"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_love_languages_words_of_affirmation",
                "name": "Words of Affirmation",
                "short_name": "Words of Affirmation",
                "construct_kind": ["type", "preference"],
                "official_definition": "Valuing verbal expressions of appreciation, encouragement, and affection.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_love_languages_quality_time",
                "name": "Quality Time",
                "short_name": "Quality Time",
                "construct_kind": ["type", "preference"],
                "official_definition": "Valuing focused presence, shared attention, and undistracted time together.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_love_languages_receiving_gifts",
                "name": "Receiving Gifts",
                "short_name": "Receiving Gifts",
                "construct_kind": ["type", "preference"],
                "official_definition": "Valuing tangible symbols of care, thoughtfulness, and remembrance.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_love_languages_acts_of_service",
                "name": "Acts of Service",
                "short_name": "Acts of Service",
                "construct_kind": ["type", "preference"],
                "official_definition": "Valuing helpful actions that reduce burden or demonstrate care through effort.",
                "scoring_type": "type_assignment",
            },
            {
                "id": "con_love_languages_physical_touch",
                "name": "Physical Touch",
                "short_name": "Physical Touch",
                "construct_kind": ["type", "preference"],
                "official_definition": "Valuing affectionate physical contact as a primary signal of closeness and care.",
                "scoring_type": "type_assignment",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_love_languages_low_resolution_limit",
                "inference_type": "practical_limit",
                "text": (
                    "Love Languages endures because it is low-friction and easy to use, but that same simplicity leaves it "
                    "too low-resolution to capture attachment dynamics, power, conflict, or developmental history."
                ),
                "confidence": "high",
                "linked_entities": ["instr_attachment_styles"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_love_languages_home",
                "resource_type": "overview",
                "title": "The 5 Love Languages",
                "url": "https://5lovelanguages.com/",
                "publisher": "Love Language Brand",
                "officiality": "official",
                "notes": "Official home page for the Five Love Languages brand ecosystem and associated materials.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_love_languages_relational_reductionism",
                "risk_type": "overinterpretation",
                "severity": "medium",
                "description": (
                    "Relationship problems can be reduced to a single favorite language, obscuring conflict style, attachment, resentment, or structural issues."
                ),
                "mitigation": "Use the framework as a conversation opener and pair it with richer models of relationship dynamics.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_love_languages_relationship_support",
                "use_context": "relationship_support",
                "utility_type": "communication_adaptation",
                "suitability_level": "medium",
                "cautions": "Helpful for naming preference mismatches, but too thin to stand alone as a relationship theory.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_love_languages_attachment_styles_overlap",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_love_languages",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_attachment_styles",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "Love Languages and attachment frameworks both show up in relationship discourse, but they address different questions: "
                    "preferred expressions of care versus security and regulation dynamics."
                ),
                "confidence": "high",
                "notes": "Useful relational crosswalk for agents navigating popular relationship frameworks.",
            }
        ],
    },
    "natal-astrology": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_natal_astrology_chart_components",
                "claim_type": "construct_claim",
                "claim_text": (
                    "Natal astrology interprets personality and life themes through the combined symbolism of planets, "
                    "signs, houses, and aspects within a birth chart."
                ),
                "source_resource_ids": ["res_natal_astrology_astrowiki"],
            },
            {
                "id": "clm_natal_astrology_birth_data_requirement",
                "claim_type": "implementation_claim",
                "claim_text": (
                    "Birth-chart tools position exact birth date, time, and location as the required inputs for generating a natal chart."
                ),
                "source_resource_ids": ["res_natal_astrology_overview"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_natal_astrology_planets",
                "name": "Planets",
                "short_name": "Planets",
                "construct_kind": ["chart_component"],
                "official_definition": "Planetary placements representing distinct functions, drives, or principles within the natal chart.",
                "scoring_type": "chart_interpretation",
            },
            {
                "id": "con_natal_astrology_signs",
                "name": "Signs",
                "short_name": "Signs",
                "construct_kind": ["chart_component"],
                "official_definition": "Zodiac signs that color how planets and angles are expressed in the chart.",
                "scoring_type": "chart_interpretation",
            },
            {
                "id": "con_natal_astrology_houses",
                "name": "Houses",
                "short_name": "Houses",
                "construct_kind": ["chart_component"],
                "official_definition": "Twelve chart sectors describing life areas in which planetary and zodiacal themes are expressed.",
                "scoring_type": "chart_interpretation",
            },
            {
                "id": "con_natal_astrology_aspects",
                "name": "Aspects",
                "short_name": "Aspects",
                "construct_kind": ["chart_component"],
                "official_definition": "Angular relationships between planets that describe how chart components interact with one another.",
                "scoring_type": "chart_interpretation",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_natal_astrology_empirical_limit",
                "inference_type": "practical_limit",
                "text": (
                    "Natal astrology is a powerful symbolic and narrative language, but it should be treated as interpretive meaning-making rather than evidence-based measurement."
                ),
                "confidence": "high",
                "linked_entities": ["instr_human_design"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_natal_astrology_astrowiki",
                "resource_type": "reference",
                "title": "Birth Chart",
                "url": "https://www.astro.com/astrowiki/en/Birth_Chart",
                "publisher": "Astrodienst AstroWiki",
                "officiality": "secondary",
                "notes": "Reference page explaining the birth chart as the core interpretive object in natal astrology.",
            }
        ],
        "extra_risks": [
            {
                "id": "rsk_natal_astrology_identity_capture",
                "risk_type": "identity_capture",
                "severity": "high",
                "description": (
                    "People can fuse with chart descriptions and use astrology as a durable explanatory frame that crowds out context, agency, and developmental change."
                ),
                "mitigation": "Keep astrology in the symbolic lane and avoid treating chart interpretation as total identity truth.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_natal_astrology_coaching",
                "use_context": "coaching",
                "utility_type": "symbolic_reflection",
                "suitability_level": "medium",
                "cautions": "Useful for symbolic reflection only when the interpretive nature of the system stays explicit.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_natal_astrology_human_design_lineage",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_natal_astrology",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_human_design",
                "relationship_type": "historically_related",
                "relationship_strength": "high",
                "rationale": (
                    "Natal astrology and Human Design occupy overlapping symbolic territory, and Human Design inherits part of its symbolic "
                    "machinery from astrology while building a newer composite system on top."
                ),
                "confidence": "high",
                "notes": "Lineage-aware symbolic systems mapping.",
            }
        ],
    },
    "via-character-strengths": {
        "include_primary_construct": False,
        "extra_claims": [
            {
                "id": "clm_via_character_strengths_six_virtues",
                "claim_type": "construct_claim",
                "claim_text": (
                    "The VIA classification groups 24 character strengths under six broad virtue categories: Wisdom, "
                    "Courage, Humanity, Justice, Temperance, and Transcendence."
                ),
                "source_resource_ids": ["res_via_character_strengths_overview"],
            },
            {
                "id": "clm_via_character_strengths_applied_development",
                "claim_type": "usage_claim",
                "claim_text": (
                    "VIA materials position character strengths as capacities that can be identified and developed for "
                    "greater flourishing across coaching, education, and well-being practice."
                ),
                "source_resource_ids": ["res_via_character_strengths_character_strengths_page"],
            },
        ],
        "extra_constructs": [
            {
                "id": "con_via_wisdom",
                "name": "Wisdom",
                "short_name": "Wisdom",
                "construct_kind": ["virtue_domain", "dimension"],
                "official_definition": "Virtue domain covering strengths involved in acquiring and using knowledge well.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_via_courage",
                "name": "Courage",
                "short_name": "Courage",
                "construct_kind": ["virtue_domain", "dimension"],
                "official_definition": "Virtue domain covering strengths involved in will, perseverance, and action despite difficulty.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_via_humanity",
                "name": "Humanity",
                "short_name": "Humanity",
                "construct_kind": ["virtue_domain", "dimension"],
                "official_definition": "Virtue domain covering strengths of care, love, and interpersonal warmth.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_via_justice",
                "name": "Justice",
                "short_name": "Justice",
                "construct_kind": ["virtue_domain", "dimension"],
                "official_definition": "Virtue domain covering strengths that support fairness, citizenship, and leadership in collective life.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_via_temperance",
                "name": "Temperance",
                "short_name": "Temperance",
                "construct_kind": ["virtue_domain", "dimension"],
                "official_definition": "Virtue domain covering strengths that regulate excess and support balance or restraint.",
                "scoring_type": "rank_order_grouping",
            },
            {
                "id": "con_via_transcendence",
                "name": "Transcendence",
                "short_name": "Transcendence",
                "construct_kind": ["virtue_domain", "dimension"],
                "official_definition": "Virtue domain covering strengths that connect a person to meaning, awe, hope, and appreciation.",
                "scoring_type": "rank_order_grouping",
            },
        ],
        "extra_inferences": [
            {
                "id": "inf_via_character_strengths_shadow_limits",
                "inference_type": "practical_limit",
                "text": (
                    "VIA is unusually strong for positive-personality and virtue language, but it under-describes shadow, "
                    "defense, and exploitative behavior compared with darker or more conflict-oriented frameworks."
                ),
                "confidence": "high",
                "linked_entities": ["instr_cliftonstrengths", "instr_dark_triad"],
            }
        ],
        "extra_resources": [
            {
                "id": "res_via_character_strengths_character_strengths_page",
                "resource_type": "overview",
                "title": "Character Strengths",
                "url": "https://www.viacharacter.org/character-strengths",
                "publisher": "VIA Institute on Character",
                "officiality": "official",
                "notes": "Official overview page describing VIA character strengths and their use in practice.",
            }
        ],
        "crosswalks": [
            {
                "id": "xwk_via_cliftonstrengths_strengths",
                "source_entity_type": "instrument",
                "source_entity_id": "instr_via_character_strengths",
                "target_entity_type": "instrument",
                "target_entity_id": "instr_cliftonstrengths",
                "relationship_type": "same_layer_different_cut",
                "relationship_strength": "medium",
                "rationale": (
                    "VIA and CliftonStrengths both offer strengths-based person description, but VIA is virtue-oriented and more explicitly "
                    "grounded in positive psychology, whereas CliftonStrengths is a branded talent-development system."
                ),
                "confidence": "high",
                "notes": "Comparative mapping across strengths vocabularies with different moral and workplace emphasis.",
            },
            {
                "id": "xwk_via_wisdom_cliftonstrengths_strategic_thinking",
                "source_entity_type": "construct",
                "source_entity_id": "con_via_wisdom",
                "target_entity_type": "construct",
                "target_entity_id": "con_cliftonstrengths_strategic_thinking",
                "relationship_type": "same_layer_different_cut",
                "relationship_strength": "high",
                "rationale": (
                    "VIA Wisdom and CliftonStrengths Strategic Thinking both emphasize using knowledge and perspective well, "
                    "but VIA frames that pattern as virtue while CliftonStrengths frames it as talent."
                ),
                "confidence": "high",
                "notes": "A strong bi-directional bridge across strengths vocabularies.",
            },
            {
                "id": "xwk_via_humanity_cliftonstrengths_relationship_building",
                "source_entity_type": "construct",
                "source_entity_id": "con_via_humanity",
                "target_entity_type": "construct",
                "target_entity_id": "con_cliftonstrengths_relationship_building",
                "relationship_type": "loose_overlap",
                "relationship_strength": "high",
                "rationale": (
                    "Humanity and Relationship Building both emphasize warmth and connection, though VIA emphasizes ethical "
                    "character while CliftonStrengths emphasizes relational effectiveness."
                ),
                "confidence": "high",
                "notes": "Shared interpersonal emphasis with different normative framing.",
            },
            {
                "id": "xwk_via_courage_cliftonstrengths_influencing",
                "source_entity_type": "construct",
                "source_entity_id": "con_via_courage",
                "target_entity_type": "construct",
                "target_entity_id": "con_cliftonstrengths_influencing",
                "relationship_type": "loose_overlap",
                "relationship_strength": "medium",
                "rationale": (
                    "VIA Courage and CliftonStrengths Influencing can both show up as visible action and speaking up, "
                    "but they are grounded in different theories of what that action means."
                ),
                "confidence": "medium",
                "notes": "Useful as a partial bridge between virtue and performance vocabularies.",
            },
        ],
        "extra_risks": [
            {
                "id": "rsk_via_character_strengths_positivity_bias",
                "risk_type": "positivity_bias",
                "severity": "medium",
                "description": (
                    "A strengths-only lens can mute conflict, shadow, or harm dynamics if VIA language is used to avoid "
                    "harder conversations about limitations or destructive patterns."
                ),
                "mitigation": "Pair strengths reflection with frameworks that can name costs, overuse, and interpersonal harm.",
            }
        ],
        "extra_use_cases": [
            {
                "id": "use_via_character_strengths_coaching",
                "use_context": "coaching",
                "utility_type": "developmental_reflection",
                "suitability_level": "high",
                "cautions": (
                    "Works best when strengths are treated as developable capacities and not as proof of moral superiority."
                ),
            }
        ],
    },
}


PLACEHOLDER_BUNDLES = {
    spec["slug"]: placeholder_bundle(**(spec | PLACEHOLDER_ENHANCEMENTS_BY_SLUG.get(spec["slug"], {})))
    for spec in PLACEHOLDER_SPECS
}

SEED_INSTRUMENT_BUNDLES = {
    "big-five": BIG_FIVE_BUNDLE,
    "enneagram": ENNEAGRAM_BUNDLE,
    "mbti": MBTI_BUNDLE,
    **PLACEHOLDER_BUNDLES,
}
