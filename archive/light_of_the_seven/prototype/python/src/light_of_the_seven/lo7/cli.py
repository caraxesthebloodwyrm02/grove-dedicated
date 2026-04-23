from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from light_of_the_seven.lo7.build import build_manifest, manifest_to_canonical_json
from light_of_the_seven.lo7.config import load_corpus_config
from light_of_the_seven.lo7.html_render import load_manifest_path, render_heatmap_html


def main_manifest() -> None:
    p = argparse.ArgumentParser(
        description="Lo7 manifest: writes document manifest (v1) as JSON."
    )
    p.add_argument("--config", type=Path, required=True, help="Path to lo7_corpus.yaml")
    p.add_argument(
        "--out",
        type=str,
        default="-",
        help="Output file, or - for stdout (default)",
    )
    p.add_argument(
        "--ref-date",
        type=str,
        default="",
        help="Optional YYYY-MM-DD reference for heatmap end (else max(today, file dates))",
    )
    args = p.parse_args()
    cfg = load_corpus_config(args.config)
    ref: date | None = None
    if args.ref_date:
        y, m, d = (int(x) for x in args.ref_date.split("-"))
        ref = date(y, m, d)
    m = build_manifest(cfg, reference_date=ref)
    s = manifest_to_canonical_json(m)
    if args.out in ("-", ""):
        sys.stdout.write(s)
    else:
        Path(args.out).write_text(s, encoding="utf-8")


def main_heatmap() -> None:
    p = argparse.ArgumentParser(
        description="Lo7 heatmap: static HTML from manifest JSON only (no repo walk)."
    )
    p.add_argument("--in", dest="in_path", type=Path, required=True, help="Path to manifest.json")
    p.add_argument("--out", type=Path, required=True, help="Output heatmap.html path")
    p.add_argument(
        "--motion",
        action="store_true",
        help="Enable optional §9 display-only bar-length CSS pulse (no audio).",
    )
    args = p.parse_args()
    man = load_manifest_path(args.in_path)
    body = render_heatmap_html(man, motion=bool(args.motion))
    args.out.write_text(body, encoding="utf-8")
