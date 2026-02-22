import flet as ft


def build_rooms_controls(rooms, on_change_room):
    return [
        ft.ListTile(
            leading=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE),
            title=ft.Text(value.room.room_name),
            on_click=lambda e, room_id=key: on_change_room(room_id),
        )
        for key, value in rooms.items()
    ]


def build_users_controls(users, on_send_private):
    return [
        ft.ListTile(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
            title=ft.Text(user),
            on_click=lambda e, user=user: on_send_private(user),
        )
        for user in users
    ]


def build_drawer(rooms_controls, users_controls, new_room_btn):
    return ft.NavigationDrawer(
        controls=[
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
            ft.Row([new_room_btn], alignment=ft.MainAxisAlignment.CENTER),
        ]
    )
