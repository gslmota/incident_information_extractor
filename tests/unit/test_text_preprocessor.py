from datetime import datetime, timedelta

from src.infrastructure.processors import TextPreprocessor

class TestTextPreprocessor:
    def setup_method(self) -> None:
        self.preprocessor = TextPreprocessor()

    def test_normalize_whitespace(self) -> None:
        text = "Falha   no    servidor\t\tprincipal\n\n"
        result = self.preprocessor.preprocess(text)
        assert "   " not in result
        assert "\t\t" not in result
        assert "\n\n" not in result

    def test_normalize_relative_dates(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        text = "Hoje ocorreu um problema. Ontem também houve falha."
        result = self.preprocessor.preprocess(text)
        
        assert today in result
        assert yesterday in result
        assert "hoje" not in result.lower()
        assert "ontem" not in result.lower()

    def test_normalize_time_formats(self) -> None:
        test_cases = [
            ("às 14h30", "14:30"),
            ("14h", "14:00"),
            ("às 9h", "9:00"),
        ]
        
        for input_text, expected_time in test_cases:
            result = self.preprocessor.preprocess(input_text)
            assert expected_time in result

    def test_full_preprocessing(self) -> None:
        text = "Ontem  às   14h30,  houve   falha."
        result = self.preprocessor.preprocess(text)
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        assert yesterday in result
        assert "14:30" in result
        assert "ontem" not in result.lower()
        assert "  " not in result