from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentText:
    content: str

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("Incident text cannot be empty")
