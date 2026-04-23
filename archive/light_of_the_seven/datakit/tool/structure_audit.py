#!/usr/bin/env python3
import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


LABELS = {
    "divergence": "Non-Standard Divergence Detected",
    "legacy": "Legacy Artifact Detected",
    "redundancy": "Redundant Concept Detected",
    "missing": "Canonical Requirement Missing",
}


EXAMPLE_SCHEMA_YAML = """schema_version: 1
thesis_name: Example Thesis

traverse:
  max_depth: 3
  include_files: true
  include_dirs: true
  follow_symlinks: false

canon:
  evaluate: depth      # depth | all
  depth: 1
  allowed_paths:
    - README.md
    - core
    - data
    - documents
    - examples
    - scripts
    - templates
    - tool
  required_paths:
    - README.md

ignore:
  globs:
    - "**/.git/**"
    - "**/__pycache__/**"
    - "venv/**"
    - "daatkit/**"

legacy:
  globs:
    - "**/*deprecated*"
    - "**/*old*"
  regex:
    - "(?i)legacy"

redundancy:
  groups:
    - name: temp
      canonical: temp
      aliases: [temp, tmp, tiemp]
      scope: sibling

harmonization:
  enabled: true
  archive_root: .audit_archive
"""


EXAMPLE_SCHEMA_WINDOWS_C_DRIVE_YAML = """schema_version: 1
thesis_name: Windows C Drive (Example)

traverse:
  max_depth: 1
  include_files: false
  include_dirs: true
  follow_symlinks: false

canon:
  evaluate: depth
  depth: 1
  allowed_paths:
    - Windows
    - Users
    - Program Files
    - Program Files (x86)
    - ProgramData
    - PerfLogs
  required_paths:
    - Windows
    - Users

ignore:
  globs: []

legacy:
  globs:
    - "**/temp"
    - "**/tmp"
  regex:
    - "(?i)tiemp"

redundancy:
  groups:
    - name: temp
      canonical: temp
      aliases: [temp, tmp, tiemp]
      scope: sibling

harmonization:
  enabled: true
  archive_root: .audit_archive
"""


@dataclass(frozen=True)
class ScannedItem:
    relative_path: str
    absolute_path: str
    name: str
    item_type: str
    depth: int


def _normalize_path(p: str) -> str:
    p2 = p.replace("\\", "/").strip()
    while p2.startswith("./"):
        p2 = p2[2:]
    return p2.rstrip("/")


def _match_any_glob(rel_path: str, patterns: list[str], *, case_sensitive: bool) -> str | None:
    if not patterns:
        return None

    rel_norm = rel_path if case_sensitive else rel_path.lower()

    for pat in patterns:
        if not isinstance(pat, str):
            continue
        pat_norm = _normalize_path(pat)
        pat_norm = pat_norm if case_sensitive else pat_norm.lower()
        if fnmatch.fnmatchcase(rel_norm, pat_norm):
            return pat

    return None


def _compile_regexes(patterns: list[str], *, case_sensitive: bool) -> list[tuple[str, re.Pattern[str]]]:
    compiled: list[tuple[str, re.Pattern[str]]] = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for pat in patterns:
        if not isinstance(pat, str):
            continue
        try:
            compiled.append((pat, re.compile(pat, flags=flags)))
        except re.error:
            continue

    return compiled


def _match_any_regex(text: str, patterns: list[tuple[str, re.Pattern[str]]]) -> str | None:
    for raw, rx in patterns:
        if rx.search(text):
            return raw
    return None


def _scan_tree(
    root: Path,
    *,
    ignore_globs: list[str],
    max_depth: int,
    include_files: bool,
    include_dirs: bool,
    follow_symlinks: bool,
    case_sensitive: bool,
) -> tuple[list[ScannedItem], dict[str, Any]]:
    items: list[ScannedItem] = []
    errors: list[dict[str, Any]] = []
    ignored_count = 0

    root_abs = root.resolve()

    def rel_posix(p: Path) -> str:
        rel = p.relative_to(root_abs)
        return rel.as_posix().lstrip("./")

    def walk_dir(current: Path, depth: int) -> None:
        nonlocal ignored_count

        if max_depth >= 0 and depth > max_depth:
            return

        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        entry_path = Path(entry.path)
                        rel = rel_posix(entry_path)

                        ignore_hit = _match_any_glob(rel, ignore_globs, case_sensitive=case_sensitive)
                        if ignore_hit is not None:
                            ignored_count += 1
                            if entry.is_dir(follow_symlinks=follow_symlinks):
                                continue
                            continue

                        is_dir = entry.is_dir(follow_symlinks=follow_symlinks)
                        is_file = entry.is_file(follow_symlinks=follow_symlinks)

                        if is_dir:
                            if include_dirs:
                                items.append(
                                    ScannedItem(
                                        relative_path=rel,
                                        absolute_path=str(entry_path),
                                        name=entry.name,
                                        item_type="dir",
                                        depth=depth,
                                    )
                                )
                            if max_depth < 0 or depth < max_depth:
                                walk_dir(entry_path, depth + 1)

                        elif is_file:
                            if include_files:
                                items.append(
                                    ScannedItem(
                                        relative_path=rel,
                                        absolute_path=str(entry_path),
                                        name=entry.name,
                                        item_type="file",
                                        depth=depth,
                                    )
                                )
                    except PermissionError as e:
                        errors.append(
                            {
                                "relative_path": str(entry.path),
                                "error": "PermissionError",
                                "message": str(e),
                            }
                        )
                    except OSError as e:
                        errors.append(
                            {
                                "relative_path": str(entry.path),
                                "error": "OSError",
                                "message": str(e),
                            }
                        )
        except PermissionError as e:
            errors.append({"relative_path": str(current), "error": "PermissionError", "message": str(e)})
        except OSError as e:
            errors.append({"relative_path": str(current), "error": "OSError", "message": str(e)})

    walk_dir(root_abs, 1)

    return items, {"errors": errors, "ignored_count": ignored_count}


def _load_schema(schema_path: Path) -> dict[str, Any]:
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    raw = schema_path.read_text(encoding="utf-8", errors="replace")

    if schema_path.suffix.lower() in (".yaml", ".yml"):
        if yaml is None:
            raise RuntimeError("pyyaml is required to load YAML schema files")
        data = yaml.safe_load(raw)
    else:
        data = json.loads(raw)

    if not isinstance(data, dict):
        raise ValueError("Schema root must be a mapping")

    return data


def _dump_output(obj: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(obj, ensure_ascii=False, indent=2)

    if yaml is None:
        raise RuntimeError("pyyaml is not available; install pyyaml or use --format json")

    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True)


def _path_is_allowed(
    rel_path: str,
    *,
    allowed_paths: list[str],
    allowed_globs: list[str],
    evaluate_mode: str,
    case_sensitive: bool,
) -> bool:
    rel_norm = rel_path if case_sensitive else rel_path.lower()

    for p in allowed_paths:
        p_norm = p if case_sensitive else p.lower()
        if evaluate_mode == "depth":
            if rel_norm == p_norm:
                return True
        else:
            if rel_norm == p_norm or rel_norm.startswith(p_norm + "/"):
                return True

    if _match_any_glob(rel_path, allowed_globs, case_sensitive=case_sensitive) is not None:
        return True

    return False


def _detect_redundancy(
    items: list[ScannedItem],
    groups: list[dict[str, Any]],
    *,
    case_sensitive: bool,
) -> tuple[list[dict[str, Any]], set[str]]:
    findings: list[dict[str, Any]] = []
    flagged_paths: set[str] = set()

    def norm(s: str) -> str:
        return s if case_sensitive else s.lower()

    for g in groups:
        name = str(g.get("name") or "").strip() or "group"
        canonical = str(g.get("canonical") or "").strip() or name
        aliases = [str(x) for x in (g.get("aliases") or []) if isinstance(x, (str, int, float))]
        aliases = [str(x) for x in aliases]
        scope = str(g.get("scope") or "sibling").strip() or "sibling"

        alias_set = {norm(a) for a in aliases} | {norm(canonical)}

        if scope != "sibling":
            continue

        by_parent: dict[str, list[ScannedItem]] = {}
        for it in items:
            if norm(it.name) not in alias_set:
                continue
            parent = it.relative_path.rsplit("/", 1)[0] if "/" in it.relative_path else ""
            by_parent.setdefault(parent, []).append(it)

        for parent, matches in by_parent.items():
            if len(matches) < 2:
                continue

            keep: ScannedItem | None = None
            for it in matches:
                if norm(it.name) == norm(canonical):
                    keep = it
                    break
            if keep is None:
                keep = sorted(matches, key=lambda x: x.relative_path)[0]

            merge_from = [it.relative_path for it in matches if it.relative_path != keep.relative_path]

            for it in matches:
                flagged_paths.add(it.relative_path)

            findings.append(
                {
                    "label": LABELS["redundancy"],
                    "group": name,
                    "canonical": canonical,
                    "parent": parent,
                    "items": [
                        {
                            "relative_path": it.relative_path,
                            "name": it.name,
                            "type": it.item_type,
                        }
                        for it in sorted(matches, key=lambda x: x.relative_path)
                    ],
                    "keep": keep.relative_path,
                    "merge_from": merge_from,
                }
            )

    return findings, flagged_paths


def _build_harmonization_plan(
    *,
    run_id: str,
    archive_root: str,
    divergence: list[dict[str, Any]],
    legacy: list[dict[str, Any]],
    redundancy: list[dict[str, Any]],
) -> dict[str, Any]:
    def dest(category: str, rel: str) -> str:
        return f"{archive_root}/{run_id}/{category}/{rel}".replace("\\", "/")

    actions: list[dict[str, Any]] = []

    for item in legacy:
        rel = item["relative_path"]
        actions.append(
            {
                "action": "archive",
                "category": "legacy",
                "source": rel,
                "destination": dest("legacy", rel),
                "label": LABELS["legacy"],
                "reason": item.get("reason"),
            }
        )

    for item in divergence:
        rel = item["relative_path"]
        actions.append(
            {
                "action": "review_then_archive",
                "category": "non_standard",
                "source": rel,
                "destination": dest("non_standard", rel),
                "label": LABELS["divergence"],
                "reason": item.get("reason") or "Not matched by canon allow rules",
            }
        )

    for group in redundancy:
        actions.append(
            {
                "action": "consolidate",
                "category": "redundancy",
                "group": group.get("group"),
                "parent": group.get("parent"),
                "keep": group.get("keep"),
                "merge_from": group.get("merge_from"),
                "label": LABELS["redundancy"],
            }
        )

    return {
        "dry_run": True,
        "archive_root": archive_root,
        "actions": actions,
    }


def _extract_logical_instructions(report: dict[str, Any]) -> list[str]:
    findings = report.get("findings", {})
    instructions: list[str] = []

    instructions.append("Confirm the Canon/Schema matches the authoritative source of truth.")

    if findings.get("missing"):
        instructions.append(
            "Resolve missing canonical requirements: add missing concepts to the Thesis or update the Canon if the truth changed."
        )

    if findings.get("divergence"):
        instructions.append(
            "Review Non-Standard Divergences: either incorporate into Canon or archive/remove as non-standard."
        )

    if findings.get("legacy_artifacts"):
        instructions.append("Validate each Legacy Artifact, then archive/remove per policy.")

    if findings.get("redundancy"):
        instructions.append(
            "Consolidate Redundant Concepts by selecting a single authoritative source and merging/archiving the rest (dry-run plan provided)."
        )

    instructions.append("Re-run the audit until divergence/legacy/redundancy trends toward zero.")
    return instructions


def run_structure_audit(
    target: Path,
    schema: dict[str, Any],
    *,
    max_depth_override: int | None,
    canon_depth_override: int | None,
    disable_plan: bool,
    case_sensitive: bool,
) -> dict[str, Any]:
    schema_version = int(schema.get("schema_version", 0) or 0)
    if schema_version != 1:
        raise ValueError("Unsupported schema_version (expected 1)")

    thesis_name = str(schema.get("thesis_name") or "Thesis")

    traverse_cfg = schema.get("traverse", {}) or {}
    max_depth = int(traverse_cfg.get("max_depth", 3) or 3)
    if max_depth_override is not None:
        max_depth = max_depth_override

    include_files = bool(traverse_cfg.get("include_files", True))
    include_dirs = bool(traverse_cfg.get("include_dirs", True))
    follow_symlinks = bool(traverse_cfg.get("follow_symlinks", False))

    ignore_cfg = schema.get("ignore", {}) or {}
    ignore_globs = [_normalize_path(x) for x in (ignore_cfg.get("globs") or []) if isinstance(x, str)]

    canon_cfg = schema.get("canon", {}) or {}
    evaluate = str(canon_cfg.get("evaluate") or "depth").strip() or "depth"
    if evaluate not in ("depth", "all"):
        raise ValueError("canon.evaluate must be one of: depth, all")

    canon_depth = int(canon_cfg.get("depth", 1) or 1)
    if canon_depth_override is not None:
        canon_depth = canon_depth_override

    allowed_paths = [_normalize_path(x) for x in (canon_cfg.get("allowed_paths") or []) if isinstance(x, str)]
    allowed_globs = [_normalize_path(x) for x in (canon_cfg.get("allowed_globs") or []) if isinstance(x, str)]
    required_paths = [_normalize_path(x) for x in (canon_cfg.get("required_paths") or []) if isinstance(x, str)]

    legacy_cfg = schema.get("legacy", {}) or {}
    legacy_globs = [_normalize_path(x) for x in (legacy_cfg.get("globs") or []) if isinstance(x, str)]
    legacy_regex_raw = [x for x in (legacy_cfg.get("regex") or []) if isinstance(x, str)]
    legacy_regex = _compile_regexes(legacy_regex_raw, case_sensitive=case_sensitive)

    redundancy_cfg = schema.get("redundancy", {}) or {}
    redundancy_groups = [g for g in (redundancy_cfg.get("groups") or []) if isinstance(g, dict)]

    harmon_cfg = schema.get("harmonization", {}) or {}
    plan_enabled = bool(harmon_cfg.get("enabled", True)) and (not disable_plan)
    archive_root = str(harmon_cfg.get("archive_root") or ".audit_archive")

    if not target.exists():
        raise FileNotFoundError(f"Target does not exist: {target}")

    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    scanned, scan_meta = _scan_tree(
        target,
        ignore_globs=ignore_globs,
        max_depth=max_depth,
        include_files=include_files,
        include_dirs=include_dirs,
        follow_symlinks=follow_symlinks,
        case_sensitive=case_sensitive,
    )

    redundancy_findings, redundancy_paths = _detect_redundancy(
        scanned,
        redundancy_groups,
        case_sensitive=case_sensitive,
    )

    divergence: list[dict[str, Any]] = []
    for it in scanned:
        if evaluate == "depth" and it.depth != canon_depth:
            continue

        if not allowed_paths and not allowed_globs:
            continue

        is_allowed = _path_is_allowed(
            it.relative_path,
            allowed_paths=allowed_paths,
            allowed_globs=allowed_globs,
            evaluate_mode=evaluate,
            case_sensitive=case_sensitive,
        )

        if is_allowed:
            continue

        extra = ""
        if it.relative_path in redundancy_paths:
            extra = " (also flagged as redundancy)"

        divergence.append(
            {
                "label": LABELS["divergence"],
                "relative_path": it.relative_path,
                "type": it.item_type,
                "reason": f"Not in canon allowlist{extra}",
            }
        )

    missing: list[dict[str, Any]] = []
    for req in required_paths:
        p = target / req
        if not p.exists():
            missing.append({"label": LABELS["missing"], "relative_path": req, "reason": "Required by canon"})

    legacy_findings: list[dict[str, Any]] = []
    for it in scanned:
        glob_hit = _match_any_glob(it.relative_path, legacy_globs, case_sensitive=case_sensitive)
        rx_hit = _match_any_regex(it.relative_path, legacy_regex) or _match_any_regex(it.name, legacy_regex)

        if glob_hit is None and rx_hit is None:
            continue

        reason_parts = []
        if glob_hit is not None:
            reason_parts.append(f"glob:{glob_hit}")
        if rx_hit is not None:
            reason_parts.append(f"regex:{rx_hit}")

        legacy_findings.append(
            {
                "label": LABELS["legacy"],
                "relative_path": it.relative_path,
                "type": it.item_type,
                "reason": ", ".join(reason_parts),
            }
        )

    report: dict[str, Any] = {
        "meta": {
            "run_id": run_id,
            "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "thesis_name": thesis_name,
            "target": str(target),
            "schema_version": schema_version,
            "canon": {"evaluate": evaluate, "depth": canon_depth},
            "traverse": {
                "max_depth": max_depth,
                "include_files": include_files,
                "include_dirs": include_dirs,
                "follow_symlinks": follow_symlinks,
            },
        },
        "scan": {
            "items": len(scanned),
            "ignored": int(scan_meta.get("ignored_count") or 0),
            "errors": scan_meta.get("errors") or [],
        },
        "findings": {
            "missing": missing,
            "divergence": divergence,
            "legacy_artifacts": legacy_findings,
            "redundancy": redundancy_findings,
        },
    }

    if plan_enabled:
        report["harmonization_plan"] = _build_harmonization_plan(
            run_id=run_id,
            archive_root=archive_root,
            divergence=divergence,
            legacy=legacy_findings,
            redundancy=redundancy_findings,
        )

    report["logical_instructions"] = _extract_logical_instructions(report)

    return report


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="structure_audit",
        description="Audit a Thesis (directory) against a Canon/Schema and report divergence, legacy artifacts, and redundancy.",
    )

    parser.add_argument("--target", help="Path to the Thesis root to scan.")
    parser.add_argument("--schema", help="Path to Canon/Schema (YAML or JSON).")

    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format.",
    )
    parser.add_argument("--out", default="-", help="Output path, or '-' for stdout.")

    parser.add_argument("--max-depth", type=int, default=None, help="Override traverse.max_depth")
    parser.add_argument("--canon-depth", type=int, default=None, help="Override canon.depth (when canon.evaluate=depth)")

    parser.add_argument("--case-sensitive", action="store_true", help="Enable case-sensitive matching")
    parser.add_argument("--no-plan", action="store_true", help="Disable dry-run harmonization plan")

    parser.add_argument("--print-example-schema", action="store_true", help="Print a minimal example schema and exit")
    parser.add_argument(
        "--print-example-c-drive-schema",
        action="store_true",
        help="Print an example schema for auditing C:\\ (depth=1) and exit",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    if args.print_example_schema:
        print(EXAMPLE_SCHEMA_YAML)
        return 0

    if args.print_example_c_drive_schema:
        print(EXAMPLE_SCHEMA_WINDOWS_C_DRIVE_YAML)
        return 0

    if not args.target or not args.schema:
        raise SystemExit("--target and --schema are required unless printing an example schema")

    schema_path = Path(args.schema)
    target = Path(args.target)

    schema = _load_schema(schema_path)

    report = run_structure_audit(
        target,
        schema,
        max_depth_override=args.max_depth,
        canon_depth_override=args.canon_depth,
        disable_plan=args.no_plan,
        case_sensitive=args.case_sensitive,
    )

    rendered = _dump_output(report, args.format)

    if args.out == "-":
        print(rendered)
    else:
        out_path = Path(args.out)
        out_path.write_text(rendered, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
