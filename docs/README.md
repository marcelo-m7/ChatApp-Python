# Documentação por Domínio

Este diretório organiza a documentação do projeto por domínio, com índices navegáveis, templates reutilizáveis e versionamento semântico de documentos.

## Índices por domínio

- [Architecture](architecture/README.md)
- [Agents](agents/README.md)
- [Tasks](tasks/README.md)
- [Testing](testing/README.md)
- [Decisions](decisions/README.md)
- [Recommendations](recommendations/README.md)
- [Evidence](evidence/README.md)

## Templates mínimos

- [ADR template](templates/adr-template.md)
- [Task spec template](templates/task-spec-template.md)
- [Evidence template](templates/evidence-template.md)
- [Test plan template](templates/test-plan-template.md)

## Convenções de versionamento semântico de documentos

Todos os documentos em `docs/` devem incluir metadados no topo com o campo `doc_version` no formato SemVer (`MAJOR.MINOR.PATCH`).

### Regras

- **MAJOR**: mudanças incompatíveis (estrutura, significado, ou contratos documentais).
- **MINOR**: adição de conteúdo retrocompatível (novas seções, exemplos ou critérios).
- **PATCH**: ajustes editoriais, correções de links, ortografia e clarificações sem alteração de intenção.

### Metadados recomendados

```yaml
---
title: Nome do Documento
doc_version: 1.0.0
status: draft | active | deprecated
owners:
  - @time-ou-pessoa
last_updated: YYYY-MM-DD
---
```

## Convenções de nomenclatura

- Preferir nomes em `kebab-case` para arquivos.
- Para ADRs: `ADR-XXXX-titulo-curto.md`.
- Para tarefas: `TASK-XXXX-titulo-curto.md`.
- Para evidências: `EVID-XXXX-titulo-curto.md`.
- Para planos de teste: `TESTPLAN-XXXX-titulo-curto.md`.
