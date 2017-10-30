import pygame
from pygame import draw
from clientSide.Player import Player
from domain.Gun import Gun
from threading import Thread
from utils.Utils import RED, GREEN, BLUE, BLACK, WHITE, SKY, PURPLE, YELLOW, pointInsideRect, circlesCollide, squaresCollide, logf
import json


resolutions = [(800, 600)]
choseResolution = 0
resolution = resolutions[choseResolution]
step = resolution[0]/16
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 15)

choseResolution = 0
resolution = resolutions[choseResolution]


class Game(Thread):
    name = ''
    map = 0
    player = None
    players = []
    maxPlayerId = 0
    maxNumPlayers = 100
    items = []
    maxItemId = 0
    bullets = []
    maxBullerId = 0
    crashed = False
    screen = pygame.display
    id = -1
    skt = 1
    showInventory = False
    fpsCounter = 0
    lastDisplay = 0
    fps = 0
    serverData = []  # Data recived from the server

    def __init__(self, name, map, socket, id):
        Thread.__init__(self)
        self.name = name
        self.map = map
        self.player = Player(BLUE)
        self.skt = socket
        self.id = id
        self.dataCapture = DataCapture(self.skt, self.serverData, [self.crashed])

    def run(self):
        self.player.prepare()
        self.players.append(self.player)

        self.dataCapture.start()

        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Survival\'s King')
        clock = pygame.time.Clock()
        pygame.init()

        crashed = False
        while not crashed:
            self.handleUpdates()
            clock.tick(30)
        pygame.quit()
        self.dataCapture.join()

    def handleControls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.crashed = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.crashed = True
        self.showInventory = True if keys[pygame.K_f] else False
        if keys[pygame.K_w]:
            self.player.pos = (self.player.pos[0], self.player.pos[1] - self.player.moveSpeed)
        if keys[pygame.K_s]:
            self.player.pos = (self.player.pos[0], self.player.pos[1] + self.player.moveSpeed)
        if keys[pygame.K_a]:
            self.player.pos = (self.player.pos[0] - self.player.moveSpeed, self.player.pos[1])
        if keys[pygame.K_d]:
            self.player.pos = (self.player.pos[0] + self.player.moveSpeed, self.player.pos[1])
        if pygame.mouse.get_pressed()[0] == 1:
            if keys[pygame.K_f]:
                gr, it, eq = self.mouseOver()
                if 0 <= it < len(self.player.itens):
                    pass
                if 0 <= gr < len(self.player.ground):
                    self.player.itens.append(self.player.ground[gr])
                    self.items.remove(self.player.ground[gr])
                if 0 <= eq <= len(self.player.itens):
                    pass
            # else:
            #     self.player.equipedGun.fire(self.player, self.player.pos,
            #                       (pygame.mouse.get_pos()[0] - self.player.pos[0], pygame.mouse.get_pos()[1] - self.player.pos[1]), self.bullets)

    def handleUpdates(self):
        self.updateFromServer()
        self.handleControls()
        self.localPlayerUpdate()
        self.sendUpdatesToServer()

    def localPlayerUpdate(self):
        for player in self.players:
            player.ground = []
            for bullet in self.bullets:
                if bullet.player != self.player and circlesCollide((player.pos, player.ray), ((bullet.pos), 0)):
                    player.takeShot(bullet)
                if bullet.die:
                    self.bullets.remove(bullet)
            for item in self.items:
                if circlesCollide(((player.pos), player.ray), ((item.pos), 3)):
                    player.ground.append(item)

    def updateFromServer(self):
        while len(self.serverData):
            response = self.serverData.pop(0)
            if response["state"] != "gaming":
                logf("Client: Locks like you are not inside a game")
                self.crashed = True
            else:
                value = response["value"]
                p = self.getPlayer(value["addr"])
                if not p:
                    logf("Client: There is IP that is not gaming, but a recive data about he. Lets create he")
                    p = Player(WHITE)
                    p.prepare()
                p.pos = value["pos"]

    def sendUpdatesToServer(self):
        response = {"state": "gaming", "value": {"gameId": self.id, "actions": [], "pos": self.player.pos}}
        self.skt.sendto(json.dumps(response).encode(), ("::1", 5000))

    def getPlayer(self, addr):
        for player in self.players:
            if player.addr == addr:
                return player
        return None

    def mouseOver(self):
        global step
        global resolution
        mpos = pygame.mouse.get_pos()
        # MOUSE IN GROUND
        for idx in range(10):
            xi = resolution[0] / 2 - 4 * step + (idx % 2) * step
            yi = 2 * step + int(idx / 2) * step
            if xi < mpos[0] < xi + step and yi < mpos[1] < yi + step:
                return (idx, -1, -1)
        # MOUSE IN INVENTORY
        for idx in range(10):
            xi = resolution[0] / 2 - step + (idx % 2) * step
            yi = 2 * step + int(idx / 2) * step
            if xi < mpos[0] < xi + step and yi < mpos[1] < yi + step:
                return (-1, idx, -1)
        # MOUSE IN EQUIPS
        for idx in range(3):
            xi = resolution[0] / 2 + 2 * step
            yi = 2 * step + idx * 2 * step
            if xi < mpos[0] < xi + step and yi < mpos[1] < yi + step:
                return (-1, -1, idx)
        return (-1, -1, -1)

    def drawAll(self):
        for item in self.items:
            self.drawItem(item)

        self.drawStatsPanel(self.player)

        if self.showInventory:
            self.drawInventory(self.player.itens, self.player.ground)

        self.fpsCounter += 1
        if pygame.time.get_ticks()-self.lastDisplay>=1000:
            self.lastDisplay = pygame.time.get_ticks()
            self.fps = self.fpsCounter
            self.fpsCounter = 0

        fpsText = font.render('FPS: ' + str(self.fps), False, (200, 200, 200))
        self.screen.blit(fpsText, (10, 10))

        self.screen.update()
        self.screen.fill((0,0,0))

    def drawPlayer(self, p):
        if p.hp > 0:
            draw.circle(self.screen, p.color, p.pos, p.ray)
            #  draw.circle(display, (0,0,0), p.pos, 2)
            life = pygame.Rect(p.pos[0] - p.ray, p.pos[1]+20, p.ray*2*(p.hp/p.maxHp), 2)
            draw.rect(self.screen, (0, 200, 0), life, 0)

    def drawStatsPanel(self, p):
        res = resolution[choseResolution]
        bg = pygame.Rect(res[0]/4, res[1]*0.9, res[0]/2, res[1]/10)
        draw.rect(self.screen, (50, 50, 50), bg, 0)

        topMargin = 10
        sideMargin = 10
        life = pygame.Rect(bg.x + sideMargin, bg.y + topMargin, (bg.width - 2*sideMargin) * (p.hp/p.maxHp), 18)
        draw.rect(self.screen, (0, 120, 0), life, 0)

        energy = pygame.Rect(life.x, life.y + 2*topMargin + 4, (bg.width - 2*sideMargin) * (p.energy/p.maxEnergy), 18)
        draw.rect(self.screen, (100, 100, 0), energy, 0)

        gunRay = 30
        draw.circle(self.screen, (50, 50, 50), (int(res[0]/4-gunRay), res[1]-gunRay), gunRay, 0)

    def drawInventory(self, itens, ground):
        global step
        # GROUND GRIDS
        for idx in range(10):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - 4 * step + (idx % 2) * step,
                               2 * step + int(idx/2) * step, step, step)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)
        # GROUND ACCECIBLE ITENS
        for idx, item in enumerate(ground):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - 4 * step + (idx % 2) * step + .2 * step,
                               2 * step + int(idx/2) * step + .2 * step, step*.6, step*.6)
            pygame.draw.rect(self.screen, (70, 20, 20), rect, 0)

        # INVENTORY GRIDS
        for idx in range(10):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - step + (idx % 2) * step,
                               2 * step + int(idx/2) * step, step, step)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)
        # INVENTOTY ITENS
        for idx, item in enumerate(itens):
            rect = pygame.Rect(resolution[choseResolution][0] / 2 - step + (idx % 2) * step + .2 * step,
                               2 * step + int(idx/2) * step + .2 * step, step*.6, step*.6)
            pygame.draw.rect(self.screen, (100, 50, 50), rect, 0)

        # HELMET GRID
        rect = pygame.Rect(resolution[choseResolution][0] / 2 + 2 * step,
                           2 * step, step, step)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)
        # ARMOR GRID
        rect = pygame.Rect(resolution[choseResolution][0] / 2 + 2 * step,
                           4 * step, step, step)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)
        # GUN GRID
        rect = pygame.Rect(resolution[choseResolution][0] / 2 + 2 * step,
                           6 * step, step, step)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)

    def drawBullet(self, b):
        draw.line(self.screen, (100, 100, 0), b.startBulletPoint(), b.endBulletPoint(), b.size)

    def drawItem(self, i):
        draw.circle(self.screen, (0, 0, 140), i.pos, 5)


class DataCapture(Thread):

    def __init__(self, socket, serverData, crashed):
        Thread.__init__(self)
        self.skt = socket
        self.serverData = serverData
        self.crashed = crashed

    def run(self):
        while not self.crashed[0]:
            data = json.loads(self.skt.recvfrom(1024)[0].decode())
            self.serverData.append(data)
            # if data["state"] == "exit": return

