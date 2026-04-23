#!/usr/bin/env bash
# One-command manifest + static heatmap (§2.1: two on-disk artifacts).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="${1:-_lo7}"
CONFIG="${2:-lo7_corpus.yaml}"
mkdir -p "$OUT"
if [[ ! -f "$CONFIG" ]]; then
  echo "Config not found: $CONFIG" >&2
  exit 1
fi
uv run lo7-manifest --config "$CONFIG" --out "$OUT/manifest.json"
uv run lo7-heatmap --in "$OUT/manifest.json" --out "$OUT/heatmap.html"
echo "Wrote $OUT/manifest.json and $OUT/heatmap.html"
