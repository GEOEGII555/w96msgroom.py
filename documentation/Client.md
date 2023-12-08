# The Client class.
The base for all the bots ✨

## Instance attributes:

### `sio: socketio.Client`
The socket.io client. Why do you need to touch this?
### `online_users: list[User]`
All online users. It's easier to work with the functions that are provied below for finding users.
### `session_id: str`
The session ID of the bot.
### `username: str`
The username of the bot. Don't modify directly, see below for a function that changes this.
### `user_id: str`
The user ID of the bot.

## Functions:

### `rename(new_username: str)`
Try to change the name of the bot.

### `send_text_message(text: str)`
Try to send a text message.

### `is_online(user: User)`
Check if a user is online. (searches for a user with the same session ID)

### `get_user(session_id: str)`
Get a user with a specific session ID.

### `update_online_users()`
Ask the server to bulk update the list of users.
If the server fulfills our request, on_online_users_update event is fired.

### `run()`
Start the bot ✨

Returns after a connection has been established.
This function won't wait until you stop the bot.

### `stop()`
Stop it!
Your bot will disconnect from the server.

## Events

### `on_online_users_update()`
Override this.

This function gets executed when the list of users gets bulk updated.
Usually happens after connecting to the server, reconnecting and after calling Client.update_online_users().

The new list of users can be found in Client.online_users.

### `on_user_change(user: User, content: str)`
Override this.

This function gets executed when a user changes their name.
It receives 2 arguments: the user (with the updated name), and the old name of that user.

All users can be found in Client.online_users.

### `on_user_leave(user: User)`
Override this.

This function gets executed when a user leaves.
The user which left is passed as an argument to this function.

All users which are still online can be found in Client.online_users.

### `on_user_join(user: User)`
Override this.

This function gets executed when a new user joins.
The new user is passed as an argument to this function.

All users can be found in Client.online_users.

### `on_text_message(user: User, content: str)`
Override this.

This function gets executed when a user (this bot is ignored, must be sent by someone else) sends a text message.

The user which sent the message and the content of the message are passed into the function as an argument.