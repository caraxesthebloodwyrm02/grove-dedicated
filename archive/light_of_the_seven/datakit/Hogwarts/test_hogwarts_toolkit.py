"""Unit tests for hogwarts_toolkit.py

Tests cover the TemporalPatronus class including:
- Basic instantiation and casting
- Temporal anchor management
- Manifest output formatting
- Tier 3 provenance tracking
- Factory method presets (snapes_doe, harry_later_years)
"""

import unittest
from datetime import datetime

import hogwarts_toolkit


class TemporalPatronusBasicTests(unittest.TestCase):
    """Tests for basic TemporalPatronus functionality."""

    def test_init_stores_caster_and_memory(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Wizard",
            memory="A happy memory",
        )
        self.assertEqual(patronus.caster, "Test Wizard")
        self.assertEqual(patronus.memory, "A happy memory")

    def test_init_form_is_none(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Wizard",
            memory="A happy memory",
        )
        self.assertIsNone(patronus._form)

    def test_init_temporal_anchors_empty(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Wizard",
            memory="A happy memory",
        )
        self.assertEqual(patronus._temporal_anchors, [])

    def test_init_provenance_empty(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Wizard",
            memory="A happy memory",
        )
        self.assertEqual(patronus._provenance, [])


class TemporalPatronusCastingTests(unittest.TestCase):
    """Tests for casting and anchor methods."""

    def setUp(self) -> None:
        self.patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Albus Dumbledore",
            memory="The greater good",
        )

    def test_cast_sets_form(self) -> None:
        self.patronus.cast("Phoenix")
        self.assertEqual(self.patronus._form, "Phoenix")

    def test_cast_adds_present_anchor(self) -> None:
        self.patronus.cast("Phoenix")
        self.assertIn(
            "Present: Albus Dumbledore casts Phoenix", self.patronus._temporal_anchors
        )

    def test_cast_returns_self_for_chaining(self) -> None:
        result = self.patronus.cast("Phoenix")
        self.assertIs(result, self.patronus)

    def test_anchor_to_past_adds_anchor(self) -> None:
        self.patronus.anchor_to_past("Defeating Grindelwald")
        self.assertIn("Past: Defeating Grindelwald", self.patronus._temporal_anchors)

    def test_anchor_to_past_returns_self(self) -> None:
        result = self.patronus.anchor_to_past("Defeating Grindelwald")
        self.assertIs(result, self.patronus)

    def test_anchor_to_future_adds_anchor(self) -> None:
        self.patronus.anchor_to_future("Guiding Harry from beyond")
        self.assertIn(
            "Future: Guiding Harry from beyond", self.patronus._temporal_anchors
        )

    def test_anchor_to_future_returns_self(self) -> None:
        result = self.patronus.anchor_to_future("Guiding Harry from beyond")
        self.assertIs(result, self.patronus)

    def test_method_chaining_works(self) -> None:
        result = (
            self.patronus.cast("Phoenix")
            .anchor_to_past("Youth with Grindelwald")
            .anchor_to_future("The King's Cross meeting")
        )
        self.assertIs(result, self.patronus)
        self.assertEqual(len(self.patronus._temporal_anchors), 3)


class TemporalPatronusManifestTests(unittest.TestCase):
    """Tests for the manifest() method."""

    def test_manifest_raises_if_not_cast(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Caster",
            memory="A memory",
        )
        with self.assertRaises(ValueError) as ctx:
            patronus.manifest()
        self.assertIn("Cannot manifest without casting first", str(ctx.exception))

    def test_manifest_contains_header(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Caster",
            memory="A memory",
        )
        patronus.cast("Otter")
        output = patronus.manifest()
        self.assertIn("✨ EXPECTO PATRONUM ✨", output)

    def test_manifest_contains_caster(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Hermione Granger",
            memory="S.P.E.W. success",
        )
        patronus.cast("Otter")
        output = patronus.manifest()
        self.assertIn("Caster: Hermione Granger", output)

    def test_manifest_contains_form(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Hermione Granger",
            memory="S.P.E.W. success",
        )
        patronus.cast("Otter")
        output = patronus.manifest()
        self.assertIn("Form: Otter", output)

    def test_manifest_contains_memory(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Hermione Granger",
            memory="S.P.E.W. success",
        )
        patronus.cast("Otter")
        output = patronus.manifest()
        self.assertIn("Powered by: S.P.E.W. success", output)

    def test_manifest_contains_temporal_anchors_section(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus.cast("Form").anchor_to_past("Past event")
        output = patronus.manifest()
        self.assertIn("Temporal Anchors:", output)
        self.assertIn("⏳ Past: Past event", output)


class TemporalPatronusProvenanceTests(unittest.TestCase):
    """Tests for Tier 3 provenance tracking."""

    def test_manifest_with_provenance_raises_if_not_cast(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        with self.assertRaises(ValueError):
            patronus.manifest_with_provenance()

    def test_manifest_with_provenance_returns_dict(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus.cast("Form")
        result = patronus.manifest_with_provenance()
        self.assertIsInstance(result, dict)

    def test_manifest_with_provenance_contains_required_keys(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus.cast("Form")
        result = patronus.manifest_with_provenance()

        required_keys = [
            "Query_Contract_ID",
            "Request_Timestamp",
            "User_Query",
            "Response_Tier_Generated",
            "Generated_Response_Text",
            "Operational_Status_Report",
            "Source_Provenance_Array",
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_manifest_with_provenance_tier_is_tier3(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus.cast("Form")
        result = patronus.manifest_with_provenance()
        self.assertEqual(result["Response_Tier_Generated"], "Tier 3 (Source/Technical)")

    def test_manifest_with_provenance_contains_manifest_text(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test Caster",
            memory="Memory",
        )
        patronus.cast("Form")
        result = patronus.manifest_with_provenance()
        self.assertIn("Test Caster", result["Generated_Response_Text"])
        self.assertIn("EXPECTO PATRONUM", result["Generated_Response_Text"])

    def test_manifest_with_provenance_uses_stored_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus._provenance = [{"test_key": "test_value"}]
        patronus.cast("Form")
        result = patronus.manifest_with_provenance()
        self.assertEqual(
            result["Source_Provenance_Array"], [{"test_key": "test_value"}]
        )

    def test_manifest_with_provenance_accepts_custom_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus.cast("Form")
        custom_provenance = [{"custom": "data"}]
        result = patronus.manifest_with_provenance(source_provenance=custom_provenance)
        self.assertEqual(result["Source_Provenance_Array"], custom_provenance)

    def test_operational_status_contains_expected_fields(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus(
            caster="Test",
            memory="Memory",
        )
        patronus.cast("Form")
        result = patronus.manifest_with_provenance()
        status = result["Operational_Status_Report"]
        self.assertIn("ScopeEnforcer_Status", status)
        self.assertIn("CPU_Consumption", status)
        self.assertIn("Memory_Consumption", status)


class TemporalPatronusPresetProvenanceTests(unittest.TestCase):
    """Tests for preset provenance data."""

    def test_get_preset_provenance_snape(self) -> None:
        provenance = hogwarts_toolkit.TemporalPatronus._get_preset_provenance("snape")
        self.assertIsInstance(provenance, list)
        self.assertGreater(len(provenance), 0)
        self.assertIn("Source_Reference_File", provenance[0])

    def test_get_preset_provenance_harry(self) -> None:
        provenance = hogwarts_toolkit.TemporalPatronus._get_preset_provenance("harry")
        self.assertIsInstance(provenance, list)
        self.assertGreater(len(provenance), 0)

    def test_get_preset_provenance_unknown_returns_empty(self) -> None:
        provenance = hogwarts_toolkit.TemporalPatronus._get_preset_provenance("unknown")
        self.assertEqual(provenance, [])


class SnapesDoePresetTests(unittest.TestCase):
    """Tests for the snapes_doe() factory method."""

    def test_snapes_doe_returns_patronus(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.snapes_doe()
        self.assertIsInstance(patronus, hogwarts_toolkit.TemporalPatronus)

    def test_snapes_doe_caster_is_snape(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.snapes_doe()
        self.assertEqual(patronus.caster, "Severus Snape")

    def test_snapes_doe_form_is_silver_doe(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.snapes_doe()
        self.assertEqual(patronus._form, "Silver Doe")

    def test_snapes_doe_memory_mentions_lily(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.snapes_doe()
        self.assertIn("Lily", patronus.memory)

    def test_snapes_doe_has_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.snapes_doe()
        self.assertGreater(len(patronus._provenance), 0)

    def test_snapes_doe_manifest_contains_expected_lines(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.snapes_doe()
        output = patronus.manifest()
        self.assertIn("Severus Snape", output)
        self.assertIn("Silver Doe", output)
        self.assertIn("First meeting with Lily", output)
        self.assertIn("Guiding Harry through the Forbidden Forest", output)


class HarryLaterYearsPresetTests(unittest.TestCase):
    """Tests for the harry_later_years() factory method."""

    def test_harry_later_years_returns_patronus(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.harry_later_years()
        self.assertIsInstance(patronus, hogwarts_toolkit.TemporalPatronus)

    def test_harry_later_years_caster_is_harry(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.harry_later_years()
        self.assertEqual(patronus.caster, "Harry Potter")

    def test_harry_later_years_form_is_stag(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.harry_later_years()
        self.assertEqual(patronus._form, "Stag")

    def test_harry_later_years_has_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.harry_later_years()
        self.assertGreater(len(patronus._provenance), 0)

    def test_harry_later_years_manifest_contains_expected_lines(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.harry_later_years()
        output = patronus.manifest()
        self.assertIn("Harry Potter", output)
        self.assertIn("Stag", output)
        self.assertIn("Final duel with Voldemort", output)
        self.assertIn("Standing with Albus", output)


class LunaHarePresetTests(unittest.TestCase):
    """Tests for the luna_hare() factory method."""

    def test_luna_hare_returns_patronus(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.luna_hare()
        self.assertIsInstance(patronus, hogwarts_toolkit.TemporalPatronus)

    def test_luna_hare_caster_is_luna(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.luna_hare()
        self.assertEqual(patronus.caster, "Luna Lovegood")

    def test_luna_hare_form_is_hare(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.luna_hare()
        self.assertEqual(patronus._form, "Hare")

    def test_luna_hare_memory_mentions_thestrals(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.luna_hare()
        self.assertIn("Thestrals", patronus.memory)

    def test_luna_hare_has_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.luna_hare()
        self.assertGreater(len(patronus._provenance), 0)

    def test_luna_hare_manifest_contains_expected_lines(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.luna_hare()
        output = patronus.manifest()
        self.assertIn("Luna Lovegood", output)
        self.assertIn("Hare", output)
        self.assertIn("Thestrals", output)
        self.assertIn("Quibbler", output)


class DumbledorePhoenixPresetTests(unittest.TestCase):
    """Tests for the dumbledore_phoenix() factory method."""

    def test_dumbledore_phoenix_returns_patronus(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.dumbledore_phoenix()
        self.assertIsInstance(patronus, hogwarts_toolkit.TemporalPatronus)

    def test_dumbledore_phoenix_caster_is_dumbledore(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.dumbledore_phoenix()
        self.assertEqual(patronus.caster, "Albus Dumbledore")

    def test_dumbledore_phoenix_form_is_phoenix(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.dumbledore_phoenix()
        self.assertEqual(patronus._form, "Phoenix")

    def test_dumbledore_phoenix_memory_mentions_love(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.dumbledore_phoenix()
        self.assertIn("love", patronus.memory.lower())

    def test_dumbledore_phoenix_has_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.dumbledore_phoenix()
        self.assertGreater(len(patronus._provenance), 0)

    def test_dumbledore_phoenix_manifest_contains_expected_lines(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.dumbledore_phoenix()
        output = patronus.manifest()
        self.assertIn("Albus Dumbledore", output)
        self.assertIn("Phoenix", output)
        self.assertIn("Grindelwald", output)
        self.assertIn("King's Cross", output)


class HermioneOtterPresetTests(unittest.TestCase):
    """Tests for the hermione_otter() factory method."""

    def test_hermione_otter_returns_patronus(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.hermione_otter()
        self.assertIsInstance(patronus, hogwarts_toolkit.TemporalPatronus)

    def test_hermione_otter_caster_is_hermione(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.hermione_otter()
        self.assertEqual(patronus.caster, "Hermione Granger")

    def test_hermione_otter_form_is_otter(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.hermione_otter()
        self.assertEqual(patronus._form, "Otter")

    def test_hermione_otter_memory_mentions_knowledge(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.hermione_otter()
        self.assertIn("knowledge", patronus.memory.lower())

    def test_hermione_otter_has_provenance(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.hermione_otter()
        self.assertGreater(len(patronus._provenance), 0)

    def test_hermione_otter_manifest_contains_expected_lines(self) -> None:
        patronus = hogwarts_toolkit.TemporalPatronus.hermione_otter()
        output = patronus.manifest()
        self.assertIn("Hermione Granger", output)
        self.assertIn("Otter", output)
        self.assertIn("Philosopher's Stone", output)
        self.assertIn("Minister for Magic", output)


class CastingSymptomsTests(unittest.TestCase):
    """Tests for the CASTING_SYMPTOMS class attribute."""

    def test_casting_symptoms_is_list(self) -> None:
        self.assertIsInstance(hogwarts_toolkit.TemporalPatronus.CASTING_SYMPTOMS, list)

    def test_casting_symptoms_not_empty(self) -> None:
        self.assertGreater(len(hogwarts_toolkit.TemporalPatronus.CASTING_SYMPTOMS), 0)

    def test_casting_symptoms_contains_shimmer(self) -> None:
        symptoms_text = " ".join(hogwarts_toolkit.TemporalPatronus.CASTING_SYMPTOMS)
        self.assertIn("shimmer", symptoms_text.lower())


if __name__ == "__main__":
    unittest.main()
