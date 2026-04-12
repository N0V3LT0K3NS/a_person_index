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
    claim_text: str = "",
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
    inference_id_suffix: str = "starter",
    inference_type: str = "starter_position",
    inference_confidence: str = "medium",
    inference_text: str | None = None,
    risk_type: str = "overinterpretation",
    risk_severity: str = "medium",
    risk_description: str = "Outputs may be overread when context, method limits, or source quality are ignored.",
    risk_mitigation: str = "Treat the framework as one layer among several and preserve uncertainty.",
    use_context: str = "self_reflection",
    utility_type: str = "self_understanding",
    suitability_level: str = "medium",
    cautions: str = "Use as a descriptive aid, not a total account of the person.",
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
                    "change_summary": "Generic umbrella record for the initial registry scaffold.",
                    "scoring_changes": None,
                    "construct_changes": None,
                    "norming_changes": None,
                    "administration_changes": None,
                }
            ]
        },
        "constructs.yaml": {
            "constructs": [
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
            ]
        },
        "claims.yaml": {
            "claims": [
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
        },
        "resources.yaml": {
            "resources": [
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
        },
        "annotations.yaml": {"annotations": annotations},
        "inferences.yaml": {
            "inferences": [
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
        },
        "crosswalks.yaml": {"crosswalks": []},
        "risks.yaml": {
            "risks": [
                {
                    "id": risk_id,
                    "instrument_id": instrument_id,
                    "risk_type": risk_type,
                    "severity": risk_severity,
                    "description": risk_description,
                    "mitigation": risk_mitigation,
                }
            ]
        },
        "use_cases.yaml": {
            "use_cases": [
                {
                    "id": use_case_id,
                    "instrument_id": instrument_id,
                    "use_context": use_context,
                    "utility_type": utility_type,
                    "suitability_level": suitability_level,
                    "cautions": cautions,
                }
            ]
        },
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
    "crosswalks.yaml": {"crosswalks": []},
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
        "construct_name": "Conative profile",
        "construct_definition": "A profile intended to summarize instinctive methods of action and problem solving.",
        "claim_text": "Kolbe claims to measure natural conative strengths related to action and workflow.",
        "inference_text": "Kolbe occupies a distinct niche because it frames differences in terms of action style rather than personality trait or type identity.",
        "risk_description": "Workplace use can harden flexible work preferences into deterministic role assumptions.",
        "cautions": "Use as a workflow discussion aid rather than a fixed capacity judgment.",
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
        "claim_text": "Culture Index claims to predict workplace behavior and fit through a brief assessment profile.",
        "inference_text": "Its practical relevance is concentrated in hiring and organizational decision contexts, which raises the stakes of evidence and misuse concerns.",
        "risk_description": "Using proprietary workplace outputs for high-stakes decisions can amplify false precision and bias.",
        "cautions": "High-stakes use should be treated with skepticism and strong guardrails.",
    },
    {
        "slug": "human-design",
        "canonical_name": "Human Design",
        "short_names": ["Human Design"],
        "short_description": "A symbolic system combining astrology, I Ching, chakras, Kabbalah, and other traditions into a bodygraph-based self-description framework.",
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
        "claim_text": "Human Design claims to reveal innate energetic patterns and decision strategies through a symbolic chart.",
        "inference_text": "Human Design is socially powerful as identity language and symbolic meaning-making, not as empirical measurement.",
        "risk_description": "The system invites deterministic self-narration and heavy identity fusion.",
        "cautions": "Treat as symbolic language rather than literal person measurement.",
    },
    {
        "slug": "natal-astrology",
        "canonical_name": "Natal Astrology",
        "short_names": ["Natal Astrology", "Birth Chart Astrology"],
        "aliases": ["Birth Chart"],
        "short_description": "A symbolic charting system that interprets birth time and place through zodiacal and planetary symbolism.",
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
        "claim_text": "Natal astrology claims that birth-chart symbolism meaningfully describes temperament, patterning, and life themes.",
        "inference_text": "Astrology belongs in the corpus because it functions as a durable symbolic identity language even without empirical standing.",
        "risk_description": "Symbolic charts can be treated as destiny or objective explanation rather than interpretive story language.",
        "cautions": "Keep empirical and symbolic layers clearly separated.",
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


PLACEHOLDER_BUNDLES = {
    spec["slug"]: placeholder_bundle(**spec)
    for spec in PLACEHOLDER_SPECS
}

SEED_INSTRUMENT_BUNDLES = {
    "big-five": BIG_FIVE_BUNDLE,
    "enneagram": ENNEAGRAM_BUNDLE,
    "mbti": MBTI_BUNDLE,
    **PLACEHOLDER_BUNDLES,
}
