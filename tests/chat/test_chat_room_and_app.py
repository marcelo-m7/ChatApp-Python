from chat.chat_app import ChatApp
from chat.chat_room import ChatRoom
from chat.entities.message import Message


def test_chat_room_adds_only_messages_for_same_room():
    room = ChatRoom(room_id="geral", room_name="Sala Geral")

    room.add_message(Message(user_name="alice", text="oi", message_type="chat_message", room_id="geral"))
    room.add_message(Message(user_name="bob", text="fora", message_type="chat_message", room_id="casual"))

    messages = room.get_messages()
    assert len(messages) == 1
    assert messages[0].text == "oi"


def test_chat_app_add_message_to_room_appends_message():
    app = ChatApp()
    message = Message(user_name="alice", text="mensagem", message_type="chat_message", room_id="geral")

    app.add_message_to_room(message)

    stored_messages = app.rooms["geral"].room.messages
    assert len(stored_messages) == 1
    assert stored_messages[0] == message


def test_new_private_room_creates_room_with_owner_and_receiver():
    app = ChatApp()

    room_id = app.new_private_room(owner="alice", reciver="bob", room_id="alicebob")

    private_room = app.rooms[room_id].room
    assert private_room.private is True
    assert private_room.owner == "alice"
    assert private_room.current_users == ["alice", "bob"]
    assert private_room.room_name == "Chat Privado entre alice e bob"
