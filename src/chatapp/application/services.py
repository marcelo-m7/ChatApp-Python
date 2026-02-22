"""Application service layer."""

from __future__ import annotations

import os
from dataclasses import dataclass

from assistants.assistants import Assistants
from chat.chat_app import ChatApp
from chat.entities.file import File
from chat.entities.message import Message

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".doc", ".docx", ".txt"}


class ChatService:
    def __init__(self, chat_app: ChatApp):
        self.chat_app = chat_app

    def send_message(self, message: Message) -> Message:
        self.chat_app.add_message_to_room(message)
        return message

    def create_room(self, room_id: str, room_name: str):
        self.chat_app.new_room(room_id, room_name)
        return self.chat_app.rooms[room_id]

    def join_user(self, user_name: str, user_id: str):
        self.chat_app.add_user(user_name=user_name, user_id=user_id)
        return self.chat_app.active_users[user_id]

    def create_private_room(self, owner: str, receiver: str, room_id: str) -> str:
        return self.chat_app.new_private_room(owner=owner, receiver=receiver, room_id=room_id)

    def get_messages(self, room_id: str) -> list[Message]:
        return self.chat_app.rooms[room_id].messages


@dataclass
class FileUploadInput:
    file_name: str
    file_size: int
    upload_dir: str
    download_url_template: str


class FileService:
    def build_file_metadata(self, payload: FileUploadInput) -> File:
        ext = os.path.splitext(payload.file_name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError("Tipo de arquivo não permitido")

        file_path = os.path.join(payload.upload_dir, payload.file_name).replace("\\", "/")
        return File(
            file_url=payload.download_url_template.format(filename=payload.file_name),
            file_name=payload.file_name,
            file_path=file_path,
            file_size=payload.file_size,
        )


class AssistantService:
    def __init__(self, assistant: Assistants | None = None):
        self.assistant = assistant or Assistants()

    def process(self, message: Message) -> Message | None:
        return self.assistant.process_message(message)
