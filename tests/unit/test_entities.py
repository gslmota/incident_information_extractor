import pytest
from datetime import datetime

from src.domain.entities import IncidentInfo, IncidentText


class TestIncidentInfo:
    def test_to_dict_with_datetime(self) -> None:
        incident = IncidentInfo(
            data_ocorrencia=datetime(2025, 8, 14, 14, 0),
            local="São Paulo",
            tipo_incidente="Falha no servidor",
            impacto="Sistema indisponível por 2 horas"
        )
        
        result = incident.to_dict()
        
        assert result == {
            "data_ocorrencia": "2025-08-14 14:00",
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível por 2 horas"
        }

    def test_to_dict_without_datetime(self) -> None:
        incident = IncidentInfo(
            data_ocorrencia=None,
            local="São Paulo",
            tipo_incidente="Falha no servidor",
            impacto="Sistema indisponível por 2 horas"
        )
        
        result = incident.to_dict()
        
        assert result["data_ocorrencia"] is None


class TestIncidentText:
    def test_valid_text(self) -> None:
        text = IncidentText("Falha no servidor principal")
        assert text.content == "Falha no servidor principal"

    def test_empty_text_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Incident text cannot be empty"):
            IncidentText("")

    def test_whitespace_only_text_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Incident text cannot be empty"):
            IncidentText("   ")