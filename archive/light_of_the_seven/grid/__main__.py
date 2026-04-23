from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional


def _read_text(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if args.text is None:
        raise SystemExit("TEXT is required unless --file is provided")
    return args.text


def _format_output(payload: Dict[str, Any], output: str) -> str:
    if output == "json":
        return json.dumps(payload, indent=2, ensure_ascii=False)

    if output == "yaml":
        try:
            import yaml  # type: ignore
        except Exception as e:
            raise SystemExit(f"YAML output requested but PyYAML is not installed: {e}") from e
        return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)

    if output == "table":
        lines = ["GRID Analyze Result", ""]
        lines.append(f"Text length: {len(payload.get('text', ''))}")
        lines.append(f"Entities: {len(payload.get('entities', []))}")
        lines.append(f"Relationships: {len(payload.get('relationships', []))}")
        if payload.get("note"):
            lines.append("")
            lines.append(str(payload["note"]))
        return "\n".join(lines)

    raise SystemExit(f"Unknown output format: {output}")


def analyze_command(args: argparse.Namespace) -> int:
    start = time.perf_counter()

    text = _read_text(args)

    init_end = time.perf_counter()

    payload: Dict[str, Any] = {
        "text": text,
        "entities": [],
        "relationships": [],
        "confidence_threshold": args.confidence,
        "max_entities": args.max_entities,
        "use_rag": bool(args.use_rag),
    }

    if args.use_rag:
        payload["note"] = (
            "RAG is not available from this CLI in the current workspace snapshot. "
            "Use tools/rag/cli.py for RAG operations."
        )

    ner_end = time.perf_counter()
    rel_end = ner_end

    if args.timings:
        timings = {
            "init_ms": (init_end - start) * 1000,
            "ner_ms": (ner_end - init_end) * 1000,
            "relationships_ms": (rel_end - ner_end) * 1000,
            "total_ms": (rel_end - start) * 1000,
        }
        print(json.dumps(timings, indent=2), file=sys.stderr)

    sys.stdout.write(_format_output(payload, args.output))
    sys.stdout.write("\n")
    return 0


def serve_command(args: argparse.Namespace) -> int:
    try:
        from backend.server import main as server_main
    except Exception as e:
        raise SystemExit(f"Unable to import backend server entrypoint: {e}") from e

    server_main()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="grid")
    subparsers = parser.add_subparsers(dest="command")

    analyze = subparsers.add_parser("analyze", help="Analyze text (fallback implementation)")
    analyze.add_argument("text", nargs="?", help="Text to analyze")
    analyze.add_argument("--file", help="Read text from file")
    analyze.add_argument("--output", choices=["json", "table", "yaml"], default="table")
    analyze.add_argument("--use-rag", action="store_true", default=False)
    analyze.add_argument("--openai-key")
    analyze.add_argument("--confidence", type=float, default=0.7)
    analyze.add_argument("--max-entities", type=int, default=0)
    analyze.add_argument("--timings", action="store_true", default=False)
    analyze.add_argument("--debug", action="store_true", default=False)
    analyze.set_defaults(func=analyze_command)

    serve = subparsers.add_parser("serve", help="Run the local Mothership backend server")
    serve.set_defaults(func=serve_command)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 1

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1

    if getattr(args, "debug", False):
        debug_payload = {
            "command": args.command,
            "python": sys.version,
            "executable": sys.executable,
            "cwd": str(Path.cwd()),
        }
        print(json.dumps(debug_payload, indent=2), file=sys.stderr)

    return int(func(args))


if __name__ == "__main__":
    raise SystemExit(main())
