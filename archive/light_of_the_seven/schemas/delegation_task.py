import dataclasses
from typing import Optional, Literal, List, Dict, Any

@dataclasses.dataclass
class DelegationTask:
    """
    Schema for a delegatable task, designed to be machine-readable.
    """
    id: str
    title: str
    description: str
    status: Literal['not-started', 'in-progress', 'completed', 'blocked']
    assignee: Optional[str] = None
    priority: Literal['low', 'medium', 'high', 'critical'] = 'medium'
    context_files: List[str] = dataclasses.field(default_factory=list)
    command_to_execute: Optional[str] = None
    expected_output_format: Optional[str] = None
    metadata: Dict[str, Any] = dataclasses.field(default_factory=dict)
