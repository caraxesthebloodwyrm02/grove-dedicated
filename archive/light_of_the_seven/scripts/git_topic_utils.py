import re
import unicodedata

BRANCH_REGEX = re.compile(r"^topic\/[a-z0-9]+(?:-[a-z0-9]+)*(?:-\d+)?$")


def _normalize_text(s: str) -> str:
    """Lowercase, remove accents, replace spaces and invalid chars with '-'"""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    # keep a-z, 0-9 and dashes
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s


def build_branch_name(theme: str, short: str, issue: str | None = None) -> str:
    t = _normalize_text(theme)
    s = _normalize_text(short)
    parts = [p for p in (t, s) if p]
    branch = "topic/" + "-".join(parts)
    if issue:
        issue_clean = _normalize_text(str(issue))
        branch = f"{branch}-{issue_clean}"
    return branch


def is_valid_branch_name(branch: str) -> bool:
    return bool(BRANCH_REGEX.match(branch))
