import flet as ft

from chatapp.application.services import ChatService
from chatapp.application.upload_service import UploadService
from chatapp.config.settings import settings


class FileHandler:
    def __init__(self, page: ft.Page, chat_service: ChatService, upload_service: UploadService):
        self.page = page
        self.chat_service = chat_service
        self.upload_service = upload_service
        self.file_picker = ft.FilePicker(
            on_result=self.pick_files_result,
            on_upload=self.on_upload_progress,
        )
        self.page.overlay.append(self.file_picker)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return

        for file in e.files:
            try:
                upload_url = self.page.get_upload_url(file.name, 60)
                if not upload_url:
                    raise ValueError(f"Falha ao obter URL de upload para {file.name}")

                self.file_picker.upload([ft.FilePickerUploadFile(file.name, upload_url=upload_url)])
                message = self.upload_service.create_file_message(
                    user_name=self.page.session.get("user_name"),
                    room_id=self.page.session.get("current_room"),
                    file_name=file.name,
                    file_size=file.size,
                    upload_dir=settings.upload_dir,
                    download_url_template=settings.file_server_download_url_template,
                )
                self.chat_service.send_message(message)
                self.page.pubsub.send_all(message)
                self.show_snack(f"Arquivo enviado: {file.name}, Tamanho: {file.size} KBs")
            except ValueError as ex:
                self.show_snack(str(ex))
            except Exception as ex:
                self.show_snack(f"Erro ao enviar arquivo: {str(ex)}")

    def on_upload_progress(self, e: ft.FilePickerUploadEvent):
        self.show_snack(f"Upload {e.file_name}: {e.progress*100:.0f}%")

    def show_snack(self, message: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(message), open=True)
        self.page.update()
