from chat.chat_room import ChatRoom
from chat.entities.message import Message


def test_chat_room_adds_message_only_when_room_matches():
    room = ChatRoom("geral", "Sala Geral")

    valid_message = Message(user_name="ana", text="oi", message_type="chat_message", room_id="geral")
    invalid_message = Message(user_name="ana", text="ops", message_type="chat_message", room_id="casual")

    room.add_message(valid_message)
    room.add_message(invalid_message)

    assert room.get_messages() == [valid_message]


def test_private_chat_room_starts_with_owner_and_accepts_other_user():
    room = ChatRoom("anajoao", "Privada", owner="ana", private=True)

    room.add_user("joao")

    assert room.room.private is True
    assert room.get_users() == ["ana", "joao"]
