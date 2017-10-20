import utils.Utils as Utils
from domain.Bullet import Bullet
import pygame


class Gun():
    range = 300
    acurracy = 5
    maxLoad = 50
    load = 50
    bulletSize = 2
    lastShotTime = 0
    sps = 4 #Shots Per Second
    damage = 10


    def __init__(self):
        pass

    def fire(self, shotter, startPoint, direction, bulletsToDraw):
        if pygame.time.get_ticks()-self.lastShotTime > 1000/self.sps:
            b = Bullet()
            b.player = shotter
            b.damage = self.damage
            b.startPosition = startPoint
            b.size = self.bulletSize
            b.direction = Utils.vetUnitario(direction)
            # MAKE ACURRACY AS BELLOW
            # b.direction = ( b.direction[0] + b.direction[0]*rand()/self.acurracy , b.direction[1] + b.direction[1]*rand()/self.acurracy )
            b.range = 300
            bulletsToDraw.append(b)
            self.lastShotTime = pygame.time.get_ticks()

