from __future__ import annotations

from personality_registry.loader import load_repository_strict


PLACEHOLDER_MARKERS = [
    "Starter registry entry",
    "Starter source placeholder",
    "Starter placeholder claim",
    "Placeholder construct for a newly scaffolded instrument entry.",
    "This is a starter registry entry",
    "https://example.org/",
    "initial registry scaffold",
]


def test_seeded_instruments_do_not_contain_placeholder_copy(repo_root):
    instruments_root = repo_root / "instruments"
    assert instruments_root.exists()

    offending_files: list[str] = []
    for path in sorted(instruments_root.rglob("*")):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if any(marker in content for marker in PLACEHOLDER_MARKERS):
            offending_files.append(str(path.relative_to(repo_root)))

    assert offending_files == []


def test_seeded_instruments_meet_resource_and_crosswalk_baseline(repo_root):
    repository = load_repository_strict(repo_root)

    thin_instruments: list[str] = []
    for slug, bundle in sorted(repository.instruments.items()):
        if len(bundle.resources) < 2 or len(bundle.crosswalks) < 1:
            thin_instruments.append(
                f"{slug}: resources={len(bundle.resources)} crosswalks={len(bundle.crosswalks)}"
            )

    assert thin_instruments == []


def test_known_seeded_instruments_have_top_level_construct_depth(repo_root):
    repository = load_repository_strict(repo_root)
    expected_min_constructs = {
        "attachment-styles": 2,
        "cliftonstrengths": 4,
        "cqs": 4,
        "culture-index": 7,
        "dark-triad": 3,
        "disc": 4,
        "hexaco": 6,
        "human-design": 4,
        "kolbe": 4,
        "love-languages": 5,
        "natal-astrology": 4,
        "via-character-strengths": 6,
    }

    failures: list[str] = []
    for slug, minimum in expected_min_constructs.items():
        bundle = repository.instruments[slug]
        if len(bundle.constructs) < minimum:
            failures.append(f"{slug}: expected>={minimum} got={len(bundle.constructs)}")

    assert failures == []
