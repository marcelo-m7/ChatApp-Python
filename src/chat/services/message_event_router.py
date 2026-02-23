from __future__ import annotations

from typing import Optional

from chat.entities.message import Message
from chat.interfaces import AssistantAdapterProtocol, MessageRendererProtocol, MessageRouteResult


class MessageEventRouter:
    def __init__(
        self,
        renderer: MessageRendererProtocol,
        assistant_adapter: Optional[AssistantAdapterProtocol] = None,
    ):
        self.renderer = renderer
        self.assistant_adapter = assistant_adapter

    def route(self, message: Message, current_room_id: str) -> MessageRouteResult:
        if message.room_id != current_room_id:
            return MessageRouteResult()

        if message.message_type == "login_message":
            return MessageRouteResult(
                controls=[self.renderer.render_login_message(message)],
                should_update_users=True,
            )

        controls = []
        if message.message_type == "chat_message":
            controls.append(self.renderer.render_chat_message(message))
        elif message.message_type == "file_message":
            controls.append(self.renderer.render_file_message(message))
        else:
            return MessageRouteResult()

        if self.assistant_adapter and self.assistant_adapter.should_handle(message):
            assistant_response = self.assistant_adapter.process_message(message)
            if assistant_response:
                controls.append(self.renderer.render_chat_message(assistant_response))

        return MessageRouteResult(controls=controls)
