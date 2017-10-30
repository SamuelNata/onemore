import json
import socket
import threading
import time
from math import sqrt

import pygame
from pygame import draw, display

from clientSide.Player import Player

resolution = [(800, 600)]
choseResolution = 0
step = resolution[choseResolution][0]/16
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 15)

timeMillis = lambda: int(round(time.time()*1000))

simpleplayerDataReceiveModel = {"id":0, "posx":0, "posy":0, "alive":True}
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
1 - Connect to game
2 - Create a new game
3 - Exit
Select the number:
"""

class  Client(threading.Thread):
    __host = '127.0.0.1'
    __port = 5000
    __nome = ""
    __mySocket = socket.socket()
    __sendPerSecond = 20
    __lastSend = 0
    __gameId = -1
    __myAddr = ''

    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome

    def run(self):
        # self.__host = input('Type the server ip: ')
        self.__mySocket = socket.socket()
        self.__mySocket.connect((self.__host, self.__port))
        print("Client conectado a porta ", self.__port, " e IP ", self.__host)
        global mainMenu
        command = int(input(mainMenu))
        while command < 3:
            if command == 1:
                self.connectToGame(input("Type de game id: "))
            elif command == 2:
                if self.createNewGame():
                    self.playing()
            command = int(input(mainMenu))

    def connectToGame(self, gameId):
        print('Connecting to game', gameId)
        self.__mySocket.send(('{"ask":0, "gameId":'+str(gameId)+'}').encode())
        response = json.loads(self.__mySocket.recv(1024).decode())
        print(response)
        if response['value'] == 'SUCCESS':
            print("Connection successful")
            return True
        elif response['value'] == 'FAIL':
            print("Cant connect: ", response['msg'])
            return False
        else:
            print("A error occurred.")
            return False

    def createNewGame(self):
        self.__mySocket.send(('{"ask":1}').encode())
        response = json.loads(self.__mySocket.recv(1024).decode())
        if response['value'] == 'SUCCESS':
            self.__gameId = response['gameId']
            if self.connectToGame(self.__gameId):
                return True
        elif response['value'] == 'FAIL':
            print('Cant create game: ', response['msg'])
            return False
        else:
            print('A error occurred. :O')
            return False

    def playing(self):
        gameDisplay = pygame.display.set_mode(resolution[choseResolution])
        pygame.display.set_caption('Survival\'s King')
        clock = pygame.time.Clock()
        crashed = False
        p = Player((250, 0, 0))
        p.prepare()
        p.position = (100, 100)
        gameItems = []
        players = []
        players.append(p)

        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                p.pos = (p.pos[0], p.pos[1] - p.moveSpeed)
            if keys[pygame.K_s]:
                p.pos = (p.pos[0], p.pos[1] + p.moveSpeed)
            if keys[pygame.K_a]:
                p.pos = (p.pos[0] - p.moveSpeed, p.pos[1])
            if keys[pygame.K_d]:
                p.pos = (p.pos[0] + p.moveSpeed, p.pos[1])
            if pygame.mouse.get_pressed()[0] == 1:
                if keys[pygame.K_f]:
                    (gr, it, eq) = self.mouseOver()
                    if it >= 0 and len(p.itens) > it:
                        pass
                    if gr >= 0 and len(p.ground) > gr:
                        pass
                        # p.itens.append(p.ground[gr])
                        # gameItems.remove(p.ground[gr])
                    if eq >= 0 and len(p.itens) > eq:
                        pass
                else:
                    pass
                    # p.equipedGun.fire(p, p.pos,
                    #                   (pygame.mouse.get_pos()[0] - p.pos[0], pygame.mouse.get_pos()[1] - p.pos[1]),
                    #                   bullets)

            # for item in gameItems:
            #     self.drawItem(item, gameDisplay)

            for player in players:
                player.ground = []
                # for bullet in bullets:
                #     drawBullet(bullet, gameDisplay)
                #     if hit(player, bullet):
                #         player.takeShot(bullet)
                #     if bullet.die:
                #         bullets.remove(bullet)

                # for item in gameItens:
                #     if colide(player, item):
                #         player.ground.append(item)
                self.drawPlayer(player, gameDisplay)

            self.drawStatsPanel(p, gameDisplay)

            if keys[pygame.K_f]:
                self.drawInventory(gameDisplay, p.itens, p.ground)

            display.update()
            # simpleplayerDataReceiveModel = {"id":0, "posx":0, "posy":0, "alive":True}
            dict = {"ask":2, "id":0, "posx":p.pos[0], "posy":p.pos[1], "alive":(p.hp>0)}
            self.__mySocket.send(json.dumps(dict).encode())
            if self.__mySocket.recv(1024).decode() != 'ok':
                crashed = True
                print('Servidor não retornou OK')
            gameDisplay.fill((0, 0, 0))

            clock.tick(30)
        pygame.quit()

    def module(self, v):
        return sqrt(v[1]**2+v[0]**2)

    def vetUnitario(self, v):
        return (v[0]/module(v), v[1]/module(v))

    def drawPlayer(self, p, display):
        if p.hp>0:
            draw.circle(display, p.color, p.pos, p.ray)
            # draw.circle(display, (0,0,0), p.pos, 2)
            life = pygame.Rect(p.pos[0] - p.ray, p.pos[1]+20, p.ray*2*(p.hp/p.maxHp), 2)
            draw.rect(display, (0,200,0), life, 0)

    def drawStatsPanel(self, p, display):
        res = resolution[choseResolution]
        bg = pygame.Rect(res[0]/4, res[1]*0.9, res[0]/2, res[1]/10)
        draw.rect(display, (50, 50 , 50), bg, 0)

        topMargin = 10
        sideMargin = 10
        life = pygame.Rect(bg.x + sideMargin, bg.y + topMargin, (bg.width - 2*sideMargin) * (p.hp/p.maxHp), 18)
        draw.rect(display, (0, 120, 0), life, 0)

        energy = pygame.Rect(life.x, life.y + 2*topMargin + 4, (bg.width - 2*sideMargin) * (p.energy/p.maxEnergy), 18)
        draw.rect(display, (100, 100, 0), energy, 0)

        gunRay = 30
        draw.circle(display, (50,50,50), (int(res[0]/4-gunRay), res[1]-gunRay), gunRay, 0)

    def drawInventory(self, display, itens, ground):
        global step
        # GROUND GRIDS
        for idx in range(10):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - 4 * step + (idx % 2) * step,
                               2 * step + int(idx/2) * step, step, step)
            pygame.draw.rect(display, (200,200,200), rect, 3)
        # GROUND ACCECIBLE ITENS
        for idx, item in enumerate(ground):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - 4 * step + (idx % 2) * step + .2 * step,
                               2 * step + int(idx/2) * step + .2 * step, step*.6, step*.6)
            pygame.draw.rect(display, (70,20,20), rect, 0)

        # INVENTORY GRIDS
        for idx in range(10):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - step + (idx % 2) * step,
                               2 * step + int(idx/2) * step, step, step)
            pygame.draw.rect(display, (200,200,200), rect, 3)
        # INVENTOTY ITENS
        for idx, item in enumerate(itens):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - step + (idx % 2) * step + .2 * step,
                               2 * step + int(idx/2) * step + .2 * step, step*.6, step*.6)
            pygame.draw.rect(display, (100,50,50), rect, 0)

        # HELMET GRID
        rect = pygame.Rect(resolution[choseResolution][0] / 2 + 2* step,
                           2 * step , step, step)
        pygame.draw.rect(display, (200, 200, 200), rect, 3)
        # ARMOR GRID
        rect = pygame.Rect(resolution[choseResolution][0] / 2 + 2 * step,
                           4 * step, step, step)
        pygame.draw.rect(display, (200, 200, 200), rect, 3)
        # GUN GRID
        rect = pygame.Rect(resolution[choseResolution][0] / 2 + 2 * step,
                           6 * step, step, step)
        pygame.draw.rect(display, (200,200,200), rect, 3)

    def drawBullet(self, b, display):
        draw.line(display, (100, 100, 0), b.startBulletPoint(), b.endBulletPoint(), b.size)

    def drawItem(self, i, display):
        draw.circle(display, (0, 0, 140), i.pos, 5)

    def hit (self, player, bullet):
        if player==bullet.player:
            return False
        pos1 = player.pos
        pos2 = bullet.endBulletPoint()
        return sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 ) <= player.ray

    def colide(self, thing1, thing2):
        pos1 = thing1.pos
        pos2 = thing2.pos
        ray = thing1.ray + thing2.ray
        return sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 ) <= ray

    def isInsideRect(self, pInicial, pFinal, point):
        return point[0]>pInicial[0] and point[1]>pInicial[1] and point[0]<pFinal[0] and point[1]<pFinal[1]

    def mouseOver(self):
        global step
        mpos = pygame.mouse.get_pos()
        # MOUSE IN GROUND
        for idx in range(10):
            xi = resolution[choseResolution][0] / 2 - 4 * step + (idx % 2) * step
            yi = 2 * step + int(idx/2) * step
            if mpos[0] > xi and mpos[1] > yi and mpos[0] < xi + step and mpos[1] < yi + step:
                return idx, -1, -1
        # MOUSE IN INVENTORY
        for idx in range(10):
            xi = resolution[choseResolution][0] / 2 - step + (idx % 2) * step
            yi = 2 * step + int(idx/2) * step
            if mpos[0] > xi and mpos[1] > yi and mpos[0] < xi + step and mpos[1] < yi + step:
                return -1, idx, -1
        # MOUSE IN EQUIPS
        for idx in range(3):
            xi = resolution[choseResolution][0] / 2 + 2 * step
            yi = 2 * step + idx * 2 * step
            if mpos[0] > xi and mpos[1] > yi and mpos[0] < xi + step and mpos[1] < yi + step:
                return -1, -1, idx
        return -1, -1, -1
