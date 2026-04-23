"""Hogwarts-Grid Sensory Bridge: Emotion → Sound/Vision Layer Mappings.

NON-CANONICAL: This module is a creative/educational tool.
It does not represent official Harry Potter lore.

This bridge connects the Hogwarts emotion transformation system to Grid's
Sound Layer and Vision Layer schemas, enabling:
- Real-time sonification of emotional states
- Graph-based visualization of patronus manifestations
- Cross-layer coherent representations

The mappings follow Grid's "information as force" philosophy:
- Emotions are entities with polarity and intensity
- Patronus forms are manifestations with sensory signatures
- Transformations are relationships that can be traced and visualized
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ancient_magic_lib import AncientMagicLib, UserEmotion

# ==============================================================================
# CONSTANTS & CONFIGURATION
# ==============================================================================

# Sound Layer parameters (aligned with grid/schemas/sound_layer_schema.json)
PITCH_BASE_HZ = 220.0  # A3 as base
PITCH_RANGE_HZ = (110.0, 880.0)  # A2 to A5
LOUDNESS_RANGE_DB = (-24.0, -3.0)
TIMBRE_BRIGHTNESS_RANGE = (0.0, 1.0)

# Vision Layer parameters (aligned with grid/schemas/vision_layer_schema.json)
NODE_SIZE_RANGE = (10, 100)
EDGE_WEIGHT_RANGE = (0.1, 1.0)
GLOW_INTENSITY_RANGE = (0.0, 1.0)

# House color mappings for visual theming
HOUSE_COLORS = {
    "gryffindor": {"primary": "#AE0001", "secondary": "#EEBA30"},
    "slytherin": {"primary": "#1A472A", "secondary": "#AAAAAA"},
    "ravenclaw": {"primary": "#0E1A40", "secondary": "#946B2D"},
    "hufflepuff": {"primary": "#ECB939", "secondary": "#372E29"},
    "unknown": {"primary": "#666666", "secondary": "#CCCCCC"},
}


class Polarity(Enum):
    """Information polarity types from Grid's ontology."""

    SUPPORTIVE = "supportive"
    NEUTRAL = "neutral"
    ADVERSARIAL = "adversarial"


# ==============================================================================
# EMOTION → GRID MAPPING TABLES
# ==============================================================================

EMOTION_TO_POLARITY: dict[str, Polarity] = {
    "happy": Polarity.SUPPORTIVE,
    "sad": Polarity.NEUTRAL,
    "angry": Polarity.ADVERSARIAL,
    "calm": Polarity.SUPPORTIVE,
    "hopeful": Polarity.SUPPORTIVE,
    "loving": Polarity.SUPPORTIVE,
    "brave": Polarity.SUPPORTIVE,
    "nostalgic": Polarity.NEUTRAL,
    "bittersweet": Polarity.NEUTRAL,
    "determined": Polarity.SUPPORTIVE,
    "protective": Polarity.SUPPORTIVE,
    "serene": Polarity.SUPPORTIVE,
    "grief": Polarity.NEUTRAL,
    "devotion": Polarity.SUPPORTIVE,
    "defiant": Polarity.ADVERSARIAL,
    "wistful": Polarity.NEUTRAL,
}

EMOTION_CONFIDENCE_BOOST: dict[str, float] = {
    "happy": 0.20,
    "sad": 0.00,
    "angry": -0.10,
    "calm": 0.10,
    "hopeful": 0.30,
    "loving": 0.25,
    "brave": 0.15,
    "nostalgic": 0.05,
    "bittersweet": 0.05,
    "determined": 0.20,
    "protective": 0.15,
    "serene": 0.15,
    "grief": -0.05,
    "devotion": 0.25,
    "defiant": 0.10,
    "wistful": 0.00,
}

# Emotion to base pitch offset (semitones from base)
EMOTION_PITCH_SEMITONES: dict[str, int] = {
    "happy": 7,  # Perfect fifth up (bright)
    "sad": -5,  # Perfect fourth down (somber)
    "angry": 1,  # Minor second up (tense)
    "calm": 0,  # Root (stable)
    "hopeful": 12,  # Octave up (aspirational)
    "loving": 4,  # Major third up (warm)
    "brave": 5,  # Perfect fourth up (heroic)
    "nostalgic": -7,  # Perfect fifth down (reflective)
    "bittersweet": -3,  # Minor third down
    "determined": 7,  # Perfect fifth (resolute)
    "protective": 3,  # Minor third up
    "serene": 0,  # Root (peaceful)
    "grief": -12,  # Octave down (heavy)
    "devotion": 9,  # Major sixth up
    "defiant": 6,  # Tritone (unstable, rebellious)
    "wistful": -2,  # Major second down
}

# Emotion to timbre characteristics
EMOTION_TIMBRE: dict[str, dict[str, float]] = {
    "happy": {"brightness": 0.85, "roughness": 0.1, "warmth": 0.7},
    "sad": {"brightness": 0.3, "roughness": 0.2, "warmth": 0.5},
    "angry": {"brightness": 0.7, "roughness": 0.8, "warmth": 0.2},
    "calm": {"brightness": 0.5, "roughness": 0.05, "warmth": 0.8},
    "hopeful": {"brightness": 0.9, "roughness": 0.1, "warmth": 0.75},
    "loving": {"brightness": 0.6, "roughness": 0.05, "warmth": 0.95},
    "brave": {"brightness": 0.75, "roughness": 0.3, "warmth": 0.6},
    "nostalgic": {"brightness": 0.4, "roughness": 0.15, "warmth": 0.7},
    "bittersweet": {"brightness": 0.45, "roughness": 0.2, "warmth": 0.6},
    "determined": {"brightness": 0.7, "roughness": 0.25, "warmth": 0.5},
    "protective": {"brightness": 0.55, "roughness": 0.35, "warmth": 0.65},
    "serene": {"brightness": 0.5, "roughness": 0.0, "warmth": 0.85},
    "grief": {"brightness": 0.2, "roughness": 0.3, "warmth": 0.4},
    "devotion": {"brightness": 0.65, "roughness": 0.05, "warmth": 0.9},
    "defiant": {"brightness": 0.8, "roughness": 0.6, "warmth": 0.3},
    "wistful": {"brightness": 0.35, "roughness": 0.1, "warmth": 0.65},
}


# ==============================================================================
# DATA CLASSES FOR SENSORY OUTPUT
# ==============================================================================


@dataclass
class SoundLayerOutput:
    """Sound Layer representation of an emotional/patronus state.

    Aligned with grid/schemas/sound_layer_schema.json
    """

    pitch_hz: float
    loudness_db: float
    timbre_brightness: float
    timbre_roughness: float
    timbre_warmth: float
    rhythm_bpm: float = 72.0  # Resting heartbeat as default
    uncertainty_noise_level: float = 0.0
    source_emotion: str = ""
    source_intensity: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "pitch": {
                "frequency_hz": self.pitch_hz,
                "midi_note": self._hz_to_midi(self.pitch_hz),
            },
            "loudness": {
                "db": self.loudness_db,
                "normalized": self._db_to_normalized(self.loudness_db),
            },
            "timbre": {
                "brightness": self.timbre_brightness,
                "roughness": self.timbre_roughness,
                "warmth": self.timbre_warmth,
            },
            "rhythm": {"bpm": self.rhythm_bpm},
            "uncertainty": {"noise_level": self.uncertainty_noise_level},
            "metadata": {
                "source_emotion": self.source_emotion,
                "source_intensity": self.source_intensity,
            },
        }

    @staticmethod
    def _hz_to_midi(hz: float) -> int:
        """Convert frequency to MIDI note number."""
        if hz <= 0:
            return 0
        return int(round(69 + 12 * math.log2(hz / 440.0)))

    @staticmethod
    def _db_to_normalized(db: float) -> float:
        """Convert dB to 0-1 normalized value."""
        # Map -24dB to 0.0, -3dB to 1.0
        return max(0.0, min(1.0, (db + 24) / 21))


@dataclass
class VisionNode:
    """A node in the Vision Layer graph."""

    id: str
    label: str
    type: str  # "emotion", "patronus", "character", "event"
    size: float = 50.0
    color: str = "#666666"
    glow: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionEdge:
    """An edge in the Vision Layer graph."""

    source: str
    target: str
    relationship: str  # "transforms_to", "casts", "anchors_to"
    weight: float = 0.5
    style: str = "solid"  # "solid", "dashed", "dotted", "animated"
    color: str = "#888888"


@dataclass
class VisionLayerOutput:
    """Vision Layer representation of emotional/patronus relationships.

    Aligned with grid/schemas/vision_layer_schema.json
    """

    nodes: list[VisionNode] = field(default_factory=list)
    edges: list[VisionEdge] = field(default_factory=list)
    layout: str = "force-directed"
    background_color: str = "#1a1a2e"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "graph": {
                "nodes": [
                    {
                        "id": n.id,
                        "label": n.label,
                        "type": n.type,
                        "visual": {
                            "size": n.size,
                            "color": n.color,
                            "glow": n.glow,
                        },
                        "metadata": n.metadata,
                    }
                    for n in self.nodes
                ],
                "edges": [
                    {
                        "source": e.source,
                        "target": e.target,
                        "relationship": e.relationship,
                        "visual": {
                            "weight": e.weight,
                            "style": e.style,
                            "color": e.color,
                        },
                    }
                    for e in self.edges
                ],
            },
            "layout": self.layout,
            "background_color": self.background_color,
        }

    def add_node(self, node: VisionNode) -> None:
        """Add a node to the graph."""
        self.nodes.append(node)

    def add_edge(self, edge: VisionEdge) -> None:
        """Add an edge to the graph."""
        self.edges.append(edge)


# ==============================================================================
# BRIDGE CLASS: HOGWARTS → GRID SENSORY LAYERS
# ==============================================================================


class HogwartsGridBridge:
    """Bridge connecting Hogwarts emotion/patronus system to Grid's sensory layers.

    This class provides the mapping logic to translate:
    - UserEmotion → SoundLayerOutput (sonification)
    - UserEmotion → VisionLayerOutput (visualization)
    - PatronusResult → Combined sensory representation

    Example:
        >>> bridge = HogwartsGridBridge()
        >>> sound = bridge.emotion_to_sound("happy", intensity=0.9)
        >>> print(sound.pitch_hz)  # Higher pitch for happy emotion
        >>> vision = bridge.build_transformation_graph(["sad", "bittersweet", "hopeful"])
        >>> print(len(vision.nodes))  # 3 emotion nodes + edges
    """

    def __init__(
        self,
        pitch_base_hz: float = PITCH_BASE_HZ,
        loudness_base_db: float = -12.0,
    ):
        """Initialize the bridge with configurable base parameters.

        Args:
            pitch_base_hz: Base frequency for pitch mapping (default A3 = 220Hz).
            loudness_base_db: Base loudness level (default -12dB).
        """
        self.pitch_base_hz = pitch_base_hz
        self.loudness_base_db = loudness_base_db
        self._lore_data: dict[str, Any] | None = None

    # --------------------------------------------------------------------------
    # SOUND LAYER MAPPINGS
    # --------------------------------------------------------------------------

    def emotion_to_sound(
        self,
        emotion: str,
        intensity: float = 1.0,
        include_uncertainty: bool = True,
    ) -> SoundLayerOutput:
        """Map an emotion to Sound Layer parameters.

        Args:
            emotion: The emotion type (e.g., "happy", "sad", "brave").
            intensity: Emotion intensity from 0.0 to 1.0.
            include_uncertainty: Whether to add uncertainty noise for low intensity.

        Returns:
            SoundLayerOutput with pitch, loudness, timbre, and rhythm.
        """
        emotion_key = emotion.lower().strip()

        # Get base values with fallbacks
        semitones = EMOTION_PITCH_SEMITONES.get(emotion_key, 0)
        timbre = EMOTION_TIMBRE.get(
            emotion_key,
            {"brightness": 0.5, "roughness": 0.2, "warmth": 0.5},
        )

        # Calculate pitch from semitones offset
        pitch_hz = self.pitch_base_hz * (2 ** (semitones / 12.0))
        pitch_hz = max(PITCH_RANGE_HZ[0], min(PITCH_RANGE_HZ[1], pitch_hz))

        # Scale loudness by intensity
        loudness_range = LOUDNESS_RANGE_DB[1] - LOUDNESS_RANGE_DB[0]
        loudness_db = LOUDNESS_RANGE_DB[0] + (intensity * loudness_range)

        # Scale timbre by intensity (more intense = more pronounced)
        brightness = timbre["brightness"] * (0.5 + 0.5 * intensity)
        roughness = timbre["roughness"] * intensity
        warmth = timbre["warmth"]

        # Calculate uncertainty noise (inverse of intensity)
        uncertainty = 0.0
        if include_uncertainty and intensity < 0.5:
            uncertainty = (0.5 - intensity) * 0.4  # Max 0.2 noise at 0 intensity

        # Rhythm: faster for high-energy emotions, slower for contemplative
        high_energy = {"happy", "angry", "brave", "defiant", "determined"}
        base_bpm = 72.0
        if emotion_key in high_energy:
            rhythm_bpm = base_bpm + (intensity * 40)  # Up to 112 BPM
        else:
            rhythm_bpm = base_bpm - (intensity * 20)  # Down to 52 BPM

        return SoundLayerOutput(
            pitch_hz=pitch_hz,
            loudness_db=loudness_db,
            timbre_brightness=brightness,
            timbre_roughness=roughness,
            timbre_warmth=warmth,
            rhythm_bpm=rhythm_bpm,
            uncertainty_noise_level=uncertainty,
            source_emotion=emotion_key,
            source_intensity=intensity,
        )

    def patronus_to_sound(
        self,
        patronus_form: str | None,
        caster_house: str = "unknown",
    ) -> SoundLayerOutput:
        """Map a Patronus manifestation to Sound Layer parameters.

        Args:
            patronus_form: The Patronus form string (e.g., "Silver Stag", "Incorporeal Doe (mist)").
            caster_house: The caster's Hogwarts house for theming.

        Returns:
            SoundLayerOutput representing the Patronus's auditory signature.
        """
        if patronus_form is None:
            # Failed casting: silent/minimal sound
            return SoundLayerOutput(
                pitch_hz=0.0,
                loudness_db=-48.0,
                timbre_brightness=0.0,
                timbre_roughness=0.0,
                timbre_warmth=0.0,
                uncertainty_noise_level=0.5,
                source_emotion="none",
                source_intensity=0.0,
            )

        form_lower = patronus_form.lower()

        # Determine clarity level from form string
        if "silver" in form_lower:
            clarity = 1.0  # Fully formed
            loudness_base = -6.0
        elif "incorporeal" in form_lower or "mist" in form_lower:
            clarity = 0.3  # Barely formed
            loudness_base = -18.0
        else:
            clarity = 0.7  # Standard form
            loudness_base = -12.0

        # Determine animal type for pitch character
        animals = {
            "stag": {"pitch_offset": 0, "brightness": 0.8},
            "doe": {"pitch_offset": -2, "brightness": 0.7},
            "wolf": {"pitch_offset": -5, "brightness": 0.6},
            "otter": {"pitch_offset": 5, "brightness": 0.85},
            "phoenix": {"pitch_offset": 12, "brightness": 0.95},
            "swan": {"pitch_offset": 3, "brightness": 0.75},
            "lion": {"pitch_offset": -3, "brightness": 0.7},
            "hare": {"pitch_offset": 7, "brightness": 0.8},
        }

        # Find matching animal
        pitch_offset = 0
        brightness = 0.7
        for animal, params in animals.items():
            if animal in form_lower:
                pitch_offset = params["pitch_offset"]
                brightness = params["brightness"]
                break

        pitch_hz = self.pitch_base_hz * (2 ** (pitch_offset / 12.0))

        return SoundLayerOutput(
            pitch_hz=pitch_hz,
            loudness_db=loudness_base,
            timbre_brightness=brightness * clarity,
            timbre_roughness=(1.0 - clarity) * 0.3,
            timbre_warmth=0.7 * clarity,
            rhythm_bpm=60.0 + (clarity * 30),
            uncertainty_noise_level=(1.0 - clarity) * 0.3,
            source_emotion=patronus_form,
            source_intensity=clarity,
        )

    # --------------------------------------------------------------------------
    # VISION LAYER MAPPINGS
    # --------------------------------------------------------------------------

    def emotion_to_node(
        self,
        emotion: str,
        intensity: float = 1.0,
        node_id: str | None = None,
    ) -> VisionNode:
        """Create a Vision Layer node from an emotion.

        Args:
            emotion: The emotion type.
            intensity: Emotion intensity (affects size and glow).
            node_id: Optional custom node ID.

        Returns:
            VisionNode representing the emotion.
        """
        emotion_key = emotion.lower().strip()
        polarity = EMOTION_TO_POLARITY.get(emotion_key, Polarity.NEUTRAL)

        # Color by polarity
        color_map = {
            Polarity.SUPPORTIVE: "#4CAF50",  # Green
            Polarity.NEUTRAL: "#9E9E9E",  # Gray
            Polarity.ADVERSARIAL: "#F44336",  # Red
        }

        # Size scales with intensity
        size = NODE_SIZE_RANGE[0] + (intensity * (NODE_SIZE_RANGE[1] - NODE_SIZE_RANGE[0]))

        # Glow for high-intensity emotions
        glow = max(0.0, (intensity - 0.5) * 2.0)  # Only glows above 0.5 intensity

        return VisionNode(
            id=node_id or f"emotion_{emotion_key}",
            label=emotion_key.title(),
            type="emotion",
            size=size,
            color=color_map[polarity],
            glow=glow,
            metadata={
                "polarity": polarity.value,
                "intensity": intensity,
                "confidence_boost": EMOTION_CONFIDENCE_BOOST.get(emotion_key, 0.0),
            },
        )

    def patronus_to_node(
        self,
        patronus_form: str | None,
        caster: str = "Unknown",
        house: str = "unknown",
    ) -> VisionNode:
        """Create a Vision Layer node from a Patronus form.

        Args:
            patronus_form: The Patronus form string.
            caster: Name of the caster.
            house: Caster's Hogwarts house.

        Returns:
            VisionNode representing the Patronus.
        """
        if patronus_form is None:
            return VisionNode(
                id=f"patronus_failed_{caster.lower().replace(' ', '_')}",
                label="Failed Casting",
                type="patronus",
                size=NODE_SIZE_RANGE[0],
                color="#333333",
                glow=0.0,
                metadata={"caster": caster, "house": house, "success": False},
            )

        # Determine visual properties from form
        form_lower = patronus_form.lower()
        colors = HOUSE_COLORS.get(house.lower(), HOUSE_COLORS["unknown"])

        if "silver" in form_lower:
            glow = 1.0
            size = NODE_SIZE_RANGE[1]
            color = "#C0C0C0"  # Silver
        elif "incorporeal" in form_lower:
            glow = 0.3
            size = NODE_SIZE_RANGE[0] + 20
            color = colors["secondary"]
        else:
            glow = 0.7
            size = NODE_SIZE_RANGE[0] + 40
            color = colors["primary"]

        return VisionNode(
            id=f"patronus_{caster.lower().replace(' ', '_')}",
            label=patronus_form,
            type="patronus",
            size=size,
            color=color,
            glow=glow,
            metadata={"caster": caster, "house": house, "success": True},
        )

    def build_transformation_graph(
        self,
        emotion_sequence: list[str],
        intensities: list[float] | None = None,
    ) -> VisionLayerOutput:
        """Build a graph showing emotion transformation sequence.

        This creates a directed graph where nodes are emotions and edges
        represent transformations between emotional states.

        Args:
            emotion_sequence: List of emotions in transformation order.
            intensities: Optional list of intensities for each emotion.

        Returns:
            VisionLayerOutput containing the transformation graph.
        """
        if not emotion_sequence:
            return VisionLayerOutput()

        if intensities is None:
            intensities = [1.0] * len(emotion_sequence)

        output = VisionLayerOutput()

        # Create nodes for each emotion
        for i, emotion in enumerate(emotion_sequence):
            intensity = intensities[i] if i < len(intensities) else 1.0
            node = self.emotion_to_node(
                emotion,
                intensity=intensity,
                node_id=f"emotion_{i}_{emotion.lower()}",
            )
            output.add_node(node)

        # Create edges for transformations
        for i in range(len(emotion_sequence) - 1):
            source_emotion = emotion_sequence[i].lower()
            target_emotion = emotion_sequence[i + 1].lower()

            # Edge weight based on "distance" between emotions
            source_polarity = EMOTION_TO_POLARITY.get(source_emotion, Polarity.NEUTRAL)
            target_polarity = EMOTION_TO_POLARITY.get(target_emotion, Polarity.NEUTRAL)

            # Same polarity = stronger connection
            if source_polarity == target_polarity:
                weight = 0.8
                style = "solid"
            else:
                weight = 0.4
                style = "dashed"

            edge = VisionEdge(
                source=f"emotion_{i}_{source_emotion}",
                target=f"emotion_{i + 1}_{target_emotion}",
                relationship="transforms_to",
                weight=weight,
                style=style,
                color="#FFD700",  # Gold for transformation
            )
            output.add_edge(edge)

        return output

    def build_patronus_graph(
        self,
        presets: list[dict[str, Any]],
    ) -> VisionLayerOutput:
        """Build a graph showing Patronus relationships from lore presets.

        Args:
            presets: List of patronus preset dictionaries from hogwarts_lore.json.

        Returns:
            VisionLayerOutput containing the Patronus relationship graph.
        """
        output = VisionLayerOutput()

        for preset in presets:
            caster = preset.get("caster", "Unknown")
            form = preset.get("form", "Unknown")
            house = preset.get("house", "unknown")
            anchors = preset.get("temporal_anchors", {})

            # Add Patronus node
            patronus_node = self.patronus_to_node(form, caster, house)
            output.add_node(patronus_node)

            # Add caster node
            caster_node = VisionNode(
                id=f"caster_{caster.lower().replace(' ', '_')}",
                label=caster,
                type="character",
                size=60,
                color=HOUSE_COLORS.get(house.lower(), HOUSE_COLORS["unknown"])["primary"],
                glow=0.5,
                metadata={"house": house},
            )
            output.add_node(caster_node)

            # Add "casts" edge
            output.add_edge(
                VisionEdge(
                    source=caster_node.id,
                    target=patronus_node.id,
                    relationship="casts",
                    weight=0.9,
                    style="solid",
                    color="#C0C0C0",
                )
            )

            # Add temporal anchor nodes and edges
            for anchor_type, anchor_text in anchors.items():
                anchor_node = VisionNode(
                    id=f"anchor_{caster.lower().replace(' ', '_')}_{anchor_type}",
                    label=anchor_text[:30] + "..." if len(anchor_text) > 30 else anchor_text,
                    type="event",
                    size=30,
                    color="#6A5ACD",  # Slate blue for temporal events
                    glow=0.2,
                    metadata={"anchor_type": anchor_type, "full_text": anchor_text},
                )
                output.add_node(anchor_node)

                output.add_edge(
                    VisionEdge(
                        source=patronus_node.id,
                        target=anchor_node.id,
                        relationship="anchors_to",
                        weight=0.6,
                        style="dotted" if anchor_type == "future" else "solid",
                        color="#9370DB",  # Medium purple
                    )
                )

        return output

    # --------------------------------------------------------------------------
    # COMBINED SENSORY OUTPUT
    # --------------------------------------------------------------------------

    def create_full_sensory_state(
        self,
        emotion: str,
        intensity: float = 1.0,
        patronus_form: str | None = None,
        caster: str = "Unknown",
        house: str = "unknown",
    ) -> dict[str, Any]:
        """Create a complete sensory state combining Sound and Vision layers.

        Args:
            emotion: The driving emotion.
            intensity: Emotion intensity.
            patronus_form: Optional Patronus form if manifested.
            caster: Caster name.
            house: Caster's house.

        Returns:
            Dictionary with both sound_layer and vision_layer outputs.
        """
        # Generate sound output
        if patronus_form:
            sound = self.patronus_to_sound(patronus_form, house)
        else:
            sound = self.emotion_to_sound(emotion, intensity)

        # Generate vision output
        vision = VisionLayerOutput()

        # Add emotion node
        emotion_node = self.emotion_to_node(emotion, intensity)
        vision.add_node(emotion_node)

        # Add patronus node if manifested
        if patronus_form:
            patronus_node = self.patronus_to_node(patronus_form, caster, house)
            vision.add_node(patronus_node)

            # Add manifestation edge
            vision.add_edge(
                VisionEdge(
                    source=emotion_node.id,
                    target=patronus_node.id,
                    relationship="manifests_as",
                    weight=intensity,
                    style="animated" if "silver" in patronus_form.lower() else "solid",
                    color="#FFD700",
                )
            )

        # Calculate confidence from Grid perspective
        base_confidence = 0.5
        boost = EMOTION_CONFIDENCE_BOOST.get(emotion.lower(), 0.0)
        confidence = min(1.0, max(0.0, base_confidence + (intensity * 0.4) + boost))

        return {
            "sound_layer": sound.to_dict(),
            "vision_layer": vision.to_dict(),
            "grid_metrics": {
                "polarity": EMOTION_TO_POLARITY.get(emotion.lower(), Polarity.NEUTRAL).value,
                "confidence": confidence,
                "intensity": intensity,
                "source": "hogwarts_exhibit",
            },
            "metadata": {
                "emotion": emotion,
                "patronus_form": patronus_form,
                "caster": caster,
                "house": house,
            },
        }

    # --------------------------------------------------------------------------
    # LORE DATA LOADING
    # --------------------------------------------------------------------------

    def load_lore_data(self, lore_path: Path | str | None = None) -> dict[str, Any]:
        """Load Hogwarts lore data from JSON file.

        Args:
            lore_path: Path to hogwarts_lore.json. If None, uses default location.

        Returns:
            Parsed lore data dictionary.
        """
        if self._lore_data is not None:
            return self._lore_data

        if lore_path is None:
            # Default: same directory as this module
            lore_path = Path(__file__).parent / "hogwarts_lore.json"

        lore_path = Path(lore_path)

        if not lore_path.exists():
            print(f"Warning: Lore file not found at {lore_path}")
            return {}

        with open(lore_path, encoding="utf-8") as f:
            self._lore_data = json.load(f)

        return self._lore_data

    def get_patronus_presets(self) -> list[dict[str, Any]]:
        """Get all Patronus presets from lore data.

        Returns:
            List of patronus preset dictionaries.
        """
        lore = self.load_lore_data()
        presets = lore.get("patronus_presets", {})
        return [{"key": key, **value} for key, value in presets.items()]

    def get_house_info(self, house: str) -> dict[str, Any]:
        """Get house information from lore data.

        Args:
            house: House name (gryffindor, slytherin, ravenclaw, hufflepuff).

        Returns:
            House information dictionary.
        """
        lore = self.load_lore_data()
        houses = lore.get("houses", {})
        return houses.get(house.lower(), {})


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================


def create_bridge() -> HogwartsGridBridge:
    """Create a default HogwartsGridBridge instance."""
    return HogwartsGridBridge()


def emotion_to_sensory(
    emotion: str,
    intensity: float = 1.0,
) -> dict[str, Any]:
    """Quick conversion of emotion to sensory output.

    Example:
        >>> from grid_bridge import emotion_to_sensory
        >>> result = emotion_to_sensory("hopeful", intensity=0.9)
        >>> print(result["sound_layer"]["pitch"]["frequency_hz"])
    """
    bridge = HogwartsGridBridge()
    return bridge.create_full_sensory_state(emotion, intensity)


def patronus_to_sensory(
    patronus_form: str,
    caster: str = "Unknown",
    house: str = "unknown",
) -> dict[str, Any]:
    """Quick conversion of Patronus to sensory output.

    Example:
        >>> from grid_bridge import patronus_to_sensory
        >>> result = patronus_to_sensory("Silver Stag", "Harry Potter", "gryffindor")
        >>> print(result["vision_layer"]["graph"]["nodes"])
    """
    bridge = HogwartsGridBridge()
    # Infer emotion from patronus for combined output
    emotion = "brave"  # Default for Patronus casting
    return bridge.create_full_sensory_state(
        emotion=emotion,
        intensity=1.0,
        patronus_form=patronus_form,
        caster=caster,
        house=house,
    )


# ==============================================================================
# DEMO / SELF-TEST
# ==============================================================================


def _demo_sound_mappings(bridge: HogwartsGridBridge) -> None:
    """Demo: Emotion → Sound Layer mappings."""
    print("\n" + "=" * 60)
    print("SOUND LAYER MAPPINGS")
    print("=" * 60)

    emotions = ["happy", "sad", "brave", "hopeful", "grief"]
    for emotion in emotions:
        sound = bridge.emotion_to_sound(emotion, intensity=0.8)
        print(f"\n  {emotion.upper()}")
        print(f"    Pitch:      {sound.pitch_hz:.1f} Hz (MIDI {sound._hz_to_midi(sound.pitch_hz)})")
        print(f"    Loudness:   {sound.loudness_db:.1f} dB")
        print(f"    Brightness: {sound.timbre_brightness:.2f}")
        print(f"    Rhythm:     {sound.rhythm_bpm:.0f} BPM")


def _demo_patronus_sounds(bridge: HogwartsGridBridge) -> None:
    """Demo: Patronus → Sound Layer mappings."""
    print("\n" + "=" * 60)
    print("PATRONUS SOUND SIGNATURES")
    print("=" * 60)

    patronuses = [
        ("Silver Stag", "gryffindor"),
        ("Silver Doe", "slytherin"),
        ("Incorporeal Phoenix (mist)", "gryffindor"),
        (None, "unknown"),
    ]
    for form, house in patronuses:
        sound = bridge.patronus_to_sound(form, house)
        label = form or "Failed Casting"
        print(f"\n  {label}")
        print(f"    Pitch:      {sound.pitch_hz:.1f} Hz")
        print(f"    Loudness:   {sound.loudness_db:.1f} dB")
        print(f"    Brightness: {sound.timbre_brightness:.2f}")
        print(f"    Uncertainty:{sound.uncertainty_noise_level:.2f}")


def _demo_vision_graph(bridge: HogwartsGridBridge) -> None:
    """Demo: Emotion transformation → Vision Layer graph."""
    print("\n" + "=" * 60)
    print("VISION LAYER: TRANSFORMATION GRAPH")
    print("=" * 60)

    # Simulate an emotional journey: grief → bittersweet → hopeful
    sequence = ["grief", "sad", "bittersweet", "nostalgic", "hopeful"]
    intensities = [0.9, 0.7, 0.6, 0.5, 0.8]

    vision = bridge.build_transformation_graph(sequence, intensities)

    print(f"\n  Nodes: {len(vision.nodes)}")
    for node in vision.nodes:
        print(f"    - {node.label} (size={node.size:.0f}, glow={node.glow:.2f})")

    print(f"\n  Edges: {len(vision.edges)}")
    for edge in vision.edges:
        print(f"    - {edge.source.split('_')[-1]} → {edge.target.split('_')[-1]} [{edge.style}]")


def _demo_patronus_graph(bridge: HogwartsGridBridge) -> None:
    """Demo: Patronus presets → Vision Layer graph."""
    print("\n" + "=" * 60)
    print("VISION LAYER: PATRONUS RELATIONSHIP GRAPH")
    print("=" * 60)

    presets = bridge.get_patronus_presets()
    if not presets:
        print("  (No lore data loaded - skipping)")
        return

    vision = bridge.build_patronus_graph(presets[:3])  # First 3 for brevity

    print(f"\n  Nodes: {len(vision.nodes)}")
    for node in vision.nodes:
        print(f"    - [{node.type}] {node.label}")

    print(f"\n  Edges: {len(vision.edges)}")
    for edge in vision.edges:
        print(f"    - {edge.relationship}: {edge.source[:20]}... → {edge.target[:20]}...")


def _demo_full_sensory(bridge: HogwartsGridBridge) -> None:
    """Demo: Combined sensory state output."""
    print("\n" + "=" * 60)
    print("FULL SENSORY STATE")
    print("=" * 60)

    # Snape casting his doe
    state = bridge.create_full_sensory_state(
        emotion="loving",
        intensity=0.95,
        patronus_form="Silver Doe",
        caster="Severus Snape",
        house="slytherin",
    )

    print("\n  Snape's Patronus Manifestation:")
    print(f"    Grid Polarity:  {state['grid_metrics']['polarity']}")
    print(f"    Grid Confidence:{state['grid_metrics']['confidence']:.2f}")
    print(f"    Sound Pitch:    {state['sound_layer']['pitch']['frequency_hz']:.1f} Hz")
    print(f"    Sound Loudness: {state['sound_layer']['loudness']['db']:.1f} dB")
    print(f"    Vision Nodes:   {len(state['vision_layer']['graph']['nodes'])}")
    print(f"    Vision Edges:   {len(state['vision_layer']['graph']['edges'])}")


def _demo_json_export(bridge: HogwartsGridBridge) -> None:
    """Demo: JSON export for integration testing."""
    print("\n" + "=" * 60)
    print("JSON EXPORT (for Grid integration)")
    print("=" * 60)

    state = bridge.create_full_sensory_state(
        emotion="brave",
        intensity=0.85,
        patronus_form="Silver Stag",
        caster="Harry Potter",
        house="gryffindor",
    )

    # Pretty print a subset
    print("\n  Sample JSON output:")
    sample = {
        "grid_metrics": state["grid_metrics"],
        "sound_pitch_hz": state["sound_layer"]["pitch"]["frequency_hz"],
        "vision_node_count": len(state["vision_layer"]["graph"]["nodes"]),
    }
    print(f"    {json.dumps(sample, indent=4)}")


if __name__ == "__main__":
    print("=" * 60)
    print("HOGWARTS ⟷ GRID SENSORY BRIDGE")
    print("Emotion & Patronus → Sound Layer + Vision Layer")
    print("=" * 60)

    bridge = HogwartsGridBridge()

    _demo_sound_mappings(bridge)
    _demo_patronus_sounds(bridge)
    _demo_vision_graph(bridge)
    _demo_patronus_graph(bridge)
    _demo_full_sensory(bridge)
    _demo_json_export(bridge)

    print("\n" + "=" * 60)
    print("BRIDGE DEMO COMPLETE")
    print("=" * 60)
    print("\nThis module connects Hogwarts' emotion/patronus system to")
    print("Grid's Sound Layer and Vision Layer schemas for multi-sensory")
    print("representation of information dynamics.")
    print("\nUsage:")
    print("  from grid_bridge import HogwartsGridBridge, emotion_to_sensory")
    print("  bridge = HogwartsGridBridge()")
    print("  result = bridge.create_full_sensory_state('hopeful', 0.9)")
