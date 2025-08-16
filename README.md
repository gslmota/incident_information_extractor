# Incident Extractor API

API para extração automática de informações estruturadas de descrições de incidentes usando LLM local (Ollama).

## Funcionalidades

- Extração de informações estruturadas de texto livre sobre incidentes
- Processamento usando modelo de linguagem local (Ollama)
- Pipeline de pré-processamento para melhorar consistência do texto
- API REST com FastAPI
- Arquitetura limpa e bem testada
- Suporte completo ao Docker

## Informações Extraídas

A API extrai as seguintes informações de um texto descrevendo um incidente:

- **data_ocorrencia**: Data e hora do incidente (formato: YYYY-MM-DD HH:MM)
- **local**: Local onde ocorreu o incidente
- **tipo_incidente**: Tipo ou categoria do incidente
- **impacto**: Descrição breve do impacto gerado

## Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI**: Framework web moderno e rápido
- **Poetry**: Gerenciamento de dependências
- **Ollama**: Modelo de linguagem local
- **Docker & Docker Compose**: Containerização
- **pytest**: Testes automatizados
- **Pydantic**: Validação de dados
- **structlog**: Logging estruturado

## Arquitetura

O projeto segue os princípios de Clean Architecture