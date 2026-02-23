# assistants.utils

## Módulos usados em runtime (ativos)

- `assistants.utils.data_store`: construção/carregamento de `FAISS` para contexto local/web.
- `assistants.utils.manager_tools`: decoradores utilitários para debug/retry.
- `assistants.utils.paths`: resolução centralizada de caminhos de dados no repositório.

## Módulos experimentais/legados (arquivados)

- `assistants.utils.archive.vector_store`
- `assistants.utils.archive.data_store_from_web_scraper`

Esses módulos foram movidos para `archive/` e **não** devem ser usados em runtime padrão.
Os arquivos shim em `assistants.utils.vector_store` e
`assistants.utils.data_store_from_web_scraper` emitem aviso e levantam erro para evitar uso acidental.

## Caminhos de dados padronizados

Os caminhos de conhecimento agora são resolvidos por `assistants.utils.paths`, evitando strings hardcoded como `assistant/knowledge/...`.
