import pytest

from chatapp.domain.file import File
from chatapp.domain.file_rules import (
    get_extension,
    is_image_file,
    validate_allowed_extension,
)
from chatapp.domain.message import Message
from chatapp.domain.room import Room
from chatapp.domain.user import User


def test_message_is_file_when_file_instance_present():
    message = Message(
        user_name="alice",
        text="arquivo",
        message_type="chat_message",
        file=File(file_name="a.txt"),
    )

    assert message.is_file() is True


def test_message_is_file_for_file_message_type_without_payload():
    message = Message(user_name="alice", text="arquivo", message_type="file_message")
    assert message.is_file() is True


def test_room_add_message_sets_room_id():
    room = Room(room_id="geral", room_name="Sala Geral")
    message = Message(user_name="alice", text="oi", message_type="chat_message")

    room.add_message(message)

    assert message.room_id == "geral"
    assert len(room.messages) == 1


def test_room_add_message_raises_on_different_room_id():
    room = Room(room_id="geral", room_name="Sala Geral")
    message = Message(
        user_name="alice",
        text="oi",
        message_type="chat_message",
        room_id="outra",
    )

    with pytest.raises(ValueError, match="does not match"):
        room.add_message(message)


def test_room_add_and_remove_users_without_duplication():
    room = Room(room_id="geral", room_name="Sala Geral")

    room.add_user("alice")
    room.add_user("alice")
    room.remove_user("alice")

    assert room.current_users == []


def test_user_defaults_private_rooms():
    user = User(user_name="alice", user_id="a1", current_room_id="geral")
    assert user.private_rooms == []


def test_file_rules_validate_extensions_and_image_classification():
    assert get_extension("foto.PNG") == ".png"
    assert is_image_file("foto.png") is True
    assert is_image_file("arquivo.pdf") is False

    validate_allowed_extension("doc.txt")
    with pytest.raises(ValueError):
        validate_allowed_extension("malware.exe")
