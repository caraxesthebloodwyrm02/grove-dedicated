"""Minimal API entry point using FastAPI."""

from __future__ import annotations

from typing import Any, Dict

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Stub classes for when FastAPI is not available
    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass
        def post(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
        def get(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
    class HTTPException(Exception):
        pass
    class BaseModel:
        pass


app = FastAPI(title="Magical Bridge API", version="0.2.0")


class GenerateRequest(BaseModel):
    """Request model for artifact generation."""
    targets: list[str] = ["."]
    output_path: str = "artifact.json"


class ValidateSchemaRequest(BaseModel):
    """Request model for schema validation."""
    artifact_path: str = "artifact.json"
    engine: str = "handwritten"


class ValidateTypesRequest(BaseModel):
    """Request model for type validation."""
    rust_file: str = "rust/grid-core/src/lib.rs"
    mode: str = "artifact"


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": "0.2.0"}


@app.post("/api/v1/generate")
async def generate_artifacts(request: GenerateRequest) -> Dict[str, Any]:
    """Generate artifacts from Python code.

    Note: This is a minimal implementation. Full implementation would
    call the core artifact generation logic.
    """
    if not FASTAPI_AVAILABLE:
        raise HTTPException(status_code=503, detail="FastAPI not available")

    # TODO: Implement actual generation logic
    return {
        "success": True,
        "message": "Artifact generation endpoint (not yet implemented)",
        "output_path": request.output_path
    }


@app.post("/api/v1/validate/schema")
async def validate_schema(request: ValidateSchemaRequest) -> Dict[str, Any]:
    """Validate artifact schema.

    Note: This is a minimal implementation. Full implementation would
    call the core schema validation logic.
    """
    if not FASTAPI_AVAILABLE:
        raise HTTPException(status_code=503, detail="FastAPI not available")

    # TODO: Implement actual validation logic
    return {
        "success": True,
        "message": "Schema validation endpoint (not yet implemented)",
        "artifact_path": request.artifact_path,
        "engine": request.engine
    }


@app.post("/api/v1/validate/types")
async def validate_types(request: ValidateTypesRequest) -> Dict[str, Any]:
    """Validate types between Python and Rust.

    Note: This is a minimal implementation. Full implementation would
    call the core type validation logic.
    """
    if not FASTAPI_AVAILABLE:
        raise HTTPException(status_code=503, detail="FastAPI not available")

    # TODO: Implement actual validation logic
    return {
        "success": True,
        "message": "Type validation endpoint (not yet implemented)",
        "rust_file": request.rust_file,
        "mode": request.mode
    }


def create_app() -> FastAPI:
    """Create and return FastAPI app instance."""
    return app

