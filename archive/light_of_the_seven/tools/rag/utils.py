"""Utility functions for RAG system."""

from typing import List, Optional

import httpx


def check_ollama_connection(base_url: str = "http://localhost:11434") -> bool:
    """Check if Ollama is running and accessible.

    Args:
        base_url: Ollama base URL

    Returns:
        True if Ollama is accessible, False otherwise
    """
    try:
        with httpx.Client(timeout=5) as client:
            response = client.get(f"{base_url.rstrip('/')}/api/tags")
            return response.status_code == 200
    except Exception:
        return False


def list_ollama_models(base_url: str = "http://localhost:11434") -> List[str]:
    """List available Ollama models.

    Args:
        base_url: Ollama base URL

    Returns:
        List of model names
    """
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(f"{base_url.rstrip('/')}/api/tags")
            response.raise_for_status()
            data = response.json()
            models = [model["name"] for model in data.get("models", [])]
            return models
    except Exception as e:
        raise RuntimeError(f"Failed to list Ollama models: {e}") from e


def find_embedding_model(
    preferred: str = "nomic-embed-text-v2-moe:latest", base_url: str = "http://localhost:11434"
) -> Optional[str]:
    """Find available embedding model, trying alternatives.

    Args:
        preferred: Preferred model name
        base_url: Ollama base URL

    Returns:
        Available model name or None
    """
    try:
        models = list_ollama_models(base_url)

        # Check preferred first
        if preferred in models:
            return preferred

        # Try alternatives in order of preference
        alternatives = [
            "nomic-embed-text-v2-moe:latest",
            "nomic-embed-text-v2-moe",
            "nomic-embed-text-v2",
            "nomic-embed-text",
            "nomic-embed-text:latest",
        ]

        for alt in alternatives:
            if alt in models:
                return alt

        # Check for any nomic model
        for model in models:
            if "nomic" in model.lower() and "embed" in model.lower():
                return model

        return None
    except Exception:
        return None


def find_llm_model(
    preferred: str = "ministral", base_url: str = "http://localhost:11434"
) -> Optional[str]:
    """Find available LLM model, trying alternatives.

    Args:
        preferred: Preferred model name
        base_url: Ollama base URL

    Returns:
        Available model name or None
    """
    try:
        models = list_ollama_models(base_url)

        # Check preferred first
        if preferred in models:
            return preferred

        # Try alternatives
        alternatives = [
            "gpt-oss-safeguard",
            "llama2",
            "mistral",
            "mixtral",
        ]

        for alt in alternatives:
            if alt in models:
                return alt

        return None
    except Exception:
        return None
