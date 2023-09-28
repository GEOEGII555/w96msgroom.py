from .user import User

class Message:
    """
    Represents a message.
    This class contains the message content and the user who sent it.
    Note that the user property might be out of sync. The user could leave or change their username to be something different.
    User IDs don't change, those are attached to the IP of the user.
    """
    timestamp: int
    content: str
    user: User

    def __init__(self, user: str, content: str, timestamp: str) -> None:
        self.user = user
        self.content = content
        self.timestamp = timestamp
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Message):
            return False
        if self.user != other.user:
            return False
        if self.content != other.content:
            return False
        if self.timestamp != other.timestamp:
            return False
        return True