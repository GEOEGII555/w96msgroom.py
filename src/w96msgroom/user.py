class User:
    """
    Represents a user.
    If a user_id of one user is the same as the user_id of another user, both users are the same.
    Note that if one user joins from 2 accounts at the same time (basically opening 2 browser tabs), they will have the same user ID, only the session ID will be different.
    Also note that if you store an old message, the User object in there might be out of sync! The user might've left or changed their username.
    If you want to check if a user still exists, use Client.is_online(user: User), Client.get_user_by_username(username: str) and Client.get_user(user_id: str).
    """

    flags: list[str]
    session_id: str
    username: str
    user_id: str
    color: str

    def __init__(self, username: str, user_id: str, session_id: str, color: str, flags: list[str]) -> None:
        self.session_id = session_id
        self.username = username
        self.user_id = user_id
        self.color = color
        self.flags = flags

    def __eq__(self, other: object) -> bool:
        if not isinstance(object, User):
            return False
        return self.session_id == other.session_id

    def is_staff(self) -> bool:
        """
        Check if a user is a staff member.
        """
        return 'staff' in self.flags