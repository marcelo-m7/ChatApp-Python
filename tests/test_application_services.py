from chat.chat_app import ChatApp
from chat.entities.message import Message
from chatapp.application.services import AssistantService, ChatService, FileService, FileUploadInput
from chatapp.application.upload_service import UploadService


class StubAssistant:
    nome = "Programador"

    def process_message(self, message):
        if "@programador" in message.text.lower():
            return Message(
                user_name="Programador",
                text="ok",
                message_type="chat_message",
                room_id=message.room_id,
            )
        return None


def test_chat_service_send_and_get_messages():
    service = ChatService(ChatApp())
    message = Message(user_name="alice", text="oi", message_type="chat_message", room_id="geral")

    service.send_message(message)

    messages = service.get_messages("geral")
    assert len(messages) == 1
    assert messages[0].text == "oi"


def test_chat_service_creates_room_and_private_room():
    service = ChatService(ChatApp())

    room = service.create_room("arquitetura", "Arquitetura")
    private_room_id = service.create_private_room(owner="alice", receiver="bob", room_id="alicebob")

    assert room.room_id == "arquitetura"
    assert private_room_id == "alicebob"
    assert service.chat_app.rooms[private_room_id].private is True


def test_chat_service_join_user_persists_user_in_repository():
    service = ChatService(ChatApp())

    user = service.join_user(user_name="alice", user_id="a1")

    assert user is not None
    assert user.user_name == "alice"
    assert service.chat_app.active_users["a1"].current_room_id == "geral"


def test_file_service_builds_metadata_for_allowed_extension(tmp_path):
    file = FileService().build_file_metadata(
        FileUploadInput(
            file_name="doc.txt",
            file_size=10,
            upload_dir=str(tmp_path),
            download_url_template="http://localhost/download/{filename}",
        )
    )

    assert file.file_name == "doc.txt"
    assert file.file_url == "http://localhost/download/doc.txt"
    assert file.file_path.endswith("doc.txt")


def test_file_service_rejects_disallowed_extension(tmp_path):
    payload = FileUploadInput(
        file_name="script.exe",
        file_size=20,
        upload_dir=str(tmp_path),
        download_url_template="http://localhost/download/{filename}",
    )

    try:
        FileService().build_file_metadata(payload)
        assert False, "Era esperado ValueError para extensão inválida"
    except ValueError as exc:
        assert "não permitido" in str(exc)


def test_upload_service_creates_file_message(tmp_path):
    upload = UploadService(FileService())

    message = upload.create_file_message(
        user_name="alice",
        room_id="geral",
        file_name="manual.pdf",
        file_size=123,
        upload_dir=str(tmp_path),
        download_url_template="http://localhost/download/{filename}",
    )

    assert message.message_type == "file_message"
    assert message.file is not None
    assert message.file.file_name == "manual.pdf"


def test_assistant_service_only_returns_when_mentioned():
    service = AssistantService(assistant=StubAssistant())

    no_reply = service.process(
        Message(user_name="u", text="oi", message_type="chat_message", room_id="geral")
    )
    reply = service.process(
        Message(
            user_name="u",
            text="@programador ajuda",
            message_type="chat_message",
            room_id="geral",
        )
    )

    assert no_reply is None
    assert reply is not None
    assert reply.user_name == "Programador"
