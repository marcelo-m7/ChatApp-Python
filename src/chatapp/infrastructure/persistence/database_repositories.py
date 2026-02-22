from __future__ import annotations

from chat.entities.message import Message
from chat.entities.user import User
from chatapp.application.ports import MessageRepository, UserRepository


class DatabaseMessageRepository(MessageRepository):
    """Placeholder for future DB-backed persistence."""

    def add(self, message: Message) -> None:
        raise NotImplementedError("Implementação de banco será adicionada em uma próxima fase")

    def list_by_room(self, room_id: str) -> list[Message]:
        raise NotImplementedError("Implementação de banco será adicionada em uma próxima fase")


class DatabaseUserRepository(UserRepository):
    """Placeholder for future DB-backed persistence."""

    def add(self, user: User) -> None:
        raise NotImplementedError("Implementação de banco será adicionada em uma próxima fase")

    def get(self, user_id: str) -> User | None:
        raise NotImplementedError("Implementação de banco será adicionada em uma próxima fase")
