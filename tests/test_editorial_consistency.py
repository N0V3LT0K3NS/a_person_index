from __future__ import annotations

from pathlib import Path

import yaml


REQUIRED_NOTE_HEADINGS = [
    "## What it is",
    "## Why it matters",
    "## What it is good for",
    "## What it is weaker at",
    "## Common misuse",
]


def test_notes_follow_standard_section_order(repo_root):
    failures: list[str] = []
    for instrument_dir in sorted((repo_root / "instruments").iterdir()):
        if not instrument_dir.is_dir():
            continue
        notes_path = instrument_dir / "notes.md"
        notes = notes_path.read_text(encoding="utf-8")
        last_position = -1
        for heading in REQUIRED_NOTE_HEADINGS:
            position = notes.find(heading)
            if position == -1:
                failures.append(f"{instrument_dir.name}: missing heading '{heading}'")
                continue
            if position < last_position:
                failures.append(f"{instrument_dir.name}: heading out of order '{heading}'")
            last_position = position

    assert failures == []


def test_notes_title_matches_canonical_name(repo_root):
    failures: list[str] = []
    for instrument_dir in sorted((repo_root / "instruments").iterdir()):
        if not instrument_dir.is_dir():
            continue
        instrument = yaml.safe_load((instrument_dir / "instrument.yaml").read_text(encoding="utf-8"))["instrument"]
        notes = (instrument_dir / "notes.md").read_text(encoding="utf-8").splitlines()
        title = next((line[2:].strip() for line in notes if line.startswith("# ")), "")
        if title != instrument["canonical_name"]:
            failures.append(
                f"{instrument_dir.name}: notes title '{title}' != canonical '{instrument['canonical_name']}'"
            )

    assert failures == []
