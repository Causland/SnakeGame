import sys
import pygame
from random import randrange
from Tile import Tile
from Snake import Snake


class Color:
    black = (0,0,0)
    white = (255,255,255)
    blue_outline = (22,50,76)


class Direction:
    left = [-1, 0]
    right = [1, 0]
    up = [0, -1]
    down = [0, 1]


def check_events(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and snake.direction != Direction.down: snake.set_direction(Direction.up)
            elif keys[pygame.K_DOWN] and snake.direction != Direction.up: snake.set_direction(Direction.down)
            elif keys[pygame.K_RIGHT] and snake.direction != Direction.left: snake.set_direction(Direction.right)
            elif keys[pygame.K_LEFT] and snake.direction != Direction.right: snake.set_direction(Direction.left)

def check_snake_collision(snake):
    if snake.parts[-1].collidelist(snake.parts[0:-1]) > -1:
        return True
    return False

def check_wall_collision(snake, playarea):
    return not snake.parts[-1].colliderect(playarea)

def check_apple_collision(snake, apple):
    return snake.parts[-1].colliderect(apple.rect)

def get_random_location(tiles_wide, tiles_high, tile_size):
    return (randrange(tiles_wide)*tile_size[0]+tile_size[0], randrange(tiles_high)*tile_size[1]+tile_size[1])


# Configure the game window and assets
pygame.init()
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

tile_size = pygame.image.load("assets/Snake.png").get_size()
tiles_wide = 39
tiles_high = 29

window_size = window_width, window_height = tile_size[0]*tiles_wide, tile_size[1]*tiles_high
window = pygame.display.set_mode(window_size)
window.fill(Color.blue_outline)

playarea_width, playarea_height = window_width-tile_size[0]*2, window_height-tile_size[1]*2
playarea_rect = pygame.Rect(tile_size[0], tile_size[1], playarea_width, playarea_height)
window.fill(Color.black, playarea_rect)

apple = Tile("assets/Apple.png", get_random_location(tiles_wide-2, tiles_high-2, tile_size))
snake = Snake("assets/Snake.png", get_random_location(tiles_wide-2, tiles_high-2, tile_size))
death = Tile("assets/Death.png", (-1*tile_size[0], -1*tile_size[1]))

font = pygame.font.Font('freesansbold.ttf', 26)
text = font.render(f"Length: 1", True, Color.white)
text_rect = text.get_rect()
text_rect.center = (window_width/2, window_height-tile_size[1]/2)

while True:
    clock.tick(12)

    # Check for an event
    check_events(snake)


    # End game conditions
    if check_snake_collision(snake):
        death.set_location(snake.parts[-1].topleft)
        death.show(window)
        pygame.display.flip()
        break

    if check_wall_collision(snake, playarea_rect):
        death.set_location(snake.parts[-1].topleft)
        death.show(window)
        pygame.display.flip()
        break

    # Apple eaten
    if check_apple_collision(snake, apple):
        while True:
            apple.set_location(get_random_location(tiles_wide-2, tiles_high-2, tile_size))
            if apple.rect.collidelist(snake.parts) == -1:
                break
        snake.inc_length(4)
        text = font.render(f"Length: {snake.length}", True, Color.white)

    # Move snake
    snake.move()

    window.fill(Color.blue_outline)
    window.blit(text, text_rect)
    window.fill(Color.black, playarea_rect)
    snake.show(window)
    apple.show(window)
    pygame.display.flip()

sys.exit()