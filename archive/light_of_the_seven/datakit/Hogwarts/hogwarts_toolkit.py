"""Hogwarts Toolkit: Temporal Patronus and Lore Utilities.

A reusable Python module for generating and manipulating Temporal Patronus
configurations, inspired by Hogwarts lore and the legacy of Severus Snape.

This module is self-contained and uses only Python's standard library.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

__all__ = ["TemporalPatronus"]


class TemporalPatronus:
    """
    A Patronus that exists across time - Dumbledore's secret discovery.
    The charm travels backwards through time, creating its own history.

    Attributes:
        caster (str): The witch or wizard casting the Patronus.
        memory (str): The memory powering the Patronus.
        _form (str | None): The form of the Patronus (e.g., "Silver Doe").
        _temporal_anchors (list[str]): Past, present, and future anchors.
        _provenance (List[Dict[str, Any]]): Tier 3 provenance metadata.
    """

    CASTING_SYMPTOMS = [
        "Brief temporal displacement sensation (the 'shimmer' effect)",
        "Memories feeling more vivid than the present moment",
        "Eyes briefly reflecting events not yet occurred",
        "Goosebumps and time-dilation perception",
        "Patronus form revealing future emotional states",
    ]

    def __init__(self, caster: str, memory: str):
        """Initialize a TemporalPatronus with a caster and memory."""
        self.caster = caster
        self.memory = memory
        self._form: str | None = None
        self._temporal_anchors: list[str] = []
        self._provenance: List[Dict[str, Any]] = []

    def cast(self, form: str) -> "TemporalPatronus":
        """
        Cast the Patronus with a specific form.
        Returns self for method chaining.
        """
        self._form = form
        self._temporal_anchors.append(f"Present: {self.caster} casts {form}")
        return self

    def anchor_to_past(self, past_event: str) -> "TemporalPatronus":
        """Connect the Patronus to a past emotional anchor."""
        self._temporal_anchors.append(f"Past: {past_event}")
        return self

    def anchor_to_future(self, future_event: str) -> "TemporalPatronus":
        """Connect the Patronus to a future emotional anchor."""
        self._temporal_anchors.append(f"Future: {future_event}")
        return self

    def manifest(self) -> str:
        """Manifest the Patronus across all temporal anchors."""
        if not self._form:
            raise ValueError("Cannot manifest without casting first")

        result = [
            "✨ EXPECTO PATRONUM ✨",
            f"Caster: {self.caster}",
            f"Form: {self._form}",
            f"Powered by: {self.memory}",
            "",
            "Temporal Anchors:",
        ]
        for anchor in self._temporal_anchors:
            result.append(f"  ⏳ {anchor}")

        return "\n".join(result)

    def manifest_with_provenance(
        self, source_provenance: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Manifest the Patronus with Tier 3 provenance tracking.

        Args:
            source_provenance: Optional list of provenance dictionaries.
                If None, uses the stored `_provenance`.

        Returns:
            Dict[str, Any]: Tier 3-compliant response with provenance metadata.
        """
        if not self._form:
            raise ValueError("Cannot manifest without casting first")

        if source_provenance is None:
            source_provenance = self._provenance

        response_text = self.manifest()

        operational_status = {
            "ScopeEnforcer_Status": "Optimal",
            "CPU_Consumption": 0.75,  # Simulated value
            "Memory_Consumption": 512,  # Simulated value (MB)
        }

        tier3_response: Dict[str, Any] = {
            "Query_Contract_ID": str(uuid.uuid4()),
            "Request_Timestamp": datetime.now().isoformat(),
            "User_Query": f"Generate Patronus for {self.caster}",
            "Response_Tier_Generated": "Tier 3 (Source/Technical)",
            "Generated_Response_Text": response_text,
            "Operational_Status_Report": operational_status,
            "Source_Provenance_Array": source_provenance,
        }

        return tier3_response

    @classmethod
    def _get_preset_provenance(cls, preset_name: str) -> List[Dict[str, Any]]:
        """
        Get provenance data for a Patronus preset.

        Args:
            preset_name: Name of the preset (e.g., "snape", "harry").

        Returns:
            List[Dict[str, Any]]: Provenance data for the preset.
        """
        provenance_map: Dict[str, List[Dict[str, Any]]] = {
            "snape": [
                {
                    "Source_Reference_File": "SSSEVERUS SNAPE/snape_chapter_2.md",
                    "Vector_Index_ID": "vec_snape_doe_001",
                    "Retrieval_Timestamp": datetime.now().isoformat(),
                    "Raw_Snippet_Used": "Snape's love for Lily Evans transcended time...",
                    "Contradiction_Flagged": False,
                    "Contextual_Recall_Weight": 0.95,
                }
            ],
            "harry": [
                {
                    "Source_Reference_File": "HOGWARTS.md",
                    "Vector_Index_ID": "vec_harry_stag_001",
                    "Retrieval_Timestamp": datetime.now().isoformat(),
                    "Raw_Snippet_Used": "Harry's Patronus reflected his post-war resilience...",
                    "Contradiction_Flagged": False,
                    "Contextual_Recall_Weight": 0.92,
                }
            ],
            "luna": [
                {
                    "Source_Reference_File": "Founders/Ravenclaw/README.md",
                    "Vector_Index_ID": "vec_luna_hare_001",
                    "Retrieval_Timestamp": datetime.now().isoformat(),
                    "Raw_Snippet_Used": "Luna Lovegood's Patronus—a hare that embodies unconventional wisdom...",
                    "Contradiction_Flagged": False,
                    "Contextual_Recall_Weight": 0.88,
                }
            ],
            "dumbledore": [
                {
                    "Source_Reference_File": "Founders/Gryffindor/README.md",
                    "Vector_Index_ID": "vec_dumbledore_phoenix_001",
                    "Retrieval_Timestamp": datetime.now().isoformat(),
                    "Raw_Snippet_Used": "Dumbledore's phoenix Patronus mirrored Fawkes...",
                    "Contradiction_Flagged": False,
                    "Contextual_Recall_Weight": 0.94,
                }
            ],
            "hermione": [
                {
                    "Source_Reference_File": "Founders/Gryffindor/README.md",
                    "Vector_Index_ID": "vec_hermione_otter_001",
                    "Retrieval_Timestamp": datetime.now().isoformat(),
                    "Raw_Snippet_Used": "Hermione's otter represents her playful intelligence...",
                    "Contradiction_Flagged": False,
                    "Contextual_Recall_Weight": 0.90,
                }
            ],
        }
        return provenance_map.get(preset_name, [])

    @classmethod
    def snapes_doe(cls) -> "TemporalPatronus":
        """
        Snape's eternal doe, powered by love for Lily Evans.
        Anchors:
            - Present: Snape casting the doe.
            - Past: First meeting with Lily.
            - Future: Guiding Harry through the Forbidden Forest.
        """
        patronus = cls(
            caster="Severus Snape",
            memory="Love for Lily Evans - transcending time itself",
        )
        patronus._provenance = cls._get_preset_provenance("snape")
        return (
            patronus.cast("Silver Doe")
            .anchor_to_past("First meeting with Lily")
            .anchor_to_future("Guiding Harry through the Forbidden Forest")
        )

    @classmethod
    def harry_later_years(cls) -> "TemporalPatronus":
        """
        Harry's later-years stag, post-war.
        Anchors:
            - Past: Final duel with Voldemort.
            - Future: Standing with Albus at the edge of time.
        """
        patronus = cls(
            caster="Harry Potter",
            memory=(
                "Choosing to live beyond the war and build a family after "
                "defeating Voldemort"
            ),
        )
        patronus._provenance = cls._get_preset_provenance("harry")
        return (
            patronus.cast("Stag")
            .anchor_to_past("Final duel with Voldemort in the Great Hall")
            .anchor_to_future(
                "Standing with Albus at the edge of time, choosing a different future"
            )
        )

    @classmethod
    def luna_hare(cls) -> "TemporalPatronus":
        """
        Luna Lovegood's hare Patronus.
        Embodies unconventional wisdom, quiet courage, and belief in the unseen.
        """
        patronus = cls(
            caster="Luna Lovegood",
            memory="Believing in what others cannot see - Thestrals, Nargles, and friendship",
        )
        patronus._provenance = cls._get_preset_provenance("luna")
        return (
            patronus.cast("Hare")
            .anchor_to_past("First seeing Thestrals after her mother's death")
            .anchor_to_future("Publishing The Quibbler's truth for generations to come")
        )

    @classmethod
    def dumbledore_phoenix(cls) -> "TemporalPatronus":
        """
        Albus Dumbledore's phoenix Patronus.
        Represents rebirth, hope, and the triumph of love over death.
        """
        patronus = cls(
            caster="Albus Dumbledore",
            memory="The belief that love is the most powerful magic of all",
        )
        patronus._provenance = cls._get_preset_provenance("dumbledore")
        return (
            patronus.cast("Phoenix")
            .anchor_to_past("Defeating Grindelwald at Nurmengard")
            .anchor_to_future("Guiding Harry at King's Cross between life and death")
        )

    @classmethod
    def hermione_otter(cls) -> "TemporalPatronus":
        """
        Hermione Granger's otter Patronus.
        Embodies playful intelligence, fierce loyalty, and relentless determination.
        """
        patronus = cls(
            caster="Hermione Granger",
            memory="The moment she realized knowledge could save her friends",
        )
        patronus._provenance = cls._get_preset_provenance("hermione")
        return (
            patronus.cast("Otter")
            .anchor_to_past(
                "Solving the logic puzzle to protect the Philosopher's Stone"
            )
            .anchor_to_future("Reforming magical law as Minister for Magic")
        )
