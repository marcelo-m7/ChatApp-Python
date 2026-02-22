from __future__ import annotations

import flet as ft
from dotenv import load_dotenv

from chat.chat_app import ChatApp
from chat.chat_interface import ChatInterface
from chatapp.application.services import ChatService
from chatapp.config.settings import settings
from chatapp.infrastructure.auth.github_oauth import GitHubOAuthService

load_dotenv(".env")
chat_app = ChatApp()
chat_service = ChatService(chat_app)


def main(page: ft.Page):
    page.title = "Chat Em Tempo Real - Flet App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    oauth_service = GitHubOAuthService(page)
    buttons = oauth_service.build_buttons()

    def toggle_login_buttons() -> None:
        buttons.login_button.visible = not oauth_service.is_authenticated()
        buttons.logout_button.visible = oauth_service.is_authenticated()

    def start_app():
        page.clean()
        toggle_login_buttons()
        page.add(ft.Row([buttons.login_button, buttons.logout_button], alignment=ft.MainAxisAlignment.END))
        ChatInterface(page, chat_service)

    def on_login(e: ft.LoginEvent):
        if e.error:
            print(f"Error logging in: {e.error}")
        toggle_login_buttons()
        start_app()

    page.on_login = on_login
    page.on_logout = lambda _e: start_app()
    toggle_login_buttons()
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
