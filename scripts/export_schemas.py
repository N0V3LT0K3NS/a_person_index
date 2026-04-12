from __future__ import annotations

from _bootstrap import bootstrap

root = bootstrap()

import yaml

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
}


def main() -> int:
    schemas_root = root / "schemas"
    schemas_root.mkdir(parents=True, exist_ok=True)
    for source_name, model in DOCUMENT_MODEL_BY_FILE.items():
        target = schemas_root / FILE_NAMES[source_name]
        target.write_text(
            yaml.safe_dump(model.model_json_schema(), sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
    print("Exported YAML schemas in ./schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
