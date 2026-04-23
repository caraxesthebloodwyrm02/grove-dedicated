#!/usr/bin/env python3
"""
Explicit OpenAI smoke test (opt-in live call).

This script is intentionally small, bounded, and safe:
- Does NOTHING by default (offline).
- Only makes a network request when you pass --live.
- Uses a tiny prompt and low max output tokens to minimize cost.
- Reads configuration from environment variables (no hardcoded secrets).

It is also defensive across OpenAI SDK variants:
- Tries `resp.output_text` first
- Falls back to walking `resp.output` content blocks if needed
- If `--debug` is set, it will also attempt to serialize the response to a dict
  (via `model_dump()`/`to_dict()`/`dict()`) to extract text from common fields
  without printing the full payload.

Note: the default model is set to `gpt-4o-mini` because it reliably returns
text for this smoke test in most accounts.

Usage:
  # Offline (no network)
  python scripts/openai_smoketest.py

  # Live (uses credits)
  set OPENAI_API_KEY=...
  python scripts/openai_smoketest.py --live

Optional env vars:
  OPENAI_DEFAULT_MODEL        (default: gpt-4o-mini)
  OPENAI_TIMEOUT_SECONDS      (default: 30)
  OPENAI_MAX_OUTPUT_TOKENS    (default: 16)

Optional CLI overrides:
  --model, --timeout, --max-output-tokens, --debug

Exit codes:
  0 = success / offline skipped
  2 = failure (missing config or API call failed)
"""

from __future__ import annotations

import argparse
import os
import time
from typing import Any, Optional


def _env_int(name: str, default: int) -> int:
    val = os.environ.get(name)
    if val is None or val.strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default


def _print_kv(k: str, v: str) -> None:
    print(f"{k}: {v}")


def _extract_text_from_responses(resp: Any, debug: bool = False) -> str:
    """
    Extract text from a Responses API object across SDK variants.

    Preference order:
      1) resp.output_text (if present)
      2) Walk resp.output[*].content[*] blocks and join any text-like fields
      3) Serialize response to a dict and try common fields (best-effort)
    """
    # 1) Preferred helper property (supported by many SDK versions)
    try:
        t = getattr(resp, "output_text", None)
        if isinstance(t, str) and t.strip():
            return t.strip()
    except Exception:
        pass

    # Helper: best-effort conversion to dict without dumping full payload
    resp_dict: Optional[dict] = None
    for meth in ("model_dump", "to_dict", "dict"):
        try:
            fn = getattr(resp, meth, None)
            if callable(fn):
                resp_dict = fn()
                if isinstance(resp_dict, dict):
                    break
        except Exception:
            continue

    # 2) Fallback: walk the structured output
    chunks: list[str] = []

    try:
        output = getattr(resp, "output", None)
        if output is None and isinstance(resp, dict):
            output = resp.get("output")
        if output is None and isinstance(resp_dict, dict):
            output = resp_dict.get("output")
    except Exception:
        output = None

    if debug:
        _print_kv("debug_has_output_attr", str(hasattr(resp, "output")))
        _print_kv(
            "debug_serialized_dict", "yes" if isinstance(resp_dict, dict) else "no"
        )

    if output:
        for item in output:
            # item could be an object or dict
            try:
                content = getattr(item, "content", None)
                if content is None and isinstance(item, dict):
                    content = item.get("content")
            except Exception:
                content = None

            if not content:
                continue

            for block in content:
                # block could be an object or dict
                btype = None
                try:
                    btype = getattr(block, "type", None)
                    if btype is None and isinstance(block, dict):
                        btype = block.get("type")
                except Exception:
                    btype = None

                # Common cases: {"type":"output_text","text":"..."}
                try:
                    text = getattr(block, "text", None)
                    if text is None and isinstance(block, dict):
                        text = block.get("text")
                    if isinstance(text, str) and text:
                        chunks.append(text)
                        continue
                except Exception:
                    pass

                # Some variants may store text in different keys; best-effort:
                if isinstance(block, dict):
                    for key in ("output_text", "content", "value"):
                        v = block.get(key)
                        if isinstance(v, str) and v:
                            chunks.append(v)

                if debug and btype:
                    _print_kv("debug_block_type", str(btype))

        text_joined = "".join(chunks).strip()
        if text_joined:
            return text_joined

    # 3) Best-effort dict-based extraction from common locations
    if isinstance(resp_dict, dict):
        # Some SDKs may include convenience fields even if output_text isn't populated
        for key in ("output_text", "text"):
            v = resp_dict.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()

        # Try scanning nested structure for any {"type": "...text...", "text": "..."}
        try:
            out = resp_dict.get("output") or []
            for item in out:
                if not isinstance(item, dict):
                    continue
                content = item.get("content") or []
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    v = block.get("text")
                    if isinstance(v, str) and v.strip():
                        return v.strip()
        except Exception:
            pass

    return ""


def _offline_notice() -> int:
    print("OpenAI smoke test: OFFLINE (no network).")
    print("Use --live to perform a minimal API request (uses credits).")
    return 0


def _live_smoke_test(
    model: str, timeout_s: int, max_output_tokens: int, debug: bool
) -> int:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("FAIL: OPENAI_API_KEY is not set.")
        print("Hint: set OPENAI_API_KEY in your environment or secret manager.")
        return 2

    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:
        print(f"FAIL: Could not import OpenAI SDK: {type(e).__name__}: {e}")
        print("Hint: pip install -r requirements-core.txt")
        return 2

    client = OpenAI(api_key=api_key)

    # Tiny bounded prompt to minimize cost.
    prompt = "Say 'ok' only."

    t0 = time.perf_counter()
    try:
        resp = client.responses.create(
            model=model,
            input=prompt,
            max_output_tokens=max_output_tokens,
            timeout=timeout_s,
        )
        dt_ms = int((time.perf_counter() - t0) * 1000)

        output_text = _extract_text_from_responses(resp, debug=debug)

        ok = bool(output_text)
        if ok:
            print("OK: OpenAI live smoke test succeeded.")
        else:
            print(
                "FAIL: OpenAI responded but no text could be extracted from the response."
            )

        _print_kv("model", model)
        _print_kv("timeout_seconds", str(timeout_s))
        _print_kv("max_output_tokens", str(max_output_tokens))
        _print_kv("latency_ms", str(dt_ms))
        _print_kv("output", repr(output_text))

        if debug:
            # Print minimal response shape info (avoid dumping full payload)
            try:
                out = getattr(resp, "output", None)
                _print_kv("debug_output_items", str(len(out) if out else 0))
            except Exception:
                _print_kv("debug_output_items", "unknown")

            try:
                resp_id = getattr(resp, "id", None)
                if resp_id:
                    _print_kv("debug_response_id", str(resp_id))
            except Exception:
                pass

            # Show content block keys/types to help extraction debugging (safe)
            try:
                output = getattr(resp, "output", None) or []
                for i, item in enumerate(output[:1]):
                    content = getattr(item, "content", None) or []
                    _print_kv("debug_content_blocks", str(len(content)))
                    for j, block in enumerate(content[:3]):
                        btype = getattr(block, "type", None)
                        if btype:
                            _print_kv(f"debug_block_{j}_type", str(btype))
                        # If it's dict-like, list keys only
                        if isinstance(block, dict):
                            _print_kv(
                                f"debug_block_{j}_keys", ",".join(sorted(block.keys()))
                            )
            except Exception:
                pass

        return 0 if ok else 2

    except Exception as e:
        dt_ms = int((time.perf_counter() - t0) * 1000)
        print(f"FAIL: OpenAI live smoke test failed: {type(e).__name__}: {e}")
        _print_kv("model", model)
        _print_kv("timeout_seconds", str(timeout_s))
        _print_kv("max_output_tokens", str(max_output_tokens))
        _print_kv("latency_ms", str(dt_ms))
        print("Hint: verify network egress, key validity, and rate/spend limits.")
        return 2


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Opt-in OpenAI smoke test (offline by default)."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Make a minimal OpenAI API call (uses credits).",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4o-mini"),
        help="Model to use (default from OPENAI_DEFAULT_MODEL or gpt-4o-mini).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=_env_int("OPENAI_TIMEOUT_SECONDS", 30),
        help="Request timeout in seconds (default from OPENAI_TIMEOUT_SECONDS or 30).",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=_env_int("OPENAI_MAX_OUTPUT_TOKENS", 16),
        help="Max output tokens (default from OPENAI_MAX_OUTPUT_TOKENS or 16).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print extra debug info about response shape (never prints your API key).",
    )
    args = parser.parse_args(argv)

    if not args.live:
        return _offline_notice()

    # Guardrails for accidental spend
    if args.max_output_tokens > 128:
        print(
            "Refusing to run: --max-output-tokens is too high for a smoke test (>128)."
        )
        print("Hint: use --max-output-tokens 16 (recommended).")
        return 2

    if args.timeout <= 0 or args.timeout > 300:
        print(
            "Refusing to run: --timeout must be in 1..300 seconds for this smoke test."
        )
        return 2

    print("OpenAI smoke test: LIVE (bounded).")
    return _live_smoke_test(
        args.model, args.timeout, args.max_output_tokens, args.debug
    )


if __name__ == "__main__":
    raise SystemExit(main())
