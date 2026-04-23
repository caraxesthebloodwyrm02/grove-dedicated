from dataclasses import dataclass
from math import sqrt
from typing import List, Tuple

SPEED_OF_SOUND = 343.0


@dataclass
class Room:
    length: float
    width: float
    height: float


@dataclass
class Source:
    x: float
    y: float
    z: float


def reflection_times_and_amplitudes(room: Room, source: Source, tap_energy: float = 1.0) -> List[Tuple[float, str, float]]:
    distances = [
        source.x,
        room.length - source.x,
        source.y,
        room.width - source.y,
        source.z,
        room.height - source.z,
    ]

    reflections: List[Tuple[float, str, float]] = []
    labels = ["x-", "x+", "y-", "y+", "z-", "z+"]

    for label, distance in zip(labels, distances):
        time_s = max(distance, 0.0) / SPEED_OF_SOUND
        amplitude = tap_energy / max(distance, 1e-6)
        reflections.append((time_s, label, amplitude))

    reflections.sort(key=lambda item: item[0])
    return reflections


def modal_frequencies(room: Room, max_mode: int = 2) -> List[Tuple[Tuple[int, int, int], float]]:
    modes: List[Tuple[Tuple[int, int, int], float]] = []
    for n in range(max_mode + 1):
        for m in range(max_mode + 1):
            for mode_l in range(max_mode + 1):
                if (n, m, mode_l) == (0, 0, 0):
                    continue
                freq = (SPEED_OF_SOUND / 2.0) * sqrt(
                    (n / room.length) ** 2 + (m / room.width) ** 2 + (mode_l / room.height) ** 2
                )
                modes.append(((n, m, mode_l), freq))

    modes.sort(key=lambda item: item[1])
    return modes
