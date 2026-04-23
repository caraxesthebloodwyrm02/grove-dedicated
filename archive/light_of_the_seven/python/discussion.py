"""Discussion report generation and code demonstration."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


@dataclass
class Report:
    """Discussion report structure."""

    modules: int
    functions: int
    classes: int
    avg_lines: float
    missing_docs_modules: int
    missing_docs_functions: int


def load_artifacts(path: Path) -> list[dict[str, Any]]:
    """Load artifacts with UTF-8 BOM tolerance."""
    encodings = ["utf-8-sig", "utf-8", "utf-16"]
    last_error: Exception | None = None

    for encoding in encodings:
        try:
            content = path.read_text(encoding=encoding)
            if not content.strip():
                raise ValueError(f"File {path} is empty")
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError(f"Expected list, got {type(data).__name__}")
            return data
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as e:
            last_error = e
            continue

    if last_error:
        raise ValueError(f"Could not load artifacts: {last_error}")
    raise ValueError("Could not decode artifacts with any encoding")


def summarize(artifacts: Sequence[dict[str, Any]]) -> Report:
    """Generate summary statistics."""
    total_modules = len(artifacts)
    total_functions = sum(len(m.get("functions", [])) for m in artifacts)
    total_classes = sum(len(m.get("classes", [])) for m in artifacts)
    total_lines = sum(m.get("total_lines", 0) for m in artifacts)
    avg_lines = total_lines / total_modules if total_modules > 0 else 0.0
    missing_docs_modules = sum(1 for m in artifacts if not m.get("has_doc", False))
    missing_docs_functions = sum(
        sum(1 for f in m.get("functions", []) if not f.get("has_doc", False))
        for m in artifacts
    )

    return Report(
        modules=total_modules,
        functions=total_functions,
        classes=total_classes,
        avg_lines=avg_lines,
        missing_docs_modules=missing_docs_modules,
        missing_docs_functions=missing_docs_functions,
    )


def render_report(report: Report) -> str:
    """Render discussion report."""
    lines = [
        "Discussion Report",
        "=================",
        f"Modules: {report.modules}",
        f"Functions: {report.functions}",
        f"Classes: {report.classes}",
        f"Average lines per module: {report.avg_lines:.1f}",
        f"Modules missing docstring: {report.missing_docs_modules}",
        f"Functions/methods missing docstring: {report.missing_docs_functions}",
    ]
    return "\n".join(lines)


def render_generated_code() -> str:
    """Render example generated code."""
    return """Generated code examples:
// Example Rust struct mirroring Python artifact contracts
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


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    artifact_path = Path(args.artifact).resolve()
    if not artifact_path.exists():
        print(f"Error: Artifact file does not exist: {artifact_path}", file=sys.stderr)
        return 1

    try:
        artifacts = load_artifacts(artifact_path)
    except ValueError as e:
        print(f"Error loading artifacts: {e}", file=sys.stderr)
        return 1

    report = summarize(artifacts)
    output = render_report(report)

    if args.show_code:
        output += "\n\n" + render_generated_code()

    print(output)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate discussion reports")
    parser.add_argument("--artifact", type=str, required=True, help="Path to artifact JSON file")
    parser.add_argument("--show-code", action="store_true", help="Show generated code examples")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
