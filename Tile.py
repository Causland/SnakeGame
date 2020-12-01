import pygame

class Tile:
    def __init__(self, asset, topleft):
        self.image = pygame.image.load(asset)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        
        self.set_location(topleft)

    def set_location(self, topleft):
        self.rect.topleft = topleft
        
    def show(self, screen):
        screen.blit(self.image, self.rect)
