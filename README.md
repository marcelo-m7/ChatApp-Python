# ChatApp Python

Aplicação de chat em tempo real construída com Flet (UI) e FastAPI (download de arquivos), com suporte a assistente OpenAI.

## Estrutura do projeto

```text
src/
  chatapp/
    application/      # serviços/casos de uso + ports
    config/           # configurações centralizadas
    domain/           # entidades de domínio
    infrastructure/   # integrações externas (HTTP/OpenAI/OAuth/persistência)
    ui_flet/          # inicialização da UI Flet
  chat/               # implementação atual (compatível)
  assistants/         # integração de assistente
server.py             # entrypoint do serviço de arquivos
docs/                 # documentação por domínio
```

## Requisitos

- Python 3.9+
- Dependências do projeto:

```bash
pip install -r requirements.txt
```

## Execução

### UI (Flet)

```bash
python src/main.py
```

### API de download (FastAPI)

```bash
python server.py
```

## Qualidade de código

```bash
ruff check .
black --check .
mypy src
```

## Testes e cobertura

```bash
pytest
```

A suíte está em `tests/` e mede cobertura com `pytest-cov` para os módulos de aplicação, domínio e infraestrutura,
com *gate* mínimo de 80%.

## Arquitetura (visão rápida)

```text
UI (Flet) -> Application Services -> Domain -> Infrastructure
                 ^                         |
                 +------ FastAPI ---------+
```

Documentação detalhada em `docs/architecture/diagram.md` e ADRs em `docs/decisions/`.

## Variáveis de ambiente

As configurações principais estão em `src/chatapp/config/settings.py`:

- `HOST`, `PORT`, `ASSETS_DIR`, `UPLOAD_DIR`
- `FILE_SERVER_HOST`, `FILE_SERVER_PORT`, `FILE_SERVER_UPLOAD_DIR`
- `FILE_SERVER_DOWNLOAD_URL_TEMPLATE`
- `OPENAI_API_KEY`, `ASSISTANT_MODEL`, `ASSISTANT_TEMPERATURE`, `ASSISTANT_NAME`
- `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `GITHUB_REDIRECT_URL`
