# PrefixBot (extends Client).
Same as Client, but with some helper functions.

add_command(name: str, handler) lets you add a command. Everything will be handled behind the scenes!

## Events:
*Everything from Client.*

## Instance attributes:
*Everything from Client, and...*

### `prefix: str`
The bot's prefix. You can change this at any time (don't confuse other people with this, otherwise no one will use your bot. Just saying.).

### `commands: dict[str]`
All commands. Keys are their names, and values are their handler functions.

## Functions:
*Everything from Client, and...*

### `add_command(name: str, handler)`
Add a command.

This function accepts the command name (without the prefix) and a function that will be called when the command is invoked.

⚠️ Your handler's signature must be "`def handler(user: w96msgroom.User, arguments: list[str]) -> None`"! (type annotations are optional)

### `remove_command(name: str)`
Remove a command.

This function accepts the name of the command that you want to remove.

### `add_builtin_help()`
Adds the builtin help command.

⚠️ This will raise an exception if you already have a command named "help"!

You need to specify a description for your commands in the docstrings of the handlers:
```py
class ...(w96msgroom.PrefixBot):
    def cmdhandler(self, user: w96msgroom.User, args: list[str]):
        """
        Put your description and usage here.
        [PREFIX] will be replaced with your bot's prefix. For example, your bot's prefix is \"m#\", and you write this:
        Usage: [PREFIX]ben question
        This will become:
        Usage: m#ben question
        """
        # ...
```

### `handle_commands(user: User, message: str)`
This function is for parsing commands and calling their handlers.

If you are overriding on_text_message(), please call this function from there,
or your prefix commands won't work. Don't call this in anywhere else than on_text_message()
(unless you are doing some testing), or else the Windows 96 illuminati will find you some day and beat you up.