from __future__ import annotations

import flet as ft


class ChatTimeline:
    def __init__(self, room_name: str):
        self.chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.chat_room_container = ft.Container(
            content=self.chat,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        )
        self.room_name = ft.Text(f"Sala: {room_name}", size=20, weight="bold")

    def set_room_name(self, room_name: str):
        self.room_name.value = f"Sala: {room_name}"

    def append(self, control):
        self.chat.controls.append(control)

    def clear(self):
        self.chat.controls.clear()

    def remove(self, control):
        self.chat.controls.remove(control)
