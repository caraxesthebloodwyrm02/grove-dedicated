"""Generate artifacts from Python modules for Rust integration."""

from __future__ import annotations

import argparse
import ast
import json
import sys
import textwrap
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable, List, Sequence, Dict, Any, Optional


@dataclass
class FunctionArtifact:
    """Artifact representing a Python function."""

    name: str
    lineno: int
    args: int
    has_doc: bool
    is_async: bool


@dataclass
class ClassArtifact:
    """Artifact representing a Python class."""

    name: str
    lineno: int
    bases: List[str]
    has_doc: bool
    methods: List[FunctionArtifact]


@dataclass
class ModuleArtifact:
    """Artifact representing a Python module."""

    path: str
    has_doc: bool
    imports: List[str]
    total_lines: int
    functions: List[FunctionArtifact]
    classes: List[ClassArtifact]
    component_type: Optional[str] = None  # 'schema', 'engine', 'tracker', etc.
    cognitive_metrics: Dict[str, float] = field(default_factory=dict)  # load, complexity, etc.
    dependencies: List[str] = field(default_factory=list)  # other cognitive components


def discover_python_files(root: Path, target_module: Optional[str] = None) -> Iterable[Path]:
    """Discover all Python files in the given root directory."""
    for path in root.rglob("*.py"):
        if "__pycache__" not in str(path) and ".venv" not in str(path):
            # Filter by target module if specified
            if target_module:
                # Convert target_module (e.g., "light_of_the_seven.cognitive_layer") to path
                target_path = target_module.replace(".", "/")
                if target_path not in str(path):
                    continue
            yield path


def parse_module(path: Path, target_module: Optional[str] = None) -> ModuleArtifact | None:
    """Parse a Python module and extract artifacts."""
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {path}: {e}", file=sys.stderr)
        return None

    imports: List[str] = []
    functions: List[FunctionArtifact] = []
    classes: List[ClassArtifact] = []

    module_doc = ast.get_docstring(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(f"import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"from {module} import {alias.name}")
        elif isinstance(node, ast.FunctionDef):
            func = _function_from_node(node)
            if func:
                functions.append(func)
        elif isinstance(node, ast.AsyncFunctionDef):
            func = _function_from_node(node)
            if func:
                func.is_async = True
                functions.append(func)
        elif isinstance(node, ast.ClassDef):
            cls = _class_from_node(node)
            if cls:
                classes.append(cls)

    # Extract cognitive-specific information if target_module is cognitive_layer
    component_type: Optional[str] = None
    cognitive_metrics: Dict[str, float] = {}
    dependencies: List[str] = []

    if target_module and "cognitive_layer" in target_module:
        # Determine component type based on path
        path_str = str(path)
        if "schemas" in path_str:
            component_type = "schema"
        elif "decision_support" in path_str:
            component_type = "engine"
        elif "mental_models" in path_str:
            component_type = "tracker"
        elif "cognitive_load" in path_str:
            component_type = "load_manager"
        elif "integration" in path_str:
            component_type = "integration"

        # Calculate basic cognitive metrics
        cognitive_metrics = {
            "estimated_load": min(10.0, (len(functions) * 0.5 + len(classes) * 2.0) / 10.0),
            "complexity_score": min(1.0, (len(functions) + len(classes) * 3) / 50.0),
            "dependency_count": len([imp for imp in imports if "cognitive_layer" in imp]),
        }

        # Extract dependencies from imports
        for imp in imports:
            if "cognitive_layer" in imp or "grid" in imp:
                dependencies.append(imp)

    return ModuleArtifact(
        path=str(path),
        has_doc=module_doc is not None,
        imports=sorted(set(imports)),
        total_lines=len(source.splitlines()),
        functions=functions,
        classes=classes,
        component_type=component_type,
        cognitive_metrics=cognitive_metrics,
        dependencies=dependencies,
    )


def _function_from_node(node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionArtifact | None:
    """Extract function artifact from AST node."""
    return FunctionArtifact(
        name=node.name,
        lineno=node.lineno,
        args=len(node.args.args),
        has_doc=ast.get_docstring(node) is not None,
        is_async=isinstance(node, ast.AsyncFunctionDef),
    )


def _class_from_node(node: ast.ClassDef) -> ClassArtifact | None:
    """Extract class artifact from AST node."""
    methods: List[FunctionArtifact] = []
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func = _function_from_node(item)
            if func:
                methods.append(func)

    return ClassArtifact(
        name=node.name,
        lineno=node.lineno,
        bases=[_fallback_unparse(base) for base in node.bases],
        has_doc=ast.get_docstring(node) is not None,
        methods=methods,
    )


def _fallback_unparse(node: ast.AST) -> str:
    """Fallback unparse for AST nodes."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return f"{_fallback_unparse(node.value)}.{node.attr}"
    else:
        return ast.dump(node)


def summarize(artifacts: Sequence[ModuleArtifact]) -> dict:
    """Generate summary statistics from artifacts."""
    total_modules = len(artifacts)
    total_functions = sum(len(m.functions) for m in artifacts)
    total_classes = sum(len(m.classes) for m in artifacts)
    modules_with_docs = sum(1 for m in artifacts if m.has_doc)
    functions_with_docs = sum(
        sum(1 for f in m.functions if f.has_doc) for m in artifacts
    )
    avg_lines = sum(m.total_lines for m in artifacts) / total_modules if total_modules > 0 else 0

    return {
        "modules": total_modules,
        "functions": total_functions,
        "classes": total_classes,
        "modules_with_docs": modules_with_docs,
        "functions_with_docs": functions_with_docs,
        "modules_missing_docs": total_modules - modules_with_docs,
        "functions_missing_docs": total_functions - functions_with_docs,
        "average_lines_per_module": round(avg_lines, 1),
    }


def format_artifacts(artifacts: Sequence[ModuleArtifact], json_only: bool = False) -> str:
    """Format artifacts as JSON or human-readable text."""
    if json_only:
        return json.dumps([asdict(artifact) for artifact in artifacts], indent=2)

    # Human-readable format
    lines = ["== Artifacts =="]
    summary = summarize(artifacts)
    lines.append(f"Modules: {summary['modules']}")
    lines.append(f"Functions: {summary['functions']}")
    lines.append(f"Classes: {summary['classes']}")
    lines.append(f"Average lines per module: {summary['average_lines_per_module']}")
    lines.append(f"Modules missing docstring: {summary['modules_missing_docs']}")
    lines.append(f"Functions/methods missing docstring: {summary['functions_missing_docs']}")
    lines.append("")

    for artifact in artifacts:
        lines.append(f"Module: {artifact.path}")
        lines.append(f"  Lines: {artifact.total_lines}")
        lines.append(f"  Functions: {len(artifact.functions)}")
        lines.append(f"  Classes: {len(artifact.classes)}")
        lines.append("")

    return "\n".join(lines)


def main(args: argparse.Namespace) -> int:
    """Main entry point."""
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Error: Root directory does not exist: {root}", file=sys.stderr)
        return 1

    print(f"== Generating artifacts ==", file=sys.stderr)
    print(f"Scanning: {root}", file=sys.stderr)
    if args.target_module:
        print(f"Target module: {args.target_module}", file=sys.stderr)

    artifacts: List[ModuleArtifact] = []
    for py_file in discover_python_files(root, args.target_module):
        artifact = parse_module(py_file, args.target_module)
        if artifact:
            artifacts.append(artifact)

    if not artifacts:
        print("Warning: No Python modules found", file=sys.stderr)
        return 1

    summary = summarize(artifacts)
    print(f"Found {summary['modules']} modules, {summary['functions']} functions, {summary['classes']} classes", file=sys.stderr)

    output = format_artifacts(artifacts, json_only=args.json_only)
    print(output)

    if not args.json_only:
        print("\n== Summary ==", file=sys.stderr)
        for key, value in summary.items():
            print(f"{key}: {value}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(description="Generate artifacts from Python modules")
    parser.add_argument("--root", default=".", type=str, help="Root directory to scan")
    parser.add_argument("--json-only", action="store_true", help="Output JSON only")
    parser.add_argument("--target-module", type=str, help="Target module to scan (e.g., light_of_the_seven.cognitive_layer)")
    parsed_args = parser.parse_args()
    sys.exit(main(parsed_args))
