from __future__ import annotations

from chat.chat_app import ChatApp
from chat.entities.message import Message
from chat.entities.user import User
from chatapp.application.ports import MessageRepository, UserRepository


class InMemoryMessageRepository(MessageRepository):
    def __init__(self, chat_app: ChatApp):
        self.chat_app = chat_app

    def add(self, message: Message) -> None:
        self.chat_app.add_message_to_room(message)

    def list_by_room(self, room_id: str) -> list[Message]:
        return self.chat_app.rooms[room_id].messages


class InMemoryUserRepository(UserRepository):
    def __init__(self, chat_app: ChatApp):
        self.chat_app = chat_app

    def add(self, user: User) -> None:
        self.chat_app.active_users[user.user_id] = user

    def get(self, user_id: str) -> User | None:
        return self.chat_app.active_users.get(user_id)
