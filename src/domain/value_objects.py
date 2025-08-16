from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ExtractionPrompt:
    content: str

    def __str__(self) -> str:
        return self.content

    @classmethod
    def default(cls) -> "ExtractionPrompt":
        # prompt = """
        #   Você é um especialista em análise de incidentes. Extraia as seguintes informações do texto fornecido e retorne APENAS um JSON válido com os campos solicitados:
        #   - data_ocorrencia: data e hora do incidente no formato "YYYY-MM-DD HH:MM" (null se não mencionado)
        #   - local: local onde ocorreu o incidente
        #   - tipo_incidente: categoria ou tipo do incidente
        #   - impacto: descrição breve do impacto gerado

        #   Exemplo de incidente:
        #     Ontem às 14h, no escritório de São Paulo, houve uma falha no servidor principal que afetou o sistema de faturamento por 2 horas.

        #   Exemplo de resposta JSON:
        #   {{
        #     "data_ocorrencia": "2025-08-14 14:00",
        #     "local": "São Paulo",
        #     "tipo_incidente": "Falha no servidor",
        #     "impacto": "Sistema de faturamento indisponível por 2 horas"
        #   }}

        #   Texto do incidente: {incident_text}
        #   Resposta JSON:
        # """
        prompt = """
          You are an incident analysis specialist. Extract the following information from the provided text and return ONLY a valid JSON with the requested fields:
          - data_ocorrencia: date and time of the incident in the format "YYYY-MM-DD HH:MM" (null if not mentioned)
          - local: location where the incident occurred
          - tipo_incidente: category or type of the incident
          - impacto: brief description of the impact caused

          Example of an incident:
            2025-08-14 14:00, at the São Paulo office, there was a failure in the main server that affected the billing system for 2 hours.

          Example of JSON response:
          {{
            "data_ocorrencia": "2025-08-14 14:00",
            "local": "São Paulo",
            "tipo_incidente": "Server failure",
            "impacto": "Billing system unavailable for 2 hours"
          }}

          Incident text: {incident_text}
          JSON response:
        """

        return cls(content=prompt)


@dataclass(frozen=True)
class LLMResponse:
    raw_content: str
    extracted_data: Dict[str, Any]
