# Padrões de Codificação

## Regras gerais
- Preferir tipagem explícita em serviços e entidades.
- Manter regras de negócio em `chatapp/domain` e `chatapp/application`.
- Evitar duplicação de regras (ex.: validação de extensão de arquivo centralizada em `file_rules.py`).

## Testes
- Novas regras de domínio devem incluir teste unitário.
- Correções de bug devem vir acompanhadas de teste de regressão quando possível.

## Estrutura
- `domain`: entidades e regras puras.
- `application`: serviços/casos de uso.
- `infrastructure`: adaptadores externos.
