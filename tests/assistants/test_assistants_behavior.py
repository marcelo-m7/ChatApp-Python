import importlib
import sys
import types

from chat.entities.message import Message


class _ProgramadorStub:
    def get_response(self, input, conversation_history):
        return f"echo:{input}|history:{len(conversation_history)}"


class _ChatMessageStub:
    def __init__(self, content, user=None):
        self.content = content
        self.user = user


def test_assistant_processes_only_when_called(monkeypatch):
    fake_programador_module = types.SimpleNamespace(Programador=_ProgramadorStub)
    fake_langchain_schema = types.SimpleNamespace(
        HumanMessage=_ChatMessageStub,
        AIMessage=_ChatMessageStub,
    )

    monkeypatch.setitem(sys.modules, "assistants.programador", fake_programador_module)
    monkeypatch.setitem(sys.modules, "langchain.schema", fake_langchain_schema)

    assistants_module = importlib.import_module("assistants.assistants")
    assistants_module = importlib.reload(assistants_module)
    assistant = assistants_module.Assistants("Programador")

    no_call = Message(user_name="alice", text="oi", message_type="chat_message", room_id="programador")
    assert assistant.process_message(no_call) is None

    with_call = Message(
        user_name="alice",
        text="@Programador pode ajudar?",
        message_type="chat_message",
        room_id="programador",
    )
    response = assistant.process_message(with_call)

    assert response.user_name == "Programador"
    assert response.message_type == "chat_message"
    assert response.text.startswith("echo:@Programador pode ajudar?")
