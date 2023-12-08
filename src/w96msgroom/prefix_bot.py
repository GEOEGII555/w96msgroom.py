from .user import User
from .client import Client

class PrefixBot(Client):
    prefix: str

    def __init__(self, username: str, prefix: str) -> None:
        super().__init__(username)
        if len(prefix) > 2048:
            raise ValueError("prefix is longer than 2048 characters")
        self.prefix = prefix
    
    def on_text_message(self, _: User, __: str) -> None:
        """
        This function gets executed when a user (the current client is ignored, must be sent by someone else) sends a text message.
        The user which sent the message and the content of the message is passed into the function as an argument.
        ⚠️ If you are overriding this, please call self.handle_commands()
        ⚠️ passing in the user and the message, or your commands won't work!
        """
        self.handle_commands(_, __)

    
    def handle_commands(self, user: User, message: str) -> None:
        """
        This function is for parsing commands.
        If you are overriding on_text_message(), please call this function from there,
        or your prefix commands won't work. Don't call this from outside of on_text_message(),
        or else the Windows 96 illuminati (totally not from AOSP) will find you some day and beat you up.
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
            inside_quoted_string = True
            next_char_must_be_space = False
            current_argument_content = ""
            next_char_escaped = True
            for character in arguments:
                if next_char_must_be_space and character != " ":
                    raise ValueError(f"expected space after closing quotation but received '{character}'")
                if next_char_escaped:
                    current_argument_content += character
                elif character == "\\":
                    next_char_escaped = True
                    continue
                elif character == "\"":
                    if not inside_quoted_string:
                        inside_quoted_string = True
                        continue
                    next_char_must_be_space = True
                    inside_quoted_string = False
                    arguments_list.append(current_argument_content)
                    current_argument_content = ""
                    continue
                elif character == " ":
                    if not inside_quoted_string and not next_char_must_be_space:
                        arguments_list.append(current_argument_content)
                        current_argument_content = ""
                        continue
                else:
                    current_argument_content += character
                next_char_must_be_space = False
            if current_argument_content != "":
                arguments_list.append(current_argument_content)
                current_argument_content = ""
            print(arguments_list)
