import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime

from src.application.use_cases import ExtractIncidentInfoUseCase
from src.domain.entities import IncidentText
from src.domain.exceptions import InvalidJsonResponseError


class TestExtractIncidentInfoUseCase:
    def setup_method(self) -> None:
        self.llm_service = AsyncMock()
        self.text_preprocessor = Mock()
        self.json_parser = Mock()
        self.text_postprocessor = Mock()
        
        self.use_case = ExtractIncidentInfoUseCase(
            llm_service=self.llm_service,
            text_preprocessor=self.text_preprocessor,
            json_parser=self.json_parser,
            text_postprocessor=self.text_postprocessor,
        )

    @pytest.mark.asyncio
    async def test_execute_success(self) -> None:
        from src.domain.entities import IncidentInfo
        
        incident_text = IncidentText("Falha no servidor ontem às 14h")
        
        self.text_preprocessor.preprocess.return_value = "Falha no servidor 2025-08-13 14:00"
        self.llm_service.generate_response.return_value = '{"data_ocorrencia": "2025-08-13 14:00"}'
        self.json_parser.parse.return_value = {
            "data_ocorrencia": "2025-08-13 14:00",
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível"
        }
        self.text_postprocessor.normalize_field_names.return_value = {
            "data_ocorrencia": "2025-08-13 14:00",
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível"
        }
        self.text_postprocessor.build_incident_info.return_value = IncidentInfo(
            data_ocorrencia=datetime(2025, 8, 13, 14, 0),
            local="São Paulo",
            tipo_incidente="Falha no servidor",
            impacto="Sistema indisponível"
        )
        
        result = await self.use_case.execute(incident_text)
        
        assert result.data_ocorrencia == datetime(2025, 8, 13, 14, 0)
        assert result.local == "São Paulo"
        assert result.tipo_incidente == "Falha no servidor"
        assert result.impacto == "Sistema indisponível"

    @pytest.mark.asyncio
    async def test_execute_with_invalid_json_raises_error(self) -> None:
        incident_text = IncidentText("Falha no servidor")
        
        self.text_preprocessor.preprocess.return_value = "Falha no servidor"
        self.llm_service.generate_response.return_value = "resposta inválida"
        self.json_parser.parse.side_effect = Exception("Invalid JSON")
        
        with pytest.raises(InvalidJsonResponseError):
            await self.use_case.execute(incident_text)

    @pytest.mark.asyncio
    async def test_execute_with_none_datetime(self) -> None:
        from src.domain.entities import IncidentInfo
        
        incident_text = IncidentText("Falha no servidor")
        
        self.text_preprocessor.preprocess.return_value = "Falha no servidor"
        self.llm_service.generate_response.return_value = '{"data_ocorrencia": null}'
        self.json_parser.parse.return_value = {
            "data_ocorrencia": None,
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível"
        }
        self.text_postprocessor.normalize_field_names.return_value = {
            "data_ocorrencia": None,
            "local": "São Paulo",
            "tipo_incidente": "Falha no servidor",
            "impacto": "Sistema indisponível"
        }
        self.text_postprocessor.build_incident_info.return_value = IncidentInfo(
            data_ocorrencia=None,
            local="São Paulo",
            tipo_incidente="Falha no servidor",
            impacto="Sistema indisponível"
        )
        
        result = await self.use_case.execute(incident_text)
        
        assert result.data_ocorrencia is None

