import unittest
from contextlib import redirect_stdout
from io import StringIO

import parseltongue_cli


class TemporalPatronusTests(unittest.TestCase):
    def test_manifest_raises_if_not_cast(self) -> None:
        patronus = parseltongue_cli.TemporalPatronus(
            caster="Test Caster",
            memory="A vivid but unused memory",
        )
        with self.assertRaises(ValueError):
            patronus.manifest()

    def test_snapes_doe_manifest_contains_expected_lines(self) -> None:
        patronus = parseltongue_cli.TemporalPatronus.snapes_doe()
        output_lines = patronus.manifest().splitlines()

        self.assertEqual(output_lines[0], "✨ EXPECTO PATRONUM ✨")
        self.assertIn("Caster: Severus Snape", output_lines)
        self.assertIn("Form: Silver Doe", output_lines)
        self.assertIn(
            "Powered by: Love for Lily Evans - transcending time itself",
            output_lines,
        )
        self.assertIn(
            "  ⏳ Present: Severus Snape casts Silver Doe",
            output_lines,
        )
        self.assertIn("  ⏳ Past: First meeting with Lily", output_lines)
        self.assertIn(
            "  ⏳ Future: Guiding Harry through the Forbidden Forest",
            output_lines,
        )

    def test_harry_later_years_manifest_contains_expected_lines(self) -> None:
        patronus = parseltongue_cli.TemporalPatronus.harry_later_years()
        output_lines = patronus.manifest().splitlines()

        self.assertEqual(output_lines[0], "✨ EXPECTO PATRONUM ✨")
        self.assertIn("Caster: Harry Potter", output_lines)
        self.assertIn("Form: Stag", output_lines)
        self.assertIn(
            "Powered by: Choosing to live beyond the war and build a family after defeating Voldemort",
            output_lines,
        )
        self.assertIn(
            "  ⏳ Present: Harry Potter casts Stag",
            output_lines,
        )
        self.assertIn(
            "  ⏳ Past: Final duel with Voldemort in the Great Hall",
            output_lines,
        )
        self.assertIn(
            "  ⏳ Future: Standing with Albus at the edge of time, choosing a different future",
            output_lines,
        )


class CLITests(unittest.TestCase):
    def _run_main(self, argv=None):
        buf = StringIO()
        with redirect_stdout(buf):
            exit_code = parseltongue_cli.main(argv)
        return exit_code, buf.getvalue()

    def test_cli_default_invokes_snape(self) -> None:
        exit_code, output = self._run_main([])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Severus Snape", output)
        self.assertIn("Form: Silver Doe", output)

    def test_cli_snape_preset(self) -> None:
        exit_code, output = self._run_main(["snape"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Severus Snape", output)
        self.assertIn("Form: Silver Doe", output)

    def test_cli_harry_preset(self) -> None:
        exit_code, output = self._run_main(["harry"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Harry Potter", output)
        self.assertIn("Form: Stag", output)

    def test_cli_luna_preset(self) -> None:
        exit_code, output = self._run_main(["luna"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Luna Lovegood", output)
        self.assertIn("Form: Hare", output)

    def test_cli_dumbledore_preset(self) -> None:
        exit_code, output = self._run_main(["dumbledore"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Albus Dumbledore", output)
        self.assertIn("Form: Phoenix", output)

    def test_cli_hermione_preset(self) -> None:
        exit_code, output = self._run_main(["hermione"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Hermione Granger", output)
        self.assertIn("Form: Otter", output)

    def test_cli_no_color_flag(self) -> None:
        exit_code, output = self._run_main(["snape", "--no-color"])
        self.assertEqual(exit_code, 0)
        self.assertIn("Caster: Severus Snape", output)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
