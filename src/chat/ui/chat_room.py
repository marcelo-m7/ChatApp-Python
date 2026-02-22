import flet as ft


def build_chat_room(room_label: str):
    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    container = ft.Container(
        content=chat,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=5,
        padding=10,
        expand=True,
    )
    room_name = ft.Text(f"Sala: {room_label}", size=20, weight="bold")
    return chat, container, room_name
