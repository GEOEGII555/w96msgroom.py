import w96msgroom

class EvalBot(w96msgroom.Client):
    def __init__(self) -> None:
        super().__init__("eb#eval | EvalBot")

    def on_text_message(self, user: w96msgroom.User, content: str):
        args = content.split(" ")
        if args[0] == "eb#eval":
            self.send_text_message("Executed!")
            cmd = " ".join(args[1:]).replace("&quot;", '"')
            print("executing", cmd)
            try:
                exec(cmd, globals(), locals())
            except Exception:
                pass

evalbot = EvalBot()
evalbot.run()
try:
    while True:
        pass
finally:
    evalbot.stop()
