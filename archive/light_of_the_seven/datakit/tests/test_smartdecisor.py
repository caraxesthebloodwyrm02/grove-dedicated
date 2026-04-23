import unittest
from pathlib import Path
from visualizations.static.smartdecisor import (
    SmartDecisorConfig,
    TriageCase,
    DEFAULT_SCREWS,
)

class TestSmartDecisorConfig(unittest.TestCase):
    def test_defaults(self):
        config = SmartDecisorConfig()
        self.assertEqual(config.sub_phases, 16)
        self.assertEqual(config.width, 1000)
        self.assertEqual(len(config.domain_rows), 4)

    def test_advanced_config(self):
        """Test 'aware' configuration with custom domains and logic."""
        custom_domains = ["Domain_A", "Domain_B", "Domain_C"]
        config = SmartDecisorConfig(
            sub_phases=32,
            leap_sub_phase=24,
            domain_rows=custom_domains,
            domain_colours={"Domain_A": "#fff", "Domain_B": "#000", "Domain_C": "#777"}
        )
        self.assertEqual(config.sub_phase_width, 1000 / 32.0)
        self.assertEqual(config.primary_segment_width, 250)
        self.assertIn("Domain_A", config.domain_rows)

class TestTriageCaseValidation(unittest.TestCase):
    def setUp(self):
        # Standard config
        self.config = SmartDecisorConfig()
        # Advanced config for precision mapping
        self.advanced_config = SmartDecisorConfig(sub_phases=10, domain_rows=["Custom"])

    def test_validate_valid_case(self):
        case = TriageCase(
            id="TEST-001", title="Valid", domain="Foundations_of_Computation",
            phase=4, sub_phase=10, severity=1
        )
        errors = case.validate(self.config)
        self.assertEqual(errors, [])

    def test_validate_precision_boundaries(self):
        """Test precise boundary conditions."""
        # Case on the edge of sub-phases
        case_edge = TriageCase(
            id="EDGE-001", title="Edge", domain="Foundations_of_Computation",
            phase=4, sub_phase=16, severity=5
        )
        self.assertEqual(case_edge.validate(self.config), [])
        
        # Case just over the edge
        case_over = TriageCase(
            id="OVER-001", title="Over", domain="Foundations_of_Computation",
            phase=4, sub_phase=17, severity=1
        )
        errors = case_over.validate(self.config)
        self.assertIn("Sub-phase 17 out of range [1, 16]", errors[0])

    def test_validate_advanced_mapping(self):
        """Test validation against a custom 'aware' config."""
        # Domain mismatch (soft check in code, but ensuring no crash)
        case_bad_domain = TriageCase(
            id="BAD-DOM", title="Wrong Domain", domain="Unknown_Domain",
            phase=1, sub_phase=5, severity=1
        )
        # Current logic passes unknown domains (returns empty errors), which is expected behavior
        self.assertEqual(case_bad_domain.validate(self.advanced_config), [])

        # Sub-phase limit check against CUSTOM config (10 phases)
        case_deep = TriageCase(
            id="DEEP-001", title="Too Deep", domain="Custom",
            phase=1, sub_phase=12, severity=1
        )
        errors = case_deep.validate(self.advanced_config)
        self.assertTrue(any("out of range [1, 10]" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
