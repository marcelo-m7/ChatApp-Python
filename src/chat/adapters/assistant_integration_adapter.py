from __future__ import annotations

from typing import Optional

from assistants.assistants import Assistants
from chat.entities.message import Message
from chat.interfaces import AssistantAdapterProtocol


class AssistantIntegrationAdapter(AssistantAdapterProtocol):
    def __init__(self, room_id: str = "programador", assistant_name: str = "Programador"):
        self.room_id = room_id
        self.assistant = Assistants(nome=assistant_name)

    def should_handle(self, message: Message) -> bool:
        return message.room_id == self.room_id and message.message_type == "chat_message"

    def process_message(self, message: Message) -> Optional[Message]:
        return self.assistant.process_message(message)
