import threading
import socket
import json
import time
import pygame

timeMillis = lambda: int(round(time.time()*1000))
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
mainMenu = """  
0 - Connect to game
1 - Create a new game
2 - Exit
Select the number: """

class  Client(threading.Thread):
    __host = '127.0.0.1'
    __port = 5000
    __nome = ""
    __mySocket = socket.socket()
    __sendPerSecond = 20
    __lastSend = 0
    __gameId = -1

    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        # self.__host = input('Type the server ip: ')
        self.__mySocket = socket.socket()
        self.__mySocket.connect((self.__host, self.__port))
        global mainMenu
        command = int(input(mainMenu))
        while command<2:
            if command==0:
                self.connectToGame(input("Type de game id: "))
            elif command==1:
                self.createNewGame()


    def connectToGame(self, gameId):
        print('Connecting to game', gameId)
        self.__mySocket.send(json.dumps('{"ask":0, "gameId":'+str(gameId)+'}').encode())
        response = json.loads(self.__mySocket.recv(1024))
        print(response)
        if response['value']=='SUCCESS':
            print("Connection successful")
            #play()
            while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if timeMillis() - self.__lastSend >= 1 / self.__sendPerSecond:
                    self.__mySocket.send(json.dumps(playerDataReceiveModel).encode())
                    command = self.__mySocket.recv(1024)
                    self.__lastSend = timeMillis()
                if (1. / self.__sendPerSecond) - (timeMillis() - self.__lastSend) > 0:
                    time.sleep((1. / self.__sendPerSecond) - (timeMillis() - self.__lastSend))
            self.__mySocket.close()
        elif response['value']=='FAIL':
            print("Cant connect: ", response['msg'])
        else:
            print("A error occurred.")

    def createNewGame(self):
        self.__mySocket.send(json.dumps('{"ask":1}').encode())
        response = json.loads(self.__mySocket.recv(1024))
        if response['value']=='SUCCESS':
            self.__gameId = response['gameId']
            self.connectToGame(self.__gameId)
        elif response['value']=='FAIL':
            print('Cant create game: ', response['msg'])
        else:
            print('A error occurred. :O')

    def play(self):
        pass

from teste.ServerSide import Server

s = Server("SERVER", 0)
s.start()

c = Client("CLIENTE")
c.start()