import os

from chat.entities.message import Message
from chat.entities.room import Room
from chat.entities.user import User


class ChatApp:
    def __init__(self):
        self.rooms: dict[str, Room] = {
            "geral": Room("geral", "Sala Geral"),
            "casual": Room("casual", "Bate-papo Casual"),
            "estudos": Room("estudos", "Sala de Estudos"),
            "programador": Room("programador", "Bate-papo com Assistente"),
        }
        self.active_users: dict[str, User] = {}
        self.current_room = "geral"
        self.upload_dir = "uploads/"
        self.download_url = "http://127.0.0.1:3000/download/{filename}"
        os.makedirs(self.upload_dir, exist_ok=True)

    def add_user(self, user_name: str, user_id: str):
        self.active_users[user_id] = User(
            user_name=user_name,
            user_id=user_id,
            current_room_id="geral",
        )

    def new_room(self, room_id: str, room_name: str):
        self.rooms[room_id] = Room(room_id=room_id, room_name=room_name)

    def new_private_room(self, owner: str, receiver: str, room_id: str):
        room_name = f"Chat Privado entre {owner} e {receiver}"
        room = Room(room_id=room_id, room_name=room_name, owner=owner, private=True)
        room.add_user(owner)
        room.add_user(receiver)
        self.rooms[room_id] = room
        return room_id

    def add_message_to_room(self, message: Message):
        self.rooms[message.room_id].add_message(message)
