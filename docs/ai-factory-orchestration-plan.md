# Plano de Orquestração — AI-Driven Software Factory

## 1) Diagnóstico técnico do código base

### Contexto atual
- Aplicação principal em Python/Flet com entrada em `src/main.py` e servidor de arquivos FastAPI em `server.py`.
- Domínio de chat modelado em `src/chat/entities` e coordenado por `ChatApp`.
- Integração com LLM em `src/assistants` usando OpenAI via `Programador`.

### Achados técnicos
1. **Acoplamento UI + estado global**
   - `src/main.py` instancia `ChatApp` como singleton de processo e injeta direto na interface.
   - `ChatInterface` concentra construção de UI, eventos, pubsub e regras de sala no mesmo componente.
2. **Configuração de rede parcialmente hardcoded**
   - `ChatApp.download_url` usa `127.0.0.1:3000`, podendo quebrar em deploy/container.
3. **Dependências e gestão de ambiente inconsistentes**
   - `pyproject.toml` declara conjunto mínimo, mas `requirements.txt` contém stack muito maior e em encoding não padrão.
4. **Segurança e compliance operacional**
   - OAuth GitHub existe (`auth.py`), porém fluxo está desativado no bootstrap (`main.py` comenta callbacks e inicia app direto).
5. **Qualidade e evidência ausentes no ciclo atual**
   - Não há estrutura de documentação governada (`/docs`), nem pipeline explícito de gates por fase.

### Riscos principais
- Regressões funcionais por ausência de testes automatizados.
- Dificuldade de evolução por falta de ADRs e trilha de decisão.
- Risco de configuração divergente entre ambiente local, container e produção.

---

## 2) Mapa da arquitetura atual

### Módulos
- **Entrada/Runtime:** `src/main.py`
- **Interface e interação:** `src/chat/chat_interface.py`, `src/chat/chat_message.py`, `src/chat/use_cases/dialogs.py`
- **Aplicação/domínio:** `src/chat/chat_app.py`, `src/chat/chat_room.py`, `src/chat/entities/*`
- **Infra de arquivos:** `src/chat/utils/file_handler.py`, `server.py`
- **Assistentes/LLM:** `src/assistants/assistants.py`, `src/assistants/programador.py`, `src/assistants/utils/*`
- **Autenticação:** `src/chat/auth.py`

### Fluxos principais
1. Usuário abre app Flet (`main.py`) → `ChatInterface` monta UI.
2. Usuário envia mensagem → `ChatInterface` publica via pubsub → `ChatApp` persiste em sala.
3. Mensagem com menção `@programador` → `Assistants` invoca `Programador` (OpenAI) → resposta retorna como mensagem.
4. Upload/download de arquivos passa por utilitários de `file_handler` e endpoint FastAPI `/download/{filename}`.

### Dependências críticas
- Flet (UI + estado de sessão)
- FastAPI/Uvicorn (distribuição de arquivos)
- OpenAI + LangChain (assistente)
- dotenv para segredos/config

### Pontos críticos
- Mistura de camadas (apresentação + aplicação + integração externa no mesmo fluxo).
- Configuração fragmentada (porta/host em lugares diferentes).
- Ausência de padrões formais de handoff, memória e auditoria contínua.

---

## 3) Roadmap incremental por fases

## Fase 01 — Fundação de Governança Documental
**Entregáveis**
- Estrutura `/docs` com índices por pasta.
- `Agents.md` com topologia e regras operacionais.
- Backlog inicial e template ADR.

**Critérios de sucesso**
- Índices de todas as pastas criados.
- Fluxo de tarefa/decisão/evidência documentado.
- Audit Agent aprova Gate A e C.

## Fase 02 — Modelagem Operacional do Swarm
**Entregáveis**
- Prompts operacionais por agente.
- Protocolo YAML de comunicação.
- Definição de lifecycle e dependências de execução.

**Critérios de sucesso**
- Todos os agentes têm I/O padronizado.
- Handoffs obrigatórios em formato único.
- Audit Agent aprova consistência de prompts e estados.

## Fase 03 — Qualidade Incremental e Automação de Gates
**Entregáveis**
- Estratégia de testes por estágio (smoke/unit/integration).
- Checklist de gates automatizáveis (lint/test/build/docs-index).
- Matriz de evidências mínimas por fase.

**Critérios de sucesso**
- Gates B e C definidos com comandos objetivos.
- Evidências por fase registráveis em `/docs/evidence`.
- Audit Agent aprova checklist objetivo.

## Fase 04 — Execução Técnica Guiada por Agentes
**Entregáveis**
- Tarefas atômicas por módulo crítico (chat, auth, arquivos, assistants).
- ADRs para trade-offs estruturais.
- Evidências de validação por lote de tarefas.

**Critérios de sucesso**
- Taxa de bloqueio reduzida por dependências explícitas.
- Mudanças só entram com gates completos.
- Audit Agent mantém aprovação contínua de releases incrementais.

---

## 4) Topologia de agentes

## Camada 1 — Governança
- **Chief Orchestrator:** define fases, prioriza backlog, aprova avanço.
- **Strategy Agent:** converte objetivos em métricas e metas por fase.
- **Decision Agent:** formaliza ADRs em trade-offs arquiteturais.

## Camada 2 — Coordenação
- **Task Planner:** decompõe escopo em tarefas atômicas com DoD.
- **Dependency Manager:** identifica bloqueios e sequência ótima.
- **Scheduler:** libera execução e organiza handoffs.

## Camada 3 — Execução
- **Repo Organizer:** estrutura de pastas e conventions.
- **Documentation Agent:** índices, guias e memória viva.
- **Refactor Agent:** melhorias internas sem regressão.
- **Testing Agent:** estratégia e evolução de cobertura.
- **Security Agent:** segredos, riscos e controles.
- **Performance Agent:** profiling e otimizações priorizadas.
- **Integration Agent:** integrações externas e contratos.

## Camada 4 — Auditoria
- **Audit Agent:** gate final de aceite por fase.
- **Consistency Agent:** valida nomenclatura/index/convenções.
- **Quality Gate Agent:** executa/verifica lint/test/build.
- **Compliance Agent:** garante aderência ao escopo/regras.

### Limites operacionais
- Execução não altera escopo sem Decision Agent + ADR.
- Nenhum agente marca `done` sem aprovação do Audit Agent.
- Toda saída exige checklist + arquivos + evidências.

---

## 5) Sistema de memória e documentação

## Estrutura alvo
```txt
/docs
  index.md
  /architecture
    index.md
    overview.md
    module-map.md
  /agents
    index.md
    prompts/
      index.md
  /tasks
    index.md
    backlog.md
    phase-01.md
    phase-02.md
  /decisions
    index.md
    ADR-0001-template.md
  /memory
    index.md
    glossary.md
    conventions.md
    known-issues.md
  /testing
    index.md
    strategy.md
    coverage.md
  /evidence
    index.md
    phase-01/
      notes.md
      test-results.md
```

### Padrões obrigatórios
- Todo diretório com `index.md` listando filhos.
- Toda fase atualiza `/docs/index.md`.
- Toda decisão relevante gera ADR numerada.
- Evidências mínimas: notas + resultados de validação.

---

## 6) Lifecycle de tarefas

- `proposed` → `queued` (Task Planner quebra + estima)
- `queued` → `in_progress` (Scheduler libera)
- `in_progress` → `blocked` (dependência falhou)
- `in_progress` → `review` (executor concluiu)
- `review` → `done` (Audit Agent aprovou)
- `review` → `rework` (falha em gate)
- `rework` → `in_progress`

### Critérios por estado
- `queued`: prioridade, dependências e DoD definidos.
- `review`: evidências anexadas e checks executados.
- `done`: gates A/B/C/D aprovados e índice atualizado.

---

## 7) Quality Gates

## Gate A — Estrutural
- Estrutura de diretórios conforme padrão.
- Índices atualizados e links válidos.
- Arquivos posicionados na pasta correta.

## Gate B — Funcional
- Testes mínimos da fase executados.
- Lint/build (quando aplicável) sem erro bloqueador.

## Gate C — Evidência
- Evidência registrada em `/docs/evidence/<fase>/`.
- ADR criada quando houver trade-off técnico.

## Gate D — Auditoria
- Checklist revisado por Audit Agent.
- Diferenças aprovadas com justificativa objetiva.

---

## 8) Prompts operacionais dos agentes

## 8.1 Repo Organizer Agent
**Objetivo:** propor reorganização estrutural sem quebrar runtime.

**Entrada:** árvore atual, convenções do projeto, backlog da fase.

**Saída obrigatória:**
- proposta de nova árvore
- lista de migrações
- riscos de breaking change
- checklist final

## 8.2 Documentation Agent
**Objetivo:** manter `/docs` indexado e auditável.

**Entrada:** decisões, tarefas aprovadas, evidências da fase.

**Saída obrigatória:**
- paths `.md` criados/atualizados
- índices completos
- guia de escrita
- checklist final

## 8.3 Task Planner Agent
**Objetivo:** decompor fase em tarefas atômicas e ordenadas.

**Entrada:** roadmap, restrições e dependências.

**Saída obrigatória:**
- `/docs/tasks/phase-0X.md`
- critérios de pronto por tarefa
- dependências e ordem

## 8.4 Testing Agent
**Objetivo:** evoluir qualidade incremental por fase.

**Entrada:** escopo técnico e risco de regressão.

**Saída obrigatória:**
- `/docs/testing/strategy.md`
- plano smoke → unit → integration
- evidências esperadas por fase

## 8.5 Audit Agent
**Objetivo:** validar conformidade e aprovar/reprovar fase.

**Entrada:** checklist de gates, diffs e evidências.

**Saída obrigatória:**
- checklist de conformidade
- itens bloqueadores
- decisão final com justificativa

---

## Protocolo de comunicação entre agentes (obrigatório)

```yaml
agent: <nome>
task_id: <ID>
phase: <número>
status: <proposed|in_progress|blocked|review|done>
inputs:
  - <path ou referência>
outputs_expected:
  - <arquivos/artefatos>
checks:
  - <test/lint/build/doc-index>
handoff:
  next_agent: <nome>
  notes: |
    <o que foi feito, pendências, riscos>
```

---

## Rastreabilidade mandatória por fase

Cada fase **deve gerar**:
- tarefas em `/docs/tasks/`
- decisão técnica em `/docs/decisions/`
- evidências em `/docs/evidence/`
- atualização de `/docs/index.md`

## Critério de pronto da fase
Uma fase só é considerada concluída quando:
1. arquivos esperados existem (conforme plano da fase)
2. evidência mínima registrada
3. validação executada quando aplicável (test/lint/build)
4. Audit Agent aprova
