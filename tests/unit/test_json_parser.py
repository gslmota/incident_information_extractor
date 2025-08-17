import pytest

from src.infrastructure.parsers import JsonParser
from src.domain.exceptions import InvalidJsonResponseError


class TestJsonParser:
    def setup_method(self) -> None:
        self.parser = JsonParser()

    def test_parse_valid_json(self) -> None:
        text = '{"data_ocorrencia": "2025-08-14 14:00", "local": "São Paulo"}'
        result = self.parser.parse(text)
        
        assert result["data_ocorrencia"] == "2025-08-14 14:00"
        assert result["local"] == "São Paulo"

    def test_parse_json_with_markdown(self) -> None:
        text = """```json
        {
            "data_ocorrencia": "2025-08-14 14:00",
            "local": "São Paulo"
        }
        ```"""
        
        result = self.parser.parse(text)
        assert result["data_ocorrencia"] == "2025-08-14 14:00"

    def test_parse_json_with_extra_text(self) -> None:
        text = """Aqui está a resposta:
        {"data_ocorrencia": "2025-08-14 14:00", "local": "São Paulo"}
        Fim da resposta."""
        
        result = self.parser.parse(text)
        assert result["data_ocorrencia"] == "2025-08-14 14:00"

    def test_parse_invalid_json_raises_error(self) -> None:
        text = "Este não é um JSON válido"
        
        with pytest.raises(InvalidJsonResponseError):
            self.parser.parse(text)

    def test_parse_malformed_json_raises_error(self) -> None:
        text = '{"data_ocorrencia": "2025-08-14 14:00", "local": }'
        
        with pytest.raises(InvalidJsonResponseError):
            self.parser.parse(text)