#!/usr/bin/env python3
"""
DataKit Doctor: offline/online environment checks for production readiness.

Usage (offline, no network):
  python scripts/doctor.py

Usage (optional live smoke test; requires OPENAI_API_KEY):
  python scripts/doctor.py --live

Notes:
- Offline mode never makes network calls.
- Live mode makes a minimal, bounded call to OpenAI to validate connectivity.
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
ENV_EXAMPLE = CONFIG_DIR / ".env.example"
GITIGNORE = ROOT / ".gitignore"

# Heuristic: keys that must never be committed
SECRET_ENV_KEYS = (
    "OPENAI_API_KEY",
    "YOUTUBE_API_KEY",
    "SENTRY_DSN",
    "AUTH_JWT_SECRET",
)

# Files that should not exist in repo root for prod hygiene
DISALLOWED_ENV_FILES = (ROOT / ".env",)


class CheckResult:
    __slots__ = ("name", "ok", "details", "hint")

    def __init__(self, name: str, ok: bool, details: str = "", hint: str = ""):
        self.name = name
        self.ok = ok
        self.details = details
        self.hint = hint


def _print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def _print_result(res: CheckResult) -> None:
    status = "OK" if res.ok else "FAIL"
    print(f"[{status}] {res.name}")
    if res.details:
        print(f"  - {res.details}")
    if (not res.ok) and res.hint:
        print(f"  - Hint: {res.hint}")


def _run(
    cmd: List[str], cwd: Optional[Path] = None, timeout_s: int = 10
) -> Tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            text=True,
        )
        return p.returncode, (p.stdout or "").strip()
    except Exception as e:
        return 1, f"{type(e).__name__}: {e}"


def _read_text(path: Path, max_bytes: int = 2_000_000) -> str:
    data = path.read_bytes()
    if len(data) > max_bytes:
        data = data[:max_bytes]
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return data.decode(errors="replace")


def check_runtime() -> List[CheckResult]:
    pyver = sys.version.split()[0]
    ok = sys.version_info >= (3, 9)
    return [
        CheckResult(
            "Python version >= 3.9",
            ok,
            details=f"Detected Python {pyver} on {platform.system()} {platform.release()}",
            hint="Install Python 3.11+ for best compatibility/performance.",
        )
    ]


def check_repo_structure() -> List[CheckResult]:
    results: List[CheckResult] = []
    must_exist = [
        ROOT / "README.md",
        ROOT / "datakit.py",
        ROOT / "requirements-core.txt",
        CONFIG_DIR,
        ENV_EXAMPLE,
        GITIGNORE,
    ]
    for p in must_exist:
        results.append(
            CheckResult(
                f"Required path exists: {p.relative_to(ROOT)}",
                p.exists(),
                details=str(p),
                hint="Restore missing files/directories or re-run setup.",
            )
        )
    return results


def check_env_files() -> List[CheckResult]:
    results: List[CheckResult] = []

    for p in DISALLOWED_ENV_FILES:
        results.append(
            CheckResult(
                f"Untracked secret file not present: {p.relative_to(ROOT)}",
                not p.exists(),
                details="Good: no root .env checked in"
                if not p.exists()
                else "Found .env file in repo root",
                hint="Keep .env outside source control. Use config/.env.example as a template.",
            )
        )

    # Ensure env example includes expected keys (template completeness)
    if ENV_EXAMPLE.exists():
        txt = _read_text(ENV_EXAMPLE)
        for k in SECRET_ENV_KEYS:
            results.append(
                CheckResult(
                    f"Env template mentions {k}",
                    k in txt,
                    details="Present" if k in txt else "Missing",
                    hint=f"Add {k}= to config/.env.example if your app uses it.",
                )
            )
    else:
        results.append(
            CheckResult(
                "Env template exists (config/.env.example)",
                False,
                details="Missing template",
                hint="Create config/.env.example to document required env vars.",
            )
        )

    return results


def check_gitignore_hygiene() -> List[CheckResult]:
    results: List[CheckResult] = []
    if not GITIGNORE.exists():
        return [
            CheckResult(
                ".gitignore exists",
                False,
                details="Missing .gitignore",
                hint="Add .gitignore to prevent committing venv, secrets, caches, and artifacts.",
            )
        ]

    txt = _read_text(GITIGNORE)

    required_patterns = [
        "venv/",
        ".venv/",
        ".env",
        ".env.*",
        "artifacts/",
        ".cache/",
        "__pycache__/",
    ]

    for pat in required_patterns:
        results.append(
            CheckResult(
                f".gitignore contains pattern: {pat}",
                pat in txt,
                details="Present" if pat in txt else "Missing",
                hint="Add it to avoid committing generated files or secrets.",
            )
        )

    return results


def check_openai_env() -> List[CheckResult]:
    results: List[CheckResult] = []
    key = os.environ.get("OPENAI_API_KEY", "")
    results.append(
        CheckResult(
            "OPENAI_API_KEY present in environment",
            bool(key),
            details="Set" if key else "Not set",
            hint="Set OPENAI_API_KEY in your environment or secret manager (do not hardcode).",
        )
    )

    # Optional scoping vars
    for k in ("OPENAI_ORG_ID", "OPENAI_PROJECT_ID"):
        v = os.environ.get(k, "")
        results.append(
            CheckResult(
                f"{k} (optional) configured",
                True,
                details="Set" if v else "Not set (ok)",
                hint="Set this if you need to scope usage to a specific org/project.",
            )
        )

    return results


def check_openai_sdk_installed() -> List[CheckResult]:
    try:
        import openai  # noqa: F401

        return [
            CheckResult(
                "OpenAI Python SDK importable",
                True,
                details="import openai succeeded",
                hint="",
            )
        ]
    except Exception as e:
        return [
            CheckResult(
                "OpenAI Python SDK importable",
                False,
                details=f"{type(e).__name__}: {e}",
                hint="Install dependencies: pip install -r requirements-core.txt",
            )
        ]


def live_openai_smoke_test(
    model: str, timeout_s: int, max_output_tokens: int
) -> List[CheckResult]:
    """
    Minimal bounded network call to validate that:
    - OPENAI_API_KEY works
    - DNS/TLS egress works
    - API returns a response

    Note: Some SDK/model combinations may not populate `resp.output_text`.
    This implementation extracts text defensively from the structured output.
    """
    results: List[CheckResult] = []
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return [
            CheckResult(
                "Live OpenAI smoke test",
                False,
                details="OPENAI_API_KEY is not set",
                hint="Set OPENAI_API_KEY then re-run with --live.",
            )
        ]

    try:
        from openai import OpenAI
    except Exception as e:
        return [
            CheckResult(
                "Live OpenAI smoke test",
                False,
                details=f"OpenAI SDK missing: {type(e).__name__}: {e}",
                hint="Install dependencies then retry.",
            )
        ]

    def _extract_text_from_responses(resp) -> str:
        # 1) Preferred helper property (when present)
        try:
            t = getattr(resp, "output_text", None)
            if isinstance(t, str) and t.strip():
                return t.strip()
        except Exception:
            pass

        # 2) Walk structured output: resp.output[*].content[*].text
        try:
            output = getattr(resp, "output", None)
        except Exception:
            output = None

        if not output:
            return ""

        chunks: List[str] = []
        for item in output:
            try:
                content = getattr(item, "content", None)
                if content is None and isinstance(item, dict):
                    content = item.get("content")
            except Exception:
                content = None

            if not content:
                continue

            for block in content:
                # Common cases: {"type":"output_text","text":"..."} or object with .text
                try:
                    text = getattr(block, "text", None)
                    if text is None and isinstance(block, dict):
                        text = block.get("text")
                    if isinstance(text, str) and text:
                        chunks.append(text)
                        continue
                except Exception:
                    pass

                # Best-effort: other string fields
                if isinstance(block, dict):
                    for key in ("output_text", "value", "content"):
                        v = block.get(key)
                        if isinstance(v, str) and v:
                            chunks.append(v)

        return "".join(chunks).strip()

    client = OpenAI(api_key=api_key)

    prompt = "Say 'ok' only."
    t0 = time.perf_counter()
    try:
        # Responses API (modern SDK). Keep output very small to minimize cost.
        resp = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=max_output_tokens,
            timeout=timeout_s,
        )
        dt_ms = int((time.perf_counter() - t0) * 1000)

        text = _extract_text_from_responses(resp)

        # Minimal debug keys (safe to print)
        resp_id = ""
        output_items = 0
        try:
            rid = getattr(resp, "id", None)
            if rid:
                resp_id = str(rid)
        except Exception:
            resp_id = ""

        try:
            out = getattr(resp, "output", None)
            output_items = len(out) if out else 0
        except Exception:
            output_items = 0

        ok = bool(text)
        results.append(
            CheckResult(
                "Live OpenAI smoke test (minimal Responses call)",
                ok,
                details=f"Latency={dt_ms}ms, model={model}, output={text!r}, response_id={resp_id}, output_items={output_items}",
                hint="If this fails, check key validity, network egress, rate/spend limits, or try a different model.",
            )
        )
        return results
    except Exception as e:
        dt_ms = int((time.perf_counter() - t0) * 1000)
        return [
            CheckResult(
                "Live OpenAI smoke test (minimal Responses call)",
                False,
                details=f"Latency={dt_ms}ms, error={type(e).__name__}: {e}",
                hint="Check OPENAI_API_KEY, network, and account/project limits.",
            )
        ]


def check_no_obvious_secrets_in_tree() -> List[CheckResult]:
    """
    Lightweight heuristic scan for likely leaked secrets.
    Not a substitute for a dedicated secret scanner, but catches common mistakes.
    """
    results: List[CheckResult] = []
    patterns = [
        re.compile(r"OPENAI_API_KEY\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE),
        re.compile(
            r"sk-[A-Za-z0-9]{10,}", re.IGNORECASE
        ),  # common prefix; heuristic only
    ]

    suspicious: List[str] = []
    for p in ROOT.rglob("*.py"):
        # Skip virtual envs if present for any reason
        if "venv" in p.parts or ".venv" in p.parts:
            continue
        try:
            txt = _read_text(p, max_bytes=400_000)
        except Exception:
            continue
        for pat in patterns:
            if pat.search(txt):
                suspicious.append(str(p.relative_to(ROOT)))
                break

    results.append(
        CheckResult(
            "No obvious hardcoded API keys found (heuristic)",
            len(suspicious) == 0,
            details="None found"
            if not suspicious
            else f"Found in: {', '.join(suspicious[:10])}",
            hint="Remove hardcoded secrets and rotate keys if any were committed.",
        )
    )
    return results


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="DataKit production readiness doctor (offline by default)."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run a minimal OpenAI smoke test (uses credits).",
    )
    parser.add_argument(
        "--model", default=os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("OPENAI_TIMEOUT_SECONDS", "30")),
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=int(os.environ.get("OPENAI_MAX_OUTPUT_TOKENS", "16")),
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    _print_header("Runtime")
    results: List[CheckResult] = []
    results.extend(check_runtime())

    _print_header("Repository structure")
    results.extend(check_repo_structure())

    _print_header("Config & secret hygiene")
    results.extend(check_env_files())
    results.extend(check_gitignore_hygiene())
    results.extend(check_no_obvious_secrets_in_tree())

    _print_header("OpenAI configuration (offline)")
    results.extend(check_openai_env())
    results.extend(check_openai_sdk_installed())

    if args.live:
        _print_header("OpenAI live smoke test (bounded)")
        results.extend(
            live_openai_smoke_test(args.model, args.timeout, args.max_output_tokens)
        )
    else:
        print(
            "[OK] Live OpenAI smoke test skipped (offline mode). Use --live to run it."
        )

    # Print results grouped as they were added.
    _print_header("Summary")
    fail_count = 0
    for r in results:
        _print_result(r)
        if not r.ok:
            fail_count += 1

    print(f"\nChecks: {len(results)}  Failures: {fail_count}")
    return 0 if fail_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
