import pygame, sys
from menu import main_menu

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *

pygame.init()  # initialize pygame

pygame.display.set_caption('Battle City')  # set the windo  w name

WINDOW_SIZE = (600, 480)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize the window

display = pygame.Surface((320, 240))

sprites = pygame.image.load('sprite.png').convert_alpha()
bullet_image = sprites.subsurface((320, 96, 16, 16))

(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)

moving_right = False
moving_left = False
moving_up = False
moving_down = False

grass_image = sprites.subsurface((272, 32, 16, 16))
TILE_SIZE = grass_image.get_width()
brick_image = sprites.subsurface((256, 0, 16, 16))

game_map = [['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1', '2'],
            ['2', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0', '1', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '2', '1', '1', '2', '0', '2', '0', '2', '2', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '2', '1', '1', '2', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '0', '0', '0', '2', '2', '2', '2', '0', '0', '0', '0', '2', '2'],
            ['2', '0', '0', '0', '1', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '0', '0', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
            ]

tiles = []


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list


class Tank:
    def __init__(self, speed=2, direction=DIRECTION_UP, image=sprites.subsurface((0, 0, 16, 16)), position=(50, 50)):
        self.image = image
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[0], 16, 16)
        self.player_images = [sprites.subsurface((0, 0, 16, 16)),
                              sprites.subsurface((64, 0, 16, 16)),
                              sprites.subsurface((96, 0, 16, 16)),
                              sprites.subsurface((32, 0, 16, 16))]
        self.moving_state = False


class Player(Tank):
    def __init__(self, speed=2, direction=DIRECTION_UP, image=sprites.subsurface((0, 0, 16, 16)), position=(50, 50)):
        Tank.__init__(self, speed=2, direction=DIRECTION_UP, image=sprites.subsurface((0, 0, 16, 16)), position=(50, 50))
        self.pressed_keys = [False] * 4

    def move(self):
        # collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        for direction in range(4):
            if self.pressed_keys[direction]:
                self.direction = direction
                self.image = self.player_images[direction]
                self.moving_state = True
                break
        else:
            self.moving_state = False
        if self.moving_state:
            if 0 <= self.rect.x <= display.get_width() - self.image.get_width():
                if self.direction == DIRECTION_LEFT:
                    self.rect.x -= self.speed
                if self.direction == DIRECTION_RIGHT:
                    self.rect.x += self.speed
            if 0 <= self.rect.y <= display.get_height() - self.image.get_height():
                if self.direction == DIRECTION_UP:
                    self.rect.y -= self.speed
                if self.direction == DIRECTION_DOWN:
                    self.rect.y += self.speed
            hit_list = collision_test(self.rect, tiles)
            for tile in hit_list:
                if tile[1] != '1':
                    if self.direction == DIRECTION_DOWN:
                        self.rect.bottom = tile[0].top
                    if self.direction == DIRECTION_UP:
                        self.rect.top = tile[0].bottom
                    if self.direction == DIRECTION_RIGHT:
                        self.rect.right = tile[0].left
                    if self.direction == DIRECTION_LEFT:
                        self.rect.left = tile[0].right

player = Player(2, 0, sprites.subsurface((0, 0, 16, 16)), (50, 50))

class Bullet:
    def __init__(self, speed=5, direction=DIRECTION_UP, image=bullet_image, position=(player.rect.x, player.rect.y)):
        self.image = image
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[1], bullet_image.get_width(), bullet_image.get_height())


main_menu()

while True:
    display.fill((0, 0, 0))

    display.blit(player.image, (player.rect.x, player.rect.y))
    tiles = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(brick_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tiles.append((pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), tile))
            x += 1
        y += 1

    player.move()

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.pressed_keys[DIRECTION_RIGHT] = True
            if event.key == K_LEFT:
                player.pressed_keys[DIRECTION_LEFT] = True
            if event.key == K_UP:
                player.pressed_keys[DIRECTION_UP] = True
            if event.key == K_DOWN:
                player.pressed_keys[DIRECTION_DOWN] = True
            if event.key == K_ESCAPE:
                main_menu()
                player.rect.x = 50
                player.rect.y = 50
                player.image = sprites.subsurface((0, 0, 16, 16))
            if event.key == K_SPACE:
                bullet = Bullet(5, player.direction, bullet_image, (player.rect.x, player.rect.y))
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.pressed_keys[DIRECTION_RIGHT] = False
            if event.key == K_LEFT:
                player.pressed_keys[DIRECTION_LEFT] = False
            if event.key == K_UP:
                player.pressed_keys[DIRECTION_UP] = False
            if event.key == K_DOWN:
                player.pressed_keys[DIRECTION_DOWN] = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
