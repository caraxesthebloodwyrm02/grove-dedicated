from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PACK_SCHEMA_VERSION_V1 = "datakit.pack.v1"

PACK_SCHEMA_V1: Dict[str, Any] = {
    "schema_version": PACK_SCHEMA_VERSION_V1,
    "required": ["metadata"],
    "metadata": {
        "required": ["name", "description"],
        "optional": [
            "version",
            "author",
            "topic_type",
            "theme",
            "timeframe",
            "tags_global",
            "emotional_purpose",
        ],
    },
    "optional": [
        "learning_modules",
        "fun_facts",
        "challenges",
        "views",
        "navigation",
    ],
    "views": {
        "required": ["id", "type"],
        "optional": ["title", "source", "columns", "max_rows"],
        "types": ["tree", "table"],
    },
    "navigation": {
        "optional": ["free_exploration"],
        "free_exploration": {
            "item_required": ["label"],
            "item_optional": ["view_id", "view"],
        },
    },
}


@dataclass(frozen=True)
class PackIssue:
    severity: str
    path: str
    message: str


_PATH_TOKEN_RE = re.compile(r"([^\[\]\.]+)|(\[(\d+)\])")


def resolve_data_path(data: Any, path: str) -> Tuple[bool, Any]:
    if path is None:
        return False, None

    p = str(path).strip()
    if p in ("", "$"):
        return True, data

    if p.startswith("$."):
        p = p[2:]
    elif p.startswith("$"):
        p = p[1:]

    current: Any = data
    for part in p.split("."):
        if part == "":
            continue
        for m in _PATH_TOKEN_RE.finditer(part):
            key = m.group(1)
            idx = m.group(3)
            if key is not None:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return False, None
            else:
                if isinstance(current, list):
                    i = int(idx)
                    if 0 <= i < len(current):
                        current = current[i]
                    else:
                        return False, None
                else:
                    return False, None

    return True, current


def load_pack_file(path: str | Path) -> Tuple[Optional[Dict[str, Any]], List[PackIssue]]:
    p = Path(path)
    if not p.exists():
        return None, [PackIssue("error", str(p), "File not found")]

    try:
        if p.suffix.lower() == ".json":
            loaded: Any
            with open(p, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        elif p.suffix.lower() in (".yml", ".yaml"):
            try:
                import yaml
            except Exception as e:
                return None, [
                    PackIssue(
                        "error",
                        str(p),
                        f"PyYAML not available: {type(e).__name__}: {e}",
                    )
                ]

            with open(p, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
        else:
            return None, [
                PackIssue(
                    "error",
                    str(p),
                    f"Unsupported file type: {p.suffix or '(no extension)'}",
                )
            ]
    except Exception as e:
        return None, [PackIssue("error", str(p), f"Failed to load: {type(e).__name__}: {e}")]

    if not isinstance(loaded, dict):
        return None, [PackIssue("error", str(p), "Top-level document must be an object")]

    return loaded, []


def validate_pack_dict(pack: Dict[str, Any]) -> List[PackIssue]:
    issues: List[PackIssue] = []

    schema_version = pack.get("schema_version")
    if schema_version is None:
        issues.append(
            PackIssue(
                "warning",
                "schema_version",
                f"Missing schema_version (recommended: {PACK_SCHEMA_VERSION_V1})",
            )
        )
    elif not isinstance(schema_version, str):
        issues.append(PackIssue("error", "schema_version", "schema_version must be a string"))

    metadata = pack.get("metadata")
    if metadata is None:
        issues.append(PackIssue("error", "metadata", "Missing required object"))
        return issues

    if not isinstance(metadata, dict):
        issues.append(PackIssue("error", "metadata", "metadata must be an object"))
        return issues

    if not isinstance(metadata.get("name"), str) or not metadata.get("name"):
        issues.append(PackIssue("error", "metadata.name", "name must be a non-empty string"))

    if not isinstance(metadata.get("description"), str) or not metadata.get("description"):
        issues.append(
            PackIssue("error", "metadata.description", "description must be a non-empty string")
        )

    learning_modules = pack.get("learning_modules")
    if learning_modules is not None:
        if not isinstance(learning_modules, list):
            issues.append(PackIssue("error", "learning_modules", "Must be a list"))
        else:
            for i, mod in enumerate(learning_modules):
                path = f"learning_modules[{i}]"
                if not isinstance(mod, dict):
                    issues.append(PackIssue("error", path, "Module must be an object"))
                    continue

                for req in ("id", "title", "description"):
                    if not isinstance(mod.get(req), str) or not mod.get(req):
                        issues.append(PackIssue("error", f"{path}.{req}", "Must be a non-empty string"))

    fun_facts = pack.get("fun_facts")
    if fun_facts is not None:
        if not isinstance(fun_facts, list):
            issues.append(PackIssue("error", "fun_facts", "Must be a list of strings"))
        else:
            for i, fact in enumerate(fun_facts):
                if not isinstance(fact, str) or not fact:
                    issues.append(PackIssue("error", f"fun_facts[{i}]", "Must be a non-empty string"))

    challenges = pack.get("challenges")
    if challenges is not None:
        if not isinstance(challenges, list):
            issues.append(PackIssue("error", "challenges", "Must be a list"))
        else:
            for i, ch in enumerate(challenges):
                path = f"challenges[{i}]"
                if not isinstance(ch, dict):
                    issues.append(PackIssue("error", path, "Challenge must be an object"))
                    continue
                for req in ("id", "title", "description"):
                    if not isinstance(ch.get(req), str) or not ch.get(req):
                        issues.append(PackIssue("error", f"{path}.{req}", "Must be a non-empty string"))

    views = pack.get("views")
    view_ids: set[str] = set()
    view_map: Dict[str, Dict[str, Any]] = {}

    if views is not None:
        if not isinstance(views, list):
            issues.append(PackIssue("error", "views", "Must be a list"))
        else:
            for i, v in enumerate(views):
                path = f"views[{i}]"
                if not isinstance(v, dict):
                    issues.append(PackIssue("error", path, "View must be an object"))
                    continue

                vid = v.get("id")
                if not isinstance(vid, str) or not vid:
                    issues.append(PackIssue("error", f"{path}.id", "id must be a non-empty string"))
                    continue

                if vid in view_ids:
                    issues.append(PackIssue("error", f"{path}.id", f"Duplicate view id: {vid}"))
                else:
                    view_ids.add(vid)
                    view_map[vid] = v

                vtype = v.get("type")
                if not isinstance(vtype, str) or not vtype:
                    issues.append(PackIssue("error", f"{path}.type", "type must be a non-empty string"))
                    continue

                if vtype not in PACK_SCHEMA_V1["views"]["types"]:
                    issues.append(PackIssue("warning", f"{path}.type", f"Unknown view type: {vtype}"))

                source = v.get("source", "$")
                if not isinstance(source, str):
                    issues.append(PackIssue("error", f"{path}.source", "source must be a string"))
                else:
                    ok, _ = resolve_data_path(pack, source)
                    if not ok:
                        issues.append(PackIssue("error", f"{path}.source", f"Invalid source path: {source}"))

    navigation = pack.get("navigation")
    if navigation is not None:
        if not isinstance(navigation, dict):
            issues.append(PackIssue("error", "navigation", "navigation must be an object"))
        else:
            free = navigation.get("free_exploration")
            if free is not None:
                if not isinstance(free, list):
                    issues.append(PackIssue("error", "navigation.free_exploration", "Must be a list"))
                else:
                    for i, item in enumerate(free):
                        path = f"navigation.free_exploration[{i}]"
                        if not isinstance(item, dict):
                            issues.append(PackIssue("error", path, "Item must be an object"))
                            continue

                        label = item.get("label")
                        if not isinstance(label, str) or not label:
                            issues.append(PackIssue("error", f"{path}.label", "label must be a non-empty string"))

                        view_id = item.get("view_id")
                        inline_view = item.get("view")

                        if isinstance(view_id, str):
                            if view_id not in view_map:
                                issues.append(PackIssue("error", f"{path}.view_id", f"Unknown view_id: {view_id}"))
                        elif inline_view is not None:
                            if not isinstance(inline_view, dict):
                                issues.append(PackIssue("error", f"{path}.view", "view must be an object"))
                            else:
                                vtype = inline_view.get("type")
                                if not isinstance(vtype, str) or not vtype:
                                    issues.append(PackIssue("error", f"{path}.view.type", "type must be a non-empty string"))
                                source = inline_view.get("source", "$")
                                if not isinstance(source, str):
                                    issues.append(PackIssue("error", f"{path}.view.source", "source must be a string"))
                                else:
                                    ok, _ = resolve_data_path(pack, source)
                                    if not ok:
                                        issues.append(PackIssue("error", f"{path}.view.source", f"Invalid source path: {source}"))
                        else:
                            issues.append(
                                PackIssue(
                                    "error",
                                    path,
                                    "Must define either view_id or inline view",
                                )
                            )

    return issues
