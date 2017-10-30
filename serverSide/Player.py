from domain.Gun import Gun
import pygame

class Player():
    pos = (50, 50)
    moveSpeed = 5
    ray = 10
    dead = False
    collor = (70, 70, 70)
    client = 0

    def __init__(self, client):
        self.client = client


