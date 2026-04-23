import os
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

# Add src directory to path for package imports (go up from tests/ to repo root, then into src/)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from light_of_the_seven.geometry import create_svg

SVG_NS = "http://www.w3.org/2000/svg"


def svg_tag(tag: str) -> str:
    return f"{{{SVG_NS}}}{tag}"


class TestStructuredGeometry(unittest.TestCase):
    """Unit tests for the structured_geometry SVG generator."""

    def setUp(self):
        """Set up test fixtures."""
        fd, path = tempfile.mkstemp(prefix="light_of_the_seven_test_", suffix=".svg")
        os.close(fd)
        self.output_path = path
        self.primary_phases = [
            "Phase 1: Planning",
            "Phase 2: Development",
            "Phase 3: Validation",
            "Phase 4: Deployment",
        ]

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_svg_generation(self):
        """Test that the SVG is generated correctly."""
        create_svg(
            output_path=self.output_path,
            primary_phases=self.primary_phases,
        )
        self.assertTrue(os.path.exists(self.output_path))

        # Parse the generated SVG
        tree = ET.parse(self.output_path)
        root = tree.getroot()

        # Check SVG attributes
        self.assertEqual(root.attrib["width"], "1000")
        self.assertEqual(root.attrib["height"], "500")

        # Check primary phases
        primary_rects = root.findall(f"./{svg_tag('rect')}[@height='100'][@y='0']")
        self.assertEqual(len(primary_rects), 4)

        for _, rect in enumerate(primary_rects[:3]):
            self.assertEqual(rect.attrib["fill"], "rgba(0, 100, 255, 0.1)")
        self.assertEqual(primary_rects[3].attrib["fill"], "rgba(0, 200, 0, 0.1)")

        # Check sub-phases
        sub_phase_group = root.find(f".//{svg_tag('g')}[@transform='translate(0, 150)']")
        self.assertIsNotNone(sub_phase_group)
        if sub_phase_group is not None:
            sub_phase_rects = sub_phase_group.findall(f".//{svg_tag('rect')}[@height='100']")
            self.assertEqual(len(sub_phase_rects), 16)

            # Check leap point
            leap_line = sub_phase_group.find(f".//{svg_tag('line')}")
            self.assertIsNotNone(leap_line)
            if leap_line is not None:
                self.assertEqual(leap_line.attrib["stroke-dasharray"], "5,5")

            leap_circle = sub_phase_group.find(f".//{svg_tag('circle')}")
            self.assertIsNotNone(leap_circle)
            if leap_circle is not None:
                self.assertEqual(leap_circle.attrib["fill"], "red")

            # Check 50% quants
            quant_rect = sub_phase_group.find(f".//{svg_tag('rect')}[@height='20']")
            self.assertIsNotNone(quant_rect)
            if quant_rect is not None:
                self.assertEqual(quant_rect.attrib["fill"], "rgba(255, 0, 0, 0.3)")

    def test_invalid_primary_phases(self):
        """Test that an error is raised if primary_phases is not length 4."""
        with self.assertRaises(ValueError):
            create_svg(
                output_path=self.output_path,
                primary_phases=["Phase 1", "Phase 2", "Phase 3"],
            )


if __name__ == "__main__":
    unittest.main()
