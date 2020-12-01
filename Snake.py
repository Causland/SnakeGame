import pygame
from Tile import Tile
from random import randrange

class Snake(Tile):

    def __init__(self, asset, topleft):
        Tile.__init__(self, asset, topleft)
        self.length = 1
        self.direction = [0, 0]
        self.parts = [self.rect]

    def move(self):
        self.parts.append(self.parts[-1].move([self.direction[0]*self.size[0],self.direction[1]*self.size[1]]))
        if(len(self.parts) > self.length):
            self.parts.pop(0)

    def set_direction(self, direction):
        self.direction = direction

    def inc_length(self, inc):
        self.length += inc

    def show(self, screen):
        for rect in self.parts:
            screen.blit(self.image, rect)