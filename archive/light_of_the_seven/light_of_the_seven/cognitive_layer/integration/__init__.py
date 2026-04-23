"""Integration modules for connecting cognitive layer with GRID."""

from .context_enricher import ContextEnricher
from .grid_bridge import GridBridge
from .pipeline_adapter import PipelineAdapter

__all__ = [
    "GridBridge",
    "PipelineAdapter",
    "ContextEnricher",
]

