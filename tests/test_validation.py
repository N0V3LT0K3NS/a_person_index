from __future__ import annotations

from personality_registry.validation import collect_validation_errors


def test_validation_passes(repo_root):
    assert collect_validation_errors(repo_root) == []
