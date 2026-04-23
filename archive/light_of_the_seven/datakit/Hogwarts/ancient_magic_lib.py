"""Ancient Magic Library: Patronus Charm Casting via Emotion Transformation.

This module provides the AncientMagicLib and PatronusCaster classes for
dynamically transforming user emotions into Patronus forms.

The key insight is that emotions cannot be statically defined in a dataclass
because the transformation from emotion to Patronus form requires dynamic
lookup and state management during the asynchronous charm casting process.

Schema Implementation:
- AncientMagicLib: Handles the low-level charm casting and result retrieval
- PatronusCaster: High-level interface that orchestrates the casting process
- UserEmotion: Dynamic container for emotion state (not a frozen dataclass)
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum


class EmotionType(Enum):
    """Supported emotion types for Patronus casting."""

    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    HOPEFUL = "hopeful"
    LOVING = "loving"
    BRAVE = "brave"
    NOSTALGIC = "nostalgic"


@dataclass
class UserEmotion:
    """Dynamic container for user emotion state.

    NOTE: This is NOT a frozen dataclass because:
    1. Emotions can transform during the casting process
    2. Intensity may fluctuate as the charm takes hold
    3. The casting process may reveal deeper underlying emotions

    This solves the "static dataclass" parse error - emotions require
    mutable state for proper Patronus manifestation.
    """

    emotion_type: str
    intensity: float = 1.0  # 0.0 to 1.0
    underlying_emotion: str | None = None
    transformation_history: list[str] = field(default_factory=list)

    def transform(self, new_emotion: str) -> None:
        """Transform the emotion, tracking history."""
        self.transformation_history.append(self.emotion_type)
        self.underlying_emotion = self.emotion_type
        self.emotion_type = new_emotion

    def normalize(self) -> str:
        """Normalize emotion to lowercase for mapping lookup."""
        return self.emotion_type.lower().strip()


class AncientMagicLib:
    """Library for ancient Patronus charm magic.

    Methods:
        cast_patronus_charm(user_emotion: str) -> bool
            Initiates the charm casting process.

        get_patronus_result(user_emotion: str) -> str | None
            Retrieves the Patronus form once the charm completes.

    The emotion-to-Patronus mapping is dynamic, not static, because:
    - Different casters may manifest different forms for the same emotion
    - Emotional intensity affects form clarity
    - The charm itself may reveal hidden emotional truths
    """

    # Core emotion-to-Patronus mapping (canonical forms)
    EMOTION_PATRONUS_MAP: dict[str, str] = {
        "happy": "Stag",
        "sad": "Doe",
        "angry": "Wolf",
        "calm": "Otter",
        "hopeful": "Phoenix",
        "loving": "Swan",
        "brave": "Lion",
        "nostalgic": "Hare",
    }

    # Extended mappings for compound emotions
    COMPOUND_EMOTION_MAP: dict[str, str] = {
        "bittersweet": "Doe",  # Sad undertones
        "determined": "Stag",  # Happy resolve
        "protective": "Wolf",  # Channeled anger
        "serene": "Otter",  # Deep calm
        "grief": "Phoenix",  # Hope through loss
        "devotion": "Swan",  # Pure love
        "defiant": "Lion",  # Brave resistance
        "wistful": "Hare",  # Gentle nostalgia
    }

    def __init__(
        self,
        custom_mapping: dict[str, str] | None = None,
        casting_delay: float = 0.0,
    ):
        """Initialize the Ancient Magic Library.

        Args:
            custom_mapping: Optional custom emotion-to-Patronus mapping.
            casting_delay: Simulated delay for charm casting (seconds).
        """
        self._active_charms: dict[str, bool] = {}
        self._charm_results: dict[str, str | None] = {}
        self._casting_delay = casting_delay

        # Merge custom mappings with defaults
        self._emotion_map = {**self.EMOTION_PATRONUS_MAP}
        if custom_mapping:
            self._emotion_map.update(custom_mapping)

    def cast_patronus_charm(self, user_emotion: str | UserEmotion) -> bool:
        """Cast the Patronus charm with the given emotion.

        Args:
            user_emotion: The emotion powering the charm (string or UserEmotion).

        Returns:
            bool: True if charm casting initiated successfully, False otherwise.
        """
        # Handle both string and UserEmotion inputs
        if isinstance(user_emotion, UserEmotion):
            emotion_key = user_emotion.normalize()
            intensity = user_emotion.intensity
        else:
            emotion_key = user_emotion.lower().strip()
            intensity = 1.0

        # Validate emotion is mappable
        if (
            emotion_key not in self._emotion_map
            and emotion_key not in self.COMPOUND_EMOTION_MAP
        ):
            print(f"Warning: Unknown emotion '{emotion_key}'. Charm may fail.")
            self._active_charms[emotion_key] = False
            return False

        # Simulate charm casting
        print(
            f"Casting Patronus with emotion: {emotion_key} (intensity: {intensity:.2f})"
        )
        self._active_charms[emotion_key] = True

        # Pre-compute result (in real implementation, this would be async)
        if self._casting_delay > 0:
            time.sleep(self._casting_delay)

        # Determine Patronus form
        patronus_form = self._resolve_patronus_form(emotion_key, intensity)
        self._charm_results[emotion_key] = patronus_form

        return True

    def _resolve_patronus_form(
        self, emotion_key: str, intensity: float = 1.0
    ) -> str | None:
        """Resolve the Patronus form from emotion.

        Dynamic transformation logic:
        - High intensity (>0.8): Clear, fully-formed Patronus
        - Medium intensity (0.5-0.8): Standard form
        - Low intensity (<0.5): Incorporeal mist (may not manifest)
        """
        # Check compound emotions first
        if emotion_key in self.COMPOUND_EMOTION_MAP:
            base_form = self.COMPOUND_EMOTION_MAP[emotion_key]
        elif emotion_key in self._emotion_map:
            base_form = self._emotion_map[emotion_key]
        else:
            return None

        # Apply intensity modifiers
        if intensity < 0.3:
            return None  # Too weak to manifest
        elif intensity < 0.5:
            return f"Incorporeal {base_form} (mist)"
        elif intensity >= 0.8:
            return f"Silver {base_form}"
        else:
            return base_form

    def get_patronus_result(self, user_emotion: str | UserEmotion) -> str | None:
        """Get the result of a Patronus charm casting.

        Args:
            user_emotion: The emotion used in casting.

        Returns:
            Patronus form (string) if successful, None if still casting or failed.
        """
        if isinstance(user_emotion, UserEmotion):
            emotion_key = user_emotion.normalize()
        else:
            emotion_key = user_emotion.lower().strip()

        # Check if charm was cast
        if emotion_key not in self._active_charms:
            return None

        # Check if charm succeeded
        if not self._active_charms[emotion_key]:
            return None

        return self._charm_results.get(emotion_key)

    def register_emotion(self, emotion: str, patronus_form: str) -> None:
        """Dynamically register a new emotion-to-Patronus mapping.

        This is the key to solving the static dataclass limitation:
        mappings can be added at runtime.
        """
        self._emotion_map[emotion.lower().strip()] = patronus_form


class PatronusCaster:
    """High-level Patronus casting interface.

    Orchestrates the casting process by:
    1. Calling cast_patronus_charm from AncientMagicLib
    2. Polling get_patronus_result until a result is obtained
    3. Returning the final Patronus form

    This abstraction handles the async nature of charm casting
    and provides a clean synchronous interface.
    """

    def __init__(
        self,
        magic_lib: AncientMagicLib | None = None,
        max_attempts: int = 10,
        poll_interval: float = 0.1,
    ):
        """Initialize the PatronusCaster.

        Args:
            magic_lib: AncientMagicLib instance (created if not provided).
            max_attempts: Maximum polling attempts before giving up.
            poll_interval: Time between polling attempts (seconds).
        """
        self.magic_lib = magic_lib or AncientMagicLib()
        self.max_attempts = max_attempts
        self.poll_interval = poll_interval
        self._casting_callbacks: list[Callable[[str, str], None]] = []

    def cast_patronus(self, user_emotion: str | UserEmotion) -> str | None:
        """Cast a Patronus with the given emotion.

        Args:
            user_emotion: The emotion powering the Patronus.

        Returns:
            Patronus form (string) if successful, None if failed.

        Example:
            >>> caster = PatronusCaster()
            >>> result = caster.cast_patronus("happy")
            >>> print(result)  # "Silver Stag"
        """
        # Initiate the charm
        if not self.magic_lib.cast_patronus_charm(user_emotion):
            return None

        # Poll for result
        result = None
        for _attempt in range(self.max_attempts):
            result = self.magic_lib.get_patronus_result(user_emotion)
            if result is not None:
                break
            if self.poll_interval > 0:
                time.sleep(self.poll_interval)

        # Invoke callbacks
        if result:
            emotion_str = (
                user_emotion.emotion_type
                if isinstance(user_emotion, UserEmotion)
                else user_emotion
            )
            for callback in self._casting_callbacks:
                callback(emotion_str, result)

        return result

    def cast_with_emotion_object(self, emotion: UserEmotion) -> str | None:
        """Cast using a full UserEmotion object for fine-grained control.

        This method allows for emotion transformation during casting,
        which is impossible with a static/frozen dataclass.
        """
        return self.cast_patronus(emotion)

    def on_cast_complete(self, callback: Callable[[str, str], None]) -> PatronusCaster:
        """Register a callback for when casting completes.

        Args:
            callback: Function(emotion, patronus_form) to call.

        Returns:
            Self for method chaining.
        """
        self._casting_callbacks.append(callback)
        return self


# Convenience factory functions
def create_caster(custom_emotions: dict[str, str] | None = None) -> PatronusCaster:
    """Create a PatronusCaster with optional custom emotion mappings."""
    lib = AncientMagicLib(custom_mapping=custom_emotions)
    return PatronusCaster(magic_lib=lib)


def quick_cast(emotion: str) -> str | None:
    """Quick one-liner to cast a Patronus.

    Example:
        >>> from ancient_magic_lib import quick_cast
        >>> print(quick_cast("happy"))  # "Silver Stag"
    """
    return PatronusCaster().cast_patronus(emotion)


# Example usage and self-test
if __name__ == "__main__":
    print("=== Ancient Magic Library Demo ===\n")

    # Demo 1: Basic casting with string emotion
    print("1. Basic Casting:")
    caster = PatronusCaster()
    for emotion in ["happy", "sad", "angry", "calm"]:
        result = caster.cast_patronus(emotion)
        print(f"   {emotion} -> {result}")

    print()

    # Demo 2: Casting with UserEmotion object (dynamic transformation)
    print("2. Dynamic Emotion Transformation:")
    user_emotion = UserEmotion(emotion_type="sad", intensity=0.9)
    print(f"   Initial emotion: {user_emotion.emotion_type}")

    # Emotion transforms during the process (this is why we can't use frozen dataclass)
    user_emotion.transform("bittersweet")
    print(f"   Transformed to: {user_emotion.emotion_type}")
    print(f"   History: {user_emotion.transformation_history}")

    result = caster.cast_patronus(user_emotion)
    print(f"   Final Patronus: {result}")

    print()

    # Demo 3: Intensity affects manifestation
    print("3. Intensity Effects:")
    lib = AncientMagicLib()
    for intensity in [0.2, 0.4, 0.6, 1.0]:
        emotion = UserEmotion(emotion_type="happy", intensity=intensity)
        lib.cast_patronus_charm(emotion)
        result = lib.get_patronus_result(emotion)
        print(f"   happy @ {intensity:.1f} intensity -> {result}")

    print()

    # Demo 4: Custom emotion registration (dynamic, not static)
    print("4. Dynamic Emotion Registration:")
    custom_lib = AncientMagicLib()
    custom_lib.register_emotion("melancholy", "Thestral")
    custom_lib.register_emotion("euphoric", "Hippogriff")

    caster = PatronusCaster(magic_lib=custom_lib)
    print(f"   melancholy -> {caster.cast_patronus('melancholy')}")
    print(f"   euphoric -> {caster.cast_patronus('euphoric')}")

    print("\n=== Demo Complete ===")
