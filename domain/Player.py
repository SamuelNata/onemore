from domain.Gun import Gun
import pygame

class Player():
    hp = 0
    maxHp = 0
    energy = 0
    maxEnergy = 0
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

    def __init__(self, color):
        self.color = color

    def prepare(self):
        self.maxHp = 100
        self.hp = self.maxHp
        self.maxEnergy = 100
        self.energy = self.maxEnergy
        self.moveSpeed = 5

    def takeShot(self, bullet):
        self.hp -= 10
        bullet.die = True

