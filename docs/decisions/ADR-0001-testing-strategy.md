# ADR-0001 — Estratégia de testes com `pytest` e cobertura

- **Status:** Aprovado
- **Data:** 2026-02-22

## Contexto
A base tinha poucos testes e sem medição de cobertura consistente.

## Decisão
1. Padronizar testes em `pytest`.
2. Medir cobertura com `pytest-cov`.
3. Aplicar *quality gate* de cobertura mínima em 80% para os módulos principais (`application`, `domain`, `infrastructure`).

## Consequências
- Execução padronizada local e em CI.
- Redução de regressões em regras de domínio e serviços.
- Necessidade de manter testes ao evoluir casos de uso.
