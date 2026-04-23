"""
NER Training Module
Trains Named Entity Recognition on GRID-specific entities and patterns
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from core.tool_attributes import ToolProperty

TOOL_ATTRIBUTES = ToolProperty.transform()


class NERTrainer:
    """Train NER on GRID domain-specific entities"""

    def __init__(self):
        self.training_data = []
        self.entity_types = {
            "COMPONENT": [
                "CommunicationTracer",
                "ReverbDecay",
                "EntityHarmonizer",
                "NERKeywordDetector",
            ],
            "RAILWAY_TERM": [
                "Block System",
                "Interlocking",
                "Telegraph",
                "Signal Box",
                "Track Circuit",
            ],
            "AUDIO_CONCEPT": ["Echoes", "Reverb", "Delay", "EQ", "Frequency"],
            "RISK_LEVEL": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "SCOPE_KEYWORD": [
                "all",
                "everything",
                "every",
                "entire",
                "complete",
                "total",
            ],
            "PHASE": [
                "Planning",
                "Construction",
                "Operation",
                "Maintenance",
                "Expansion",
            ],
            "GEN_Z_METRIC": [
                "screen time",
                "anxiety",
                "work-life balance",
                "hybrid work",
            ],
            "WATCH_MODULE": [
                "Module 0",
                "Module 1",
                "Module 2",
                "Module 3",
                "Module 4",
            ],
        }

        self.patterns = []

    def add_training_example(self, text: str, entities: List[Dict[str, Any]]):
        """Add a labeled training example"""
        self.training_data.append(
            {
                "text": text,
                "entities": entities,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def generate_training_data(self):
        """Generate training data from session artifacts"""

        # Example 1: Communication Discovery
        self.add_training_example(
            "CommunicationTracer tracks all WebSocket events with HIGH risk threshold",
            [
                {"start": 0, "end": 19, "label": "COMPONENT"},
                {"start": 30, "end": 39, "label": "AUDIO_CONCEPT"},
                {"start": 52, "end": 56, "label": "RISK_LEVEL"},
            ],
        )

        # Example 2: Railway metaphor
        self.add_training_example(
            "The Block System prevents conflicting routes like a Circuit Breaker",
            [
                {"start": 4, "end": 16, "label": "RAILWAY_TERM"},
                {"start": 56, "end": 71, "label": "COMPONENT"},
            ],
        )

        # Example 3: Scope expansion
        self.add_training_example(
            "Delete all users in Operation phase is CRITICAL risk",
            [
                {"start": 7, "end": 10, "label": "SCOPE_KEYWORD"},
                {"start": 20, "end": 29, "label": "PHASE"},
                {"start": 40, "end": 48, "label": "RISK_LEVEL"},
            ],
        )

        # Example 4: Audio architecture
        self.add_training_example(
            "Echoes amplify recurring patterns while Reverb applies temporal decay",
            [
                {"start": 0, "end": 6, "label": "AUDIO_CONCEPT"},
                {"start": 40, "end": 46, "label": "AUDIO_CONCEPT"},
            ],
        )

        # Example 5: Gen Z
        self.add_training_example(
            "Gen Z spends 6.5 hours screen time daily with HIGH anxiety levels",
            [
                {"start": 17, "end": 28, "label": "GEN_Z_METRIC"},
                {"start": 46, "end": 50, "label": "RISK_LEVEL"},
                {"start": 51, "end": 58, "label": "GEN_Z_METRIC"},
            ],
        )

        # Example 6: Watch modules
        self.add_training_example(
            "Module 2 adds Safety with retry logic and Module 4 implements audio architecture",
            [
                {"start": 0, "end": 8, "label": "WATCH_MODULE"},
                {"start": 43, "end": 51, "label": "WATCH_MODULE"},
            ],
        )

        # Example 7: Railway history
        self.add_training_example(
            "Track Circuit innovation in 1870s enabled automatic Block System",
            [
                {"start": 0, "end": 13, "label": "RAILWAY_TERM"},
                {"start": 54, "end": 66, "label": "RAILWAY_TERM"},
            ],
        )

        # Example 8: Integration
        self.add_training_example(
            "EntityHarmonizer merges all duplicate entities across GRID and Atmosphere",
            [
                {"start": 0, "end": 16, "label": "COMPONENT"},
                {"start": 24, "end": 27, "label": "SCOPE_KEYWORD"},
            ],
        )

    def extract_patterns(self):
        """Extract common patterns from training data"""
        patterns = []

        for example in self.training_data:
            text = example["text"]
            for entity in example["entities"]:
                entity_text = text[entity["start"] : entity["end"]]
                pattern = {
                    "text": entity_text,
                    "label": entity["label"],
                    "context": text[
                        max(0, entity["start"] - 20) : min(
                            len(text), entity["end"] + 20
                        )
                    ],
                }
                patterns.append(pattern)

        self.patterns = patterns
        return patterns

    def save_training_data(self, filepath: str = "ner_training_data.json"):
        """Save training data to file"""
        data = {
            "entity_types": self.entity_types,
            "training_examples": self.training_data,
            "patterns": self.patterns,
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_examples": len(self.training_data),
                "total_patterns": len(self.patterns),
            },
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Saved {len(self.training_data)} training examples to {filepath}")
        return filepath

    def show_training_summary(self):
        """Display training summary"""
        print("\n" + "=" * 60)
        print("NER TRAINING SUMMARY")
        print("=" * 60)

        print(f"\n📊 Statistics:")
        print(f"   Entity Types: {len(self.entity_types)}")
        print(f"   Training Examples: {len(self.training_data)}")
        print(f"   Extracted Patterns: {len(self.patterns)}")

        print(f"\n🏷️ Entity Types:")
        for entity_type, examples in self.entity_types.items():
            print(f"   {entity_type}: {len(examples)} examples")

        if self.patterns:
            print(f"\n🔍 Sample Patterns:")
            for pattern in self.patterns[:5]:
                print(f"   '{pattern['text']}' → {pattern['label']}")

        print("\n" + "=" * 60 + "\n")


def main():
    """Train NER on GRID domain"""
    print("🧠 Starting NER Training...")

    trainer = NERTrainer()

    # Generate training data
    print("📝 Generating training data from session...")
    trainer.generate_training_data()

    # Extract patterns
    print("🔍 Extracting patterns...")
    trainer.extract_patterns()

    # Save
    filepath = trainer.save_training_data("e:/grid/ner_training_data.json")

    # Summary
    trainer.show_training_summary()

    print(f"✅ NER training complete!")
    print(f"📁 Training data saved to: {filepath}")


if __name__ == "__main__":
    main()
