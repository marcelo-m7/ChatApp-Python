import os

import flet as ft

from chat.chat_message import ChatMessage
from chat.entities.message import Message
from chat.use_cases.dialogs import NewRoomDialog, WelcomeDialog
from chat.utils.file_handler import FileHandler
from chatapp.application.services import AssistantService, ChatService, FileService
from chatapp.application.upload_service import UploadService


class DrawerView:
    def __init__(self, chat_service: ChatService, on_change_room, on_private, on_new_room):
        self.chat_service = chat_service
        self.on_change_room = on_change_room
        self.on_private = on_private
        self.on_new_room = on_new_room

    def build(self):
        rooms = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE),
                title=ft.Text(room.room_name),
                on_click=lambda _e, room_id=room_id: self.on_change_room(room_id),
            )
            for room_id, room in self.chat_service.chat_app.rooms.items()
        ]
        users = [
            ft.ListTile(
                leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                title=ft.Text(user.user_name),
                on_click=lambda _e, user=user.user_name: self.on_private(user),
            )
            for user in self.chat_service.chat_app.active_users.values()
        ]
        new_room_btn = ft.ElevatedButton(
            text="Nova sala",
            on_click=self.on_new_room,
            icon=ft.Icons.MEETING_ROOM,
            width=130,
        )
        return ft.NavigationDrawer(
            controls=[
                ft.Column([ft.Text("Salas de Chat", size=18, weight="bold"), *rooms], expand=True),
                ft.Column([ft.Divider(), ft.Text("Usuários Online", size=16, weight="bold"), *users]),
                ft.Row([new_room_btn], alignment=ft.MainAxisAlignment.CENTER),
            ]
        )


class InputBar(ft.Row):
    def __init__(self, message_field: ft.TextField, file_handler: FileHandler, send_action):
        super().__init__(
            controls=[
                message_field,
                ft.IconButton(
                    icon=ft.Icons.FILE_UPLOAD,
                    tooltip="Compartilhar arquivo",
                    on_click=lambda _: file_handler.file_picker.pick_files(allow_multiple=True),
                ),
                ft.IconButton(icon=ft.Icons.SEND_ROUNDED, tooltip="Enviar mensagem", on_click=send_action),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        )


class ChatView(ft.Column):
    def __init__(self, room_name: ft.Text, chat_column: ft.Column, input_bar: InputBar):
        super().__init__(controls=[ft.Row([room_name]), chat_column, input_bar], expand=True)


class ChatInterface:
    def __init__(self, page: ft.Page, chat_service: ChatService):
        self.page = page
        self.chat_service = chat_service
        self.assistant_service = AssistantService()
        self.file_service = FileService()
        self.upload_service = UploadService(self.file_service)

        self.current_room = self.page.session.get("current_room") or self.chat_service.chat_app.current_room
        self.welcome_dialog = WelcomeDialog(self.join_chat_click)
        self.new_room_dialog = NewRoomDialog(self.save_new_room)
        self.file_handler = FileHandler(self.page, self.chat_service, self.upload_service)

        self.page.overlay.extend([self.welcome_dialog.dialog, self.new_room_dialog.dialog])
        self.page.pubsub.subscribe(self.on_message)

        self.chat = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.new_message = ft.TextField(expand=True, on_submit=self.send_message_click)
        self.room_name = ft.Text(size=20, weight="bold")
        self._update_room_title()

        self.input_bar = InputBar(self.new_message, self.file_handler, self.send_message_click)
        self.chatbox = ChatView(self.room_name, self.chat, self.input_bar)

        self.page.drawer = DrawerView(
            self.chat_service,
            self.change_room_by_id,
            self.send_private_message,
            self.create_new_room_click,
        ).build()
        self.page.add(self.chatbox)
        self.welcome_dialog.join_user_name.focus()
        self.page.update()

    def _update_room_title(self):
        self.room_name.value = f"Sala: {self.chat_service.chat_app.rooms[self.current_room].room_name}"

    def refresh_drawer(self):
        self.page.drawer = DrawerView(
            self.chat_service,
            self.change_room_by_id,
            self.send_private_message,
            self.create_new_room_click,
        ).build()

    def send_private_message(self, user: str):
        receiver = user.strip().lower()
        owner = self.user_id
        private_room_id = f"{owner}{receiver}".lower()

        if private_room_id not in self.chat_service.chat_app.rooms:
            mirror = f"{receiver}{owner}".lower()
            private_room_id = mirror if mirror in self.chat_service.chat_app.rooms else self.chat_service.create_private_room(
                owner=self.user_name,
                receiver=user,
                room_id=private_room_id,
            )

        self.change_room_by_id(private_room_id)

    def change_room_by_id(self, room_id):
        self.page.session.set("current_room", room_id)
        self.current_room = room_id
        self._update_room_title()
        self.chat.controls.clear()
        for msg in self.chat_service.get_messages(room_id):
            self.on_message(msg)
        self.page.drawer.open = False
        self.page.update()

    def save_new_room(self, _e):
        room_name = self.new_room_dialog.room_name_field.value.strip()
        room_id = self.new_room_dialog.room_id_field.value.strip()
        if not room_name or not room_id:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nome e ID são obrigatórios"), open=True)
            self.page.update()
            return
        self.chat_service.create_room(room_id, room_name)
        self.new_room_dialog.dialog.open = False
        self.refresh_drawer()
        self.page.update()

    def create_new_room_click(self, _e):
        self.new_room_dialog.room_name_field.value = ""
        self.new_room_dialog.room_id_field.value = ""
        self.new_room_dialog.open()
        self.page.update()

    def send_message_click(self, _e):
        if not self.new_message.value.strip():
            return

        message = Message(
            user_name=self.user_name,
            text=self.new_message.value,
            message_type="chat_message",
            room_id=self.current_room,
        )
        self.chat_service.send_message(message)
        self.page.pubsub.send_all(message)
        self.new_message.value = ""
        self.new_message.focus()
        self.page.update()

    def join_chat_click(self, _e):
        user_name = self.welcome_dialog.join_user_name.value
        user_id = user_name.strip().lower()
        if not user_name:
            self.welcome_dialog.join_user_name.error_text = "O nome não pode estar em branco!"
            self.welcome_dialog.join_user_name.update()
            return

        self.page.session.set("user_name", user_name)
        self.page.session.set("user_id", user_id)
        self.page.session.set("current_room", "geral")
        self.user_name = user_name
        self.user_id = user_id
        self.current_room = "geral"

        self.chat_service.join_user(user_name=self.user_name, user_id=self.user_id)
        self.welcome_dialog.dialog.open = False

        for msg in self.chat_service.get_messages(self.current_room):
            self.on_message(msg)

        login_msg = Message(
            user_name=user_name,
            text=f"{user_name} entrou no chat.",
            message_type="login_message",
            room_id=self.current_room,
        )
        self.chat_service.send_message(login_msg)
        self.page.pubsub.send_all(login_msg)
        self.refresh_drawer()
        self.page.update()

    def on_edit(self, chat_message: ChatMessage):
        chat_message.controls[1].controls[1].value = chat_message.message.text

    def on_delete(self, chat_message: ChatMessage):
        self.chat.controls.remove(chat_message)
        self.page.update()

    def on_message(self, message: Message):
        if message.room_id != self.page.session.get("current_room"):
            return

        if message.message_type == "login_message":
            self.chat.controls.append(ft.Text(message.text, italic=True, color=ft.Colors.WHITE, size=12))
            self.refresh_drawer()
            self.page.update()
            return

        if message.message_type == "file_message" and message.file:
            file_ext = os.path.splitext(message.file.file_path)[1].lower()
            if file_ext in [".png", ".jpg", ".jpeg", ".gif"]:
                control = ft.Column([
                    ft.Text(f"{message.user_name} compartilhou uma imagem:"),
                    ft.Image(src=message.file.file_path, width=200, height=200, fit=ft.ImageFit.CONTAIN),
                ])
            else:
                control = ft.Column([
                    ft.Text(f"{message.user_name} compartilhou um arquivo:"),
                    ft.ElevatedButton(
                        text=os.path.basename(message.file.file_path),
                        on_click=lambda _: self.page.launch_url(message.file.file_url),
                    ),
                ])
            self.chat.controls.append(control)
            self.page.update()
            return

        self.chat.controls.append(ChatMessage(message, self.on_edit, self.on_delete))

        assistant_response = self.assistant_service.process(message) if message.room_id == "programador" else None
        if assistant_response:
            self.chat_service.send_message(assistant_response)
            self.chat.controls.append(ChatMessage(assistant_response, self.on_edit, self.on_delete))

        self.page.update()
