# Diagrama de Arquitetura (ASCII)

```text
+-----------------------+        +-------------------------+
|      UI (Flet)        |        |   API Download (FastAPI)|
| chat/chat_interface   |        | chatapp/infrastructure  |
+-----------+-----------+        +------------+------------+
            |                                 |
            | usa serviços                    |
            v                                 v
+-----------------------------------------------+
|              Application Services             |
| chatapp/application/{services,upload_service} |
+----------------------+------------------------+
                       |
                       | opera entidades/regras
                       v
+-----------------------------------------------+
|                    Domain                     |
| chatapp/domain/{message,room,user,file,...}   |
+----------------------+------------------------+
                       |
                       | persistência/integrações
                       v
+-----------------------------------------------+
|                Infrastructure                 |
| repositories, filename_utils, oauth, openai   |
+-----------------------------------------------+
```
