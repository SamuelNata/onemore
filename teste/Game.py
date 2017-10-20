import pygame
from pygame import display, draw
from domain.Player import Player
from domain.Bullet import Bullet
from math import sqrt

resolution = [(800, 600)]
choseResolution = 0

def start():
    pygame.init()
    p = Player((200,0,0))
    p.prepare()
    gameDisplay = display.set_mode( resolution[choseResolution] )
    display.set_caption('One More')
    clock = pygame.time.Clock()
    bullets = []
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            p.position = (p.position[0], p.position[1] - p.moveSpeed)
        if keys[pygame.K_s]:
            p.position = (p.position[0], p.position[1] + p.moveSpeed)
        if keys[pygame.K_a]:
            p.position = (p.position[0] - p.moveSpeed, p.position[1])
        if keys[pygame.K_d]:
            p.position = (p.position[0] + p.moveSpeed, p.position[1])
        if pygame.mouse.get_pressed()[0]==1:
            b = Bullet(p)
            b.startPosition = p.position
            b.size = 2
            b.direction = vetUnitario((pygame.mouse.get_pos()[0]-p.position[0], pygame.mouse.get_pos()[1]-p.position[1]))
            bullets.append(b)

        for bullet in bullets:
            drawBullet(bullet, gameDisplay)
            if bullet.die:
                bullets.remove(bullet)

        drawPlayer(p, gameDisplay)
        drawStatsPanel(p, gameDisplay)
        display.update()
        gameDisplay.fill((0,0,0))
        clock.tick(30)
    pygame.quit()

def module(v):
    return sqrt(v[1]**2+v[0]**2)

def vetUnitario(v):
    return (v[0]/module(v), v[1]/module(v))

def drawPlayer(p, display):
    r = 10
    draw.circle(display, p.color, p.position, r)
    life = pygame.Rect(p.position[0] - r, p.position[1]+20, r*2, 2)
    draw.rect(display, (0,200,0), life, 0)

def drawStatsPanel(p, display):
    res = resolution[choseResolution]
    bg = pygame.Rect(res[0]/4, res[1]*0.9, res[0]/2, res[1]/10)
    draw.rect(display, (50, 50 , 50), bg, 0)

    topMargin = 10
    sideMargin = 10
    life = pygame.Rect(bg.x + sideMargin, bg.y + topMargin, (bg.width - 2*sideMargin) * (p.hp/p.maxHp), 18)
    draw.rect(display, (0, 120, 0), life, 0)

    energy = pygame.Rect(life.x, life.y + 2*topMargin + 4, (bg.width - 2*sideMargin) * (p.energy/p.maxEnergy), 18)
    draw.rect(display, (100, 100, 0), energy, 0)

def drawBullet(b, display):
    draw.line(display, (100, 100, 0), b.startBulletPoint(), b.endBulletPoint(), b.size)

start()