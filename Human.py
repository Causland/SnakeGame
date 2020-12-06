import pygame
from GameCore import GameCore

pygame.init()
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

game = GameCore(True)

while True:
    clock.tick(12)

    game.check_events()

    if game.check_snake_collision():
        game.trigger_death()
        break

    if game.check_wall_collision():
        game.trigger_death()
        break

    if game.check_apple_collision():
        game.move_apple()
    

    game.update_game_state()


