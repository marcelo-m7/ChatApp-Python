from dataclasses import dataclass
from typing import Optional

from chatapp.domain.file import File


@dataclass
class Message:
    user_name: str
    text: str
    message_type: str
    room_id: Optional[str] = None
    to_user: Optional[str] = None
    file: Optional[File] = None

    def is_file(self) -> bool:
        return self.file is not None or self.message_type == "file_message"
