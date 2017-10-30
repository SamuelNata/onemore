from utils.Utils import logf

class Games():
    games = []
    maxGameId = 0

    def __init__(self):
        pass

    def getById(self, gameId):
        for game in self.games:
            if game.id == gameId:
                return game
        return None

    def getByName(self, name):
        for g in self.games:
            if g.name==name:
                return g
        return None

    def newGame(self, game):
        if not self.getByName(game.name):
            self.maxGameId += 1
            game.id = self.maxGameId
            self.games.append(game)
            return self.maxGameId
        else:
            logf("Already existis game with this name")
            return -1

    def endGame(self, gameId):
        for idx, game in enumerate(self.games):
            if game.id == gameId:
                self.games.pop(idx)

    def listAll(self):
        return [game.name for game in self.games]

class Game():
    id = -1
    players = []
    maxNumPlayers = -1
    items = []
    maxItemId = 0
    bullets = []
    maxBulletId = 0
    startTime = -1
    convergenceMapPoint = (10, 10)
    map = 0
    name = ''

    def __init__(self, name, map = 0, maxNumPlayers = -1):
        self.name = name
        self.map = map
        self.maxNumPlayers = maxNumPlayers

    def update(self):
        pass # TO Implement #########################


    # --- PLAYERS ACT METHODS ---
    def addPlayer(self, player):
        self.players.append(player)

    def getPlayer(self, client):
        for p in self.players:
            if p.client.addr == client.addr:
                return p
        return None

    def removePlayer(self, client):
        for idx, p in enumerate(self.players):
            if p.client.addr == client.addr:
                self.players.pop(idx)
                return

    def getAllClients(self):
        return [p.id for p in self.players]













