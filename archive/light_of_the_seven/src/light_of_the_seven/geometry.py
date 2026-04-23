import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


def create_svg(
    output_path: str,
    primary_phases: list[str],
    sub_phase_count: int = 16,
    leap_sub_phase: int = 11,
    total_width: int = 1000,
    total_height: int = 500,
    theme: str = "classic",
) -> None:
    """
    Generates an SVG diagram with a primary division into 4 phases, a stretched 4th phase,
    and sub-phases with a leap point calculation.

    Args:
        output_path: Path to save the SVG file.
        primary_phases: List of 4 phase names for the primary division.
        sub_phase_count: Number of sub-phases in the stretched 4th phase (default: 16).
        leap_sub_phase: Sub-phase index (1-based) to calculate the leap point (default: 11).
        total_width: Total width of the SVG (default: 1000).
        total_height: Total height of the SVG (default: 500).
    """
    if len(primary_phases) != 4:
        raise ValueError("Exactly 4 primary phases are required.")

    if theme not in {"lot7", "classic"}:
        raise ValueError("theme must be one of: lot7, classic")

    if theme == "lot7":
        bg_a = "#050307"
        bg_b = "#0b0706"
        grid_stroke = "#f6d37a"
        stroke_main = "#f6d37a"
        text_main = "#f8e7b7"
        text_dim = "#e9c878"
        phase_fill_early = "#f0b84a"
        phase_fill_late = "#f6d37a"
        sub_fill = "#f0b84a"
        highlight_fill = "#f8e7b7"
        accent_fill = "#f59e0b"
    else:
        bg_a = "#ffffff"
        bg_b = "#ffffff"
        grid_stroke = "lightgray"
        stroke_main = "black"
        text_main = "black"
        text_dim = "black"
        phase_fill_early = "rgba(0, 100, 255, 0.1)"
        phase_fill_late = "rgba(0, 200, 0, 0.1)"
        sub_fill = "rgba(255, 100, 0, 0.1)"
        highlight_fill = "red"
        accent_fill = "rgba(255, 0, 0, 0.3)"

    # Calculate dimensions
    primary_segment_width = total_width // 4
    sub_phase_width = total_width / sub_phase_count
    leap_point_x = (leap_sub_phase - 0.5) * sub_phase_width
    quant_width = sub_phase_width * 0.5

    # Create SVG root
    svg = ET.Element(
        "svg",
        width=str(total_width),
        height=str(total_height),
        xmlns="http://www.w3.org/2000/svg",
    )

    # Background grid
    defs = ET.SubElement(svg, "defs")
    if theme == "lot7":
        bg = ET.SubElement(defs, "radialGradient", id="bg", cx="50%", cy="35%", r="80%")
        ET.SubElement(bg, "stop", {"offset": "0%", "stop-color": bg_b, "stop-opacity": "1"})
        ET.SubElement(bg, "stop", {"offset": "100%", "stop-color": bg_a, "stop-opacity": "1"})

        glow = ET.SubElement(
            defs, "filter", id="goldGlow", x="-50%", y="-50%", width="200%", height="200%"
        )
        ET.SubElement(
            glow, "feGaussianBlur", {"in": "SourceGraphic", "stdDeviation": "2.3", "result": "blur"}
        )
        ET.SubElement(
            glow,
            "feColorMatrix",
            {
                "in": "blur",
                "type": "matrix",
                "values": "1 0 0 0 0  0 0.9 0 0 0  0 0 0.6 0 0  0 0 0 0.85 0",
                "result": "golden",
            },
        )
        merge = ET.SubElement(glow, "feMerge")
        ET.SubElement(merge, "feMergeNode", {"in": "golden"})
        ET.SubElement(merge, "feMergeNode", {"in": "SourceGraphic"})

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
        {
            "d": "M 20 0 L 0 0 0 20",
            "fill": "none",
            "stroke": grid_stroke,
            "stroke-width": "0.5",
            "stroke-opacity": "0.12" if theme == "lot7" else "1",
        },
    )

    if theme == "lot7":
        ET.SubElement(svg, "rect", width="100%", height="100%", fill="url(#bg)")
        ET.SubElement(svg, "rect", width="100%", height="100%", fill="url(#grid)", opacity="0.55")
        for cx, cy, r, op in [
            (80, 70, 1.4, 0.70),
            (140, 120, 1.1, 0.55),
            (240, 55, 1.8, 0.85),
            (340, 160, 1.3, 0.60),
            (520, 90, 1.5, 0.65),
            (720, 70, 1.2, 0.55),
            (880, 140, 1.7, 0.75),
            (930, 40, 1.1, 0.50),
        ]:
            ET.SubElement(
                svg,
                "circle",
                cx=str(cx),
                cy=str(cy),
                r=str(r),
                fill=text_main,
                opacity=str(op),
                filter="url(#goldGlow)",
            )
    else:
        ET.SubElement(svg, "rect", width="100%", height="100%", fill="url(#grid)")

    # Primary division (4 phases)
    for i, phase in enumerate(primary_phases):
        x = i * primary_segment_width
        if theme == "lot7":
            ET.SubElement(
                svg,
                "rect",
                x=str(x),
                y="0",
                width=str(primary_segment_width),
                height="100",
                fill=phase_fill_early if i < 3 else phase_fill_late,
                stroke=stroke_main,
                fill_opacity="0.08",
                stroke_opacity="0.70",
                filter="url(#goldGlow)",
            )
            ET.SubElement(
                svg,
                "text",
                x=str(x + primary_segment_width // 2),
                y="50",
                text_anchor="middle",
                font_family="Arial",
                font_size="12",
                fill=text_main,
                opacity="0.95",
            ).text = phase
            ET.SubElement(
                svg,
                "text",
                x=str(x + primary_segment_width // 2),
                y="70",
                text_anchor="middle",
                font_family="Arial",
                font_size="10",
                fill=text_dim,
                opacity="0.85",
            ).text = f"({primary_segment_width} units)"
        else:
            ET.SubElement(
                svg,
                "rect",
                x=str(x),
                y="0",
                width=str(primary_segment_width),
                height="100",
                fill="rgba(0, 100, 255, 0.1)" if i < 3 else "rgba(0, 200, 0, 0.1)",
                stroke="black",
            )
            ET.SubElement(
                svg,
                "text",
                x=str(x + primary_segment_width // 2),
                y="50",
                text_anchor="middle",
                font_family="Arial",
                font_size="12",
            ).text = phase
            ET.SubElement(
                svg,
                "text",
                x=str(x + primary_segment_width // 2),
                y="70",
                text_anchor="middle",
                font_family="Arial",
                font_size="10",
            ).text = f"({primary_segment_width} units)"

    # Stretched 4th phase
    if theme == "lot7":
        ET.SubElement(
            svg,
            "rect",
            x="0",
            y="150",
            width=str(total_width),
            height="100",
            fill=phase_fill_late,
            stroke=stroke_main,
            fill_opacity="0.09",
            stroke_opacity="0.70",
            filter="url(#goldGlow)",
        )
        ET.SubElement(
            svg,
            "text",
            x=str(total_width // 2),
            y="200",
            text_anchor="middle",
            font_family="Arial",
            font_size="12",
            fill=text_main,
            opacity="0.95",
        ).text = f"{primary_phases[3]} (Stretched)"
        ET.SubElement(
            svg,
            "text",
            x=str(total_width // 2),
            y="220",
            text_anchor="middle",
            font_family="Arial",
            font_size="10",
            fill=text_dim,
            opacity="0.85",
        ).text = f"({total_width} units)"
    else:
        ET.SubElement(
            svg,
            "rect",
            x="0",
            y="150",
            width=str(total_width),
            height="100",
            fill="rgba(0, 200, 0, 0.1)",
            stroke="black",
        )
        ET.SubElement(
            svg,
            "text",
            x=str(total_width // 2),
            y="200",
            text_anchor="middle",
            font_family="Arial",
            font_size="12",
        ).text = f"{primary_phases[3]} (Stretched)"
        ET.SubElement(
            svg,
            "text",
            x=str(total_width // 2),
            y="220",
            text_anchor="middle",
            font_family="Arial",
            font_size="10",
        ).text = f"({total_width} units)"

    # Sub-phases
    sub_phases_group = ET.SubElement(svg, "g", transform="translate(0, 150)")
    for i in range(1, sub_phase_count + 1):
        x = (i - 1) * sub_phase_width
        fill_opacity = "0.3" if i == leap_sub_phase else "0.1"
        if theme == "lot7":
            ET.SubElement(
                sub_phases_group,
                "rect",
                x=str(x),
                y="0",
                width=str(sub_phase_width),
                height="100",
                fill=sub_fill,
                stroke=stroke_main,
                fill_opacity="0.22" if i == leap_sub_phase else "0.10",
                stroke_opacity="0.70",
                filter="url(#goldGlow)",
            )
            ET.SubElement(
                sub_phases_group,
                "text",
                x=str(x + sub_phase_width / 2),
                y="50",
                text_anchor="middle",
                font_family="Arial",
                font_size="8",
                fill=text_main,
                opacity="0.85",
            ).text = f"{i}/{sub_phase_count}"
        else:
            ET.SubElement(
                sub_phases_group,
                "rect",
                x=str(x),
                y="0",
                width=str(sub_phase_width),
                height="100",
                fill=f"rgba(255, 100, 0, {fill_opacity})",
                stroke="black",
            )
            ET.SubElement(
                sub_phases_group,
                "text",
                x=str(x + sub_phase_width / 2),
                y="50",
                text_anchor="middle",
                font_family="Arial",
                font_size="8",
            ).text = f"{i}/{sub_phase_count}"

    # Leap point
    if theme == "lot7":
        ET.SubElement(
            sub_phases_group,
            "line",
            x1=str(leap_point_x),
            y1="100",
            x2=str(leap_point_x + sub_phase_width),
            y2="150",
            stroke=stroke_main,
            stroke_width="2",
            stroke_dasharray="5,5",
            stroke_opacity="0.85",
            filter="url(#goldGlow)",
        )
        ET.SubElement(
            sub_phases_group,
            "circle",
            cx=str(leap_point_x + sub_phase_width),
            cy="150",
            r="5",
            fill=highlight_fill,
            filter="url(#goldGlow)",
        )
        ET.SubElement(
            sub_phases_group,
            "text",
            x=str(leap_point_x + sub_phase_width + 10),
            y="150",
            text_anchor="start",
            font_family="Arial",
            font_size="10",
            fill=text_main,
            opacity="0.9",
        ).text = "Leap Point (50% Quants)"
    else:
        ET.SubElement(
            sub_phases_group,
            "line",
            {
                "x1": str(leap_point_x),
                "y1": "100",
                "x2": str(leap_point_x + sub_phase_width),
                "y2": "150",
                "stroke": "black",
                "stroke-width": "2",
                "stroke-dasharray": "5,5",
            },
        )
        ET.SubElement(
            sub_phases_group,
            "circle",
            cx=str(leap_point_x + sub_phase_width),
            cy="150",
            r="5",
            fill="red",
        )
        ET.SubElement(
            sub_phases_group,
            "text",
            x=str(leap_point_x + sub_phase_width + 10),
            y="150",
            text_anchor="start",
            font_family="Arial",
            font_size="10",
        ).text = "Leap Point (50% Quants)"

    # 50% Quants
    if theme == "lot7":
        ET.SubElement(
            sub_phases_group,
            "rect",
            x=str(leap_point_x + sub_phase_width - quant_width),
            y="140",
            width=str(quant_width),
            height="20",
            fill=accent_fill,
            stroke=stroke_main,
            fill_opacity="0.30",
            stroke_opacity="0.85",
            filter="url(#goldGlow)",
        )
        ET.SubElement(
            sub_phases_group,
            "text",
            x=str(leap_point_x + sub_phase_width - quant_width / 2),
            y="150",
            text_anchor="middle",
            font_family="Arial",
            font_size="8",
            fill=text_main,
            opacity="0.95",
        ).text = "50% Quants"
    else:
        ET.SubElement(
            sub_phases_group,
            "rect",
            x=str(leap_point_x + sub_phase_width - quant_width),
            y="140",
            width=str(quant_width),
            height="20",
            fill="rgba(255, 0, 0, 0.3)",
            stroke="black",
        )
        ET.SubElement(
            sub_phases_group,
            "text",
            x=str(leap_point_x + sub_phase_width - quant_width / 2),
            y="150",
            text_anchor="middle",
            font_family="Arial",
            font_size="8",
        ).text = "50% Quants"

    # Prettify and save
    xml_str = minidom.parseString(ET.tostring(svg)).toprettyxml(indent="  ")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)


if __name__ == "__main__":
    # Example usage
    primary_phases = [
        "Phase 1: Planning & Definition",
        "Phase 2: Development & Verification",
        "Phase 3: Validation & Refinement",
        "Phase 4: Deployment & Optimization",
    ]
    output_path = str(Path(__file__).resolve().with_name("generated_geometry.svg"))
    create_svg(
        output_path=output_path,
        primary_phases=primary_phases,
        theme="lot7",
    )
