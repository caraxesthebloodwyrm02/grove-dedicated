from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "logic_similarity.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "visualizations" / "static" / "logic_similarity_pie.png"


# Lightweight, rule-driven presets for weighting similarity signals
PRESETS: Dict[str, Dict] = {
    "balanced": {
        "weights": {"vector": 0.4, "semantic": 0.35, "temporal": 0.25},
        "rules": {"temporal_floor": 0.65, "semantic_floor": 0.7, "vector_bonus_cutoff": 0.9, "vector_bonus": 0.02},
        "note": "Even mix with mild protections against low temporal and semantic alignment.",
    },
    "vector_first": {
        "weights": {"vector": 0.55, "semantic": 0.3, "temporal": 0.15},
        "rules": {"vector_bonus_cutoff": 0.92, "vector_bonus": 0.04, "semantic_floor": 0.68},
        "note": "Emphasize embedding proximity; still guard against weak semantics.",
    },
    "temporal_guard": {
        "weights": {"vector": 0.35, "semantic": 0.3, "temporal": 0.35},
        "rules": {"temporal_floor": 0.7, "temporal_penalty": 0.1},
        "note": "Prioritize time-aware similarity; penalize gates that drift over time.",
    },
}


def load_similarity(path: Path) -> Dict[str, Dict[str, float]]:
    if not path.exists():
        raise FileNotFoundError(f"Similarity data not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: {sk: float(sv) for sk, sv in v.items()} for k, v in raw.items()}


def parse_weights(raw: str | None) -> Dict[str, float]:
    if not raw:
        return {}
    pairs = [p.strip() for p in raw.split(",") if p.strip()]
    out: Dict[str, float] = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid weight spec '{pair}'. Use vector=0.4,semantic=0.3,temporal=0.3")
        k, v = pair.split("=", 1)
        out[k.strip()] = float(v)
    return out


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Weights must sum to a positive number.")
    return {k: v / total for k, v in weights.items()}


def compute_score(
    gate: str,
    signals: Dict[str, float],
    weights: Dict[str, float],
    rules: Dict[str, float],
) -> float:
    score = (
        weights.get("vector", 0) * signals.get("vector", 0)
        + weights.get("semantic", 0) * signals.get("semantic", 0)
        + weights.get("temporal", 0) * signals.get("temporal", 0)
    )

    # Rule layer adjustments
    temporal_floor = rules.get("temporal_floor")
    if temporal_floor is not None and signals.get("temporal", 0) < temporal_floor:
        score *= (1 - rules.get("temporal_penalty", 0.08))

    semantic_floor = rules.get("semantic_floor")
    if semantic_floor is not None and signals.get("semantic", 0) < semantic_floor:
        score *= 0.94

    vector_bonus_cutoff = rules.get("vector_bonus_cutoff")
    if vector_bonus_cutoff is not None and signals.get("vector", 0) >= vector_bonus_cutoff:
        score += rules.get("vector_bonus", 0)

    return max(0.0, min(score, 1.0))


def build_scores(
    similarity_data: Dict[str, Dict[str, float]],
    weights: Dict[str, float],
    rules: Dict[str, float],
) -> List[Tuple[str, float, Dict[str, float]]]:
    results = []
    for gate, signals in similarity_data.items():
        score = compute_score(gate, signals, weights, rules)
        results.append((gate, score, signals))
    # Highest similarity first
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def render_pie(
    scores: List[Tuple[str, float, Dict[str, float]]],
    output: Path,
    title: str,
    palette: List[str],
    top_n: int | None = None,
) -> Path:
    labels = []
    values = []
    for idx, (gate, score, _) in enumerate(scores):
        if top_n is not None and idx >= top_n:
            break
        labels.append(f"{gate} ({score:.2f})")
        values.append(score)

    if not values:
        raise ValueError("No scores to plot.")

    colors = [palette[i % len(palette)] for i in range(len(values))]

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.0f%%",
        startangle=120,
        pctdistance=0.8,
    )

    plt.setp(texts, size=10, color="#0b132b")
    plt.setp(autotexts, size=9, weight="bold", color="white")

    ax.set_title(title, fontsize=14, color="#0b132b", weight="bold")
    ax.axis("equal")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


def describe(scores: List[Tuple[str, float, Dict[str, float]]], preset: str, note: str) -> None:
    print(f"\nPreset: {preset} — {note}")
    print("Gate similarity (combined | vector / semantic / temporal):")
    for gate, score, signals in scores:
        print(
            f"  {gate:<4} {score:5.2f}  |  "
            f"{signals.get('vector', 0):.2f} / {signals.get('semantic', 0):.2f} / {signals.get('temporal', 0):.2f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Minimal pie chart visualizer for transistor vs Boolean gate similarity (vector/semantic/temporal)."
    )
    parser.add_argument(
        "-d",
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help=f"Path to similarity JSON (default: {DEFAULT_DATA_PATH})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output PNG path (default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "-p",
        "--preset",
        choices=list(PRESETS.keys()),
        default="balanced",
        help="Weight/rule preset to apply.",
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="Override weights, e.g., 'vector=0.5,semantic=0.3,temporal=0.2'. Overrides preset weights.",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Transistor vs Boolean Gate Similarity",
        help="Title for the pie chart.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=None,
        help="Limit pie chart to top N gates (default: all).",
    )

    args = parser.parse_args()

    palette = ["#2d6a4f", "#40916c", "#52b788", "#74c69d", "#95d5b2", "#b7e4c7", "#d8f3dc"]
    preset_cfg = PRESETS[args.preset]
    preset_weights = preset_cfg["weights"]
    preset_rules = preset_cfg["rules"]

    # Merge custom weights if provided
    weights = preset_weights.copy()
    custom_weights = parse_weights(args.weights)
    if custom_weights:
        weights.update(custom_weights)
    weights = normalize_weights(weights)

    similarity_data = load_similarity(args.data)
    scores = build_scores(similarity_data, weights, preset_rules)

    output_path = render_pie(scores, args.output, args.title, palette, top_n=args.top_n)
    describe(scores, args.preset, preset_cfg["note"])
    print(f"\nSaved pie chart to: {output_path}")


if __name__ == "__main__":
    main()
