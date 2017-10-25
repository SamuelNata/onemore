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
        handlerList = []
        while True:
            skt = socket.socket()
            skt.bind((self.__host, self.__port))
            skt.listen(1)
            #print("Waiting connection...")
            conn, addr = skt.accept()
            #print("Receive connection from: " + str(addr))
            hp = ServerHandler(conn, addr, skt)
            handlerList.append(hp)
            hp.start()
            print('get a player to handle')


class ServerHandler(threading.Thread):
    __conn = 0
    __addr = 0
    __skt = 0
    __gameId = -1
    __playerId = -1

    def __init__(self, conn, addr, soket):
        threading.Thread.__init__(self)
        self.__conn = conn
        self.__addr = addr
        self.__skt = soket

    def run(self):
        while True:
            data = self.__skt.recv(1024)
            if not data:
                print("No data received from: ", self.__addr, ". Closing connection.")
                break
            request = json.dumps(data)
            if request['ask']==0:
                self.insertInGame(request['gameId'])
            elif request['ask']==1:
                gameId = self.newGame()
                if gameId>=0:
                    response = '{"value":"SUCCESS", "gameId":'+str(gameId)+'}'
                else:
                    response = '{"value":"FAIL", "msg":' + ' I dont know what happens :/' + '}'
            else:
                response = '{"value":"FAIL", "msg": ' + 'Invalid request' + '}'
            self.__conn.send(response.encode())
        self.__conn.close()

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