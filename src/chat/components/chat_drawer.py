from __future__ import annotations

import flet as ft


class ChatDrawer:
    def __init__(self, page: ft.Page, on_change_room, on_send_private_message, on_new_room_click):
        self.page = page
        self._on_change_room = on_change_room
        self._on_send_private_message = on_send_private_message
        self._on_new_room_click = on_new_room_click
        self.new_room_btn = ft.ElevatedButton(
            text="Nova sala",
            on_click=self._on_new_room_click,
            icon=ft.Icons.MEETING_ROOM,
            width=130,
        )
        self.drawer = ft.NavigationDrawer(controls=[])
        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Abrir menu",
            on_click=lambda _: self.open(),
        )

    def build(self, rooms: dict, active_users: dict):
        rooms_controls = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE),
                title=ft.Text(value.room.room_name),
                on_click=lambda e, room_id=key: self._on_change_room(room_id),
            )
            for key, value in rooms.items()
        ]

        users_controls = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                title=ft.Text(user.user_name),
                on_click=lambda e, name=user.user_name: self._on_send_private_message(name),
            )
            for user in active_users.values()
        ]

        self.drawer.controls = [
            ft.Column(
                controls=[
                    ft.Container(height=12),
                    ft.Text("Salas de Chat", size=18, weight="bold", text_align="center"),
                    ft.Divider(),
                    *rooms_controls,
                ],
                expand=True,
            ),
            ft.Column(
                controls=[
                    ft.Divider(),
                    ft.Text("Usuários Online", size=16, weight="bold", text_align="center"),
                    *users_controls,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row([self.new_room_btn], alignment=ft.MainAxisAlignment.CENTER),
        ]

        self.page.drawer = self.drawer

    def update_users(self, active_users: dict):
        users_controls = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                title=ft.Text(user.user_name),
                on_click=lambda e, name=user.user_name: self._on_send_private_message(name),
            )
            for user in active_users.values()
        ]
        self.drawer.controls[-2] = ft.Column(
            controls=[
                ft.Divider(),
                ft.Text("Usuários Online", size=16, weight="bold", text_align="center"),
                *users_controls,
            ],
            alignment=ft.MainAxisAlignment.END,
        )

    def open(self):
        self.page.drawer.open = True
        self.page.update()
