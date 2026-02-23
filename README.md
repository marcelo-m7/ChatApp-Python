# Chat em Tempo Real com Flet e OpenAI

## Sobre o Projeto
Este projeto é um chat em tempo real desenvolvido em Python utilizando a biblioteca [Flet](https://flet.dev/). Ele permite que os usuários:
- Criem salas de conversa
- Compartilhem arquivos
- Enviem mensagens privadas
- Interajam com um assistente virtual da OpenAI na sala "Bate-papo com Assistente", mencionando `@programador` na mensagem

---

## Dependências (fonte oficial) e travamento de versões
A **única fonte de verdade** das dependências diretas do projeto é o arquivo `pyproject.toml` na seção `[project.dependencies]`.

### Fluxo oficial
1. **Edite dependências diretas** em `pyproject.toml`.
2. **Regenere o lock de runtime** em `requirements.txt` com:

```bash
uv pip compile pyproject.toml --python-version 3.10 --no-header -o requirements.txt
```

3. **Sincronize o ambiente local** com as versões travadas:

```bash
pip install -r requirements.txt
```

> O arquivo `requirements.txt` é gerado automaticamente a partir do `pyproject.toml` e não deve ser alterado manualmente.

## Como Executar
### Iniciar o Chat
Para iniciar a interface do chat, execute o seguinte comando:
```bash
python src/main.py
```

### Iniciar o Servidor
O servidor precisa ser executado para gerenciar o compartilhamento de arquivos. Para isso, rode:
```bash
python server.py
```

Isso disponibilizará os arquivos compartilhados no chat através de um endpoint de API feita com FastAPI.

## Funcionalidades Principais
- **OAuth 2.0**: Para entrar na app, o usuário deve se conectar com uma conta GitHub.
- **Criação de Salas**: Os usuários podem criar salas personalizadas para conversas específicas.
- **Compartilhamento de Arquivos**: Suporte para o envio de imagens, documentos e outros formatos. Os ficheiro são salvos na pasta `src/uploads`
- **Assistente Virtual**: Na sala "Bate-papo com Assistente", qualquer mensagem que inclua `@programador` será processada por uma API da OpenAI e receberá uma resposta automática.
- **Persistência do histórico entre novas sessões**: O projeto base foi rearquitetado de maneira que haja um objeto que persiste os dados do aplicativo em execução.
- **Responsatividade da página**: O layout foi configurado de modo a ser responsivo para mobile.
- **Chat Privado**: Envio de mensagens privadas.
- **Páginas dinâmicas**: As diferentes sesssões são atualizadas conforme novos usuários entram ou criam novas salas.

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto
- **Flet**: Framework para construção da interface gráfica
- **Uvicorn**: Servidor ASGI para disponibilizar os arquivos compartilhados
- **OpenAI API**: Para responder mensagens com o assistente virtual
