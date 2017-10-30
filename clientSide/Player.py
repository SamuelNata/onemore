from domain.Gun import Gun
import pygame

class Player():
    hp = 0
    maxHp = 1
    energy = 0
    maxEnergy = 1
    itens = []
    pos = (50, 50)
    equipedGun = Gun()
    equipedHelmet = None
    equipedArmor = None
    itens = []
    color = (250,0,0)
    moveSpeed = 5
    ray = 10
    dead = False
    ground = []
    lastUpdate = pygame.time.get_ticks()
    addr = -1

    def __init__(self, color):
        self.color = color

    def prepare(self):
        self.maxHp = 1000
        self.hp = self.maxHp
        self.maxEnergy = 500
        self.energy = self.maxEnergy
        self.moveSpeed = 5

    def takeShot(self, bullet):
        self.hp -= 10
        bullet.die = True

