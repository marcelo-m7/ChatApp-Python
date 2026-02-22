import os

import flet as ft
from dotenv import load_dotenv

from assistants.assistants import Assistants
from chat.auth import AuthManager
from chat.chat_app import ChatApp
from chat.chat_interface import ChatInterface
from chat.utils.file_handler import FileHandler

load_dotenv(".env")
chat_app = ChatApp()


def main(page: ft.Page):
    page.title = "Chat Em Tempo Real - Flet App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    auth_manager = AuthManager(page)

    def start_app():
        page.clean()
        ChatInterface(
            page,
            chat_app,
            assistant_responder=Assistants(nome="Programador"),
            file_handler_factory=lambda page, chat_app, on_message: FileHandler(page, chat_app, on_message),
        )

    def on_login(e: ft.LoginEvent):
        if not e.error:
            auth_manager.toggle_login_buttons()
            start_app()
        else:
            print(f"Error logging in: {e.error}")
            start_app()

    start_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8550))
    host = os.getenv("HOST", "localhost")

    ft.app(
        main,
        port=port,
        view=ft.AppView.WEB_BROWSER,
        upload_dir="uploads/",
        host=host,
        assets_dir="assets",
    )
