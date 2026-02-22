import pytest

from chat.chat_app import ChatApp
from chat.entities.message import Message
from chat.entities.user import User
from chatapp.infrastructure.filename_utils import normalize_filename
from chatapp.infrastructure.persistence.database_repositories import (
    DatabaseMessageRepository,
    DatabaseUserRepository,
)
from chatapp.infrastructure.persistence.in_memory_repositories import (
    InMemoryMessageRepository,
    InMemoryUserRepository,
)


def test_normalize_filename_decodes_and_strips_path():
    assert normalize_filename("nested%2Ff%20ile.txt") == "f ile.txt"


def test_in_memory_message_repository_add_and_list():
    chat_app = ChatApp()
    repo = InMemoryMessageRepository(chat_app)
    message = Message(user_name="alice", text="oi", message_type="chat_message", room_id="geral")

    repo.add(message)

    assert repo.list_by_room("geral")[0].text == "oi"


def test_in_memory_user_repository_add_and_get():
    chat_app = ChatApp()
    repo = InMemoryUserRepository(chat_app)
    user = User(user_name="alice", user_id="a1", current_room_id="geral")

    repo.add(user)

    assert repo.get("a1") == user
    assert repo.get("missing") is None


def test_database_repository_placeholders_raise():
    msg_repo = DatabaseMessageRepository()
    user_repo = DatabaseUserRepository()

    with pytest.raises(NotImplementedError):
        msg_repo.add(Message(user_name="a", text="t", message_type="chat_message", room_id="geral"))
    with pytest.raises(NotImplementedError):
        msg_repo.list_by_room("geral")
    with pytest.raises(NotImplementedError):
        user_repo.add(User(user_name="a", user_id="1", current_room_id="geral"))
    with pytest.raises(NotImplementedError):
        user_repo.get("1")
