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

## Arquitetura

O projeto segue os princípios de Clean Architecture