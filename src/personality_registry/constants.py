from __future__ import annotations

REQUIRED_INSTRUMENT_FILES = (
    "instrument.yaml",
    "versions.yaml",
    "constructs.yaml",
    "claims.yaml",
    "resources.yaml",
    "annotations.yaml",
    "inferences.yaml",
    "crosswalks.yaml",
    "risks.yaml",
    "use_cases.yaml",
    "notes.md",
)

ROOT_DOCUMENTS = {
    "instrument.yaml": "instrument",
    "versions.yaml": "versions",
    "constructs.yaml": "constructs",
    "claims.yaml": "claims",
    "resources.yaml": "resources",
    "annotations.yaml": "annotations",
    "inferences.yaml": "inferences",
    "crosswalks.yaml": "crosswalks",
    "risks.yaml": "risks",
    "use_cases.yaml": "use_cases",
}

ENTITY_PREFIXES = {
    "analysis_mode": "mode_",
    "artifact_class": "art_",
    "actualization_protocol": "actx_",
    "instrument": "instr_",
    "version": "ver_",
    "construct": "con_",
    "resource": "res_",
    "claim": "clm_",
    "annotation": "ann_",
    "inference": "inf_",
    "crosswalk": "xwk_",
    "risk": "rsk_",
    "use_case": "use_",
    "motif": "mtf_",
    "mapping": "map_",
    "interaction_hypothesis": "ihp_",
    "technique": "tech_",
    "protocol": "proto_",
    "protocol_pack": "ppk_",
    "promotion_pathway": "rpp_",
    "contribution_model": "rcm_",
    "result_atom_schema": "ras_",
}

ENTITY_TYPES = {"instrument", "version", "construct"}
TARGETABLE_ENTITY_TYPES = {"instrument", "version", "construct"}
ANNOTATION_STATUSES = {"explicit", "implicit", "inferred", "comparative", "contested"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
SEVERITY_LEVELS = {"low", "medium", "high", "very_high", "critical"}
SUITABILITY_LEVELS = {"low", "medium", "high", "mixed"}
RELATIONSHIP_STRENGTHS = {"low", "medium", "high"}
CARDINALITIES = {"one", "many"}

REQUIRED_ANNOTATION_DIMENSIONS = (
    "instrument_family",
    "primary_measurement_target",
    "representational_form",
    "temporal_stance",
    "person_ontology",
    "administration_mode",
    "scoring_logic",
    "epistemic_basis",
    "interpretive_burden",
    "granularity",
    "context_sensitivity",
    "change_model",
    "distortion_risk",
    "deployment_context",
    "utility_profile",
    "identity_adhesion_risk",
    "worldview_load",
    "synthesis_value",
)

CROSSWALK_RELATIONSHIP_TYPES = {
    "strong_overlap",
    "loose_overlap",
    "partial_translation",
    "complementary_non_equivalent",
    "same_layer_different_cut",
    "different_layer_of_personhood",
    "often_confused",
    "culturally_associated",
    "inverse_tendency",
    "derived_from",
    "historically_related",
    "methodologically_similar",
    "methodologically_different",
    "incommensurable",
    "house_mapping_only",
}
