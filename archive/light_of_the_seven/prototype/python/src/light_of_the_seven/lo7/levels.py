"""§2.1 / BENCHMARK: deterministic 0–4 levels from per-day file count."""

from __future__ import annotations

from typing import Dict


def day_weight_to_level(n: int, empty_cell_level: int = 0) -> int:
    if n <= 0:
        return int(empty_cell_level) if 0 <= empty_cell_level <= 4 else 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    if 3 <= n <= 4:
        return 3
    return 4


def build_levels_by_day(
    day_to_paths: Dict[str, list],
    empty_cell_level: int = 0,
) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for day, items in day_to_paths.items():
        w = len(items)
        out[day] = day_weight_to_level(w, empty_cell_level=empty_cell_level)
    return out
