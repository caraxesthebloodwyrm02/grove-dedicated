"""Simple example demonstrating backend selection with TranslatorAssistant.

This module is safe to import and provides run_demo() which returns demo
results so tests can exercise the example without touching real external
resources.
"""

import json
import tempfile
from pathlib import Path

from grid.services.translator_assistant.service import TranslatorAssistant


def _write_demo_forms(directory: Path) -> None:
    request_form = {
        "id": "TranslatorAssistantRequest",
        "type": "form",
        "title": "Translator Assistant – Request",
        "fields": [
            {
                "name": "source_text",
                "label": "Source Text",
                "type": "textarea",
                "required": True,
            },
            {
                "name": "source_language",
                "label": "Source Language",
                "type": "text",
                "required": False,
                "default": "auto",
            },
            {
                "name": "target_language",
                "label": "Target Language(s)",
                "type": "text",
                "required": True,
            },
        ],
    }

    segment_form = {
        "id": "TranslatorAssistantSegment",
        "type": "form",
        "title": "Translator Assistant – Segment",
        "fields": [
            {"name": "source", "label": "Source", "type": "textarea", "required": True},
            {"name": "result", "label": "Result", "type": "textarea", "required": True},
        ],
    }

    response_form = {
        "id": "TranslatorAssistantResponse",
        "type": "form",
        "title": "Translator Assistant – Response",
        "fields": [
            {
                "name": "result_text",
                "label": "Result Text",
                "type": "textarea",
                "readonly": True,
            },
            {
                "name": "target_language",
                "label": "Target Language(s)",
                "type": "text",
                "readonly": True,
            },
        ],
    }

    (directory / "request_assistant_api.json").write_text(json.dumps(request_form))
    (directory / "assistant_segment.json").write_text(json.dumps(segment_form))
    (directory / "assistant_response.json").write_text(json.dumps(response_form))


def run_demo():
    """Create a temporary TranslatorAssistant and run two requests.

    Returns a dict with 'mock' and 'dummy_rule' results so tests can assert outputs.
    """
    with tempfile.TemporaryDirectory() as td:
        data_dir = Path(td)
        _write_demo_forms(data_dir)

        assistant = TranslatorAssistant(data_dir=data_dir)

        # request 1: default mock backend (uses mock behavior)
        req1 = {
            "source_text": "Hello demo",
            "target_language": "es",
            "mode": "translate",
        }
        r1_obj = assistant.create_request(req1)
        r1 = assistant.process_request(r1_obj)

        # request 2: use deterministic dummy_rule backend
        req2 = {
            "source_text": "one two three",
            "target_language": "fr",
            "mode": "translate",
            "model_name": "dummy_rule",
        }
        r2_obj = assistant.create_request(req2)
        r2 = assistant.process_request(r2_obj)

        return {"mock": r1, "dummy_rule": r2}


if __name__ == "__main__":
    out = run_demo()
    print("mock result:\n", out["mock"].result_text)
    print("\ndummy result:\n", out["dummy_rule"].result_text)
