from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


@dataclass
class CorpusConfig:
    root: Path
    allow: List[str] = field(default_factory=list)
    deny: List[str] = field(default_factory=list)
    week_starts_on: str = "monday"  # monday | sunday
    empty_cell_level: int = 0
    mtime_only: bool = True  # set False when frontmatter date implemented

    @classmethod
    def from_mapping(cls, data: dict) -> "CorpusConfig":
        root = Path(data["root"]).resolve()
        return cls(
            root=root,
            allow=list(data.get("allow") or []),
            deny=list(data.get("deny") or []),
            week_starts_on=str(data.get("week_starts_on") or "monday").lower(),
            empty_cell_level=int(data.get("empty_cell_level") or 0),
            mtime_only=bool(data.get("mtime_only", True)),
        )


def load_corpus_config(path: Path) -> CorpusConfig:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if not isinstance(raw, dict):
        raise ValueError("Corpus config must be a mapping")
    return CorpusConfig.from_mapping(raw)
