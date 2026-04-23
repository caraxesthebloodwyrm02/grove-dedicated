"""Backend server entrypoint.

This wrapper exists to match tooling/UI expectations that the backend can be
started via `python backend/server.py` and will listen on 127.0.0.1:8080.

It runs the Mothership FastAPI application.

Environment variables:
- MOTHERSHIP_HOST: override bind host (default: 127.0.0.1)
- MOTHERSHIP_PORT: override bind port (default: 8080)
- MOTHERSHIP_ENABLE_GRID_PULSE=1: enable optional Grid Pulse router
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn


def main() -> None:
    """Start the Mothership backend server."""

    repo_root = str(Path(__file__).resolve().parents[1])
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    host = os.getenv("MOTHERSHIP_HOST", "127.0.0.1")
    port = int(os.getenv("MOTHERSHIP_PORT", "8080"))

    uvicorn.run(
        "application.mothership.main:app",
        host=host,
        port=port,
        reload=False,
        workers=1,
    )


if __name__ == "__main__":
    main()
