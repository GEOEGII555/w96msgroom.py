import w96msgroom

class PingBot(w96msgroom.Client):
    def __init__(self) -> None:
        super().__init__("pb#ping | PingBot")

    def on_text_message(self, user: w96msgroom.User, content: str):
        if content == "pb#ping":
            self.send_text_message("Pong!")

pingbot = PingBot()
pingbot.run()
try:
    while True:
        pass
finally:
    pingbot.stop()
