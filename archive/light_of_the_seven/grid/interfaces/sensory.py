from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class SensoryInput:
    source: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0
    modality: str = "structured"
    payload: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.payload and self.data:
            self.payload = self.data
        elif not self.data and self.payload:
            self.data = self.payload


class SensoryProcessor:
    async def process(self, input_data: SensoryInput) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(input_data.data or input_data.payload)
        out.setdefault("modality", input_data.modality)
        if input_data.modality == "visual":
            out.setdefault("spatial_field", input_data.data.get("spatial_features", {}))
            out.setdefault("coherence", input_data.data.get("clarity", 0.0))
        elif input_data.modality == "text":
            out.setdefault("tokens", input_data.data.get("tokens", {}))
            out.setdefault("semantic_field", input_data.data.get("tokens", {}))
            out.setdefault("coherence", input_data.data.get("confidence", 0.8))
        elif input_data.modality == "structured":
            out.setdefault("coherence", 0.8)
        return out
