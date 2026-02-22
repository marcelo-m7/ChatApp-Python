# 1. Diagnóstico do Código Base

## Visão geral
- **Domínio atual:** aplicação de chat em tempo real com interface Flet, suporte a salas públicas/privadas, upload de arquivos e assistente baseado em OpenAI.
- **Entrypoints principais:** `src/main.py` (UI) e `server.py` (download de arquivos via FastAPI).

## Arquitetura
### Tipo de arquitetura
- Arquitetura **monolítica modular leve**: UI, domínio e integrações estão no mesmo projeto e processo lógico.
- Forte orientação a evento na UI via `page.pubsub` (Flet), com persistência em memória.

### Padrões observados
- Uso parcial de entidades (`Message`, `Room`, `User`, `File`) via dataclasses.
- Camada de “use cases” limitada (`dialogs.py`) sem separação completa de aplicação/domínio/infra.
- “God component” em `ChatInterface`, concentrando estado, renderização e regras de negócio.

### Separação de responsabilidades
- **Boa intenção estrutural** em `chat/entities`, `chat/utils`, `assistants/utils`.
- **Separação incompleta:** regras de negócio espalhadas em componentes de interface (`chat_interface.py`) e utilitários.
- **Acoplamento alto** entre UI e domínio (ex.: troca de sala, criação de mensagem, processamento de assistente e atualização de componentes no mesmo fluxo).

### Acoplamento
- Alto acoplamento entre:
  - UI (`ChatInterface`) e estado global (`ChatApp`)
  - Camada de assistentes e modelo de mensagens
  - Upload/download com detalhes de URL hardcoded

## Estrutura do Projeto
### Organização de diretórios
- Estrutura principal:
  - `src/chat/*` para chat e UI
  - `src/assistants/*` para assistente
  - `server.py` para API de arquivos
- Há coerência inicial, mas faltam pastas de **serviços**, **config**, **testes**, **documentação de arquitetura** e **observabilidade**.

### Modularização e consistência
- Entidades estão isoladas, porém os fluxos principais não seguem um “application service layer”.
- Inconsistências de nomenclatura/idioma (PT/EN mistos; ex.: `reciver`, `programador`, `chat_room`, `join_chat_click`).

## Qualidade do Código
### Legibilidade
- Código em geral legível, porém com classes grandes e métodos extensos em UI.
- Há trechos duplicados e repetição de lógica de resposta do assistente.

### Complexidade e redundância
- `on_message` concentra múltiplas responsabilidades (roteamento por tipo, renderização, atualização de usuários, invocação de assistente).
- Duplicidade na invocação de resposta do assistente para sala `programador`.

### Anti-patterns e sinais de dívida
- Estado global em memória sem estratégias explícitas de concorrência/sessão distribuída.
- Configurações sensíveis e de infraestrutura parcialmente hardcoded.
- Dependências potencialmente órfãs e utilitários não integrados ao fluxo principal.

## Dependências
### Bibliotecas principais
- UI: Flet
- API de arquivos: FastAPI/Uvicorn
- IA: OpenAI + ecossistema LangChain/FAISS
- Configuração: python-dotenv

### Serviços externos e infraestrutura
- OpenAI API
- OAuth GitHub (configurado, parcialmente desativado no fluxo principal)
- Servidor HTTP auxiliar para arquivos

### Observações de risco em dependências
- `requirements.txt` em formato UTF-16/encoding inconsistente (risco em toolchain CI/CD).
- Diferença entre `pyproject.toml` (dependências mínimas) e `requirements.txt` (stack extensa).

## Documentação Existente
- **Parcial:** `README.md` explica execução e funcionalidades, mas não há documentação de arquitetura, decisões técnicas, contratos internos e governança para agentes.

## Riscos Técnicos (prioridade)
1. **Alto:** Concentração de regras de negócio na camada UI.
2. **Alto:** Persistência apenas em memória (limite de escalabilidade e durabilidade).
3. **Médio/Alto:** Acoplamento entre fluxos de chat e assistente.
4. **Médio:** Inconsistência de configuração/depêndencias.
5. **Médio:** Ausência de testes automatizados e critérios de qualidade formais.
6. **Médio:** Segurança e validações limitadas (upload, autenticação parcialmente desativada, sanitização).

---

# 2. Arquitetura do Sistema Multi-Agente

## Modelo de orquestração
- **Orquestrador Principal (Master Architect):** define backlog, ordem de execução, gates de qualidade e critérios de aceite.
- **Execução em pipeline por fase**, com handoffs explícitos por artefato.
- **Governança por evidência:** cada agente entrega logs, checklist e diff resumido.

## Agentes propostos

### A1 — Agente Organizador de Estrutura
- **Responsabilidade:** padronizar árvore do repositório, separar camadas e preparar convenções.
- **Limites:** não alterar regras de negócio sem RFC aprovada.
- **Entradas:** diagnóstico, estrutura atual, convenções definidas.
- **Saídas:** nova estrutura de diretórios, mapa de migração, arquivo `Agents.md`.
- **Dependências:** aprovação do Orquestrador + A2 (documentação base).

### A2 — Agente de Documentação
- **Responsabilidade:** criar arquitetura documental (`/docs`) e templates.
- **Limites:** não modificar lógica de runtime.
- **Entradas:** diagnóstico, decisões arquiteturais.
- **Saídas:** índices, convenções, ADR inicial, guias operacionais.
- **Dependências:** A1.

### A3 — Agente de Refatoração
- **Responsabilidade:** reduzir acoplamento, extrair serviços/aplicação, modularizar UI.
- **Limites:** manter comportamento funcional validado por testes.
- **Entradas:** baseline estrutural + critérios de design.
- **Saídas:** módulos refatorados, migração incremental, notas de compatibilidade.
- **Dependências:** A1, A2, A4 (testes mínimos).

### A4 — Agente de Testes
- **Responsabilidade:** criar estratégia e suíte de testes (unitário/integrado/contrato).
- **Limites:** não alterar arquitetura sem alinhamento.
- **Entradas:** fluxos críticos definidos pelo Orquestrador.
- **Saídas:** testes automatizados, cobertura mínima por módulo, fixtures.
- **Dependências:** A1, A2.

### A5 — Agente de Qualidade
- **Responsabilidade:** lint, tipagem, complexidade ciclomática, duplicidade.
- **Limites:** não introduzir breaking changes.
- **Entradas:** código refatorado + testes.
- **Saídas:** relatório de qualidade e plano de correção.
- **Dependências:** A3, A4.

### A6 — Agente de Segurança
- **Responsabilidade:** revisão de autenticação, validação de upload/download, gestão de segredos.
- **Limites:** mudanças invasivas só com aprovação do Orquestrador.
- **Entradas:** fluxos e superfícies de ataque.
- **Saídas:** threat model simplificado, correções priorizadas, checklist OWASP aplicável.
- **Dependências:** A3, A4.

### A7 — Agente de Integração
- **Responsabilidade:** padronizar configuração, ambientes, Docker/execução local e CI.
- **Limites:** não redefinir regras de domínio.
- **Entradas:** estrutura final de módulos e testes.
- **Saídas:** pipeline de integração, scripts de bootstrap, matriz de ambientes.
- **Dependências:** A4, A5, A6.

### A8 — Agente de Auditoria
- **Responsabilidade:** verificar rastreabilidade, aderência ao plano e evidências finais.
- **Limites:** não executar refatoração estrutural.
- **Entradas:** artefatos de todos os agentes.
- **Saídas:** parecer final, lacunas e recomendações executivas.
- **Dependências:** todos os anteriores.

---

# 3. Plano Incremental por Fases

## Fase 1 (Obrigatória) — Fundação do Sistema
- **Objetivo estratégico:** criar base governável para execução multi-agente.
- **Entregáveis:**
  - Reorganização inicial do repositório
  - Padronização estrutural
  - Criação de `Agents.md`
  - Base documental em `/docs`
- **Agentes envolvidos:** A1, A2
- **Ordem:** A1 → A2
- **Critérios de sucesso:** estrutura alvo aplicada, convenções publicadas, onboarding replicável.
- **Riscos:** ruptura de imports; mitigação com mapa de migração e smoke tests.

## Fase 2 — Estabilização de Arquitetura
- **Objetivo:** separar UI, aplicação, domínio e infraestrutura.
- **Entregáveis:** serviços de aplicação, interfaces/ports, redução do `ChatInterface`.
- **Agentes:** A3, A4
- **Ordem:** A3 → A4 (iterativo)
- **Critérios:** fluxo funcional preservado, testes cobrindo cenários críticos.
- **Riscos:** regressão funcional; mitigação por testes de regressão.

## Fase 3 — Qualidade e Segurança
- **Objetivo:** elevar confiabilidade e reduzir débito técnico.
- **Entregáveis:** lint/type-check/complexidade, hardening de upload/auth/config.
- **Agentes:** A5, A6
- **Ordem:** A5 → A6 → A5 (revalidação)
- **Critérios:** baseline de qualidade atingida, vulnerabilidades prioritárias tratadas.
- **Riscos:** aumento de esforço por dívida oculta.

## Fase 4 — Integração e Operação
- **Objetivo:** tornar execução previsível em ambientes locais e CI.
- **Entregáveis:** pipeline CI, scripts padronizados, documentação operacional.
- **Agentes:** A7, A2
- **Ordem:** A7 → A2
- **Critérios:** build/test automatizados e reproduzíveis.
- **Riscos:** incompatibilidades de dependências/encoding.

## Fase 5 — Auditoria e Escalonamento
- **Objetivo:** validar prontidão para evolução contínua por agentes.
- **Entregáveis:** relatório de auditoria, backlog priorizado de evolução.
- **Agentes:** A8 + Orquestrador
- **Ordem:** A8 → Orquestrador
- **Critérios:** rastreabilidade ponta-a-ponta, aprovação executiva.
- **Riscos:** lacunas de evidência; mitigação com padrão obrigatório de evidências.

---

# 4. Estrutura de Documentação Proposta

## Árvore obrigatória
```text
/docs
  /architecture
  /agents
  /tasks
  /testing
  /decisions
  /evidence
  /recommendations
```

## Regras por diretório

### `/docs/architecture`
- **Index:** `README.md` com visão sistêmica, diagramas e fronteiras.
- **Convenção:** C4 simplificado + contexto/componente.
- **Versionamento:** atualizar a cada mudança estrutural relevante.
- **Nomenclatura:** `architecture-<tema>-v<major>.<minor>.md`.

### `/docs/agents`
- **Index:** catálogo de agentes, responsabilidades e contratos.
- **Convenção:** 1 arquivo por agente + SLA de execução.
- **Versionamento:** semântico por alteração de escopo.
- **Nomenclatura:** `agent-<nome>-v<major>.<minor>.md`.

### `/docs/tasks`
- **Index:** backlog e status por fase.
- **Convenção:** task com contexto, dono (agente), definição de pronto.
- **Versionamento:** histórico por sprint/fase.
- **Nomenclatura:** `task-<id>-<slug>.md`.

### `/docs/testing`
- **Index:** estratégia de testes, pirâmide e critérios de cobertura.
- **Convenção:** separar unitário/integração/e2e/contrato.
- **Versionamento:** por release.
- **Nomenclatura:** `test-plan-<release>.md`, `test-report-<date>.md`.

### `/docs/decisions`
- **Index:** log de ADRs.
- **Convenção:** ADR curta (contexto, decisão, consequências).
- **Versionamento:** imutável por ADR; mudanças geram nova ADR.
- **Nomenclatura:** `ADR-<nnn>-<titulo-curto>.md`.

### `/docs/evidence`
- **Index:** evidências por fase e agente.
- **Convenção:** anexar comandos, logs, prints, métricas, diffs.
- **Versionamento:** carimbo temporal + referência de commit.
- **Nomenclatura:** `evidence-<fase>-<agente>-<timestamp>.md`.

### `/docs/recommendations`
- **Index:** recomendações estratégicas e roadmap técnico.
- **Convenção:** classificar por impacto/esforço/risco.
- **Versionamento:** revisão mensal/trimestral.
- **Nomenclatura:** `recommendation-<tema>-<priority>.md`.

## Padrão transversal de documentação
- Todo documento deve conter: **Contexto, Objetivo, Escopo, Não-Escopo, Evidência, Próximos Passos**.
- Definir cabeçalho com: **owner, data, versão, status, links relacionados**.

---

# 5. Prompts Operacionais dos Agentes

## Prompt — A1 Agente Organizador de Estrutura
**Papel:** Especialista em arquitetura de repositórios Python e modularização incremental.

**Contexto do projeto:** Chat Flet + FastAPI + OpenAI, com acoplamento alto entre UI e regras de negócio.

**Escopo de atuação:**
1. Propor árvore alvo.
2. Mapear migração arquivo-a-arquivo.
3. Criar `Agents.md` com contratos de execução entre agentes.

**Regras operacionais:**
- Não alterar comportamento funcional nesta etapa.
- Priorizar refactors mecânicos e reversíveis.
- Gerar plano de rollback por lote de alteração.

**Limitações:**
- Sem mudanças de domínio/feature.
- Sem ajustes de segurança profundos (delegar A6).

**Formato de saída esperado:**
- `Structure Delta Report`
- `Migration Map`
- `Risk & Rollback Checklist`

**Critérios de conclusão:**
- Estrutura aprovada pelo Orquestrador.
- Imports e execução básica preservados.

---

## Prompt — A2 Agente de Documentação
**Papel:** Arquiteto de documentação técnica e governança.

**Contexto:** inexistência de base documental estruturada.

**Escopo:**
1. Criar índices de `/docs`.
2. Definir templates oficiais por diretório.
3. Publicar convenções de nomenclatura e versionamento.

**Regras:**
- Linguagem objetiva.
- Rastreabilidade para commits/PRs/tarefas.
- Templates reutilizáveis e curtos.

**Limitações:**
- Não alterar código de aplicação.

**Saída:**
- `Documentation Architecture`
- `Templates Pack`
- `Governance Guide`

**Conclusão:**
- `/docs` navegável e pronto para execução por agentes.

---

## Prompt — A3 Agente de Refatoração
**Papel:** Engenheiro de refatoração orientada a arquitetura limpa.

**Contexto:** `ChatInterface` concentra regras de negócio e UI.

**Escopo:**
1. Extrair serviços de aplicação.
2. Introduzir fronteiras (UI/Application/Domain/Infra).
3. Reduzir duplicação e complexidade de métodos críticos.

**Regras:**
- Refatoração incremental por PR pequeno.
- Cada etapa com testes de regressão mínimos.
- Manter assinatura pública quando possível.

**Limitações:**
- Sem redesign visual amplo.

**Saída:**
- `Refactor Change Set`
- `Compatibility Notes`
- `Complexity Reduction Report`

**Conclusão:**
- Acoplamento reduzido e fluxos críticos preservados.

---

## Prompt — A4 Agente de Testes
**Papel:** Especialista em estratégia e automação de testes.

**Contexto:** ausência de suíte automatizada robusta.

**Escopo:**
1. Definir matriz de testes por risco.
2. Implementar unitários e integração de fluxos essenciais.
3. Criar fixtures/mocks para OpenAI e pubsub.

**Regras:**
- Priorizar cenários críticos: envio de mensagem, troca de sala, upload/download.
- Testes determinísticos.

**Limitações:**
- Evitar acoplamento excessivo a detalhes internos de UI.

**Saída:**
- `Test Strategy`
- `Automated Test Suite`
- `Coverage & Gap Report`

**Conclusão:**
- Cobertura mínima acordada e pipeline verde.

---

## Prompt — A5 Agente de Qualidade
**Papel:** Auditor de qualidade estática e mantenabilidade.

**Contexto:** dívida técnica e inconsistências de estilo/nomeação.

**Escopo:**
1. Definir baseline de lint/tipagem/complexidade.
2. Corrigir violações prioritárias.
3. Publicar qualidade por módulo.

**Regras:**
- Não introduzir breaking change.
- Fazer correções pequenas e revisáveis.

**Limitações:**
- Não alterar regras funcionais sem alinhamento A3.

**Saída:**
- `Quality Baseline`
- `Violation Fix Pack`
- `Maintainability Report`

**Conclusão:**
- Índices de qualidade dentro da meta.

---

## Prompt — A6 Agente de Segurança
**Papel:** Engenheiro de segurança de aplicação.

**Contexto:** uploads, autenticação e segredos com controles parciais.

**Escopo:**
1. Revisar superfícies de ataque (upload/download/auth).
2. Definir controles de validação e hardening.
3. Revisar gestão de segredos e configuração.

**Regras:**
- Priorizar riscos exploráveis externamente.
- Recomendações acionáveis por severidade.

**Limitações:**
- Sem reescrever arquitetura inteira.

**Saída:**
- `Threat Model Lite`
- `Security Findings`
- `Mitigation Plan`

**Conclusão:**
- Itens críticos endereçados ou formalmente aceitos.

---

## Prompt — A7 Agente de Integração
**Papel:** Engenheiro de CI/CD e operação.

**Contexto:** execução local funcional, porém sem governança completa de integração.

**Escopo:**
1. Padronizar comandos de setup/run/test.
2. Integrar validações em pipeline.
3. Harmonizar `requirements`/`pyproject` e ambientes.

**Regras:**
- Reprodutibilidade first.
- Etapas rápidas com fallback.

**Limitações:**
- Sem alterar domínio de negócio.

**Saída:**
- `Integration Pipeline`
- `Environment Matrix`
- `Ops Runbook`

**Conclusão:**
- Build/test/deploy local/CI previsíveis.

---

## Prompt — A8 Agente de Auditoria
**Papel:** Auditor técnico de conformidade e rastreabilidade.

**Contexto:** múltiplos agentes atuando em paralelo exigem governança forte.

**Escopo:**
1. Conferir aderência ao plano por fase.
2. Validar evidências e critérios de aceite.
3. Emitir parecer final com pendências.

**Regras:**
- Evidência obrigatória para cada claim.
- Classificação de risco residual.

**Limitações:**
- Não executar mudanças técnicas.

**Saída:**
- `Audit Ledger`
- `Compliance Scorecard`
- `Executive Technical Verdict`

**Conclusão:**
- Projeto pronto para próxima onda de evolução com risco controlado.
