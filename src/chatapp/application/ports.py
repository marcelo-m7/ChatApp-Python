from __future__ import annotations

from abc import ABC, abstractmethod

from chat.entities.message import Message
from chat.entities.user import User


class MessageRepository(ABC):
    @abstractmethod
    def add(self, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_room(self, room_id: str) -> list[Message]:
        raise NotImplementedError


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, user_id: str) -> User | None:
        raise NotImplementedError
