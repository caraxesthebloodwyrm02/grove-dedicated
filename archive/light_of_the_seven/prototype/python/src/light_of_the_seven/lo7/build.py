from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Any, DefaultDict, Dict, List, Optional, Tuple

from light_of_the_seven.lo7.config import CorpusConfig
from light_of_the_seven.lo7.levels import day_weight_to_level
from light_of_the_seven.lo7.paths import collect_corpus_files, dedupe_paths
from light_of_the_seven.lo7.scan import ScannedFile, scan_file

LEVEL_DOC = "0 files=empty_cell_level, 1=1, 2=2, 3-4=3, 5+=4 (BENCHMARK.md)"


def _start_of_week(d: date, week_starts_on: str) -> date:
    if week_starts_on == "sunday":
        return d - timedelta(days=(d.isoweekday() % 7))
    return d - timedelta(days=d.weekday())


def _col_for_day(cell_date: date, week_starts_on: str) -> int:
    if week_starts_on == "sunday":
        return (cell_date.isoweekday() % 7)  # Sun=0 ... Sat=6
    return cell_date.weekday()  # Mon=0 ... Sun=6


def _build_grid(
    day_map: Dict[str, Dict[str, Any]],
    ref_date: date,
    week_starts_on: str,
    empty_cell_level: int,
) -> Tuple[List[List[int]], List[List[str]], str, Dict[str, Any]]:
    """52 x 7 levels + parallel ISO date keys for UI drill-down."""
    end_week_start = _start_of_week(ref_date, week_starts_on)
    start_week = end_week_start - timedelta(weeks=51)

    cell_levels: List[List[int]] = [[empty_cell_level for _ in range(7)] for _ in range(52)]
    cell_dates: List[List[str]] = [["" for _ in range(7)] for _ in range(52)]
    for week_i in range(52):
        wk = start_week + timedelta(weeks=week_i)
        for col in range(7):
            cell_date = wk + timedelta(days=col)
            key = cell_date.isoformat()
            dinfo = day_map.get(key)
            if dinfo is None:
                level = empty_cell_level
            else:
                level = int(dinfo["level"])
            ccol = _col_for_day(cell_date, week_starts_on)
            cell_levels[week_i][ccol] = min(4, max(0, level))
            cell_dates[week_i][ccol] = key

    out_days: Dict[str, Any] = {}
    for k, v in day_map.items():
        out_days[k] = {
            "level": int(v["level"]),
            "paths": list(v["paths"]),
            "titles": list(v["titles"]),
            "weight": float(v.get("weight", len(v["paths"]))),
        }

    return cell_levels, cell_dates, start_week.isoformat(), out_days


def _reference_date(
    file_days: List[str],
) -> date:
    if not file_days:
        return datetime.now().astimezone().date()
    last = max(file_days)
    y, m, d = (int(x) for x in last.split("-"))
    today = datetime.now().astimezone().date()
    fdate = date(y, m, d)
    return max(fdate, today)


def _batch_key(rel: str) -> Tuple[str, str]:
    parts = rel.split("/")
    if len(parts) == 1:
        return "root", ""
    return parts[0], parts[0]


def build_manifest(
    cfg: CorpusConfig,
    *,
    reference_date: Optional[date] = None,
) -> dict[str, Any]:
    root = cfg.root
    flist = collect_corpus_files(root, cfg.allow, cfg.deny)
    scanned: List[ScannedFile] = [scan_file(root, p) for p in flist]

    all_paths = [s.path for s in scanned]
    deduped = dedupe_paths(all_paths)
    path_dedupe = len(deduped) < len(set(all_paths))

    by_batch: DefaultDict[str, List[ScannedFile]] = defaultdict(list)
    for s in scanned:
        bid, pre = _batch_key(s.path)
        by_batch[bid if pre else "root"].append(s)

    batches: List[dict[str, Any]] = []
    for bid, items in sorted(by_batch.items(), key=lambda x: x[0].lower()):
        bpre = _batch_key(items[0].path)[1] if items else ""
        files_out = []
        for s in sorted(items, key=lambda x: x.path.lower()):
            files_out.append(
                {
                    "path": s.path,
                    "mtime_unix": s.mtime_unix,
                    "title": s.title,
                    "h2": s.h2,
                    "day": s.day,
                    "source_date": s.source_date,
                    "weight": 1.0,
                }
            )
        batches.append(
            {
                "id": bid,
                "path_prefix": bpre,
                "files": files_out,
            }
        )

    day_to_files: DefaultDict[str, List[ScannedFile]] = defaultdict(list)
    for s in scanned:
        day_to_files[s.day].append(s)

    day_map: Dict[str, Dict[str, Any]] = {}
    for dkey, sfiles in day_to_files.items():
        w = float(len(sfiles))
        level = day_weight_to_level(
            int(w),
            empty_cell_level=cfg.empty_cell_level,
        )
        pmap = {f.path: f.title for f in sfiles}
        ps = sorted(pmap.keys())
        day_map[dkey] = {
            "level": level,
            "paths": ps,
            "titles": [pmap[p] for p in ps],
            "weight": w,
        }

    ref = reference_date
    if ref is None:
        ref = _reference_date(list(day_to_files.keys()))

    cell_levels, cell_dates, grid_start, days_out = _build_grid(
        day_map, ref, cfg.week_starts_on, cfg.empty_cell_level
    )

    dates = sorted([s for s in day_to_files])
    dmin = dates[0] if dates else ref.isoformat()
    dmax = dates[-1] if dates else ref.isoformat()

    return {
        "schema_version": "1",
        "type_name": "OctopusManifest",
        "meta": {
            "day_bucket": "local_wall_calendar",
            "empty_cell_level": cfg.empty_cell_level,
            "mtime_only": bool(cfg.mtime_only),
            "level_thresholds": LEVEL_DOC,
            "corpus_config_note": "see lo7_corpus.yaml",
        },
        "body": {
            "file_count": len(scanned),
            "date_min": dmin,
            "date_max": dmax,
            "path_dedupe_applied": bool(path_dedupe),
        },
        "domain_batches": batches,
        "heatmap": {
            "week_starts_on": cfg.week_starts_on,
            "rows": 52,
            "columns": 7,
            "grid_start": grid_start,
            "cell_levels": cell_levels,
            "cell_dates": cell_dates,
            "days": days_out,
        },
    }


def manifest_to_canonical_json(m: dict[str, Any]) -> str:
    return json.dumps(m, sort_keys=True, ensure_ascii=False) + "\n"
