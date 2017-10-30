from threading import Thread
import socket
import json
from utils.Utils import logf, ReadWriteLock
from clientSide.Game import Game

menu = """
    MENU

1 - Get in a game
2 - Create you game
3 - List all games
4 - Exit

Make your choice by number: """

class Client(Thread):
    skt = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    serverIp = "::1"
    server = ("::1", 5000)

    def __init__(self):
        Thread.__init__(self)
        self.serverIp = "::1"
        self.port = 5002
        self.skt.bind(("::1", self.port))

    def run(self):
        global menu
        while True:
            choice = int(input(menu))
            # print("choice: ", str(choice), ";   type: ", type(choice))
            if choice == 1:
                self.getInGame()
            if choice == 2:
                self.createGame()
            if choice == 3:
                self.listRooms()
            if choice == 4:
                self.skt.close()
                return

    def getInGame(self):
        name = input("Tell me the room name (press ENTER and chose 3 to list all rooms): ")
        request = {"state":"main menu", "ask":"get in game", "value": {"name": name}}
        self.skt.sendto(json.dumps(request).encode(), (self.serverIp, self.port))
        response = json.loads(self.skt.recvfrom(1024)[0].decode())
        logf("Client: Response recived for get in game" + str(response), True)
        if not response:
            logf("Client: (FAIL) not recing date.", True)
        elif response["value"]["result"] == "Fail":
            logf("Client: (Fail) server msg = " + str(response["value"]["reason"]))
        elif response["value"]["result"] == "Success":
            self.play(name, 0, response["value"]["id"])
        else:
            logf("Client: Some thing wrong in getInGame", True)

    def createGame(self):
        name = input("Tell me the room name: ")
        map = input("Tell me the map number (betwen 1 and 1): ")
        request = {"state": "main menu", "ask": "create game", "value": {"name": name, "map": map}}
        self.skt.sendto(json.dumps(request).encode(), self.server)
        response = json.loads(self.skt.recvfrom(1024)[0].decode())
        if not response:
            logf("Client: (FAIL) not recing date.", True)
        elif response["value"]["result"] == "Fail":
            logf("Client: (Fail) server msg = " + str(response["value"]["reason"]))
        elif response["value"]["result"] == "Success":
            self.play(name, 0, response["value"]["id"])
        else:
            logf("Client: Some thing wrong in createGame", True)

    def listRooms(self):
        request = {"state": "main menu", "ask": "list games"}
        self.skt.sendto(json.dumps(request).encode(), self.server)
        response = self.skt.recvfrom(512)[0].decode()
        response = json.loads(response)
        if not response:
            logf("Client: (FAIL) not recing date.", True)
        else:
            print(" -Rooms List-")
            for gameName in response["value"]["result"]:
                print(gameName + "(?/?)")
            print(" - " + str(len(response["value"]["result"])) + " rooms found -")
            print('')

    def play(self, name, map, gameId):
        game = Game(name, map, self.skt, gameId)
        game.start()
        game.join()




































