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
(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)
(BRICK, GRASS, BETON, ICE, WATER) = range(5)

game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '.', '.', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0', '.', '0', '1', '0'],
            ['0', '.', '.', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0', '.', '.', '1', '0'],
            ['0', '.', '.', '1', '.', '.', '.', '.', '.', '.', '0', '1', '1', '0', '.', '.', '.', '.', '0', '0'],
            ['0', '.', '.', '1', '.', '.', '.', '.', '.', '.', '0', '1', '1', '0', '.', '.', '.', '.', '.', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '.', '.', '.', '0', '0', '0', '0', '.', '.', '.', '.', '.', '0'],
            ['0', '.', '.', '.', '1', '1', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
            ['0', '0', '0', '.', '.', '1', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
            ['0', '1', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '.', '.', '.', '.', '0', '0', '0', '0', '0', '.', '0'],
            ['0', '0', '0', '1', '1', '1', '0', '.', '.', '.', '.', '.', '.', '1', '1', '1', '1', '1', '.', '0'],
            ['0', '0', '0', '1', '.', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
            ['0', '1', '1', '1', '.', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
            ['0', '1', '1', '1', '1', '1', '.', '.', '.', '.', '.', '.', '.', '1', '1', '1', '1', '1', '.', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            ]

def draw(entity):
    DISPLAY.blit(entity.image, (entity.rect.x, entity.rect.y))

def get_hit_list(rect, entities):
    return [entity for entity in entities if rect.colliderect(entity.rect)]

class Tile:
    def __init__(self, type, position):
        self.type = type
        self.images = [SPRITES.subsurface((256, 0, 16, 16)),
                       SPRITES.subsurface((272, 32, 16, 16)),
                       SPRITES.subsurface((256, 16, 16, 16)),
                       SPRITES.subsurface((288, 32, 16, 16)),
                       SPRITES.subsurface((256, 48, 16, 16))
                       ]
        self.rect = pygame.Rect(position[0], position[1], 16, 16)
        self.image = self.images[type]


class Tank:
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        self.image = SPRITES.subsurface((0, 0, 16, 16))
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[1], 16, 16)
        self.level = level
        self.moving_state = False

    def fire(self):
        if self.direction == DIRECTION_UP:
            bullets.append(Bullet(self.direction, (self.rect.x + 5, self.rect.y-4), self, self.level))
        if self.direction == DIRECTION_DOWN:
            bullets.append(Bullet(self.direction, (self.rect.x + 5, self.rect.y+16), self, self.level))
        if self.direction == DIRECTION_RIGHT:
            bullets.append(Bullet(self.direction, (self.rect.x + 16, self.rect.y+6), self, self.level))
        if self.direction == DIRECTION_LEFT:
            bullets.append(Bullet(self.direction, (self.rect.x - 4, self.rect.y+6), self, self.level))



class Player(Tank):
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, speed, direction, position, level)
        self.player_images = [SPRITES.subsurface((0, 0, 16, 16)),
                              SPRITES.subsurface((64, 0, 16, 16)),
                              SPRITES.subsurface((96, 0, 16, 16)),
                              SPRITES.subsurface((32, 0, 16, 16))]
        self.pressed_keys = [False] * 4

    def move(self):
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
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type != GRASS:
                    if self.direction == DIRECTION_DOWN:
                        self.rect.bottom = tile.rect.top
                    if self.direction == DIRECTION_UP:
                        self.rect.top = tile.rect.bottom
                    if self.direction == DIRECTION_RIGHT:
                        self.rect.right = tile.rect.left
                    if self.direction == DIRECTION_LEFT:
                        self.rect.left = tile.rect.right
class Enemy(Tank):
    global enemies
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, speed, direction, position, level)
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
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type != GRASS:
                    if self.direction == DIRECTION_DOWN:
                        self.rect.bottom = tile.rect.top
                    if self.direction == DIRECTION_UP:
                        self.rect.top = tile.rect.bottom
                    if self.direction == DIRECTION_RIGHT:
                        self.rect.right = tile.rect.left
                    if self.direction == DIRECTION_LEFT:
                        self.rect.left = tile.rect.right
                    self.direction = randrange(4)
                break

    def die(self):
        enemies.remove(self)

class Level:
    def __init__(self, game_map):
        self.map = []
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x] != '.':
                    self.map.append(Tile(int(game_map[y][x]), (x * 16, y * 16)))

bullets = []
current_level = Level(game_map)
player = Player(2, 0, (50, 50), current_level)
enemies = [Enemy(2, 0, (100, 150), current_level),
           Enemy(2, 0, (50, 150), current_level)]

class Bullet:
    global enemies, bullets
    def __init__(self, direction=DIRECTION_UP, position=None, owner=None, level=None):
        self.speed = 5
        self.direction = direction
        self.rect = pygame.Rect(position[0], position[1], 4, 4)
        self.images = [SPRITES.subsurface((322, 102, 4, 4)),
                       SPRITES.subsurface((338, 102, 4, 4)),
                       SPRITES.subsurface((346, 102, 4, 4)),
                       SPRITES.subsurface((330, 102, 4, 4))]
        self.image = self.images[self.direction]
        self.owner = owner
        self.level = level
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
                for tile in get_hit_list(self.rect, self.level.map):
                    if tile.type != GRASS:
                        self.flying = False
                        break
                for enemy in get_hit_list(self.rect, enemies):
                    enemy.die()
                    self.die()
            else:
                self.die()

    def die(self):
        bullets.remove(self)

main_menu()

while True:
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(player.image, (player.rect.x, player.rect.y))
    for enemy in enemies:
        draw(enemy)

    for bullet in bullets:
        draw(bullet)

    for tile in current_level.map:
        draw(tile)


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
