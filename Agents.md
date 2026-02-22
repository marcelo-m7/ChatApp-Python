# Agents (Operação do Swarm)

## Objetivo
Este repositório é operado por múltiplos agentes especializados. Este documento define papéis, limites, fluxos e padrões de saída.

## Regras Gerais
- Nenhum agente “adivinha” contexto: sempre referenciar arquivos/paths.
- Toda mudança deve ter: tarefa + evidência + (se necessário) decisão (ADR).
- Saídas devem ser determinísticas: checklist final + arquivos alterados/criados.

## Topologia
### Camada 1 — Governança
- Chief Orchestrator: planeja, prioriza, aprova fases, gera prompts.
- Strategy Agent: traduz objetivos em roadmap e métricas.
- Decision Agent: cria ADRs quando houver trade-offs.

### Camada 2 — Coordenação
- Task Planner: quebra fases em tarefas executáveis.
- Dependency Manager: ordena tarefas e bloqueios.
- Scheduler: define ordem de execução e handoffs.

### Camada 3 — Execução
- Repo Organizer
- Documentation Agent
- Refactor Agent
- Testing Agent
- Security Agent
- Performance Agent
- Integration Agent

### Camada 4 — Auditoria
- Audit Agent (gate final)
- Consistency Agent (convenções, indexes, padrões)
- Quality Gate Agent (test/lint/build)
- Compliance Agent (regras e escopo)

## Padrão de Handoff (obrigatório)
Toda entrega entre agentes deve incluir:
- Contexto mínimo (links internos/paths)
- O que foi feito
- O que falta
- Riscos/assunções
- Checklist de validação

## Formatos obrigatórios de saída
- Checklist final
- Lista de arquivos criados/alterados
- Evidências geradas (paths)
