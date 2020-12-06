import pygame
from GameCore import GameCore

pygame.init()

game = GameCore(True)

playing = True
while playing:
    playing = game.update_game_state()


