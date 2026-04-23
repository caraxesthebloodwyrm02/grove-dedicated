#!/usr/bin/env python3
"""
Demo script for the Translator Assistant service.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from services.translator_assistant import TranslatorAssistant


def main():
    """Run the translator assistant demo."""
    print("=== Translator Assistant Demo ===\n")

    # Initialize the assistant
    try:
        assistant = TranslatorAssistant()
        print("✓ Translator Assistant initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize assistant: {e}")
        return

    # Show available form specifications
    print("\n--- Available Forms ---")
    for form_name in ["request", "segment", "response"]:
        spec = assistant.get_form_spec(form_name)
        print(f"{form_name.title()}: {spec.title}")
        print(f"  Fields: {len(spec.fields)}")
        for field in spec.fields:
            required = "required" if field.required else "optional"
            print(f"  - {field.name} ({field.type}, {required})")
        print()

    # Demo 1: Simple translation
    print("--- Demo 1: Simple Translation ---")
    request_data = {
        "source_text": "Hello, world! How are you today?",
        "source_language": "en",
        "target_language": "es",
        "mode": "translate",
        "domain": "general",
    }

    try:
        # Validate the request
        validation = assistant.validate_request(request_data)
        if validation["valid"]:
            print("✓ Request validation passed")
        else:
            print("✗ Request validation failed:")
            for error in validation["errors"]:
                print(f"  - {error}")
            return

        # Create and process the request
        request = assistant.create_request(request_data)
        response = assistant.process_request(request)

        print(f"Source: {request.source_text}")
        print(f"Target Language: {response.target_language}")
        print(f"Result: {response.result_text}")
        print(f"Confidence: {response.confidence}")
        if response.explanation:
            print(f"Explanation: {response.explanation}")

    except Exception as e:
        print(f"✗ Error processing request: {e}")

    print()

    # Demo 2: Explanation mode
    print("--- Demo 2: Explanation Mode ---")
    explanation_data = {
        "source_text": "The quick brown fox jumps over the lazy dog.",
        "source_language": "en",
        "target_language": "en",
        "mode": "explain",
        "domain": "general",
    }

    try:
        request = assistant.create_request(explanation_data)
        response = assistant.process_request(request)

        print(f"Text: {request.source_text}")
        print(f"Mode: {request.mode}")
        print(f"Explanation: {response.result_text}")

    except Exception as e:
        print(f"✗ Error processing explanation: {e}")

    print()

    # Demo 3: Long text with segments
    print("--- Demo 3: Long Text with Segments ---")
    long_text = """
    Artificial intelligence is transforming the way we work and live.
    Machine learning algorithms can now recognize patterns in vast amounts of data.
    Natural language processing enables computers to understand human language.
    Computer vision allows machines to interpret visual information.
    """.strip()

    long_data = {
        "source_text": long_text,
        "source_language": "en",
        "target_language": "fr",
        "mode": "translate",
        "domain": "scientific_research",
    }

    try:
        request = assistant.create_request(long_data)
        response = assistant.process_request(request)

        print(f"Original text ({len(long_text)} characters)")
        print(f"Translation: {response.result_text[:200]}...")

        if response.segments:
            print(f"\nSegments generated: {len(response.segments)}")
            for i, segment in enumerate(response.segments[:3]):  # Show first 3
                print(f"  Segment {i+1}: {segment.source[:50]}...")
                print(f"    -> {segment.result[:50]}...")

    except Exception as e:
        print(f"✗ Error processing long text: {e}")

    print()

    # Demo 4: Creating segments manually
    print("--- Demo 4: Manual Segment Creation ---")
    segment_data = {
        "source": "Hello world",
        "result": "Bonjour le monde",
        "comment": "Simple greeting translation",
    }

    try:
        segment = assistant.create_segment(segment_data)
        print(f"Source: {segment.source}")
        print(f"Result: {segment.result}")
        print(f"Comment: {segment.comment}")

    except Exception as e:
        print(f"✗ Error creating segment: {e}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
