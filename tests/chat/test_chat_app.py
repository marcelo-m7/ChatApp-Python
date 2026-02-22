from chat.chat_app import ChatApp
from chat.entities.message import Message


def test_add_message_to_room_persists_message_on_target_room():
    app = ChatApp()
    message = Message(user_name="ana", text="hello", message_type="chat_message", room_id="geral")

    app.add_message_to_room(message)

    assert app.rooms["geral"].room.messages[-1] == message


def test_new_private_room_sets_owner_and_participants():
    app = ChatApp()

    room_id = app.new_private_room(owner="Ana", reciver="Joao", room_id="anajoao")
    users = app.rooms[room_id].get_users()

    assert room_id == "anajoao"
    assert app.rooms[room_id].room.private is True
    assert users == ["Ana", "Joao"]
