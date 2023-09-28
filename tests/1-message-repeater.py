import w96msgroom
from w96msgroom import User

class MessageRepeaterBot(w96msgroom.Client):
    def __init__(self) -> None:
        super().__init__("Message Repeater")
    
    def on_text_message(self, user: User, content: str) -> None:
        self.send_text_message(f"Message by {user.username}: {content}\nThis bot is a test for the [w96msgroom](https://github.com/GEOEGII555/w96msgroom) library by GEOEGII555.\n(The library owner doesn't condone spamming, if you see a bot spam 24/7 using my library contact whoever started it, not me)")

bot = MessageRepeaterBot()
bot.run()
try:
    while True:
        pass
finally:
    bot.stop()