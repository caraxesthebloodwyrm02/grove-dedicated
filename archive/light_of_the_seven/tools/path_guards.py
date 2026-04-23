# -*- coding: utf-8 -*-
"""Path guards for integration slugs and integration.json paths (CWE-22). Pure logic, no I/O."""
from __future__ import annotations

from pathlib import Path
from typing import Optional


def is_safe_platform_id(s: str) -> bool:
    """True if *s* is a single, non-empty path segment with no traversal."""
    if not s or s.strip() != s:
        return False
    if ".." in s or "\x00" in s:
        return False
    p = Path(s)
    if len(p.parts) != 1 or s in (".", ".."):
        return False
    if "/" in s or "\\" in s:
        return False
    return True


def guard_integration_path(
    cwd: Path,
    platform_id: str,
) -> tuple[bool, str, Optional[Path]]:
    """
    Ensure ``integrations/<platform_id>/integration.json`` stays under *cwd* ``/integrations``.

    Returns ``(allowed, reason, resolved_target_or_none)``.
    """
    if not is_safe_platform_id(platform_id):
        return False, "invalid_platform_id", None
    integ_base = (cwd / "integrations").resolve()
    candidate = (cwd / "integrations" / platform_id / "integration.json").resolve()
    try:
        candidate.relative_to(integ_base)
    except ValueError:
        return False, "resolves_outside_integrations", candidate
    return True, "ok", candidate
