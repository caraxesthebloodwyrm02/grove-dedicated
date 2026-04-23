# Improved Structure Skeleton (Light-Touch Refactor)
# This keeps logic intact but reorganizes major functions.

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------
# Data Models
# ---------------------------
@dataclass
class TriageCase:
    id: str
    title: str
    domain: str
    category: str = ""
    demographic: str = ""
    phase: int = 4
    sub_phase: int = 1
    severity: int = 1
    status: str = "open"
    concept: Optional[str] = None
    notes: str = ""

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]):
        return cls(
            id=str(raw.get("id", "case-unknown")),
            title=str(raw.get("title", "Untitled")),
            domain=str(raw.get("domain", "Foundations_of_Computation")),
            category=str(raw.get("category", "")),
            demographic=str(raw.get("demographic", "")),
            phase=int(raw.get("phase", 4)),
            sub_phase=int(raw.get("sub_phase", 1)),
            severity=int(raw.get("severity", 1)),
            status=str(raw.get("status", "open")),
            concept=raw.get("concept"),
            notes=str(raw.get("notes", "")),
        )


# ---------------------------
# JSON Loading and Reference Context
# ---------------------------


def safe_load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_reference_context(base: Path) -> Dict[str, Any]:
    foundations = safe_load_json(base / "Foundations_of_Computation/concept_mappings.json")
    ai_swift = safe_load_json(base / "The_AI_Swift_and_Cognitive_Framework/concept_mappings.json")
    ai_links = safe_load_json(base / "The_AI_Swift_and_Cognitive_Framework/ai_links.json")
    return {"foundations": foundations, "ai_concepts": ai_swift, "ai_links": ai_links}


# ---------------------------
# SVG Helpers
# ---------------------------


def svg_root(width: int, height: int):
    return ET.Element(
        "svg", width=str(width), height=str(height), xmlns="http://www.w3.org/2000/svg"
    )


def add_text(svg, x: float, y: float, text: str, size=12):
    t = ET.SubElement(svg, "text", x=str(x), y=str(y), font_family="Arial", font_size=str(size))
    t.text = text


# ---------------------------
# SVG Generation (High-Level)
# ---------------------------


def build_svg(output: Path, cases: List[TriageCase], cfg: Dict[str, Any]):
    svg = svg_root(cfg["width"], cfg["height"])
    # (phases, grid, subphases, markers inserted here)
    output.write_text(ET.tostring(svg, encoding="unicode"))


# ---------------------------
# Logging
# ---------------------------


def case_to_log(case: TriageCase, ref: Dict[str, Any]) -> Dict[str, Any]:
    entry = asdict(case)
    # (light enrichment here)
    return entry


def write_log(
    output: Path, cases: List[TriageCase], screws: Dict[str, Any], reference: Dict[str, Any]
):
    log = {
        "summary": {"case_count": len(cases)},
        "cases": [case_to_log(c, reference) for c in cases],
        "screws": screws,
    }
    output.write_text(json.dumps(log, indent=2), encoding="utf-8")
