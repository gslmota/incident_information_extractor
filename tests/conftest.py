import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture(autouse=True, scope="session")
def mock_ollama_service():
    mock_service = AsyncMock()
    mock_service.close = AsyncMock()
    
    with patch("src.presentation.api.main.ollama_service", mock_service):
        yield mock_service