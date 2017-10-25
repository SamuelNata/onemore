import socket
import threading
import json
import pygame
import time

players = []
items = []
maps = []

playerDataReceiveModel = {"id":0, "posx":0, "posy":0, "bullets":[
                                                                    {
                                                                        "bornTime": 0,
                                                                        "startPosition": (0, 0),
                                                                        "range": 300,
                                                                        "size": 1,
                                                                        "direction": (1, 1),
                                                                        "player": None,
                                                                        "die": False,
                                                                        "lifeTime": 500,
                                                                        "damage": 10
                                                                    }
                                                                ], "alive":True}

class Server(threading.Thread):
    __host = "127.0.0.1"
    __port = 5000
    __nome = "Servidor"
    __mySocket = socket.socket()
    __map = 0

    def __init__(self, nome, mapNum):
        threading.Thread.__init__(self)
        self.__nome = nome
        self.__map = maps[mapNum] if mapNum>=0 and mapNum<len(maps) else None

    def run(self):
        handlerList = []
        while len(handlerList)<2:
            skt = socket.socket()
            skt.bind((self.__host, self.__port))
            skt.listen(1)
            conn, addr = skt.accept()
            print("Recive connection from: " + str(addr))
            hp = HandlePlayer(conn, addr)
            handlerList.append(hp)
            hp.start()
        for p in handlerList:
            p.join()


class HandlePlayer(threading.Thread):
    __conn = 0
    __addr = 0

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.__conn = conn
        self.__addr = addr

    def run(self):
        print("Recive connection from: " + str(self.__addr))
        while True:
            data = self.__conn.recv(1024).decode()
            if not data:
                print("No data recived from: ", self.__addr)
                break
            print("from", self.__addr, ": ", str(data))
            if not ('id' in data and 'posx' in data and 'posy' in data and 'bullets' in data and 'alive' in data):
                print("The client is not returning right values.")
                data = "ERROR!"
            else:
                data = "OK!"
            print("sending: " + str(data))
            self.__conn.send(data.encode())
        print("Closing connection with: ", self.__addr)
        self.__conn.close()

class  Client(threading.Thread):
    __host = '127.0.0.1'
    __port = 5000
    __nome = ""
    __mySocket = socket.socket()
    __sendPerSecond = 20
    __lastSend = 0

    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        mySocket = socket.socket()
        mySocket.connect((self.__host, self.__port))

        data = input(" -> ")

        while data != 'q':
            if pygame.time.get_ticks()-self.__lastSend >= 1./self.__sendPerSecond :
                mySocket.send(json.dumps(playerDataReceiveModel).encode())
                data = mySocket.recv(1024)
                print('Received from server: ', data)
                data = input(" -> ")
            if (1./self.__sendPerSecond)-(pygame.time.get_ticks()-self.__lastSend) > 0 :
                time.sleep((1./self.__sendPerSecond)-(pygame.time.get_ticks()-self.__lastSend))
        mySocket.close()

s = Server("Servidor", 0)
c = Client("Cliente")

s.start()
c.start()

l = []
l.append(s)
l.append(c)

for t in l:
    t.join()
