from __future__ import annotations

from dataclasses import dataclass

import flet as ft
from flet.auth.providers import GitHubOAuthProvider

from chatapp.config.settings import settings


@dataclass
class OAuthButtons:
    login_button: ft.ElevatedButton
    logout_button: ft.ElevatedButton


class GitHubOAuthService:
    def __init__(self, page: ft.Page):
        self.page = page
        self.provider = GitHubOAuthProvider(
            client_id=settings.github_client_id,
            client_secret=settings.github_client_secret,
            redirect_url=settings.github_redirect_url,
        )

    def login(self) -> None:
        self.page.login(self.provider, scope=["public_repo"])

    def logout(self) -> None:
        self.page.logout()

    def is_authenticated(self) -> bool:
        return self.page.auth is not None

    def build_buttons(self) -> OAuthButtons:
        login_button = ft.ElevatedButton("Login with GitHub", on_click=lambda _e: self.login())
        logout_button = ft.ElevatedButton("Logout", on_click=lambda _e: self.logout())
        return OAuthButtons(login_button=login_button, logout_button=logout_button)
