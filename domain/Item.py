import pygame

class Item(pygame.sprite.Sprite):
    pos = (0,0)
    name = "item"
    consumable = True
    itemType = ""
    sprite = "/sprits/isp1.png"
    ray = 3
    mouseDrag = False

    def __init__(self):
        pass

    def apply(self, p):
        pass

