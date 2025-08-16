class IncidentExtractorError(Exception):
    """Base exception for incident extractor"""


class LLMServiceError(IncidentExtractorError):
    """Error communicating with LLM service"""


class InvalidJsonResponseError(IncidentExtractorError):
    """Error parsing JSON from LLM response"""


class TextPreprocessingError(IncidentExtractorError):
    """Error during text preprocessing"""
