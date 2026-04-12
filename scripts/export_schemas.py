from __future__ import annotations

from _bootstrap import bootstrap

root = bootstrap()

import yaml

from personality_registry.extensions import DOCUMENT_MODEL_BY_FILE as EXTENSION_DOCUMENT_MODEL_BY_FILE
from personality_registry.models import DOCUMENT_MODEL_BY_FILE


FILE_NAMES = {
    "instrument.yaml": "instrument.schema.yaml",
    "versions.yaml": "version.schema.yaml",
    "constructs.yaml": "construct.schema.yaml",
    "claims.yaml": "claim.schema.yaml",
    "resources.yaml": "resource.schema.yaml",
    "annotations.yaml": "annotation.schema.yaml",
    "inferences.yaml": "inference.schema.yaml",
    "crosswalks.yaml": "crosswalk.schema.yaml",
    "risks.yaml": "risk.schema.yaml",
    "use_cases.yaml": "use_case.schema.yaml",
    "motifs/registry.yaml": "motif.schema.yaml",
    "mappings/construct_to_motif.yaml": "mapping.schema.yaml",
    "interactions/registry.yaml": "interaction_hypothesis.schema.yaml",
    "techniques/registry.yaml": "technique.schema.yaml",
    "protocols/registry.yaml": "protocol.schema.yaml",
    "research/contribution_models.yaml": "contribution_model.schema.yaml",
    "research/result_atom_schema.yaml": "result_atom_schema.schema.yaml",
}


def main() -> int:
    schemas_root = root / "schemas"
    schemas_root.mkdir(parents=True, exist_ok=True)
    document_models = {
        **DOCUMENT_MODEL_BY_FILE,
        **EXTENSION_DOCUMENT_MODEL_BY_FILE,
    }
    for source_name, model in document_models.items():
        target = schemas_root / FILE_NAMES[source_name]
        target.write_text(
            yaml.safe_dump(model.model_json_schema(), sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
    print("Exported YAML schemas in ./schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
