#!/usr/bin/env python3
"""
Parse mangrove-biome.code-workspace for hex colors, print HSL and ΔH from 215° (navy anchor).
Run: python3 mangrove_palette_spectrum.py
"""
# Demo harness (Cursor): reversible no-op marker — safe to delete with docs/cursor-demo-assets/.
from __future__ import annotations

import json
import re
from pathlib import Path
from math import fmod

RE_HEX = re.compile(r"#([0-9a-fA-F]{6})")


def hex_to_rgb(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    r, g, b = r / 255, g / 255, b / 255
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l * 100
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    h = (h * 60) % 360
    return h, s * 100, l * 100


def delta_h(a: float, b: float) -> float:
    d = fmod(a - b + 360, 360)
    return d if d <= 180 else 360 - d


def main() -> int:
    ws = Path(__file__).resolve().parent / "mangrove-biome.code-workspace"
    raw = ws.read_text(encoding="utf-8")
    # JSONC: strip // comments
    lines = []
    for line in raw.splitlines():
        ls = line.strip()
        if ls.startswith("//"):
            continue
        if " //" in line:
            line = line.split(" //")[0]
        lines.append(line)
    text = "\n".join(lines)
    data = json.loads(text)
    colors = data["settings"]["workbench.colorCustomizations"]
    anchor = 38.0  # GRID amber-500 (primary); surfaces use graphite (low S)
    print("Mangrove + GRID — HSL (anchor H = {:.0f}° = amber-500; graphite = low S)".format(anchor))
    print("-" * 100)
    print(f"{'token':<44} {'hex':<8} {'H°':>6} {'S%':>5} {'L%':>5} {'|ΔH|':>6}  note")
    print("-" * 100)
    for k in sorted(colors.keys(), key=str.lower):
        v = colors[k]
        if not isinstance(v, str):
            continue
        m = RE_HEX.search(v)
        if not m:
            continue
        hx = f"#{m.group(1).lower()}"
        r, g, b_ = hex_to_rgb(hx)
        h, s, l_ = rgb_to_hsl(r, g, b_)
        dh = delta_h(h, anchor)
        note = ""
        if hx in ("#f59e0b", "#d97706"):
            note = "GRID amber (primary / press)"
        elif hx == "#1a0f00":
            note = "primary-fg (on amber)"
        elif s < 16:
            note = "graphite surface or fg-1/2/3 (H not meaningful at low S)"
        elif dh > 45 and s > 20:
            note = "chromatic — verify fit"
        else:
            note = "—"
        print(f"{k:<44} {hx:<8} {h:6.1f} {s:5.1f} {l_:5.1f} {dh:6.1f}  {note}")
    print("-" * 100)
    print("GRID: see ~/.claude/skills/grid/colors_and_type.css — graphite surfaces, amber CTA, cyan for data only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
