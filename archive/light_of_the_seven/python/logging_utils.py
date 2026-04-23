"""Structured logging utilities for Python-Rust integration."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def get_run_id() -> str:
    """Generate a unique run ID."""
    import uuid
    return str(uuid.uuid4())[:8]


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def log_jsonl(
    log_file: Path,
    stage: str,
    status: str,
    data: Dict[str, Any] | None = None,
    run_id: str | None = None,
) -> None:
    """Write a JSONL log entry."""
    entry: Dict[str, Any] = {
        "timestamp": get_timestamp(),
        "run_id": run_id or get_run_id(),
        "stage": stage,
        "status": status,
    }
    if data:
        entry.update(data)

    # Ensure log directory exists
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Append to log file
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def get_log_file(run_id: str | None = None) -> Path:
    """Get log file path for a run."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    if run_id:
        return logs_dir / f"{run_id}.jsonl"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return logs_dir / f"{timestamp}.log"


def capture_environment() -> Dict[str, str]:
    """Capture environment version information."""
    import subprocess
    import sys

    env: Dict[str, str] = {}

    # Python version
    env["python_version"] = sys.version.split()[0]

    # Try to get cargo version
    try:
        result = subprocess.run(
            ["cargo", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            env["cargo_version"] = result.stdout.strip()
    except Exception:
        pass

    # Try to get rustc version
    try:
        result = subprocess.run(
            ["rustc", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            env["rustc_version"] = result.stdout.strip()
    except Exception:
        pass

    return env
