from typing import Protocol

from chat.entities.message import Message


class PubSubPort(Protocol):
    def subscribe(self, handler) -> None: ...

    def send_all(self, message: Message) -> None: ...


class AssistantResponderPort(Protocol):
    def process_message(self, message: Message): ...


class FileHandlerPort(Protocol):
    file_picker: object
