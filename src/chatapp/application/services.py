"""Application service layer wrappers."""

from __future__ import annotations

from assistants.assistants import Assistants
from chat.chat_app import ChatApp
from chat.entities.message import Message


class ChatService:
    def __init__(self, chat_app: ChatApp):
        self.chat_app = chat_app

    def add_message(self, room_id: str, message: Message) -> None:
        self.chat_app.add_message_to_room(room_id, message)


class RoomService:
    def __init__(self, chat_app: ChatApp):
        self.chat_app = chat_app

    def create_room(self, room_name: str, room_type: str):
        return self.chat_app.create_room(room_name, room_type)


class AssistantService:
    def __init__(self):
        self.assistant = Assistants()

    def process(self, prompt: str, conversation_history: str):
        return self.assistant.process_message(prompt, conversation_history)
