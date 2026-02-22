from chat.entities.message import Message
from chatapp.application.services import FileService, FileUploadInput


class UploadService:
    def __init__(self, file_service: FileService):
        self.file_service = file_service

    def create_file_message(
        self,
        *,
        user_name: str,
        room_id: str,
        file_name: str,
        file_size: int,
        upload_dir: str,
        download_url_template: str,
    ) -> Message:
        file = self.file_service.build_file_metadata(
            FileUploadInput(
                file_name=file_name,
                file_size=file_size,
                upload_dir=upload_dir,
                download_url_template=download_url_template,
            )
        )
        return Message(
            user_name=user_name,
            text=f"Arquivo compartilhado: {file_name}",
            message_type="file_message",
            room_id=room_id,
            file=file,
        )
