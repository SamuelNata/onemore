class Client():
    addr = 0
    port = 0
    gameId = -1
    playerId = -1

    def __init__(self, addr, port):
        self.addr = addr