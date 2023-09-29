import socketio
from . import constants
from .user import User

class Client:
    sio: socketio.Client
    online_users: list[User]
    session_id: str
    username: str
    user_id: str

    def __init__(self, username: str) -> None:
        self.sio = socketio.Client()
        self.username = username
        self.online_users = []
        self.session_id = ""
        self.user_id = ""
    
    def rename(self, new_username: str) -> None:
        """
        Change the username of the bot.
        """
        if self.username == new_username:
            return
        self.username = new_username
        self.sio.emit("change-user", new_username)
    
    def send_text_message(self, text: str) -> None:
        """
        Send a text message.
        """
        if len(text) > 2048:
            raise ValueError("message length must be less or equal to 2048.")
        self.sio.emit("message", dict(type="text", content=text))

    def _on_text_chat_message(self, data) -> None:
        if data['session_id'] == self.session_id:
            return
        for x in self.online_users:
            if data['session_id'] == x.session_id:
                self.on_text_message(x, data['content'])
                break
        else:
            raise RuntimeError("got a text message from a user we don't know!")

    def on_text_message(self, _: User, __: str) -> None:
        """
        Override this.
        This function gets executed when a user (the current client is ignored, must be sent by someone else) sends a text message.
        The user which sent the message and the content of the message is passed into the function as an argument.
        """
        pass

    def _on_online_message(self, users) -> None:
        self.online_users.clear()
        for user in users:
            self.online_users.append(User(
                username=user['user'],
                user_id=user['id'],
                session_id=user['session_id'],
                color=user['color'],
                flags=user['flags']
            ))
        self.on_online_users_update()
    
    def _on_user_join_message(self, user) -> None:
        user_obj = User(
            username=user['user'],
            user_id=user['id'],
            session_id=user['session_id'],
            color=user['color'],
            flags=user['flags']
        )
        self.online_users.append(user_obj)
        if user['session_id'] != self.session_id:
            self.on_user_join(user_obj)

    def on_user_join(self, _: User) -> None:
        """
        Override this.
        This function gets executed when a new user joins.
        The new user is passed as an argument to this function.
        All users can be found in Client.online_users.
        """
        pass

    def _on_user_leave_message(self, user) -> None:
        if user['session_id'] != self.session_id:
            user_obj = None
            for x in self.online_users:
                if x.session_id == user['session_id']:
                    user_obj = x
                    break
            if not user_obj:
                raise RuntimeError("got a message about a user leaving, but we don't know that user!")
            self.online_users.remove(user_obj)
            self.on_user_leave(user_obj)

    def on_user_leave(self, _: User) -> None:
        """
        Override this.
        This function gets executed when a user leaves.
        The user which left is passed as an argument to this function.
        All users which are still online can be found in Client.online_users.
        """
        pass

    def _on_user_change_message(self, user) -> None:
        if user['session_id'] != self.session_id:
            for x in self.online_users:
                if x.session_id == user['session_id']:
                    user_obj = x
                    break
            if not user_obj:
                raise RuntimeError("got a message about a user changing their name, but we don't know that user!")
            self.online_users.remove(user_obj)
            user_obj.username = user['newUser']
            self.online_users.append(user_obj)
            self.on_user_change(user_obj, user['oldUser'])

    def on_user_change(self, _: User, __: str) -> None:
        """
        Override this.
        This function gets executed when a user changes their name.
        This function receives 2 arguments: the user (with the updated name), and the old name of that user.
        All users can be found in Client.online_users.
        """
        pass

    def _on_auth_success(self, user_id, session_id) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.update_online_users()
    
    def on_online_users_update(self) -> None:
        """
        Override this.
        This function gets executed when the list of users gets bulk updated.
        Usually happens after connecting to the server, reconnecting and after calling Client.update_online_users().
        The new list of users can be found in Client.online_users.
        """
        pass

    def update_online_users(self) -> None:
        """
        Request the server to bulk update the list of users.
        If the server fulfills our request, on_online_users_update event is fired.
        """
        self.sio.emit("online")

    def run(self) -> None:
        """
        Start the bot.
        """
        self.sio.on("online", self._on_online_message)
        self.sio.on("auth-complete", self._on_auth_success)
        self.sio.on("user-join", self._on_user_join_message)
        self.sio.on("user-leave", self._on_user_leave_message)
        self.sio.on("nick-changed", self._on_user_change_message)
        self.sio.on("message", self._on_text_chat_message)
        self.sio.connect(constants.WS_URL, transports=['websocket'])
        self.sio.emit("auth", {"user": self.username})
    
    def stop(self) -> None:
        """
        Stop it!
        """
        self.sio.disconnect()
        self.sio = socketio.Client()