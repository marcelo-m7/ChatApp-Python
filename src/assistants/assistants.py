from assistants.programador import Programador
from chat.entities.message import Message
from langchain.schema import AIMessage, HumanMessage


class Assistants:
    def __init__(self, nome: str = "Programador"):
        self.nome = nome
        self.specialist = Programador() if nome == "Programador" else None
        self.call = f"@{self.nome}".lower()
        self.chat_history = []

    def should_respond(self, message: Message) -> bool:
        return self.call in message.text.lower()

    def process_message(self, message: Message):
        self.chat_history.append(HumanMessage(content=message.text, user=message.user_name))
        if not self.should_respond(message):
            return None

        response = self.specialist.get_response(
            input=message.text,
            conversation_history=self.chat_history,
        )
        self.chat_history.append(AIMessage(content=response))
        return Message(user_name=self.nome, text=response, message_type="chat_message", room_id=message.room_id)
