from ...domain.entities import IncidentInfo, IncidentText
from ...domain.exceptions import InvalidJsonResponseError
from ...domain.value_objects import ExtractionPrompt
from ..interfaces import (
    JsonParserInterface,
    LLMServiceInterface,
    TextPostprocessorInterface,
    TextPreprocessorInterface,
)


class ExtractIncidentInfoUseCase:
    def __init__(
        self,
        llm_service: LLMServiceInterface,
        text_preprocessor: TextPreprocessorInterface,
        json_parser: JsonParserInterface,
        text_postprocessor: TextPostprocessorInterface,
    ) -> None:
        self._llm_service = llm_service
        self._text_preprocessor = text_preprocessor
        self._json_parser = json_parser
        self._text_postprocessor = text_postprocessor

    async def execute(self, incident_text: IncidentText) -> IncidentInfo:
        preprocessed_text = self._text_preprocessor.preprocess(incident_text.content)

        prompt = ExtractionPrompt.default()
        formatted_prompt = prompt.content.format(incident_text=preprocessed_text)

        llm_response = await self._llm_service.generate_response(formatted_prompt)

        try:
            extracted_data = self._json_parser.parse(llm_response)
        except Exception as e:
            raise InvalidJsonResponseError(
                f"LLM response: {llm_response[:200]}... | Error: {e}"
            )

        normalized_data = self._text_postprocessor.normalize_field_names(extracted_data)
        return self._text_postprocessor.build_incident_info(normalized_data)
