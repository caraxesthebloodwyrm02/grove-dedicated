from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

_FM_BOUNDARY = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*", re.DOTALL | re.MULTILINE)
_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_DATE_LINE = re.compile(r"(?m)^date:\s*(\d{4}-\d{2}-\d{2})\s*$")


@dataclass
class ScannedFile:
    path: str
    mtime_unix: int
    title: str
    h2: List[str] = field(default_factory=list)
    source_date: Optional[str] = None
    day: str = ""  # YYYY-MM-DD
    weight: float = 1.0


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _parse_frontmatter_date(content: str) -> Optional[str]:
    m = _FM_BOUNDARY.match(content)
    if not m:
        return _optional_inline_date(content)
    block = m.group(1)
    dm = _DATE_LINE.search(block)
    if dm:
        return dm.group(1)
    return _optional_inline_date(content)


def _optional_inline_date(content: str) -> Optional[str]:
    m = _DATE_LINE.search(content)
    return m.group(1) if m else None


def _title_and_h2(content: str) -> Tuple[str, List[str]]:
    h1m = _H1.search(content)
    title = h1m.group(1).strip() if h1m else ""
    h2s = [x.strip() for x in _H2.findall(content)]
    return title, h2s


def scan_file(root: Path, file_path: Path) -> ScannedFile:
    rel = file_path.relative_to(root).as_posix()
    st = file_path.stat()
    mtime_unix = int(st.st_mtime)
    raw = _read_text(file_path)
    title, h2s = _title_and_h2(raw)
    if not title:
        title = file_path.stem
    source_date = _parse_frontmatter_date(raw)
    if source_date:
        day = source_date
    else:
        day = datetime.fromtimestamp(mtime_unix).date().isoformat()
    return ScannedFile(
        path=rel,
        mtime_unix=mtime_unix,
        title=title,
        h2=h2s,
        source_date=source_date,
        day=day,
        weight=1.0,
    )
