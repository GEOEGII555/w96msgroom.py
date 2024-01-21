# The User class.
Represents a user.
If a user_id of one user is the same as the user_id of another user, both users are the same.
Note that if one user joins from 2 accounts at the same time (basically opening 2 browser tabs), they will have the same user ID, only the session ID will be different.
Also note that if you store an old message, the User object in there might be out of sync! The user might've left or changed their username.
If you want to check if a user still exists, use Client.is_online(user: User) and Client.get_user(session_id: str) to get an up to date version of this user.

## Instance attributes:

### `flags: list[str]`
Contains the flags sent by the message room.
### `session_id: str`
The user's session ID.
### `username: str`
Contains the user's username (at the time of creating the User object).
### `user_id: str`
The user's ID.
### `color: str`
The color that the message room choosed for the user.

## Functions:

### `is_staff()`
Returns a boolean value: True if the user is a staff (`"staff" in self.flags`), or False if not.

### `is_system()`
Check if a user is actually "System" (assuming the object contains valid data).

## Special functions:

### `user == another` (`__eq__`)
Checks if both users have the same session ID.
