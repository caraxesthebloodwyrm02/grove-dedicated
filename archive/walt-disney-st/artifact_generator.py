from __future__ import annotations

import argparse
import ast
import json
import textwrap
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Sequence


EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "env"}


@dataclass
class FunctionArtifact:
    name: str
    lineno: int
    args: int
    has_doc: bool
    is_async: bool


@dataclass
class ClassArtifact:
    name: str
    lineno: int
    bases: List[str]
    has_doc: bool
    methods: List[FunctionArtifact]


@dataclass
class ModuleArtifact:
    path: str
    has_doc: bool
    imports: List[str]
    total_lines: int
    functions: List[FunctionArtifact]
    classes: List[ClassArtifact]


def discover_python_files(targets: Sequence[Path]) -> Iterable[Path]:
    for target in targets:
        if target.is_dir():
            for path in target.rglob("*.py"):
                if any(part in EXCLUDE_DIRS for part in path.parts):
                    continue
                yield path
        elif target.is_file() and target.suffix == ".py":
            yield target


def parse_module(path: Path) -> ModuleArtifact:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    imports: List[str] = []
    functions: List[FunctionArtifact] = []
    classes: List[ClassArtifact] = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            name = ast.unparse(node) if hasattr(ast, "unparse") else _fallback_unparse(node)
            imports.append(name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(_function_from_node(node))
        elif isinstance(node, ast.ClassDef):
            classes.append(_class_from_node(node))

    return ModuleArtifact(
        path=str(path),
        has_doc=ast.get_docstring(tree) is not None,
        imports=imports,
        total_lines=len(source.splitlines()),
        functions=functions,
        classes=classes,
    )


def _function_from_node(node: ast.AST) -> FunctionArtifact:
    assert isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    args = len(getattr(node.args, "args", [])) + len(getattr(node.args, "kwonlyargs", []))
    return FunctionArtifact(
        name=node.name,
        lineno=node.lineno,
        args=args,
        has_doc=ast.get_docstring(node) is not None,
        is_async=isinstance(node, ast.AsyncFunctionDef),
    )


def _class_from_node(node: ast.ClassDef) -> ClassArtifact:
    bases = []
    for base in node.bases:
        try:
            bases.append(ast.unparse(base))
        except Exception:
            bases.append(getattr(base, "id", "<unknown>"))

    methods = []
    for child in node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.append(_function_from_node(child))

    return ClassArtifact(
        name=node.name,
        lineno=node.lineno,
        bases=bases,
        has_doc=ast.get_docstring(node) is not None,
        methods=methods,
    )


def _fallback_unparse(node: ast.AST) -> str:
    if isinstance(node, ast.Import):
        return ", ".join(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        base = f"from {node.module or ''} import"
        names = ", ".join(alias.name for alias in node.names)
        return f"{base} {names}".strip()
    return "<unknown>"


def summarize(artifacts: Sequence[ModuleArtifact]) -> str:
    total_modules = len(artifacts)
    total_functions = sum(len(m.functions) for m in artifacts)
    total_classes = sum(len(m.classes) for m in artifacts)
    missing_docs = sum(not m.has_doc for m in artifacts)
    missing_func_docs = sum(
        1 for m in artifacts for f in m.functions if not f.has_doc
    ) + sum(1 for m in artifacts for c in m.classes for f in c.methods if not f.has_doc)

    lines = [
        "Artifact Insights",
        "=================",
        f"Modules analyzed: {total_modules}",
        f"Total lines: {sum(m.total_lines for m in artifacts)}",
        f"Functions: {total_functions}",
        f"Classes: {total_classes}",
        f"Modules missing docstring: {missing_docs}",
        f"Functions/methods missing docstring: {missing_func_docs}",
        "",
    ]

    longest_functions = sorted(
        (
            (m.path, f.name, f.lineno)
            for m in artifacts
            for f in [*m.functions, *(fn for c in m.classes for fn in c.methods)]
        ),
        key=lambda item: item[2],
        reverse=True,
    )[:5]
    if longest_functions:
        lines.append("Top functions by starting line number (proxy for size):")
        for path, name, lineno in longest_functions:
            lines.append(f"- {name} @ {path}:{lineno}")
        lines.append("")

    return "\n".join(lines)


def format_artifacts(artifacts: Sequence[ModuleArtifact]) -> str:
    chunks = []
    for module in artifacts:
        header = f"[{module.path}]"
        chunks.append(header)
        chunks.append("-" * len(header))
        chunks.append(f"Docstring: {'yes' if module.has_doc else 'no'}")
        chunks.append(f"Lines: {module.total_lines}")
        if module.imports:
            chunks.append("Imports:")
            chunks.extend(f"  - {imp}" for imp in module.imports)
        if module.functions:
            chunks.append("Functions:")
            for fn in module.functions:
                kind = "async " if fn.is_async else ""
                doc = "yes" if fn.has_doc else "no"
                chunks.append(f"  - {kind}{fn.name} (args: {fn.args}, doc: {doc}, line: {fn.lineno})")
        if module.classes:
            chunks.append("Classes:")
            for cls in module.classes:
                doc = "yes" if cls.has_doc else "no"
                bases = ", ".join(cls.bases) if cls.bases else "object"
                chunks.append(f"  - {cls.name} (bases: {bases}, doc: {doc}, line: {cls.lineno})")
                for method in cls.methods:
                    kind = "async " if method.is_async else ""
                    doc_m = "yes" if method.has_doc else "no"
                    chunks.append(
                        f"      • {kind}{method.name} (args: {method.args}, doc: {doc_m}, line: {method.lineno})"
                    )
        chunks.append("")
    return "\n".join(chunks)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate artifacts from Python modules and print insights."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Python files or directories to analyze (default: current directory).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output artifacts as JSON in addition to the human-readable summary.",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output ONLY JSON (suppresses human-readable summary). Implies --json.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write JSON output to file instead of stdout. Implies --json-only.",
    )

    args = parser.parse_args(argv)
    if args.out:
        args.json = True
        args.json_only = True
    if args.json_only:
        args.json = True
    paths = list(discover_python_files(args.targets))
    if not paths:
        print("No Python files found in the provided targets.")
        return

    artifacts = [parse_module(path) for path in paths]

    if not args.json_only:
        print(summarize(artifacts))
        print(format_artifacts(artifacts))

    if args.json:
        serialized = [asdict(artifact) for artifact in artifacts]
        # Output with artifact_version wrapper for new format, but also support legacy array format
        output = {
            "artifact_version": "1.0",
            "modules": serialized
        }
        json_output = json.dumps(output, indent=2)

        if args.out:
            # Write to file
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json_output, encoding="utf-8")
            if not args.json_only:
                print(f"JSON artifacts written to {args.out}")
        else:
            # Write to stdout
            if not args.json_only:
                print("JSON artifacts:")
            print(json_output)


if __name__ == "__main__":
    main()
