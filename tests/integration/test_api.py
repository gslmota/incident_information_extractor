import pytest
from unittest.mock import AsyncMock, patch, Mock
from fastapi.testclient import TestClient

from src.presentation.api import app, get_use_case


class TestIncidentExtractorAPI:
    def test_health_check(self) -> None:
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "message": "Incident Extractor API is running"
        }

    def test_extract_incident_info_success(self) -> None:
        from src.domain.entities import IncidentInfo
        from datetime import datetime
        
        mock_use_case = AsyncMock()
        mock_incident = IncidentInfo(
            data_ocorrencia=datetime(2025, 8, 14, 14, 0),
            local="São Paulo", 
            tipo_incidente="Falha no servidor",
            impacto="Sistema indisponível por 2 horas"
        )
        mock_use_case.execute.return_value = mock_incident
        
        app.dependency_overrides[get_use_case] = lambda: mock_use_case
        try:
            client = TestClient(app)
            request_data = {
                "text": "Ontem às 14h, no escritório de São Paulo, houve uma falha no servidor principal que afetou o sistema por 2 horas."
            }
            
            response = client.post("/extract", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["data_ocorrencia"] == "2025-08-14 14:00"
            assert data["local"] == "São Paulo"
            assert data["tipo_incidente"] == "Falha no servidor"
            assert data["impacto"] == "Sistema indisponível por 2 horas"
        finally:
            app.dependency_overrides.clear()

    def test_extract_incident_info_empty_text(self) -> None:
        with patch("src.presentation.api.get_use_case"):
            client = TestClient(app)
            request_data = {"text": ""}
            
            response = client.post("/extract", json=request_data)
            
            assert response.status_code == 422

    def test_extract_incident_info_missing_text(self) -> None:
        with patch("src.presentation.api.get_use_case"):
            client = TestClient(app)
            response = client.post("/extract", json={})
            
            assert response.status_code == 422

    def test_extract_incident_info_llm_error(self) -> None:
        from src.domain.exceptions import LLMServiceError
        
        mock_use_case = AsyncMock()
        mock_use_case.execute.side_effect = LLMServiceError("Connection failed")
        
        app.dependency_overrides[get_use_case] = lambda: mock_use_case
        try:
            client = TestClient(app)
            request_data = {
                "text": "Falha no servidor"
            }
            
            response = client.post("/extract", json=request_data)
            
            assert response.status_code == 500
            assert "Erro no serviço LLM" in response.json()["detail"]
        finally:
            app.dependency_overrides.clear()