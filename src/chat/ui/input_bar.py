import flet as ft


ALLOWED_UPLOAD_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"]


def build_input_bar(on_submit, on_upload_click):
    new_message = ft.TextField(
        hint_text="Escreva uma mensagem...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=on_submit,
        border_radius=5,
    )

    input_bar = ft.Row(
        controls=[
            new_message,
            ft.IconButton(
                icon=ft.Icons.FILE_UPLOAD,
                tooltip="Compartilhar arquivo",
                on_click=on_upload_click,
            ),
            ft.IconButton(
                icon=ft.Icons.SEND_ROUNDED,
                tooltip="Enviar mensagem",
                on_click=on_submit,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=10,
    )

    container = ft.Container(
        content=input_bar,
        padding=10,
        border_radius=5,
        alignment=ft.alignment.bottom_center,
    )
    return new_message, input_bar, container
