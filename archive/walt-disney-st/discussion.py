from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


@dataclass
class Report:
    modules: int
    functions: int
    classes: int
    avg_lines: float
    missing_doc_modules: int
    missing_doc_functions: int


def load_artifacts(path: Path) -> list[dict[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"Unable to read {path}: {exc}") from exc


def summarize(artifacts: Iterable[dict[str, Any]]) -> Report:
    artifacts = list(artifacts)
    modules = len(artifacts)
    functions = sum(len(m.get("functions", [])) for m in artifacts)
    classes = sum(len(m.get("classes", [])) for m in artifacts)
    total_lines = sum(m.get("total_lines", 0) for m in artifacts)
    missing_doc_modules = sum(1 for m in artifacts if not m.get("has_doc"))
    missing_doc_functions = sum(
        1
        for m in artifacts
        for f in m.get("functions", [])
        if not f.get("has_doc")
    ) + sum(
        1
        for m in artifacts
        for c in m.get("classes", [])
        for f in c.get("methods", [])
        if not f.get("has_doc")
    )
    avg_lines = (total_lines / modules) if modules else 0.0
    return Report(
        modules=modules,
        functions=functions,
        classes=classes,
        avg_lines=avg_lines,
        missing_doc_modules=missing_doc_modules,
        missing_doc_functions=missing_doc_functions,
    )


def render_report(report: Report) -> str:
    lines = [
        "Discussion Report",
        "=================",
        f"Modules: {report.modules}",
        f"Functions: {report.functions}",
        f"Classes: {report.classes}",
        f"Average lines per module: {report.avg_lines:.1f}",
        f"Modules missing docstring: {report.missing_doc_modules}",
        f"Functions/methods missing docstring: {report.missing_doc_functions}",
    ]
    return "\n".join(lines)


def render_generated_code() -> str:
    return """// Example Rust struct mirroring Python artifact contracts
#[derive(Debug, Clone)]
pub struct FunctionArtifact {
    pub name: String,
    pub lineno: usize,
    pub args: usize,
    pub has_doc: bool,
    pub is_async: bool,
}

// Example Python dataclass
# @dataclass
# class FunctionArtifact:
#     name: str
#     lineno: int
#     args: int
#     has_doc: bool
#     is_async: bool
"""


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate discussion reports from artifact JSON."
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        default=Path("artifact.json"),
        help="Path to artifact JSON (default: artifact.json)",
    )
    parser.add_argument(
        "--show-code",
        action="store_true",
        help="Also print an example of generated code mappings.",
    )
    args = parser.parse_args(argv)

    artifacts = load_artifacts(args.artifact)
    report = summarize(artifacts)
    print(render_report(report))
    if args.show_code:
        print()
        print("Generated code examples:")
        print(render_generated_code())


if __name__ == "__main__":
    main()
