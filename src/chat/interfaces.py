from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Protocol

from chat.entities.message import Message


class AssistantAdapterProtocol(Protocol):
    def should_handle(self, message: Message) -> bool:
        ...

    def process_message(self, message: Message) -> Optional[Message]:
        ...


class MessageRendererProtocol(Protocol):
    def render_chat_message(self, message: Message) -> Any:
        ...

    def render_login_message(self, message: Message) -> Any:
        ...

    def render_file_message(self, message: Message) -> Any:
        ...


@dataclass
class MessageRouteResult:
    controls: list[Any] = field(default_factory=list)
    should_update_users: bool = False
