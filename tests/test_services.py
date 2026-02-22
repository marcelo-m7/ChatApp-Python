import unittest

from chat.chat_app import ChatApp
from chat.entities.message import Message
from chatapp.application.services import AssistantService, ChatService, FileService, FileUploadInput


class StubAssistant:
    def process_message(self, message):
        if "@programador" in message.text.lower():
            return Message(user_name="Programador", text="ok", message_type="chat_message", room_id=message.room_id)
        return None


class ServicesTest(unittest.TestCase):
    def setUp(self):
        self.chat_service = ChatService(ChatApp())

    def test_chat_service_send_and_get_messages(self):
        message = Message(user_name="alice", text="oi", message_type="chat_message", room_id="geral")
        self.chat_service.send_message(message)
        messages = self.chat_service.get_messages("geral")
        self.assertEqual(1, len(messages))
        self.assertEqual("oi", messages[0].text)

    def test_file_service_metadata(self):
        file = FileService().build_file_metadata(
            FileUploadInput(
                file_name="doc.txt",
                file_size=10,
                upload_dir="uploads/",
                download_url_template="http://localhost/{filename}",
            )
        )
        self.assertEqual("doc.txt", file.file_name)
        self.assertTrue(file.file_url.endswith("doc.txt"))

    def test_assistant_service_only_when_called(self):
        service = AssistantService(assistant=StubAssistant())
        self.assertIsNone(service.process(Message(user_name="u", text="oi", message_type="chat_message", room_id="geral")))
        self.assertIsNotNone(service.process(Message(user_name="u", text="@programador ajuda", message_type="chat_message", room_id="geral")))


if __name__ == "__main__":
    unittest.main()
