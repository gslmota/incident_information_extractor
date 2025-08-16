from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class IncidentInfo:
    data_ocorrencia: Optional[datetime]
    local: str
    tipo_incidente: str
    impacto: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data_ocorrencia": (
                self.data_ocorrencia.strftime("%Y-%m-%d %H:%M")
                if self.data_ocorrencia
                else None
            ),
            "local": self.local,
            "tipo_incidente": self.tipo_incidente,
            "impacto": self.impacto,
        }


@dataclass(frozen=True)
class IncidentText:
    content: str

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("Incident text cannot be empty")
