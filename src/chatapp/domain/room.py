from dataclasses import dataclass, field

from chatapp.domain.message import Message


@dataclass
class Room:
    room_id: str
    room_name: str
    owner: str = "system"
    private: bool = False
    messages: list[Message] = field(default_factory=list)
    current_users: list[str] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        if message.room_id and message.room_id != self.room_id:
            raise ValueError("Message room_id does not match room")
        message.room_id = self.room_id
        self.messages.append(message)

    def add_user(self, user_name: str) -> None:
        if user_name not in self.current_users:
            self.current_users.append(user_name)

    def remove_user(self, user_name: str) -> None:
        if user_name in self.current_users:
            self.current_users.remove(user_name)
