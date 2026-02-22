# ChatApp Python

Aplicação de chat em tempo real construída com Flet (UI) e FastAPI (download de arquivos), com suporte a assistente OpenAI.

## Estrutura do projeto

```text
src/
  chatapp/
    application/      # serviços/casos de uso
    config/           # configurações centralizadas
    domain/           # entidades de domínio
    infrastructure/   # integrações externas (FastAPI etc.)
    ui_flet/          # inicialização da UI Flet
  chat/               # implementação atual (compatível)
  assistants/         # integração de assistente
server.py             # entrypoint FastAPI
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

## Variáveis de ambiente

As configurações principais estão em `src/chatapp/config/settings.py`:

- `HOST`, `PORT`
- `SERVER_HOST`, `SERVER_PORT`
- `UPLOAD_DIR`, `SERVER_UPLOAD_DIR`
- `ASSETS_DIR`
