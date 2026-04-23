from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from grid.essence.core_state import EssentialState


@dataclass
class Context:
    values: Dict[str, Any] = field(default_factory=dict)
    temporal_depth: float = 1.0
    spatial_field: Dict[str, Any] = field(default_factory=dict)
    relational_web: Dict[str, Any] = field(default_factory=dict)
    quantum_signature: str = ""

    async def evolve(self, state: "EssentialState") -> "Context":
        return Context(
            temporal_depth=self.temporal_depth + 0.5,
            spatial_field=dict(self.spatial_field),
            relational_web=dict(self.relational_web),
            quantum_signature=f"{self.quantum_signature}_evolved",
            values=dict(self.values),
        )
