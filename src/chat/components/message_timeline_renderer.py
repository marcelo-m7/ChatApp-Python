from __future__ import annotations

import os

import flet as ft

from chat.chat_message import ChatMessage
from chat.entities.message import Message
from chat.interfaces import MessageRendererProtocol


class MessageTimelineRenderer(MessageRendererProtocol):
    def __init__(self, page: ft.Page, on_edit, on_delete):
        self.page = page
        self.on_edit = on_edit
        self.on_delete = on_delete

    def render_chat_message(self, message: Message):
        return ChatMessage(message, self.on_edit, self.on_delete)

    def render_login_message(self, message: Message):
        return ft.Text(message.text, italic=True, color=ft.Colors.WHITE, size=12)

    def render_file_message(self, message: Message):
        file_ext = os.path.splitext(message.file.file_path)[1].lower()
        if file_ext in [".png", ".jpg", ".jpeg", ".gif"]:
            return ft.Column([
                ft.Text(f"{message.user_name} compartilhou uma imagem:"),
                ft.Image(
                    src=message.file.file_path,
                    width=200,
                    height=200,
                    visible=True,
                    fit=ft.ImageFit.CONTAIN,
                ),
            ])

        return ft.Column([
            ft.Text(f"{message.user_name} compartilhou um arquivo:"),
            ft.ElevatedButton(
                text=os.path.basename(message.file.file_path),
                on_click=lambda _: self.page.launch_url(message.file.file_url),
            ),
        ])
