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

## Desenvolvimento

### Qualidade de Código

O projeto utiliza ferramentas de qualidade de código que são executadas automaticamente:

#### Git Pre-commit Hook

Um hook de pré-commit está configurado para garantir a qualidade do código antes de cada commit:

- **Black**: Formatação automática do código
- **MyPy**: Verificação de tipos estática

##### Configuração do Hook

Para configurar o pre-commit hook em um novo clone do projeto:

```bash
git clone https://github.com/gslmota/incident_information_extractor.git
cd incident_information_extractor

# Instale as dependências
poetry install

# Configure o pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Formatar código com black
echo "Formatando código com black..."
poetry run black src

# Verificar tipos com mypy
echo "Verificando tipos com mypy..."
poetry run mypy src

# Se mypy falhar, cancelar commit
if [ $? -ne 0 ]; then
    echo "Erro no mypy. Commit cancelado."
    exit 1
fi

echo "Pré-commit executado com sucesso!"
EOF

# Torne o hook executável
chmod +x .git/hooks/pre-commit
```

##### Como Funciona

O hook executa automaticamente ao fazer `git commit` e:
1. Formata todo o código da pasta `src/` com Black
2. Verifica os tipos com MyPy
3. Se houver erros de tipo, o commit é cancelado

#### Comandos Manuais

Você também pode executar as ferramentas manualmente:

```bash
# Formatação com Black
poetry run black src

# Verificação de tipos com MyPy
poetry run mypy src

# Executar testes
poetry run pytest
```

#### Bypass do Pre-commit Hook

Se necessário, você pode pular o hook temporariamente:

```bash
git commit --no-verify
```

O projeto também possui um workflow do GitHub Actions que executa verificações automáticas de código. Atualmente, apenas executa linting e testes, sem configuração para validar pull requests.

## Arquitetura

Este projeto implementa **Clean Architecture** seguindo os princípios de **Domain-Driven Design (DDD)** e **SOLID**. A estrutura foi cuidadosamente organizadas para facilitar manutenibilidade, testabilidade e extensibilidade em projetos de ML.

### Estrutura de Pastas

```
src/
├── domain/                          # Camada de Domínio (Regras de Negócio)
│   ├── entities/                    # Entidades principais do domínio
│   │   ├── incident.py             # IncidentInfo - dados estruturados do incidente
│   │   └── incident_text.py        # IncidentText - texto bruto + validações
│   ├── value_objects/               # Objetos de valor imutáveis
│   │   ├── extraction_prompt.py    # Templates de prompt para LLM
│   │   └── llm_response.py         # Wrapper para resposta do LLM
│   └── exceptions.py               # Exceções específicas do domínio
├── application/                     # Camada de Aplicação (Casos de Uso)
│   ├── interfaces/                  # Contratos abstratos (Dependency Inversion)
│   │   ├── llm_service.py          # Interface para serviços LLM
│   │   └── text_processing.py      # Interfaces para processamento de texto
│   └── use_cases/                   # Workflows de negócio
│       └── extract_incident_info.py # Caso de uso principal de extração
├── infrastructure/                  # Camada de Infraestrutura (Implementações)
│   ├── models/                     # Serviços de Machine Learning
│   │   └── ollama_service.py       # Implementação concreta do Ollama
│   ├── processors/                 # Pipeline de processamento de texto
│   │   ├── text_preprocessor.py    # Limpeza e normalização de entrada
│   │   └── text_postprocessor.py   # Normalização e estruturação de saída
│   └── parsers/                    # Extração e parsing de dados
│       └── json_parser.py          # Parser para respostas JSON do LLM
└── presentation/                    # Camada de Apresentação (Interface Externa)
    └── api/                        # API REST
        ├── main.py                 # FastAPI application e rotas
        └── schemas.py              # Request/Response schemas (Pydantic)
```


## Como Executar o Projeto

### Execução Local (Desenvolvimento)

Para rodar o projeto localmente, você precisa:

1. **Instalar e configurar o Ollama:**
   ```bash
   # Instalar Ollama (Linux/macOS)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Iniciar o serviço Ollama
   ollama serve
   
   # Em outro terminal, baixar o modelo tinyllama
   ollama pull tinyllama
   ```

2. **Instalar dependências do projeto:**
   ```bash
   # Instalar Poetry (se não tiver)
   pip install poetry
   
   # Instalar dependências
   poetry install
   ```

3. **Executar a API:**
   ```bash
   # Rodar via comando atualizado
   poetry run uvicorn src.presentation.api.main:app --reload --host localhost --port 8000
   
   # Ou usar o script de debug otimizado
   python debug_scripts/run_local.py
   ```
   
   Ou usar o **debug do VS Code** com a configuração de launch.json
4. **Acessar a aplicação:**
   - API: http://localhost:8000
   - Documentação: http://localhost:8000/docs

### Execução com Docker (Produção)

#### Abordagem Padrão

```bash
# Subir todos os serviços
docker-compose up --build

# A API estará disponível em http://localhost:8000
# O modelo será baixado automaticamente na primeira requisição
```

#### Abordagem Alternativa (Conexão Limitada)

Devido a limitações de internet durante o desenvolvimento, utilizei uma estratégia alternativa, pois estava na fazenda com conexão de 10mb.

```bash
# 1. Subir os serviços
docker-compose up --build

# 2. Baixar o modelo manualmente no container (recomendado para conexão limitada)
docker exec -it ollama ollama pull tinyllama

# 3. A API já estará pronta para uso!
```

**Alternativa**: Deixar a API baixar automaticamente na primeira requisição, mas pode demorar mais com conexão lenta.

**Como baixar modelo manualmente no container:**
```bash
# Entrar no container Ollama
docker exec -it ollama bash

# Dentro do container, baixar o modelo
ollama pull tinyllama

# Verificar se o modelo foi baixado
ollama list

# Sair do container
exit
```

**Observações importantes:**
- Esta não é a abordagem mais eficiente para produção
- Em produção, o modelo deveria estar pré-carregado na imagem
- O modelo fica persistido no volume Docker entre reinicializações
- Após o primeiro download, não é necessário baixar novamente, pois ele fica salvo no volume
- Foi utilizada a versão Python 3.12-slim. Em produção, seria recomendável usar uma versão Alpine por ser menor e mais segura, porém devido às restrições de rede que eu tinha para build, não foi possível alterar.

### Executando Testes

O projeto possui uma suite completa de testes unitários e de integração:

```bash

# Executar todos os testes
pytest tests/ -v

# Executar apenas testes unitários
pytest tests/unit/ -v

# Executar apenas testes de integração  
pytest tests/integration/ -v

```

### Testando a API

```bash
# Teste de saúde
curl http://localhost:8000/health

# Exemplo de extração de incidente
curl -X POST "http://localhost:8000/extract" \
     -H "Content-Type: application/json" \
     -d '{"text": "Ocorreu um incidente ontem às 14:30 no servidor de produção. O sistema ficou indisponível por 2 horas devido a falha no banco de dados."}'
```

