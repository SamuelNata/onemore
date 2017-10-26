import socket
import threading
import json
import pygame
import time
from domain.Player import Player

maps = []
games = []
maxGameId = 0
maxPlayerId = 0

timeMillis = lambda: int(round(time.time()*1000))

def getGame(gameId):
    global games
    for game in games:
        if game['id']==gameId:
            return game
    return None

players = []
items = []

playerDataReceiveModel = {"id":0, "posx":0, "posy":0, "bullets":[{      "bornTime": 0,
                                                                        "startPosition": (0, 0),
                                                                        "range": 300,
                                                                        "size": 1,
                                                                        "direction": (1, 1),
                                                                        "player": None,
                                                                        "die": False,
                                                                        "lifeTime": 500,
                                                                        "damage": 10
                                                                                    }], "alive":True}

class Server(threading.Thread):
    __host = "127.0.0.1"
    __port = 5000
    __nome = "Servidor"
    __map = 0

    def __init__(self, nome, mapNum):
        threading.Thread.__init__(self)
        self.__nome = nome
        self.__map = maps[mapNum] if mapNum>=0 and mapNum<len(maps) else None

    def run(self):
        skt = socket.socket()
        skt.bind((self.__host, self.__port))
        skt.listen(5)
        while True:
            conn, addr = skt.accept()
            data = skt.recv(1024)
            self.ServerHandler(conn, data)

            print('get a package to handle')
            conn.close()

    def ServerHandler(self, conn, data):
        if not data:
            print("No data received")# from: ", addr, ". Closing connection.")
            return
        request = json.dumps(data)
        if request['ask']==0:
            self.insertInGame(request['gameId'])
            response = '{"value":"SUCCESS"}'
        elif request['ask']==1:
            gameId = self.newGame()
            if gameId>=0:
                response = '{"value":"SUCCESS", "gameId":'+str(gameId)+'}'
            else:
                response = '{"value":"FAIL", "msg":' + ' I dont know what happens :/' + '}'
        else:
            response = '{"value":"FAIL", "msg": ' + 'Invalid request' + '}'
        conn.send(response.encode())

    def insertInGame(self, gameId):
        game = getGame(gameId)
        r, g, b = 150, 0, 0
        p = Player((100+r,100+g,100+b))
        global maxPlayerId
        maxPlayerId += 1
        p.id = maxPlayerId
        game["players"].append(p)

    def newGame(self):
        global maxGameId
        global games
        if len(games)>1:
            return -1
        else:
            maxGameId += 1
            games.append( {"id":maxGameId, "players":[], "items":[], "bullets":[]} )