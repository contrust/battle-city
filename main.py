import pygame, sys
from menu import main_menu
from pygame.locals import *
from random import randrange
CLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Battle City')
WINDOW_SIZE = (600, 480)
SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
DISPLAY = pygame.Surface((320, 240))
SPRITES = pygame.image.load('sprite.png').convert_alpha()
bullet_image = SPRITES.subsurface((320, 96, 16, 16))
grass_image = SPRITES.subsurface((272, 32, 16, 16))
TILE_SIZE = grass_image.get_width()
brick_image = SPRITES.subsurface((256, 0, 16, 16))
(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)

game_map = [['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', 'q', '2', '1', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0', '1', '2'],
            ['2', '0', '0', '1', '0', '0', '0', '0', '0', '0', '2', '1', '1', '2', '0', '0', '0', '0', '2', '2'],
            ['2', '0', '0', '1', '0', '0', '0', '0', '0', '0', '2', '1', '1', '2', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '0', '0', '0', '2', '2', '2', '2', '0', '0', '0', '0', '0', '2'],
            ['2', '0', '0', '0', '1', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '0', '0', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '2', '2', '0', '0', '0', '0', '2', '2', '2', '2', '2', '0', '2'],
            ['2', '2', '2', '1', '1', '1', '2', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '2'],
            ['2', '2', '2', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2']
            ]

tiles = []


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list


class Tank:
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50)):
        self.image = SPRITES.subsurface((0, 0, 16, 16))
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[1], 16, 16)
        self.moving_state = False

    def fire(self):
        bullets.append(Bullet(5, self.direction, (self.rect.x, self.rect.y)))



class Player(Tank):
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50)):
        Tank.__init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50))
        self.player_images = [SPRITES.subsurface((0, 0, 16, 16)),
                              SPRITES.subsurface((64, 0, 16, 16)),
                              SPRITES.subsurface((96, 0, 16, 16)),
                              SPRITES.subsurface((32, 0, 16, 16))]
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
            if 0 <= self.rect.x <= DISPLAY.get_width() - self.image.get_width():
                if self.direction == DIRECTION_LEFT:
                    self.rect.x -= self.speed
                if self.direction == DIRECTION_RIGHT:
                    self.rect.x += self.speed
            if 0 <= self.rect.y <= DISPLAY.get_height() - self.image.get_height():
                if self.direction == DIRECTION_UP:
                    self.rect.y -= self.speed
                if self.direction == DIRECTION_DOWN:
                    self.rect.y += self.speed
            for tile in collision_test(self.rect, tiles):
                if tile[1] != '1':
                    if self.direction == DIRECTION_DOWN:
                        self.rect.bottom = tile[0].top
                    if self.direction == DIRECTION_UP:
                        self.rect.top = tile[0].bottom
                    if self.direction == DIRECTION_RIGHT:
                        self.rect.right = tile[0].left
                    if self.direction == DIRECTION_LEFT:
                        self.rect.left = tile[0].right
class Enemy(Tank):
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50)):
        Tank.__init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50))
        self.enemy_images = [SPRITES.subsurface((128, 0, 16, 16)),
                              SPRITES.subsurface((192, 0, 16, 16)),
                              SPRITES.subsurface((224, 0, 16, 16)),
                              SPRITES.subsurface((160, 0, 16, 16))]

    def move_stupidly(self):
            self.image = self.enemy_images[self.direction]
            if 0 <= self.rect.x <= DISPLAY.get_width() - self.image.get_width():
                if self.direction == DIRECTION_LEFT:
                    self.rect.x -= self.speed
                if self.direction == DIRECTION_RIGHT:
                    self.rect.x += self.speed
            if 0 <= self.rect.y <= DISPLAY.get_height() - self.image.get_height():
                if self.direction == DIRECTION_UP:
                    self.rect.y -= self.speed
                if self.direction == DIRECTION_DOWN:
                    self.rect.y += self.speed
            for tile in collision_test(self.rect, tiles):
                if tile[1] != '1':
                    if self.direction == DIRECTION_DOWN:
                        self.rect.bottom = tile[0].top
                    if self.direction == DIRECTION_UP:
                        self.rect.top = tile[0].bottom
                    if self.direction == DIRECTION_RIGHT:
                        self.rect.right = tile[0].left
                    if self.direction == DIRECTION_LEFT:
                        self.rect.left = tile[0].right
                    self.direction = randrange(4)
                break
        


player = Player(2, 0, (50, 50))
enemies = [Enemy(2, 0, (100, 150)),
           Enemy(2, 0, (50, 150))]
bullets = []

class Bullet:
    def __init__(self, speed=5, direction=DIRECTION_UP, position=(player.rect.x, player.rect.y)):
        self.image = bullet_image
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[1], bullet_image.get_width(), bullet_image.get_height())
        self.images = [SPRITES.subsurface((320, 100, 8, 8)),
                       SPRITES.subsurface((336, 100, 8, 8)),
                       SPRITES.subsurface((344, 100, 8, 8)),
                       SPRITES.subsurface((328, 100, 8, 8))]
        self.flying = True

    def fly(self):
            if self.flying:
                self.image = self.images[self.direction]
                if 0 <= self.rect.x <= DISPLAY.get_width() - self.image.get_width():
                    if self.direction == DIRECTION_LEFT:
                        self.rect.x -= self.speed
                    if self.direction == DIRECTION_RIGHT:
                        self.rect.x += self.speed
                if 0 <= self.rect.y <= DISPLAY.get_height() - self.image.get_height():
                    if self.direction == DIRECTION_UP:
                        self.rect.y -= self.speed
                    if self.direction == DIRECTION_DOWN:
                        self.rect.y += self.speed
                for tile in collision_test(self.rect, tiles):
                    if tile[1] != '1':
                        self.flying = False
                        break
            else:
                bullets.remove(self)

main_menu()

while True:
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(player.image, (player.rect.x, player.rect.y))
    for enemy in enemies:
        DISPLAY.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
    for bullet in bullets:
        DISPLAY.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
    tiles = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                DISPLAY.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                DISPLAY.blit(brick_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tiles.append((pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), tile))
            x += 1
        y += 1

    player.move()
    for enemy in enemies:
        enemy.move_stupidly()
    for bullet in bullets[:]:
        bullet.fly()

    for event in pygame.event.get():
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
                player.image = SPRITES.subsurface((0, 0, 16, 16))
            if event.key == K_SPACE:
                player.fire()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                player.pressed_keys[DIRECTION_RIGHT] = False
            if event.key == K_LEFT:
                player.pressed_keys[DIRECTION_LEFT] = False
            if event.key == K_UP:
                player.pressed_keys[DIRECTION_UP] = False
            if event.key == K_DOWN:
                player.pressed_keys[DIRECTION_DOWN] = False

    surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
    SCREEN.blit(surf, (0, 0))
    pygame.display.update()
    CLOCK.tick(60)
