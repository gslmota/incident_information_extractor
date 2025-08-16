import pytest
from datetime import datetime
from src.infrastructure.text_postprocessor import TextPostprocessor


class TestTextPostprocessor:
    def setup_method(self) -> None:
        self.postprocessor = TextPostprocessor()

    def test_parse_datetime_formats(self) -> None:
        valid_formats = [
            ("2025-08-13 14:00", datetime(2025, 8, 13, 14, 0)),
            ("2025-08-13", datetime(2025, 8, 13, 0, 0)),
        ]
        
        for date_str, expected in valid_formats:
            result = self.postprocessor._parse_datetime(date_str)
            assert result == expected

    def test_parse_invalid_datetime_returns_none(self) -> None:
        invalid_formats = ["invalid-date", "2025/08/13", ""]
        
        for date_str in invalid_formats:
            result = self.postprocessor._parse_datetime(date_str)
            assert result is None

    def test_normalize_field_names(self) -> None:
        input_data = {
            "data_ocoorrencia": "2025-08-13 14:00",
            "location": "São Paulo",
            "tipo": "Falha no servidor",
            "impact": "Sistema indisponível"
        }
        
        result = self.postprocessor.normalize_field_names(input_data)
        
        expected = {
            "data_ocorrencia": "2025-08-13 14:00",
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível"
        }
        
        assert result == expected

    def test_build_incident_info(self) -> None:
        input_data = {
            "data_ocorrencia": "2025-08-13 14:00",
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível"
        }
        
        result = self.postprocessor.build_incident_info(input_data)
        
        assert result.data_ocorrencia == datetime(2025, 8, 13, 14, 0)
        assert result.local == "São Paulo"
        assert result.tipo_incidente == "Falha no servidor"
        assert result.impacto == "Sistema indisponível"