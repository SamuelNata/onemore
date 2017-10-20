import pygame

class Bullet():
    bornTime = 0
    startPosition = (0, 0)
    range = 300
    acurracy = 5
    size = 1
    direction = (1, 1)
    player = None
    die = False
    lifeTime = 500

    def __init__(self, p):
        self.bornTime = pygame.time.get_ticks()
        self.player = p

    def endPosition(self):
        return (self.startPosition[0]+self.direction[0]*self.range,
                self.startPosition[1]+self.direction[1]*self.range)

    def startBulletPoint(self):
        deltaTime = (pygame.time.get_ticks() - self.bornTime - self.lifeTime/10)
        deltaTime = 0 if deltaTime<0 else deltaTime
        return (
            self.startPosition[0] + self.direction[0] * 0.9 * self.range * deltaTime / self.lifeTime,
            self.startPosition[1] + self.direction[1] * 0.9 * self.range * deltaTime / self.lifeTime)

    def endBulletPoint(self):
        deltaTime = (pygame.time.get_ticks() - self.bornTime)
        deltaTime = 0 if deltaTime < 0 else deltaTime
        self.die = True if deltaTime>=self.lifeTime else False
        return (
            self.startPosition[0] + self.direction[0] * 0.9 * self.range * deltaTime / self.lifeTime,
            self.startPosition[1] + self.direction[1] * 0.9 * self.range * deltaTime / self.lifeTime)
