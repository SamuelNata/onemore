from threading import Condition, Thread
from serverSide.Client import Client
from serverSide.Game import Game, Games
from serverSide.Player import Player
import socket
from utils.Utils import logf
import json

clients = []
requestQueue = []
existsRequest = Condition()
games = Games()
host = "::1"  #  "127.0.0.1"
portRecive = 5000
portSend = 5001
sktRecive = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sktSend = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def removeClient(client):
    global clients
    for idx, c in enumerate(clients):
        if c.addr == client.addr:
            clients.pop(idx)
            return

def getClient(addr):
    global clients
    for c in clients:
       if c.addr == addr:
           return c
    return None

# Receve Requisições (Producer)
class RequestReciver(Thread):
    def run(self):
        global sktRecive
        global host
        global portRecive
        global clients
        sktRecive = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sktRecive.bind((host, portRecive))
        global clients
        global requestQueue
        while True:
            data, addr = sktRecive.recvfrom(1024)
            data = data.decode()
            logf("Server: Request Reciver: Recive new Data from " + str(addr), True)
            existsRequest.acquire()
            if not data:
                logf("Server: Client " + str(addr) + " is not sending information.", True)
            else:
                client = getClient(addr[0])
                if not client:
                    client = Client(addr[0], addr[1])
                clients.append(client)
                requestQueue.append((client, json.loads(data)))
                logf("Server: Appended new request.", True)
            existsRequest.notify()
            existsRequest.release()

# Responde Requisições (Consumer)
class RequestHandler(Thread):

    def run(self):
        global requestQueue
        global clients
        global sktSend
        global portSend
        sktSend.bind((host, portSend))
        while True:
            existsRequest.acquire()
            if not requestQueue:
                existsRequest.wait()
            client, request = requestQueue.pop(0)
            logf("Handling " + str(client.addr), True)

            if request["state"] == "main menu":
                self.mainMenuHandle(client, request)
            elif request["state"] == "gaming":
                self.gamingHandle(client, request)
            existsRequest.release()


    def mainMenuHandle(self, client, request):
        global games
        logf("Server: Request " + str(request), True)
        if request["ask"] == "get in game":  # GET IN GAME
            logf("Server: User request to get in game", True)
            name = request["value"]["name"]
            logf('Server: Adding player of client ' + str(client.addr) + " to game " + name, True)
            player = Player(client)
            game = games.getByName(name)
            if not game:
                logf("Server: FAIL: There is not game with name " + name, True)
                response = {"state": "main menu", "value": {"result": "Fail", "reason": "Chose game dosen't exists"}}
            else:
                game.addPlayer(player)
                logf("Server: Sucess", True)
                response = {"state": "main menu", "value": {"result": "Success", "name": game.nome, "map": game.map, "id": game.id}}
        elif request["ask"] == "create game":  # CREATE GAME
            logf("Server: User request to create game", True)
            if "maxNumPlayers" in request["value"]:
                g = Game(request["value"]["name"], request["value"]["map"], request["value"]["maxNumPlayers"])
            else:
                g = Game(request["value"]["name"], request["value"]["map"])
            gameId = games.newGame(g)
            if gameId != -1:
                logf('Server: Created new game with id ' + str(gameId), True)
                logf('Server: Adding player of client ' + str(client.addr) + " to game " + str(gameId), True)
                player = Player(client)
                games.getById(gameId).addPlayer(player)
                response = {"state": "main menu", "value": {"result": "Success", "name": games.getById(gameId).name,
                                                            "map": games.getById(gameId).map, "id": gameId}}
            else:
                response = {"state": "main menu", "value": {"result": "Fail", "reason": "Can't create game"}}
        elif request["ask"] == "list games":  # LIST GAMES
            logf("Server: User request to list all games", True)
            response = {"state": "main menu", "value": {"result": games.listAll()}}
        else:  # EXIT
            logf("Server: User exit", True)
            removeClient(client)
            return
            # response = {"state": "main menu", "value": {"result": "Success"}}
        global sktSend
        logf("Server: Responding client", True)
        sktSend.sendto(json.dumps(response).encode(), (client.addr, 5002))

    def gamingHandle(self, client, request):
        global games
        data = request["value"]
        game = games.getById(data["gameId"])
        p = game.getPlayer(client)
        value = {"addr": p.client.addr}

        for act in data["actions"]:
            if act["name"] == "exit game":
                game.removePlayer(client)
                return
            #  other IF cases, to implement

        if "pos" in data:
            p.pos = data["pos"]
            value["pos"] = p.pos
            logf("Recive from client " + str(client.addr) + " pos " + str(data["pos"]))

        response = {"state": "gaming", "value": value}
        global sktSend
        for player in game.players:
            if player.client.addr != p.client.addr:
                sktSend.sentto(json.dumps(response).encode(), (player.client.addr, 5000))



























