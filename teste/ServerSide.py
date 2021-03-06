import json
import socket
import threading
import time

from clientSide.Player import Player

maps = []
games = []
maxGameId = 0
maxPlayerId = 0

timeMillis = lambda: int(round(time.time()*1000))


def getGame(gameId):
    global games
    for game in games:
        if game['id'] == gameId:
            return game
    return None

simpleplayerDataReceiveModel = {"id": 0, "posx": 0, "posy": 0, "alive": True}

playerDataReceiveModel = {"id": 0, "posx": 0, "posy": 0, "bullets": [{"bornTime": 0,
                                                                      "startPosition": (0, 0),
                                                                      "range": 300,
                                                                      "size": 1,
                                                                      "direction": (1, 1),
                                                                      "player": None,
                                                                      "die": False,
                                                                      "lifeTime": 500,
                                                                      "damage": 10
                                                                      }], "alive": True}


class Server(threading.Thread):
    __host = "127.0.0.1"
    __port = 5000
    __nome = "Servidor"
    __map = 0
    __skt = socket.socket()

    def __init__(self, nome, mapNum):
        threading.Thread.__init__(self)
        self.__nome = nome
        self.__map = maps[mapNum] if mapNum >= 0 and mapNum < len(maps) else None

    def run(self):
        print("Servidor conectado a porta ", self.__port, " e escutando no IP ", self.__host)
        self.__skt.bind((self.__host, self.__port))
        self.__skt.listen(1)
        handlers = []
        while True:
            conn, addr = self.__skt.accept()
            sh = ServerHandler(conn, addr)
            sh.start()
            handlers.append(sh)

class ServerHandler(threading.Thread):
    __conn = 0
    __addr = 0

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.__conn = conn
        self.__addr = addr

    def run(self):
        while True:
            data = self.__conn.recv(1024).decode()
            print("data: ", data, ";   Type: ", type(data))
            if data=='':
                print("Client close connection")
                return
            data = json.loads(data)
            if not data:
                print("No data received")
                return

            request = data
            if request['ask'] == 0:
                playerId = self.insertInGame(request['gameId'])
                response = '{"value":"SUCCESS", "playerId":' + str(playerId) + '}'
            elif request['ask'] == 1:
                gameId = self.newGame()
                if gameId >= 0:
                    response = '{"value":"SUCCESS", "gameId":' + str(gameId) + '}'
                else:
                    response = '{"value":"FAIL", "msg":' + ' I dont know what happens :/' + '}'
            elif request['ask'] == 2:
                response = "ok"
            else:
                response = '{"value":"FAIL", "msg": Invalid request}'
            self.__conn.send(response.encode())

    def insertInGame(self, gameId):
        game = getGame(gameId)
        r, g, b = 150, 0, 0
        p = Player((100+r, 100+g, 100+b))
        global maxPlayerId
        maxPlayerId += 1
        p.addr = self.__addr
        game["players"].append(p)
        return maxPlayerId

    def newGame(self):
        global maxGameId
        global games
        if len(games) > 1:
            return -1
        else:
            maxGameId += 1
            games.append({"id": maxGameId, "players": [], "items": [], "bullets": []})
            return maxGameId

    def play(self):
        print("playing...")
        # simpleplayerDataReceiveModel = {"id": 0, "posx": 0, "posy": 0, "alive": True}
        isAlive = True
        while isAlive:
            data = self.__conn.recv(1024).decode()
            data = json.loads(data)
            if not data:
                print("No data received")
            request = json.loads(data)
            print("Request: ", request, ";   type: ", type(request) )
            if not ("id" in request and "posx" in request and "posy" in request and "alive" in request) :
                print("ServiceSide:play: ta faltando campos nos dados recebidos")
            else:
                print("Recived: id=", request['id'], ", x=", request['posx'], ', y=', request['posy'], ', alive=', request['alive'])
                self.__conn.send("ok".encode())
