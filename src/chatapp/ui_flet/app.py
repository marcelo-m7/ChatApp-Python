from __future__ import annotations

import flet as ft
from dotenv import load_dotenv

from chat.auth import AuthManager
from chat.chat_app import ChatApp
from chat.chat_interface import ChatInterface
from chatapp.application.services import ChatService
from chatapp.config.settings import settings

load_dotenv(".env")
chat_app = ChatApp()
chat_service = ChatService(chat_app)


def main(page: ft.Page):
    page.title = "Chat Em Tempo Real - Flet App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    auth_manager = AuthManager(page)

    def start_app():
        page.clean()
        ChatInterface(page, chat_service)

    def on_login(e: ft.LoginEvent):
        if not e.error:
            auth_manager.toggle_login_buttons()
            start_app()
        else:
            print(f"Error logging in: {e.error}")
            start_app()

    _ = on_login
    start_app()


def run() -> None:
    ft.app(
        main,
        port=settings.port,
        view=ft.AppView.WEB_BROWSER,
        upload_dir=settings.upload_dir,
        host=settings.host,
        assets_dir=settings.assets_dir,
    )
