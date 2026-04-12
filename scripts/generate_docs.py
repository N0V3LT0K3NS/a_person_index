from __future__ import annotations

from _bootstrap import bootstrap

root = bootstrap()

from personality_registry.builder import build_docs, build_outputs


def main() -> int:
    build_outputs(root)
    build_docs(root)
    print("Generated static docs in ./site")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
