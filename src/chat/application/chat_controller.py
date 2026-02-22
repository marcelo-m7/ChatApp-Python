import os
from dataclasses import dataclass

import flet as ft

from chat.application.contracts import AssistantResponderPort, PubSubPort
from chat.chat_app import ChatApp
from chat.entities.message import Message


@dataclass
class ChatViewState:
    user_name: str | None = None
    user_id: str | None = None
    current_room: str | None = None


class ChatController:
    def __init__(
        self,
        page: ft.Page,
        chat_app: ChatApp,
        pubsub: PubSubPort,
        assistant_responder: AssistantResponderPort,
        state: ChatViewState,
        refresh_users_drawer,
        append_chat_control,
        clear_chat_controls,
        focus_message_input,
        update_room_title,
        close_drawer,
        update_page,
        create_chat_message,
    ):
        self.page = page
        self.chat_app = chat_app
        self.pubsub = pubsub
        self.assistant_responder = assistant_responder
        self.state = state
        self.refresh_users_drawer = refresh_users_drawer
        self.append_chat_control = append_chat_control
        self.clear_chat_controls = clear_chat_controls
        self.focus_message_input = focus_message_input
        self.update_room_title = update_room_title
        self.close_drawer = close_drawer
        self.update_page = update_page
        self.create_chat_message = create_chat_message

    def send_message_click(self, new_message: ft.TextField):
        if not new_message.value.strip():
            return

        message = Message(
            user_name=self.state.user_name,
            text=new_message.value,
            message_type="chat_message",
            room_id=self.state.current_room,
        )

        self.chat_app.add_message_to_room(message)
        self.pubsub.send_all(message)
        new_message.value = ""
        self.focus_message_input()
        self.update_page()

    def join_chat_click(self, join_user_name: ft.TextField, welcome_dialog: ft.AlertDialog):
        user_name = join_user_name.value
        user_id = join_user_name.value.strip().lower()

        if not user_name:
            join_user_name.error_text = "O nome não pode estar em branco!"
            join_user_name.update()
            return

        self.page.session.set("user_name", user_name)
        self.page.session.set("user_id", user_id)
        self.page.session.set("current_room", "geral")
        self.state.user_name = self.page.session.get("user_name")
        self.state.user_id = self.page.session.get("user_id")
        self.state.current_room = self.page.session.get("current_room")

        self.chat_app.add_user(user_name=self.state.user_name, user_id=self.state.user_id)
        welcome_dialog.open = False

        for msg in self.chat_app.rooms[self.state.current_room].room.messages:
            self.on_message(msg)

        self.update_page()

        msg = Message(
            user_name=user_name,
            text=f"{user_name} entrou no chat.",
            message_type="login_message",
            room_id=self.state.current_room,
        )
        self.chat_app.add_message_to_room(msg)
        self.pubsub.send_all(msg)

    def change_room_by_id(self, room_id: str):
        self.page.session.set("current_room", room_id)
        self.state.current_room = room_id
        self.update_room_title(self.chat_app.rooms[room_id].room.room_name)
        self.clear_chat_controls()
        for msg in self.chat_app.rooms[room_id].room.messages:
            self.on_message(msg)
        self.close_drawer()
        self.update_page()

    def send_private_message(self, user: str):
        reciver = user.strip().lower()
        owner = self.state.user_id
        private_room_id = str(owner + reciver).lower()

        if private_room_id in self.chat_app.rooms.keys():
            self.change_room_by_id(private_room_id)
            return

        private_room_id2 = str(reciver + owner).lower()
        if private_room_id2 in self.chat_app.rooms.keys():
            self.change_room_by_id(private_room_id2)
            return

        private_room_id = self.chat_app.new_private_room(
            owner=self.state.user_name,
            reciver=user,
            room_id=private_room_id,
        )
        self.change_room_by_id(private_room_id)

    def on_message(self, message: Message):
        if message.room_id != self.page.session.get("current_room"):
            return

        should_render_chat_message = message.message_type == "chat_message"

        if message.message_type == "chat_message":
            control = self.create_chat_message(message)
            self.append_chat_control(control)
            self.update_page()

        elif message.message_type == "login_message":
            self.append_chat_control(
                ft.Text(message.text, italic=True, color=ft.Colors.WHITE, size=12)
            )
            self.refresh_users_drawer()
            self.update_page()
            return

        elif message.message_type == "file_message":
            file_ext = os.path.splitext(message.file.file_path)[1].lower()
            if file_ext in [".png", ".jpg", ".jpeg", ".gif"]:
                control = ft.Column(
                    [
                        ft.Text(f"{message.user_name} compartilhou uma imagem:"),
                        ft.Image(
                            src=message.file.file_path,
                            width=200,
                            height=200,
                            visible=True,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                    ]
                )
            else:
                control = ft.Column(
                    [
                        ft.Text(f"{message.user_name} compartilhou um arquivo:"),
                        ft.ElevatedButton(
                            text=os.path.basename(message.file.file_path),
                            on_click=lambda _: self.page.launch_url(message.file.file_url),
                        ),
                    ]
                )
            self.append_chat_control(control)
            self.update_page()

        assistant_name = getattr(self.assistant_responder, "nome", "").strip().lower()
        should_process_assistant_response = (
            should_render_chat_message
            and message.room_id == "programador"
            and message.message_type not in {"login_message", "file_message"}
            and message.user_name.strip().lower() != assistant_name
        )

        if should_process_assistant_response:
            assistant_response = self.assistant_responder.process_message(message)
            if assistant_response:
                self.append_chat_control(self.create_chat_message(assistant_response))
                self.update_page()
