"""codeContext:smartdecisor

Static triage visualization and logging tool for GRID / DataKit.

This module:
- Helps making smart decisions quickly for high-stakes scenarios.
- Turns triage JSON + tuning "screws" into:
  - A static SVG inspired by `error.svg` and `structured_geometry.py`
  - A triage log JSON with summaries and light cross-references.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Path configuration for GRID integration
SCRIPT_DIR = Path(__file__).parent
VISUALIZATIONS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = VISUALIZATIONS_DIR.parent

# Executive report roots for cross-referencing
ROOT_DIR = PROJECT_ROOT.parent
FOUNDATIONS_EXEC_DIR = ROOT_DIR / "Foundations_of_Computation" / "Executive_Report"
AI_SWIFT_EXEC_DIR = ROOT_DIR / "The_AI_Swift_and_Cognitive_Framework" / "Executive_Report"

TOOL_NAME = "codeContext:smartdecisor"

@dataclass
class SmartDecisorConfig:
    """Central configuration for SmartDecisor visualization."""
    sub_phases: int = 16
    leap_sub_phase: int = 11
    width: int = 1000
    height: int = 500
    
    # Domain visual encoding
    domain_rows: List[str] = None
    domain_colours: Dict[str, str] = None
    
    # Text labels
    phase_labels: List[str] = None
    
    def __post_init__(self):
        if self.domain_rows is None:
            self.domain_rows = [
                "Foundations_of_Computation",
                "The_Logistic_Field_Hardware_Domain",
                "Structure_of_Programming_and_Cognitive_Architecture",
                "The_AI_Swift_and_Cognitive_Framework",
            ]
        if self.domain_colours is None:
            self.domain_colours = {
                "Foundations_of_Computation": "#1f77b4",  # blue
                "The_Logistic_Field_Hardware_Domain": "#2ca02c",  # green
                "Structure_of_Programming_and_Cognitive_Architecture": "#9467bd",  # purple
                "The_AI_Swift_and_Cognitive_Framework": "#d62728",  # red
            }
        if self.phase_labels is None:
            self.phase_labels = [
                "Concept & Design",
                "Development & Test",
                "Pilot & Validation",
                "Scaling & Maintenance",
            ]

    @property
    def primary_segment_width(self) -> int:
        return self.width // 4

    @property
    def sub_phase_width(self) -> float:
        return self.width / float(self.sub_phases)


DEFAULT_SCREWS: Dict[str, float] = {
    "risk_weight": 1.0,
    "impact_weight": 1.0,
    "effort_weight": 1.0,
}


@dataclass
class TriageCase:
    """Single triage item projected onto the 4×16 structure."""

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
    def from_dict(cls, raw: Dict[str, Any]) -> "TriageCase":
        return cls(
            id=str(raw.get("id", "case-unknown")),
            title=str(raw.get("title", "Untitled case")),
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

    def validate(self, config: SmartDecisorConfig) -> List[str]:
        """Validate case against configuration rules."""
        errors = []
        if not (1 <= self.phase <= 4):
            errors.append(f"Phase {self.phase} out of range [1, 4]")
        
        if not (1 <= self.sub_phase <= config.sub_phases):
            errors.append(f"Sub-phase {self.sub_phase} out of range [1, {config.sub_phases}]")
            
        if not (1 <= self.severity <= 5):
            errors.append(f"Severity {self.severity} out of range [1, 5]")
            
        return errors


def _safe_load_json(path: Path) -> Dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def load_reference_context() -> Dict[str, Any]:
    """Load reference JSON used for light cross-linking in logs."""
    foundations_concepts = _safe_load_json(FOUNDATIONS_EXEC_DIR / "concept_mappings.json")
    ai_concepts = _safe_load_json(AI_SWIFT_EXEC_DIR / "concept_mappings.json")
    ai_links = _safe_load_json(AI_SWIFT_EXEC_DIR / "ai_links.json")

    return {
        "foundations_concepts": foundations_concepts,
        "ai_concepts": ai_concepts,
        "ai_links": ai_links,
    }


def _resolve_ai_link_key(ai_concepts: Dict[str, Any], concept: str) -> Optional[str]:
    """Best-effort mapping from AI concept name to an ai_links key."""
    examples = ai_concepts.get("examples")
    if not isinstance(examples, list):
        return None

    for example in examples:
        if not isinstance(example, dict):
            continue
        node = example.get(concept)
        if isinstance(node, dict):
            ai_link = node.get("ai_link")
            if isinstance(ai_link, str):
                return ai_link
    return None


def load_triage_data(path: Optional[Path]) -> Tuple[List[TriageCase], Dict[str, Any]]:
    """Load triage cases and screws from JSON."""
    screws: Dict[str, Any] = dict(DEFAULT_SCREWS)
    if path is None:
        raw: Dict[str, Any] = {}
    else:
        raw = _safe_load_json(path)

    if raw:
        raw_screws = raw.get("screws")
        if isinstance(raw_screws, dict):
            for k, v in raw_screws.items():
                if isinstance(v, (int, float)):
                    screws[k] = float(v)

        case_items = raw.get("cases") or []
        cases = [TriageCase.from_dict(item) for item in case_items if isinstance(item, dict)]
        if cases:
            return cases, screws

    # Fallback demo data
    demo_cases = [
        TriageCase(
            id="DEMO-FOUNDATIONS",
            title="Explain force with anchors",
            domain="Foundations_of_Computation",
            category="education",
            demographic="students",
            phase=1,
            sub_phase=3,
            severity=2,
            status="open",
            concept="force",
            notes="Uses car accelerator and bed-pushing anchors.",
        ),
        TriageCase(
            id="DEMO-AI-SWIFT",
            title="Adaptive parking meter rollout",
            domain="The_AI_Swift_and_Cognitive_Framework",
            category="market_trend",
            demographic="urban_cities",
            phase=4,
            sub_phase=11,
            severity=4,
            status="open",
            concept="adaptive_learning_system",
            notes="Streaming-style personalization for different districts.",
        ),
    ]
    return demo_cases, screws


def _domain_row_index(domain: str, config: SmartDecisorConfig) -> int:
    """Map a domain name to a vertical row index in the stretched band."""
    if domain in config.domain_rows:
        return config.domain_rows.index(domain)
    # Place unknown domains after known rows
    return len(config.domain_rows)


def _draw_grid(svg: ET.Element, width: int, height: int) -> None:
    """Draw the background grid pattern."""
    defs = ET.SubElement(svg, "defs")
    pattern = ET.SubElement(
        defs,
        "pattern",
        id="grid",
        width="20",
        height="20",
        patternUnits="userSpaceOnUse",
    )
    ET.SubElement(
        pattern,
        "path",
        d="M 20 0 L 0 0 0 20",
        fill="none",
        stroke="lightgray",
        stroke_width="0.5",
    )
    ET.SubElement(svg, "rect", width="100%", height="100%", fill="url(#grid)")


def _draw_primary_phases(svg: ET.Element, config: SmartDecisorConfig) -> None:
    """Draw the 4 primary phases across the top."""
    seg_width = config.primary_segment_width
    
    for i, label in enumerate(config.phase_labels):
        x = i * seg_width
        # Light blue for first 3, light green for scaling (3rd index)
        fill = "rgba(0, 100, 255, 0.1)" if i < 3 else "rgba(0, 200, 0, 0.1)"
        
        ET.SubElement(
            svg,
            "rect",
            x=str(x),
            y="0",
            width=str(seg_width),
            height="100",
            fill=fill,
            stroke="black",
        )
        ET.SubElement(
            svg,
            "text",
            x=str(x + seg_width // 2),
            y="50",
            text_anchor="middle",
            font_family="Arial",
            font_size="12",
        ).text = label
        ET.SubElement(
            svg,
            "text",
            x=str(x + seg_width // 2),
            y="70",
            text_anchor="middle",
            font_family="Arial",
            font_size="10",
        ).text = f"({seg_width} units)"


def _draw_stretched_phase(svg: ET.Element, width: int, y: int = 150) -> None:
    """Draw the stretched 4th phase container."""
    ET.SubElement(
        svg,
        "rect",
        x="0",
        y=str(y),
        width=str(width),
        height="100",
        fill="rgba(0, 200, 0, 0.1)",
        stroke="black",
    )
    ET.SubElement(
        svg,
        "text",
        x=str(width // 2),
        y=str(y + 50),
        text_anchor="middle",
        font_family="Arial",
        font_size="12",
    ).text = "Scaling & Maintenance (Stretched)"
    ET.SubElement(
        svg,
        "text",
        x=str(width // 2),
        y=str(y + 70),
        text_anchor="middle",
        font_family="Arial",
        font_size="10",
    ).text = f"({width} units)"


def _aggregate_intensity(cases: List[TriageCase], sub_phase_count: int) -> List[float]:
    """Aggregate severity per sub-phase to drive background opacity."""
    totals = [0.0 for _ in range(sub_phase_count)]
    for case in cases:
        if 1 <= case.sub_phase <= sub_phase_count:
            idx = case.sub_phase - 1
            sev = max(1, min(case.severity, 5))
            totals[idx] += float(sev)
    return totals


def _draw_sub_phase_band(
    svg: ET.Element,
    cases: List[TriageCase],
    config: SmartDecisorConfig,
    y_offset: int = 150,
) -> ET.Element:
    """Draw the sub-phase band with severity-driven opacity."""
    sub_phase_totals = _aggregate_intensity(cases, config.sub_phases)
    max_total = max(sub_phase_totals) if sub_phase_totals else 0.0
    
    sub_width = config.sub_phase_width
    group = ET.SubElement(svg, "g", transform=f"translate(0, {y_offset})")

    for i in range(1, config.sub_phases + 1):
        x = (i - 1) * sub_width
        base_total = sub_phase_totals[i - 1] if i - 1 < len(sub_phase_totals) else 0.0
        
        if max_total > 0:
            opacity = 0.1 + 0.3 * (base_total / max_total)
        else:
            opacity = 0.1
        
        ET.SubElement(
            group,
            "rect",
            x=str(x),
            y="0",
            width=str(sub_width),
            height="100",
            fill=f"rgba(255, 100, 0, {opacity:.2f})",
            stroke="black",
        )
        ET.SubElement(
            group,
            "text",
            x=str(x + sub_width / 2.0),
            y="50",
            text_anchor="middle",
            font_family="Arial",
            font_size="8",
        ).text = f"{i}/{config.sub_phases}"

    _draw_leap_point(group, config, sub_width)
    return group


def _draw_leap_point(group: ET.Element, config: SmartDecisorConfig, sub_width: float) -> None:
    """Draw the leap point dashed line and marker."""
    leap_x = (config.leap_sub_phase - 0.5) * sub_width
    
    ET.SubElement(
        group,
        "line",
        x1=str(leap_x),
        y1="100",
        x2=str(leap_x + sub_width),
        y2="150",
        stroke="black",
        stroke_width="2",
        stroke_dasharray="5,5",
    )
    ET.SubElement(
        group,
        "circle",
        cx=str(leap_x + sub_width),
        cy="150",
        r="5",
        fill="red",
    )
    ET.SubElement(
        group,
        "text",
        x=str(leap_x + sub_width + 10),
        y="150",
        text_anchor="start",
        font_family="Arial",
        font_size="10",
    ).text = "Leap Point (50% Quants)"
    
    half_quant = sub_width * 0.5
    ET.SubElement(
        group,
        "rect",
        x=str(leap_x + sub_width - half_quant),
        y="140",
        width=str(half_quant),
        height="20",
        fill="rgba(255, 0, 0, 0.3)",
        stroke="black",
    )
    ET.SubElement(
        group,
        "text",
        x=str(leap_x + sub_width - half_quant / 2.0),
        y="150",
        text_anchor="middle",
        font_family="Arial",
        font_size="8",
    ).text = "50% Quants"


def _draw_markers(
    group: ET.Element,
    cases: List[TriageCase],
    config: SmartDecisorConfig,
) -> None:
    """Draw individual triage case markers."""
    sub_width = config.sub_phase_width
    markers_group = ET.SubElement(group, "g", id="triage_markers")

    for case in cases:
        if case.sub_phase < 1 or case.sub_phase > config.sub_phases:
            continue
            
        row_index = _domain_row_index(case.domain, config)
        cx = (case.sub_phase - 0.5) * sub_width
        cy = 20 + row_index * 15
        colour = config.domain_colours.get(case.domain, "#333333")

        circle = ET.SubElement(
            markers_group,
            "circle",
            cx=str(cx),
            cy=str(cy),
            r="6",
            fill=colour,
            stroke="black",
            stroke_width="1",
        )

        title = ET.SubElement(circle, "title")
        title.text = (
            f"{case.id}: {case.title}\n"
            f"Domain: {case.domain}\n"
            f"Phase: {case.phase}.{case.sub_phase}\n"
            f"Severity: {case.severity}\n"
            f"Category: {case.category}"
        )


def _draw_legend(svg: ET.Element, config: SmartDecisorConfig, x: int = 50, y: int = 320) -> None:
    """Draw the domain legend."""
    legend_group = ET.SubElement(svg, "g", transform=f"translate({x}, {y})")
    
    curr_y = 0
    for domain in config.domain_rows:
        colour = config.domain_colours.get(domain, "#333333")
        ET.SubElement(
            legend_group,
            "circle",
            cx="0",
            cy=str(curr_y),
            r="5",
            fill=colour,
            stroke="black",
            stroke_width="1",
        )
        ET.SubElement(
            legend_group,
            "text",
            x="12",
            y=str(curr_y + 4),
            text_anchor="start",
            font_family="Arial",
            font_size="10",
        ).text = domain
        curr_y += 18

    ET.SubElement(
        legend_group,
        "text",
        x="300",
        y="0",
        text_anchor="start",
        font_family="Arial",
        font_size="9",
        fill="gray",
    ).text = "Audience proximity is left open; adjacency is structural, not prescriptive."


def create_smartdecisor_svg(
    output_path: Path,
    cases: List[TriageCase],
    config: SmartDecisorConfig,
) -> None:
    """Generate an SVG triage map using the new modular helpers."""
    
    if config.sub_phases <= 0:
        raise ValueError("sub_phases must be positive")

    svg = ET.Element(
        "svg",
        width=str(config.width),
        height=str(config.height),
        xmlns="http://www.w3.org/2000/svg",
    )

    _draw_grid(svg, config.width, config.height)
    _draw_primary_phases(svg, config)
    _draw_stretched_phase(svg, config.width)
    
    sub_group = _draw_sub_phase_band(svg, cases, config)
    _draw_markers(sub_group, cases, config)
    
    _draw_legend(svg, config)

    xml_str = minidom.parseString(ET.tostring(svg)).toprettyxml(indent="  ")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(xml_str, encoding="utf-8")


def _case_to_log_entry(
    case: TriageCase,
    reference: Dict[str, Any],
) -> Dict[str, Any]:
    """Convert a triage case into a log dictionary with light enrichment."""
    entry: Dict[str, Any] = asdict(case)

    foundations_concepts = reference.get("foundations_concepts", {})
    ai_concepts = reference.get("ai_concepts", {})
    ai_links = reference.get("ai_links", {})

    if case.domain == "Foundations_of_Computation" and case.concept:
        node = foundations_concepts.get(case.concept)
        if isinstance(node, dict):
            abstract = node.get("abstract")
            if isinstance(abstract, str):
                entry["concept_abstract"] = abstract

    if case.domain == "The_AI_Swift_and_Cognitive_Framework" and case.concept:
        ai_link_key = _resolve_ai_link_key(ai_concepts, case.concept)
        if ai_link_key:
            link_node = ai_links.get(ai_link_key)
            if isinstance(link_node, dict):
                entry["ai_link"] = ai_link_key
                script = link_node.get("script")
                if isinstance(script, str):
                    entry["ai_script"] = script

    return entry


def write_triage_log(
    output_path: Path,
    cases: List[TriageCase],
    screws: Dict[str, Any],
    reference: Dict[str, Any],
) -> None:
    """Write a structured triage log capturing decisions and context."""
    domain_counts: Dict[str, int] = {}
    max_severity = 0
    for case in cases:
        domain_counts[case.domain] = domain_counts.get(case.domain, 0) + 1
        if case.severity > max_severity:
            max_severity = case.severity

    log_obj: Dict[str, Any] = {
        "tool": TOOL_NAME,
        "timestamp_utc": _dt.datetime.utcnow().isoformat() + "Z",
        "screws": screws,
        "summary": {
            "case_count": len(cases),
            "domain_counts": domain_counts,
            "max_severity": max_severity,
        },
        "cases": [_case_to_log_entry(c, reference) for c in cases],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(log_obj, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: Optional[List[str]] = None, config: Optional[SmartDecisorConfig] = None) -> None:
    """CLI entry point. Config can be injected for testing."""
    parser = argparse.ArgumentParser(description="Static triage visualization.")
    parser.add_argument("--input", type=str, help="Triage JSON file")
    parser.add_argument("--output-svg", type=str, help="Output SVG path")
    parser.add_argument("--log", type=str, help="Log JSON path")
    parser.add_argument("--sub-phases", type=int, default=16)
    parser.add_argument("--leap-sub-phase", type=int, default=11)
    parser.add_argument("--width", type=int, default=1000)
    parser.add_argument("--height", type=int, default=500)

    args = parser.parse_args(argv)

    if config is None:
        config = SmartDecisorConfig(
            sub_phases=args.sub_phases,
            leap_sub_phase=args.leap_sub_phase,
            width=args.width,
            height=args.height,
        )

    input_path = Path(args.input) if args.input else None
    
    if args.output_svg:
        output_svg = Path(args.output_svg)
    else:
        output_svg = PROJECT_ROOT / "smartdecisor_triage.svg"
        
    if args.log:
        log_path = Path(args.log)
    else:
        log_path = PROJECT_ROOT / "smartdecisor_log.json"

    cases, screws = load_triage_data(input_path)
    reference = load_reference_context()
    
    validation_errors = []
    for case in cases:
        errs = case.validate(config)
        if errs:
            validation_errors.append(f"Case {case.id}: {', '.join(errs)}")
            
    if validation_errors:
        print("Scanned validation warnings:")
        for e in validation_errors:
            print(f"  - {e}")

    create_smartdecisor_svg(output_svg, cases, config)
    write_triage_log(log_path, cases, screws, reference)

    print(f"✅ {TOOL_NAME} SVG written to: {output_svg}")
    print(f"📝 Triage log written to: {log_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
