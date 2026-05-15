import flet as ft

from assistants.assistants import Assistants
from chat.application.chat_controller import ChatController, ChatViewState
from chat.chat_app import ChatApp
from chat.chat_message import ChatMessage
from chat.entities.message import Message
from chat.ui.chat_room import build_chat_room
from chat.ui.drawer import build_drawer, build_rooms_controls, build_users_controls
from chat.ui.input_bar import ALLOWED_UPLOAD_EXTENSIONS, build_input_bar
from chat.use_cases.dialogs import NewRoomDialog, WelcomeDialog
from chat.utils.file_handler import FileHandler


class ChatInterface:
    def __init__(self, page: ft.Page, chat_app: ChatApp, assistant_responder=None, file_handler_factory=None):
        self.page = page
        self.chat_app = chat_app
        self.page.title = "Chat em Tempo Real"

        self.state = ChatViewState(current_room=self.page.session.get("current_room") or self.chat_app.current_room)
        self.assistant_responder = assistant_responder or Assistants(nome="Programador")

        self.welcome_dialog = WelcomeDialog(self._join_chat_click)
        self.new_room_dialog = NewRoomDialog(self.save_new_room)

        file_handler_factory = file_handler_factory or (
            lambda page, chat_app, on_message: FileHandler(page, chat_app, on_message)
        )
        self.file_handler = file_handler_factory(self.page, self.chat_app, self._on_message)

        self.controller = ChatController(
            page=self.page,
            chat_app=self.chat_app,
            pubsub=self.page.pubsub,
            assistant_responder=self.assistant_responder,
            state=self.state,
            refresh_users_drawer=self.update_users_drawer,
            append_chat_control=lambda control: self.chat.controls.append(control),
            clear_chat_controls=lambda: self.chat.controls.clear(),
            focus_message_input=lambda: self.new_message.focus(),
            update_room_title=lambda room: setattr(self.room_name, "value", f"Sala: {room}"),
            close_drawer=lambda: setattr(self.page.drawer, "open", False),
            update_page=self.page.update,
            create_chat_message=lambda message: ChatMessage(message, self.on_edit, self.on_delete),
        )

        self.page.overlay.append(self.welcome_dialog.dialog)
        self.page.overlay.append(self.new_room_dialog.dialog)
        self.page.pubsub.subscribe(self._on_message)

        self.__create_menu_drawer()
        self.__create_chatbox()

        self.welcome_dialog.join_user_name.focus()
        self.page.update()

    def __create_menu_drawer(self):
        self.new_room_btn = ft.ElevatedButton(
            text="Nova sala",
            on_click=self.create_new_room_click,
            icon=ft.Icons.MEETING_ROOM,
            width=130,
        )
        rooms_controls = build_rooms_controls(self.chat_app.rooms, self.controller.change_room_by_id)
        current_users = [user.user_name for user in self.chat_app.active_users.values()]
        users_controls = build_users_controls(current_users, self.controller.send_private_message)
        self.menu_drawer = build_drawer(rooms_controls, users_controls, self.new_room_btn)
        self.page.drawer = self.menu_drawer
        self.menu_button = ft.IconButton(
            icon=ft.Icons.MENU,
            tooltip="Abrir menu",
            on_click=lambda _: self.open_drawer(),
        )

    def update_users_drawer(self):
        current_users = [user.user_name for user in self.chat_app.active_users.values()]
        users_controls = build_users_controls(current_users, self.controller.send_private_message)
        self.menu_drawer.controls[-2] = ft.Column(
            controls=[
                ft.Divider(),
                ft.Text("Usuários Online", size=16, weight="bold", text_align="center"),
                *users_controls,
            ],
            alignment=ft.MainAxisAlignment.END,
        )
        self.page.update()

    def open_drawer(self):
        self.page.drawer.open = True
        self.page.update()

    def __create_chatbox(self):
        self.chat, self.chat_room_container, self.room_name = build_chat_room(
            self.chat_app.rooms[self.state.current_room].room.room_name
        )

        self.new_message, _, self.user_formulary_container = build_input_bar(
            on_submit=self._send_message_click,
            on_upload_click=self._upload_files_click,
        )

        self.chatbox = ft.Column(
            controls=[
                ft.Row([self.menu_button, self.room_name], alignment=ft.MainAxisAlignment.START),
                self.chat_room_container,
                self.user_formulary_container,
            ],
            expand=True,
        )
        self.page.add(self.chatbox)

    def _upload_files_click(self, _):
        self.file_handler.file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=ALLOWED_UPLOAD_EXTENSIONS,
        )

    def save_new_room(self, e):
        room_name = self.new_room_dialog.room_name_field.value.strip()
        room_id = self.new_room_dialog.room_id_field.value.strip()
        if not room_name:
            self.new_room_dialog.room_name_field.error_text = "O nome não pode estar em branco!"
            self.page.update()
            return
        if not room_id:
            self.new_room_dialog.room_id_field.error_text = "O ID não pode estar em branco!"
            self.page.update()
            return

        self.chat_app.new_room(room_id, room_name)
        self.new_room_dialog.dialog.open = False
        self.__create_menu_drawer()
        self.page.update()

    def create_new_room_click(self, e):
        self.new_room_dialog.room_name_field.value = ""
        self.new_room_dialog.room_id_field.value = ""
        self.new_room_dialog.open()
        self.page.update()

    def _send_message_click(self, e):
        self.controller.send_message_click(self.new_message)

    def _join_chat_click(self, e):
        self.controller.join_chat_click(self.welcome_dialog.join_user_name, self.welcome_dialog.dialog)

    def _on_message(self, message: Message):
        self.controller.on_message(message)

    def on_edit(self, chat_message: ChatMessage):
        def save_edit(e):
            chat_message.message.text = edit_field.value
            chat_message.controls[1].controls[1].value = chat_message.message.text
            chat_message.controls[1].controls[1].update()
            chat_message.update()
            edit_dlg.open = False
            self.page.update()

        edit_field = ft.TextField(value=chat_message.message.text)
        edit_dlg = ft.AlertDialog(
            title=ft.Text("Editar Mensagem"),
            content=edit_field,
            actions=[
                ft.ElevatedButton(text="Salvar", on_click=save_edit),
                ft.ElevatedButton(text="Cancelar", on_click=lambda e: setattr(edit_dlg, "open", False) or self.page.update()),
            ],
        )
        self.page.overlay.append(edit_dlg)
        edit_dlg.open = True
        self.page.update()

    def on_delete(self, chat_message: ChatMessage):
        self.chat.controls.remove(chat_message)
        self.page.update()
