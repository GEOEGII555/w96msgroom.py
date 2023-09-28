import w96msgroom

client = w96msgroom.Client("doNothingBot")
client.run()
try:
    while True:
        pass
finally:
    client.stop()