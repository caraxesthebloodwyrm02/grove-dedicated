"""Grid Services Package

This module provides lazy imports for service classes to avoid import-time
failures when optional dependencies (like mistralai) are not installed.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mistral_agent import MistralAgentService
    from .retrieval_service import Document, RetrievalService

__all__ = ["MistralAgentService", "get_mistral_agent", "Document", "RetrievalService"]

# Lazy imports to avoid import-time failures when optional deps are missing
_MistralAgentService = None
_get_mistral_agent = None
_Document = None
_RetrievalService = None


def __getattr__(name: str):
    """Lazy import mechanism for services."""
    global _MistralAgentService, _get_mistral_agent, _Document, _RetrievalService

    if name == "MistralAgentService":
        if _MistralAgentService is None:
            from .mistral_agent import MistralAgentService as _MistralAgentService
        return _MistralAgentService

    if name == "get_mistral_agent":
        if _get_mistral_agent is None:
            from .mistral_agent import get_mistral_agent as _get_mistral_agent
        return _get_mistral_agent

    if name == "Document":
        if _Document is None:
            from .retrieval_service import Document as _Document
        return _Document

    if name == "RetrievalService":
        if _RetrievalService is None:
            from .retrieval_service import RetrievalService as _RetrievalService
        return _RetrievalService

    raise AttributeError(f"module 'grid.services' has no attribute {name!r}")
