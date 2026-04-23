"""ContextRefiner: root-level CLI tool to reduce pronouns and tighten context
between AI output and code.

Run from the repository root (e:\\grid):

    python context_refiner.py "the current test results show me the api is fine"
    echo "the current test results show me the api is fine" | python context_refiner.py

Prototype is intentionally simple and Python-basics-friendly.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

from core.tool_attributes import ToolProperty

TOOL_ATTRIBUTES = ToolProperty.transform()


PRONOUNS = {
    "i",
    "me",
    "my",
    "mine",
    "we",
    "us",
    "our",
    "ours",
    "you",
    "your",
    "yours",
    "he",
    "him",
    "his",
    "she",
    "her",
    "hers",
    "it",
    "its",
    "they",
    "them",
    "their",
    "theirs",
    "this",
    "that",
    "these",
    "those",
}


DEFAULT_CONTEXT_MAP: Dict[str, str] = {
    # Slightly richer pattern first so longer phrase wins
    "test results show": "test suite currently indicates",
    "test results": "test suite",
    "tests": "test suite",
    "result": "test outcome",
    "api": "API",
}


COMPRESSION_STOPWORDS = {
    "really",
    "just",
    "actually",
    "basically",
}


COMPRESSION_PHRASES: Dict[str, str] = {
    "in order to": "to",
    "due to the fact that": "because",
}


SEMANTIC_PHRASES: Dict[str, str] = {
    "looks like": "appears to",
    "seems to": "appears to",
    "kind of": "",
    "sort of": "",
}


TEMPORAL_PHRASES: Dict[str, str] = {
    "right now": "currently",
    "now": "currently",
    "today": "currently",
    "yesterday": "previously",
    "tomorrow": "upcoming",
}


def refine_text(
    text: str,
    context_map: Dict[str, str] | None = None,
    *,
    compress: bool = True,
    semantic: bool = True,
    temporal: bool = True,
) -> str:
    """Basic refinement: remove stand-alone pronouns and apply simple mappings.

    This is deliberately straightforward so you can read and modify it easily.
    """

    if context_map is None:
        context_map = DEFAULT_CONTEXT_MAP

    tokens = text.split()
    kept_tokens: list[str] = []
    for t in tokens:
        stripped = t.lower().strip(".,!?:;\"'’“”()[]{}<>-—")
        normalized = stripped.replace("’", "'")
        base = normalized.split("'")[0]
        if base in PRONOUNS:
            continue
        kept_tokens.append(t)

    refined = " ".join(kept_tokens)

    # Phrase-level replacements (order matters for multi-word keys)
    for vague, specific in sorted(context_map.items(), key=lambda kv: -len(kv[0])):
        refined = refined.replace(vague, specific)
        refined = refined.replace(vague.capitalize(), specific)

    if compress:
        refined = compress_text(refined)

    refined = apply_semantic_and_temporal(refined, semantic=semantic, temporal=temporal)

    return refined.strip()


def compress_text(text: str) -> str:
    tokens = text.split()
    kept_tokens = []
    for token in tokens:
        stripped = token.lower().strip(".,!?:;")
        if stripped in COMPRESSION_STOPWORDS:
            continue
        kept_tokens.append(token)

    compressed = " ".join(kept_tokens)

    for source, target in sorted(
        COMPRESSION_PHRASES.items(), key=lambda kv: -len(kv[0])
    ):
        compressed = compressed.replace(source, target)
        compressed = compressed.replace(source.capitalize(), target)

    return compressed.strip()


def apply_semantic_and_temporal(
    text: str,
    *,
    semantic: bool = True,
    temporal: bool = True,
) -> str:
    updated = text

    if semantic:
        for source, target in sorted(
            SEMANTIC_PHRASES.items(), key=lambda kv: -len(kv[0])
        ):
            updated = updated.replace(source, target)
            updated = updated.replace(source.capitalize(), target)

    if temporal:
        for source, target in sorted(
            TEMPORAL_PHRASES.items(), key=lambda kv: -len(kv[0])
        ):
            updated = updated.replace(source, target)
            updated = updated.replace(source.capitalize(), target)

    return " ".join(updated.split())


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refine copied AI/helper text before pasting into code, commits, or docs.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to refine. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        help="Path to a file whose contents will be refined.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive mode: refine multiple snippets in one session.",
    )
    return parser.parse_args(argv)


def interactive_loop() -> int:
    print(
        "Interactive mode: paste text, end with a line containing only 'EOF'. Type 'QUIT' to exit."
    )
    while True:
        print("\n--- New snippet (end with EOF, or QUIT to exit) ---")
        lines: list[str] = []
        for line in sys.stdin:
            stripped = line.rstrip("\n")
            marker = stripped.strip().upper()
            if marker == "QUIT":
                return 0
            if marker == "EOF":
                break
            lines.append(stripped)
        if not lines:
            break
        raw = "\n".join(lines)
        refined = refine_text(raw)
        print(refined)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if getattr(args, "file", None):
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
    elif args.text is not None:
        raw = args.text
    elif getattr(args, "interactive", False) or sys.stdin.isatty():
        return interactive_loop()
    else:
        raw = sys.stdin.read()

    refined = refine_text(raw)
    print(refined)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
