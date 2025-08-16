import difflib
from datetime import datetime
from typing import Any, Dict, Optional

from ..application.interfaces import TextPostprocessorInterface
from ..domain.entities import IncidentInfo


class TextPostprocessor(TextPostprocessorInterface):
    EXPECTED_FIELDS = {
        "data_ocorrencia": [
            "data_ocoorrencia",
            "data_ocorencia",
            "data_ocorrência",
            "data_incidente",
            "data",
        ],
        "local": ["location", "lugar", "localizacao", "localização"],
        "tipo_incidente": [
            "tipo_incidentde",
            "tipo_incidende",
            "tipo",
            "categoria",
            "type",
        ],
        "impacto": ["impact", "impactos", "consequencia", "consequência", "efeito"],
    }

    def normalize_field_names(self, data: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {}

        for expected_field, variations in self.EXPECTED_FIELDS.items():
            value = None

            if expected_field in data:
                value = data[expected_field]
            else:
                for variation in variations:
                    if variation in data:
                        value = data[variation]
                        break

                if value is None:
                    best_match = self._find_best_field_match(
                        expected_field, list(data.keys())
                    )
                    if best_match:
                        value = data[best_match]

            if value is not None:
                normalized[expected_field] = value

        return normalized

    def _find_best_field_match(
        self, target_field: str, available_fields: list[str], threshold: float = 0.6
    ) -> Optional[str]:
        best_match = None
        best_ratio = 0.0

        for field in available_fields:
            ratio = difflib.SequenceMatcher(
                None, target_field.lower(), field.lower()
            ).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = field

        return best_match

    def build_incident_info(self, data: Dict[str, Any]) -> IncidentInfo:
        data_ocorrencia = self._parse_datetime(data.get("data_ocorrencia"))

        return IncidentInfo(
            data_ocorrencia=data_ocorrencia,
            local=data.get("local", ""),
            tipo_incidente=data.get("tipo_incidente", ""),
            impacto=data.get("impacto", ""),
        )

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return None
