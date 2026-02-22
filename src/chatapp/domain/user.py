from dataclasses import dataclass, field


@dataclass
class User:
    user_name: str
    user_id: str
    current_room_id: str
    private_rooms: list[str] = field(default_factory=list)
