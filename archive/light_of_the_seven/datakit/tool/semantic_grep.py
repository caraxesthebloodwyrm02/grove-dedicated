#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


DEFAULT_EXTENSIONS = [
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".py",
]


@dataclass(frozen=True)
class Chunk:
    file_path: str
    start_line: int
    end_line: int
    text: str


def _iter_files(root: Path, extensions: list[str], max_bytes: int) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in extensions:
            if root.stat().st_size <= max_bytes:
                yield root
        return

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        try:
            if path.stat().st_size > max_bytes:
                continue
        except OSError:
            continue
        yield path


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def _chunk_text(text: str, file_path: str, chunk_lines: int, overlap_lines: int) -> list[Chunk]:
    lines = text.splitlines()
    if not lines:
        return []

    chunks: list[Chunk] = []
    step = max(1, chunk_lines - overlap_lines)
    for start in range(0, len(lines), step):
        end = min(len(lines), start + chunk_lines)
        chunk_text = "\n".join(lines[start:end]).strip()
        if chunk_text:
            chunks.append(
                Chunk(
                    file_path=file_path,
                    start_line=start + 1,
                    end_line=end,
                    text=chunk_text,
                )
            )
        if end >= len(lines):
            break
    return chunks


def _hash_key(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8", errors="ignore"))
        h.update(b"\0")
    return h.hexdigest()


def _load_embedder(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(model_name)
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "sentence-transformers is required for semantic mode. "
            "Install it (and torch) or run with --mode keyword."
        ) from e


def _embed_texts(embedder, texts: list[str], batch_size: int = 32) -> np.ndarray:
    vectors = embedder.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return np.asarray(vectors, dtype=np.float32)


def _cosine_sim_matrix(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
    q = query_vec.reshape(1, -1)
    return (doc_vecs @ q.T).reshape(-1)


def _keyword_score(query: str, text: str) -> float:
    tokens = [t for t in re.split(r"\W+", query.lower()) if t]
    if not tokens:
        return 0.0
    tl = text.lower()
    hits = sum(1 for t in tokens if t in tl)
    return hits / max(1, len(set(tokens)))


def _extract_instructions(query: str, top_chunks: list[dict[str, Any]]) -> list[str]:
    instructions: list[str] = []

    instructions.append("Identify the relevant files and sections from the top matches.")
    instructions.append(
        "Read the matched line ranges in order of score; extract definitions, invariants, and constraints."
    )

    ql = query.lower()
    if any(w in ql for w in ["bug", "error", "fix", "issue", "broken"]):
        instructions.append(
            "Locate error messages / stack traces in the matched sections and trace callers upward."
        )
        instructions.append(
            "Form a minimal reproduction path using the matched references, then apply a targeted fix."
        )

    if any(w in ql for w in ["implement", "create", "add", "build", "tool"]):
        instructions.append(
            "Derive an interface from the matches (inputs/outputs), then sketch a minimal implementation plan."
        )

    if top_chunks:
        instructions.append(
            "Cross-check similar matches for conflicts; prefer the most recent or most authoritative reference."
        )

    instructions.append("Summarize findings into a structured output (problem, evidence, steps, expected result).")
    return instructions


def run_semantic_grep(
    context: str,
    refs_path: Path,
    *,
    mode: str,
    model: str,
    top_k: int,
    extensions: list[str],
    chunk_lines: int,
    overlap_lines: int,
    max_file_bytes: int,
    min_score: float,
) -> dict[str, Any]:
    files = list(_iter_files(refs_path, extensions, max_file_bytes))

    all_chunks: list[Chunk] = []
    for f in files:
        text = _safe_read_text(f)
        all_chunks.extend(_chunk_text(text, str(f), chunk_lines, overlap_lines))

    results: list[dict[str, Any]] = []

    if mode == "semantic":
        embedder = _load_embedder(model)
        texts = [c.text for c in all_chunks]
        if not texts:
            scored = np.array([], dtype=np.float32)
        else:
            doc_vecs = _embed_texts(embedder, texts)
            query_vec = _embed_texts(embedder, [context])[0]
            scored = _cosine_sim_matrix(query_vec, doc_vecs)

        idxs = np.argsort(-scored)[: max(0, top_k)] if scored.size else np.array([], dtype=int)
        for i in idxs.tolist():
            score = float(scored[i])
            if score < min_score:
                continue
            c = all_chunks[i]
            results.append(
                {
                    "score": score,
                    "file": c.file_path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "text": c.text,
                }
            )

    else:
        # keyword mode
        scored_pairs: list[tuple[float, Chunk]] = []
        for c in all_chunks:
            s = _keyword_score(context, c.text)
            if s > 0:
                scored_pairs.append((s, c))

        scored_pairs.sort(key=lambda x: x[0], reverse=True)
        for s, c in scored_pairs[: max(0, top_k)]:
            if s < min_score:
                continue
            results.append(
                {
                    "score": float(s),
                    "file": c.file_path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "text": c.text,
                }
            )

    instructions = _extract_instructions(context, results)

    return {
        "query": context,
        "mode": mode,
        "references_root": str(refs_path),
        "top_k": top_k,
        "matches": results,
        "logical_instructions": instructions,
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="semantic_grep",
        description="Semantic grep over reference data to produce structured, readable output.",
    )

    parser.add_argument(
        "--context",
        required=True,
        help="Query/context text OR @path/to/file to load context from file.",
    )
    parser.add_argument(
        "--refs",
        required=True,
        help="Folder or file containing references/data to search.",
    )
    parser.add_argument(
        "--mode",
        choices=["semantic", "keyword"],
        default="semantic",
        help="Search mode. 'semantic' uses embeddings, 'keyword' uses token presence.",
    )
    parser.add_argument(
        "--model",
        default="all-MiniLM-L6-v2",
        help="SentenceTransformers model name (semantic mode).",
    )
    parser.add_argument("--top-k", type=int, default=8, help="Number of results.")
    parser.add_argument(
        "--extensions",
        default=",".join(DEFAULT_EXTENSIONS),
        help="Comma-separated list of file extensions to include.",
    )
    parser.add_argument("--chunk-lines", type=int, default=60)
    parser.add_argument("--overlap-lines", type=int, default=10)
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--min-score", type=float, default=0.15)

    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--out",
        default="-",
        help="Output path, or '-' for stdout.",
    )
    return parser.parse_args(argv)


def _load_context_arg(context_arg: str) -> str:
    if context_arg.startswith("@"):
        p = Path(context_arg[1:]).expanduser()
        return _safe_read_text(p)
    return context_arg


def _dump_output(obj: dict[str, Any], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(obj, ensure_ascii=False, indent=2)

    if yaml is None:
        raise RuntimeError("pyyaml is not available; install pyyaml or use --format json")

    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    context = _load_context_arg(args.context)
    refs_path = Path(args.refs).expanduser()

    extensions = [e.strip().lower() for e in args.extensions.split(",") if e.strip()]

    result = run_semantic_grep(
        context,
        refs_path,
        mode=args.mode,
        model=args.model,
        top_k=args.top_k,
        extensions=extensions,
        chunk_lines=args.chunk_lines,
        overlap_lines=args.overlap_lines,
        max_file_bytes=args.max_file_bytes,
        min_score=args.min_score,
    )

    rendered = _dump_output(result, args.format)

    if args.out == "-":
        print(rendered)
    else:
        out_path = Path(args.out)
        out_path.write_text(rendered, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
