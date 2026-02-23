import flet as ft

from chat.adapters.assistant_integration_adapter import AssistantIntegrationAdapter
from chat.chat_app import ChatApp
from chat.chat_message import ChatMessage
from chat.components.chat_drawer import ChatDrawer
from chat.components.chat_timeline import ChatTimeline
from chat.components.message_timeline_renderer import MessageTimelineRenderer
from chat.entities.message import Message
from chat.services.message_event_router import MessageEventRouter
from chat.use_cases.dialogs import NewRoomDialog, WelcomeDialog
from chat.utils.file_handler import FileHandler


class ChatInterface:
    def __init__(self, page: ft.Page, chat_app: ChatApp):
        self.page = page
        self.chat_app = chat_app
        self.page.title = "Chat em Tempo Real"
        self.user_name: str
        self.current_room = self.page.session.get("current_room") or self.chat_app.current_room

        self.welcome_dialog = WelcomeDialog(self.join_chat_click)
        self.new_room_dialog = NewRoomDialog(self.save_new_room)
        self.file_handler = FileHandler(self.page, self.chat_app, self.on_message)

        self.page.overlay.append(self.welcome_dialog.dialog)
        self.page.overlay.append(self.new_room_dialog.dialog)

        self.page.pubsub.subscribe(self.on_message)

        self.drawer = ChatDrawer(
            page=self.page,
            on_change_room=self.change_room_by_id,
            on_send_private_message=self.send_private_message,
            on_new_room_click=self.create_new_room_click,
        )
        self.drawer.build(self.chat_app.rooms, self.chat_app.active_users)

        initial_room_name = self.chat_app.rooms[self.current_room].room.room_name
        self.timeline = ChatTimeline(room_name=initial_room_name)

        self.message_router = MessageEventRouter(
            renderer=MessageTimelineRenderer(
                page=self.page,
                on_edit=self.on_edit,
                on_delete=self.on_delete,
            ),
            assistant_adapter=AssistantIntegrationAdapter(),
        )

        self.__create_user_formulary()
        self.__create_chatbox()

        self.welcome_dialog.join_user_name.focus()
        self.page.update()

    def __create_chatbox(self):
        self.chatbox = ft.Column(
            controls=[
                ft.Row([self.drawer.menu_button, self.timeline.room_name], alignment=ft.MainAxisAlignment.START),
                self.timeline.chat_room_container,
                self.user_formulary_container,
            ],
            expand=True,
        )
        self.page.add(self.chatbox)

    def __create_user_formulary(self):
        self.new_message = ft.TextField(
            hint_text="Escreva uma mensagem...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=self.send_message_click,
            border_radius=5,
        )
        self.input_bar = ft.Row(
            controls=[
                self.new_message,
                ft.IconButton(
                    icon=ft.Icons.FILE_UPLOAD,
                    tooltip="Compartilhar arquivo",
                    on_click=lambda _: self.file_handler.file_picker.pick_files(
                        allow_multiple=True,
                        allowed_extensions=["png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"],
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip="Enviar mensagem",
                    on_click=self.send_message_click,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        )
        self.user_formulary_container = ft.Container(
            content=self.input_bar,
            padding=10,
            border_radius=5,
            alignment=ft.alignment.bottom_center,
        )

    def update_users_drawer(self):
        self.drawer.update_users(self.chat_app.active_users)
        self.page.update()

    def send_private_message(self, user: str):
        print("Enviando mensagem privada para: ", user)
        reciver = user.strip().lower()
        owner = self.user_id
        private_room_id = str(owner + reciver).lower()

        if private_room_id in self.chat_app.rooms.keys():
            self.change_room_by_id(private_room_id)
            return

        private_room_id2 = str(reciver + owner).lower()
        if private_room_id2 in self.chat_app.rooms.keys():
            self.change_room_by_id(private_room_id2)
            return

        private_room_id = self.chat_app.new_private_room(owner=self.user_name, reciver=user, room_id=private_room_id)
        self.change_room_by_id(private_room_id)

    def change_room_by_id(self, room_id):
        print(f"Changing room to: {room_id}")
        self.page.session.set("current_room", room_id)
        self.current_room = room_id
        self.timeline.set_room_name(self.chat_app.rooms[room_id].room.room_name)
        self.timeline.clear()
        for msg in self.chat_app.rooms[room_id].room.messages:
            self.on_message(msg)
        self.page.drawer.open = False
        self.page.update()

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
        self.drawer.build(self.chat_app.rooms, self.chat_app.active_users)
        self.page.update()

    def create_new_room_click(self, e):
        self.new_room_dialog.room_name_field.value = ""
        self.new_room_dialog.room_id_field.value = ""
        self.new_room_dialog.open()
        self.page.update()

    def send_message_click(self, e):
        if self.new_message.value.strip():
            message = Message(
                user_name=self.user_name,
                text=self.new_message.value,
                message_type="chat_message",
                room_id=self.current_room,
            )

            self.chat_app.add_message_to_room(message)
            self.page.pubsub.send_all(message)

            self.new_message.value = ""
            self.new_message.focus()
            self.page.update()

    def join_chat_click(self, e):
        user_name = self.welcome_dialog.join_user_name.value
        user_id = self.welcome_dialog.join_user_name.value.strip().lower()

        if not user_name:
            self.welcome_dialog.join_user_name.error_text = "O nome não pode estar em branco!"
            self.welcome_dialog.join_user_name.update()
        else:
            self.page.session.set("user_name", user_name)
            self.page.session.set("user_id", user_id)
            self.page.session.set("current_room", "geral")
            self.user_name = self.page.session.get("user_name")
            self.user_id = self.page.session.get("user_id")
            self.current_room = self.page.session.get("current_room")

            self.chat_app.add_user(user_name=self.user_name, user_id=self.user_id)
            self.welcome_dialog.dialog.open = False

            for msg in self.chat_app.rooms[self.current_room].room.messages:
                self.on_message(msg)

            self.page.update()

            msg = Message(
                user_name=user_name,
                text=f"{user_name} entrou no chat.",
                message_type="login_message",
                room_id=self.current_room,
            )

            self.chat_app.add_message_to_room(msg)
            self.page.pubsub.send_all(msg)

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
        self.timeline.remove(chat_message)
        self.page.update()

    def on_message(self, message: Message):
        result = self.message_router.route(
            message=message,
            current_room_id=self.page.session.get("current_room"),
        )

        if not result.controls:
            return

        for control in result.controls:
            self.timeline.append(control)

        if result.should_update_users:
            self.update_users_drawer()
            return

        self.page.update()
