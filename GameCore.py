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

class GameCore:

    def __init__(self, display):
        self.display_on = display

        self.tile_size = pygame.image.load("assets/Snake.png").get_size()
        self.tiles_wide = 39
        self.tiles_high = 29

        self.window_size = self.window_width, self.window_height = self.tile_size[0]*self.tiles_wide, self.tile_size[1]*self.tiles_high

        self.playarea_width, self.playarea_height = self.window_width-self.tile_size[0]*2, self.window_height-self.tile_size[1]*2
        self.playarea_rect = pygame.Rect(self.tile_size[0], self.tile_size[1], self.playarea_width, self.playarea_height)
        
        self.apple = Tile("assets/Apple.png", self.get_random_location())
        self.snake = Snake("assets/Snake.png", self.get_random_location())
        
        #Non-Core optional display assets
        if display:
            self.window = pygame.display.set_mode(self.window_size)
            self.window.fill(Color.blue_outline)
            self.window.fill(Color.black, self.playarea_rect)
            self.death = Tile("assets/Death.png", (-1*self.tile_size[0], -1*self.tile_size[1]))
            self.font = pygame.font.Font('freesansbold.ttf', 26)
            self.text = self.font.render(f"Length: 1", True, Color.white)
            self.text_rect = self.text.get_rect()
            self.text_rect.center = (self.window_width/2, self.window_height-self.tile_size[1]/2)

    def reset(self):
        self.apple = Tile("assets/Apple.png", self.get_random_location())
        self.snake = Snake("assets/Snake.png", self.get_random_location())

        if self.display_on:
            self.death = Tile("assets/Death.png", (-1*self.tile_size[0], -1*self.tile_size[1]))
            self.text = self.font.render(f"Length: 1", True, Color.white)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and self.snake.direction != Direction.down: self.snake.set_direction(Direction.up)
                elif keys[pygame.K_DOWN] and self.snake.direction != Direction.up: self.snake.set_direction(Direction.down)
                elif keys[pygame.K_RIGHT] and self.snake.direction != Direction.left: self.snake.set_direction(Direction.right)
                elif keys[pygame.K_LEFT] and self.snake.direction != Direction.right: self.snake.set_direction(Direction.left)

    def check_snake_collision(self):
        if self.snake.parts[-1].collidelist(self.snake.parts[0:-1]) > -1:
            return True
        return False

    def check_wall_collision(self):
        return not self.snake.parts[-1].colliderect(self.playarea_rect)

    def check_apple_collision(self):
        return self.snake.parts[-1].colliderect(self.apple.rect)

    def get_random_location(self):
        return (randrange(self.tiles_wide-2)*self.tile_size[0]+self.tile_size[0], randrange(self.tiles_high-2)*self.tile_size[1]+self.tile_size[1])

    def trigger_death(self):
        self.death.set_location(self.snake.parts[-1].topleft)
        self.death.show(self.window)
        pygame.display.flip()

    def move_apple(self):
        while True:
            self.apple.set_location(self.get_random_location())
            if self.apple.rect.collidelist(self.snake.parts) == -1:
                break
        self.snake.inc_length(4)

        if self.display_on:
            self.text = self.font.render(f"Length: {self.snake.length}", True, Color.white)

    def update_game_state(self):
        self.snake.move()

        if self.display_on:
            self.window.fill(Color.blue_outline)
            self.window.blit(self.text, self.text_rect)
            self.window.fill(Color.black, self.playarea_rect)
            self.snake.show(self.window)
            self.apple.show(self.window)
            pygame.display.flip()

