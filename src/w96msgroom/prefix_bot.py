import inspect
import traceback

from .user import User
from .client import Client

class PrefixBot(Client):
    """
    Same as Client, but with some helper functions.
    add_command(name: str, handler) lets you add a command. Everything will be handled behind the scenes!
    """
    prefix: str
    commands: dict[str]

    def __init__(self, username: str, prefix: str) -> None:
        super().__init__(username)
        if len(prefix) > 2048:
            raise ValueError("prefix is longer than 2048 characters")
        self.prefix = prefix
        self.commands = dict()

    def add_builtin_help(self) -> None:
        '''
        Adds the builtin help command.

        ⚠️ This will raise an exception if you already have a command named "help"!

        You need to specify a description for your commands in the docstrings of the handlers:
        |class ...(w96msgroom.PrefixBot):
        |    def cmdhandler(self, user: w96msgroom.User, args: list[str]):
        |        """
        |        Put your description and usage here.
        |        [PREFIX] will be replaced with your bot's prefix. For example, your bot's prefix is \"m#\", and you write this:
        |        Usage: [PREFIX]ben question
        |        This will become:
        |        Usage: m#ben question
        |        """
        |        # ...
        '''
        self.add_command("help", self._help_command)

    def add_command(self, name: str, handler) -> None:
        """
        Add a command.
        This function accepts the command name (without the prefix) and a function that will be called when the command is invoked.
        ⚠️ Your handler's signature must be "def handler(user: w96msgroom.User, arguments: list[str]) -> None"! (type annotations are optional)
        """
        if name in self.commands.keys():
            raise ValueError(f"a command with name \'{name}\' already exists")
        self.commands[name] = handler
    
    def remove_command(self, name: str) -> None:
        """
        Remove a command.
        This function accepts the name of the command that you want to remove.
        """
        if name not in self.commands.keys():
            raise ValueError(f"a command with name \'{name}\' does not exist")
        del self.commands[name]

    def _help_command(self, user: User, arguments: list[str]):
        """
        Use this command to get help on this bot.
        Usage:
            [PREFIX]help - list all commands.
            [PREFIX]help commandName - get help on a specific command.
        """
        if len(arguments) < 1:
            help_index = f"""**{self.username} - a cool msgroom bot.** (made with [w96msgroom](https://github.com/GEOEGII555/w96msgroom.py))
*To get help on a specific command, invoke {self.prefix}help commandName.*\n"""
            for K in self.commands:
                help_index += K
                help_index += ", "
            help_index =  help_index.removesuffix(", ")
            self.send_text_message(help_index)
        else:
            command_name = " ".join(arguments)
            if command_name not in self.commands:
                self.send_text_message(f"I don't know a command named {command_name}! Are you sure your spelling is correct?")
                return
            documentation = inspect.getdoc(self.commands[command_name]).replace("[PREFIX]", self.prefix)
            if not documentation:
                documentation = "*No docstring provided.*"
            self.send_text_message(f"Help on command {command_name}:\n" + documentation)

    def on_text_message(self, user: User, message: str) -> None:
        """
        This function gets executed when a user (the current client is ignored, must be sent by someone else) sends a text message.
        The user which sent the message and the content of the message is passed into the function as an argument.
        ⚠️ If you are overriding this, please call self.handle_commands()
        ⚠️ with the user and the message, or your commands won't work!
        """
        try:
            self.handle_commands(user, message)
        except Exception as exc:
            e = type(exc).__name__
            if str(exc):
                e += ": " + str(exc)
            self.send_text_message(f"❌ {user.username}, an error happened: {e}{'.' if not e.endswith('.') and not e.endswith('!') and not e.endswith('?') else ''}")
            print(*traceback.format_exception(type(exc), exc, exc.__traceback__), sep="", end="")

    def handle_commands(self, user: User, message: str) -> None:
        """
        This function is for parsing commands.
        If you are overriding on_text_message(), please call this function from there,
        or your prefix commands won't work. Don't call this in anywhere else than on_text_message()
        (unless you are doing some testing), or else the Windows 96 illuminati will find you some day and beat you up.
        """
        if not message.startswith(self.prefix):
            return
        if user.session_id == self.session_id:
            return
        message = message.removeprefix(self.prefix)
        if not " " in message:
            arguments = []
            command = message
        else:
            command, arguments = message.split(" ", 1)
            """
            Why? Because we need to check for "quoted strings" and interpret them as one argument.
            Or else "my cool long username" will be interpreted as "my, cool, long, and username".
            If you want to insert a quote ("), please escape it by putting \ before the quote.
            """
            arguments_list = []
            inside_quoted_string = False
            next_char_must_be_space = False
            current_argument_content = ""
            next_char_escaped = False
            previous_character = None
            for character in arguments:
                if next_char_must_be_space and character != " ":
                    raise ValueError(f"expected space after closing quotation but received '{character}'")
                if next_char_escaped:
                    current_argument_content += character
                elif character == "\\":
                    next_char_escaped = True
                    previous_character = character
                    continue
                elif character == '"':
                    if not inside_quoted_string:
                        if previous_character != " " and previous_character != None:
                            raise ValueError(f"unescaped quote after a non-whitespace character (like te\"xt\")")
                        inside_quoted_string = True
                        previous_character = character
                        continue
                    next_char_must_be_space = True
                    inside_quoted_string = False
                    arguments_list.append(current_argument_content)
                    current_argument_content = ""
                    previous_character = character
                    continue
                elif character == " ":
                    if not inside_quoted_string and not next_char_must_be_space:
                        arguments_list.append(current_argument_content)
                        current_argument_content = ""
                        previous_character = character
                        continue
                    if inside_quoted_string:
                        current_argument_content += character
                else:
                    current_argument_content += character
                next_char_must_be_space = False
                previous_character = character
            if current_argument_content != "":
                arguments_list.append(current_argument_content)
                current_argument_content = ""
            arguments = arguments_list
        if command not in self.commands.keys():
            return
        self.commands[command](user, arguments)
