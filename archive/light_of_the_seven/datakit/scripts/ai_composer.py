"""
AI-driven music generation using the Circle of Fifths.

This script uses:
- Markov chains to model chord progressions.
- Reinforcement learning to optimize harmonic transitions.
- Neural networks for generative music composition.

Requirements:
- numpy
- tensorflow (for neural networks)
- markovify (for Markov chains)
"""

import json
import random
from typing import Dict, List, Optional

import markovify  # type: ignore
import numpy as np

# Define the Circle of Fifths (clockwise)
CIRCLE_OF_FIFTHS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]

# Define chord types (e.g., major, minor, diminished)
CHORD_TYPES = {
    "major": ["I", "IV", "V"],
    "minor": ["ii", "iii", "vi"],
    "diminished": ["vii°"],
}

# Define transition probabilities for Markov chains
TRANSITION_PROBS = {
    "C": {"G": 0.7, "F": 0.3},
    "G": {"D": 0.7, "C": 0.3},
    "D": {"A": 0.7, "G": 0.3},
    "A": {"E": 0.7, "D": 0.3},
    "E": {"B": 0.7, "A": 0.3},
    "B": {"F#": 0.7, "E": 0.3},
    "F#": {"C#": 0.7, "B": 0.3},
    "C#": {"G#": 0.7, "F#": 0.3},
    "G#": {"D#": 0.7, "C#": 0.3},
    "D#": {"A#": 0.7, "G#": 0.3},
    "A#": {"F": 0.7, "D#": 0.3},
    "F": {"C": 0.7, "A#": 0.3},
}


class MarkovChainComposer:
    """Compose music using Markov chains."""

    def __init__(self, transition_probs: Optional[Dict] = None):
        """
        Initialize the Markov chain composer.

        Args:
            transition_probs: A dictionary of transition probabilities.
                             If None, uses default probabilities.
        """
        self.transition_probs = transition_probs or TRANSITION_PROBS
        self.model = self._build_markov_model()

    def _build_markov_model(self) -> markovify.Chain:
        """
        Build a Markov chain model for chord progressions.

        Returns:
            A Markov chain model.
        """
        # Convert transition probabilities to a format markovify can use
        corpus = []
        for start_key, transitions in self.transition_probs.items():
            for end_key, prob in transitions.items():
                corpus.extend([start_key] * int(prob * 100))
                corpus.append(end_key)

        return markovify.Chain(corpus, state_size=1)

    def generate_progression(self, start_key: str, length: int = 4) -> List[str]:
        """
        Generate a chord progression using the Markov chain.

        Args:
            start_key: The starting key (e.g., "C").
            length: The length of the progression (default: 4).

        Returns:
            A list of keys representing the progression.
        """
        progression = [start_key]
        for _ in range(length - 1):
            next_key = self.model.move(progression[-1])
            progression.append(next_key)
        return progression


class ReinforcementLearningComposer:
    """Compose music using reinforcement learning."""

    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9):
        """
        Initialize the reinforcement learning composer.

        Args:
            learning_rate: The learning rate for Q-learning (default: 0.1).
            discount_factor: The discount factor for Q-learning (default: 0.9).
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_table = self._initialize_q_table()

    def _initialize_q_table(self) -> Dict:
        """
        Initialize the Q-table for reinforcement learning.

        Returns:
            A Q-table (dictionary of dictionaries).
        """
        q_table = {}
        for key in CIRCLE_OF_FIFTHS:
            q_table[key] = {}
            for next_key in CIRCLE_OF_FIFTHS:
                q_table[key][next_key] = 0.0
        return q_table

    def _get_reward(self, current_key: str, next_key: str) -> float:
        """
        Calculate the reward for transitioning from `current_key` to `next_key`.

        Args:
            current_key: The current key (e.g., "C").
            next_key: The next key (e.g., "G").

        Returns:
            A reward value (higher is better).
        """
        # Reward smooth transitions (e.g., perfect fifths)
        current_idx = CIRCLE_OF_FIFTHS.index(current_key)
        next_idx = CIRCLE_OF_FIFTHS.index(next_key)
        distance = abs(next_idx - current_idx)

        if distance == 1 or distance == len(CIRCLE_OF_FIFTHS) - 1:
            return 1.0  # Perfect fifth or fourth
        elif distance == 5 or distance == len(CIRCLE_OF_FIFTHS) - 5:
            return 0.5  # Major third or minor sixth
        else:
            return -1.0  # Dissonant interval

    def update_q_table(
        self, current_key: str, next_key: str, reward: Optional[float] = None
    ) -> None:
        """
        Update the Q-table based on the observed reward.

        Args:
            current_key: The current key (e.g., "C").
            next_key: The next key (e.g., "G").
            reward: The observed reward. If None, calculates it.
        """
        if reward is None:
            reward = self._get_reward(current_key, next_key)

        # Q-learning update rule
        max_future_q = max(self.q_table[next_key].values())
        current_q = self.q_table[current_key][next_key]
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_future_q - current_q
        )
        self.q_table[current_key][next_key] = new_q

    def generate_progression(self, start_key: str, length: int = 4) -> List[str]:
        """
        Generate a chord progression using Q-learning.

        Args:
            start_key: The starting key (e.g., "C").
            length: The length of the progression (default: 4).

        Returns:
            A list of keys representing the progression.
        """
        progression = [start_key]
        for _ in range(length - 1):
            # Choose the next key with the highest Q-value
            next_key = max(self.q_table[progression[-1]].items(), key=lambda x: x[1])[0]
            progression.append(next_key)
            # Update the Q-table
            self.update_q_table(progression[-2], progression[-1])
        return progression


class NeuralNetworkComposer:
    """Compose music using a neural network (placeholder)."""

    def __init__(self):
        """Initialize the neural network composer."""
        self.model = self._build_neural_network()

    def _build_neural_network(self):
        """Build a neural network for music generation (placeholder)."""
        # In a real implementation, this would use TensorFlow/Keras
        return None

    def generate_progression(self, start_key: str, length: int = 4) -> List[str]:
        """
        Generate a chord progression using a neural network (placeholder).

        Args:
            start_key: The starting key (e.g., "C").
            length: The length of the progression (default: 4).

        Returns:
            A list of keys representing the progression.
        """
        # Placeholder: Random progression
        return [random.choice(CIRCLE_OF_FIFTHS) for _ in range(length)]


def load_ai_links() -> Dict:
    """
    Load AI-driven music generation rules.

    Returns:
        A dictionary containing AI-driven rules.
    """
    try:
        with open("../data/ai_links.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def main():
    """Run the AI-driven music composer."""
    print("=== AI-Driven Music Composer ===")
    print("Choose a composition method:")
    print("1. Markov Chains")
    print("2. Reinforcement Learning")
    print("3. Neural Network (Placeholder)")

    choice = input("Enter your choice (1-3): ").strip()

    start_key = input("Enter a starting key (e.g., C, G, D): ").strip().capitalize()
    if start_key not in CIRCLE_OF_FIFTHS:
        print("Invalid key. Defaulting to C.")
        start_key = "C"

    if choice == "1":
        composer = MarkovChainComposer()
        print("\n🎹 Generating progression using Markov Chains...")
    elif choice == "2":
        composer = ReinforcementLearningComposer()
        print("\n🎹 Generating progression using Reinforcement Learning...")
    elif choice == "3":
        composer = NeuralNetworkComposer()
        print("\n🎹 Generating progression using a Neural Network (Placeholder)...")
    else:
        print("Invalid choice. Defaulting to Markov Chains.")
        composer = MarkovChainComposer()

    progression = composer.generate_progression(start_key)
    print(f"\nChord Progression: {' → '.join(progression)}")

    # Load AI links
    ai_links = load_ai_links()
    if ai_links:
        print("\nAI-Driven Rules:")
        print(ai_links.get("circle_ai", {}).get("script", "No rules found."))


if __name__ == "__main__":
    main()
