import pytest
from unittest.mock import AsyncMock, patch

# Global mock for ollama_service during tests
@pytest.fixture(autouse=True, scope="session")
def mock_ollama_service():
    """Mock the global ollama_service variable for all tests"""
    mock_service = AsyncMock()
    mock_service.close = AsyncMock()
    
    with patch("src.presentation.api.ollama_service", mock_service):
        yield mock_service