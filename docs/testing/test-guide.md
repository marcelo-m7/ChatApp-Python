# Guia de Testes

## Objetivo
Garantir regressões mínimas nas regras centrais de chat, upload e entidades de domínio.

## Como executar

```bash
pytest
```

Ou explicitando cobertura:

```bash
pytest --cov=src/chatapp/application --cov=src/chatapp/domain --cov=src/chatapp/infrastructure --cov-report=term-missing
```

## Escopo atual
- Serviços de aplicação (`ChatService`, `FileService`, `AssistantService`, `UploadService`).
- Entidades de domínio (`Message`, `Room`, `User`, `File`).
- Infraestrutura local (repositórios em memória, normalização de nome de arquivo, placeholders de DB).

## Critério de qualidade
- Cobertura mínima: **80%** (via `--cov-fail-under=80`).
