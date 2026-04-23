from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Iterable, List, Sequence


def _is_denied(rel_posix: str, deny: Sequence[str]) -> bool:
    for pat in deny:
        if not pat:
            continue
        if _match_one(rel_posix, pat):
            return True
    return False


def _match_one(rel_posix: str, pat: str) -> bool:
    """Path relative to root (posix); pattern as in config."""
    if not pat:
        return False
    if pat == "*.md":
        return "/" not in rel_posix and rel_posix.endswith(".md")
    if pat.endswith("/**"):
        pre = pat[:-3].rstrip("/")
        if not pre:
            return True
        return rel_posix == pre or rel_posix.startswith(pre + "/")
    if "/**/" in pat:
        pre, g = pat.split("/**/", 1)
        if not (rel_posix == pre or rel_posix.startswith(pre + "/")):
            return False
        rest = rel_posix[len(pre) + 1 :] if rel_posix.startswith(pre + "/") else ""
        if rel_posix == pre:
            return False
        return bool(fnmatch.fnmatch(rest, g)) or bool(fnmatch.fnmatch(Path(rest).name, g))
    if "*" in pat and pat.endswith("/**") is False and "/" in pat and pat.index("*") < pat.rindex(
        "/"
    ):
        # e.g. the_swift_essence_*/** — handled in expand, not here
        pass
    return fnmatch.fnmatch(rel_posix, pat) or fnmatch.fnmatch(Path(rel_posix).name, pat)


def _expand_pattern(root: Path, pattern: str) -> List[Path]:
    """Return concrete *.md files matching one allow line."""
    if not pattern or pattern.startswith("#"):
        return []
    if pattern == "*.md":
        return [p for p in root.glob("*.md") if p.is_file()]

    if pattern.endswith("/**"):
        pre = pattern[:-3].rstrip("/")
        if not pre or pre == "*":
            return [p for p in root.rglob("*.md") if p.is_file()]
        # e.g. knowledge_*/**
        if "*" in pre and not pre.startswith("**") and pre.endswith("*"):
            # directory glob + recursive md
            out: list[Path] = []
            for d in root.glob(pre):
                if d.is_dir():
                    out.extend(p for p in d.rglob("*.md") if p.is_file())
            return out
        d = root / pre
        if d.is_dir():
            return [p for p in d.rglob("*.md") if p.is_file()]
        return []

    if "/**/" in pattern:
        pre, g = pattern.split("/**/", 1)
        d = root / pre
        if not d.is_dir():
            return []
        out: list[Path] = []
        for p in d.rglob(g):
            if p.is_file() and p.suffix == ".md":
                out.append(p)
        return out

    p = root / pattern
    if p.is_file() and p.suffix == ".md":
        return [p]
    if "*" in pattern:
        return [f for f in root.glob(pattern) if f.is_file() and f.suffix == ".md"]
    return []


def collect_corpus_files(root: Path, allow: Sequence[str], deny: Sequence[str]) -> List[Path]:
    """All *.md under root matching allow and not matching deny (deny by pattern)."""
    # Union allow via explicit expand; then apply deny (pattern match on rel path)
    seen: set[Path] = set()
    for pat in allow:
        for p in _expand_pattern(root, pat):
            try:
                p.relative_to(root)
            except ValueError:
                continue
            seen.add(p.resolve())

    out: list[Path] = []
    for p in sorted(seen, key=lambda x: str(x).lower()):
        rel = p.relative_to(root).as_posix()
        if not _is_denied(rel, deny):
            out.append(p)
    return out


def dedupe_paths(paths: Iterable[str]) -> list[str]:
    """
    Deduplicate nested *light_of_the_seven* style duplicates while keeping stable order.
    """
    seen: set[str] = set()
    res: list[str] = []
    for raw in paths:
        norm = _collapse_nested_light(raw)
        if norm in seen:
            continue
        seen.add(norm)
        res.append(raw)
    return res


def _collapse_nested_light(p: str) -> str:
    # Collapse pathological duplicate segments if present
    parts = p.split("/")
    out: list[str] = []
    for part in parts:
        if not out or part != out[-1]:
            out.append(part)
    return "/".join(out)
