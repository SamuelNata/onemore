import pygame
from pygame import display, draw
from domain.Player import Player

resolution = [(800, 600)]
def start():
    pygame.init()
    p = Player((200,0,0))
    p.prepare()
    gameDisplay = display.set_mode( resolution[0] )
    display.set_caption('One More')
    clock = pygame.time.Clock()

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

        draw.circle(gameDisplay, p.color, p.position, 10)

        display.update()
        gameDisplay.fill((0,0,0))
        clock.tick(30)
    pygame.quit()


def drawPlayer(p, display):
    draw.circle(display, p.color, p.position,  10)
    # life = pygame.Rect(p.x-1, p.y-1, 12, 2)
    # display.blit(life, p.position)

start()