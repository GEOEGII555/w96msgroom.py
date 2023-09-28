import w96msgroom
from w96msgroom import User

class WelcomerBot(w96msgroom.Client):

    def __init__(self) -> None:
        super().__init__("WelcomerBot")
    
    def on_user_join(self, user: User) -> None:
        self.send_text_message(f"Welcome {user.username} to Windows 96 msgroom!")
    
    def on_user_leave(self, user: User) -> None:
        self.send_text_message(f"Bye, {user.username}!")

bot = WelcomerBot()
bot.run()
try:
    while True:
        pass
finally:
    bot.stop()