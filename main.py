import pygame, sys, threading
from menu import main_menu
from pygame.locals import *
from random import randrange
CLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Battle City')
WINDOW_SIZE = (400, 400)
SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
DISPLAY = pygame.Surface((208, 224))
SPRITES = pygame.image.load('sprite.png').convert_alpha()
BOLD_SPRITES = pygame.image.load('sprite1.png')
(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)
(BRICK, GRASS, BETON, ICE, WATER) = range(5)
(HELMET, TIMES, SHOVEL, STAR, GRENADE, TANK_BONUS) = range(6)

game_map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '.', '.', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['0', '.', '.', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['0', '.', '.', '1', '.', '.', '.', '.', '.', '.', '0', '1', '1'],
            ['0', '.', '.', '1', '.', '.', '.', '.', '.', '.', '0', '1', '1'],
            ['0', '0', '0', '0', '0', '0', '0', '.', '.', '.', '0', '0', '0'],
            ['0', '.', '.', '.', '1', '1', '0', '.', '.', '.', '.', '.', '.'],
            ['0', '0', '0', '.', '.', '1', '0', '.', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '0', '0', '0', '0', '0', '0', '.', '.', '.', '.'],
            ['0', '1', '1', '0', '1', '1', '0', '.', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '0', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ]

def draw(entity):
    DISPLAY.blit(entity.image, (entity.rect.x, entity.rect.y))

def get_hit_list(rect, entities):
    return [entity for entity in entities if rect.colliderect(entity.rect)]

class Tile:
    def __init__(self, type, position):
        self.type = type
        self.images = [BOLD_SPRITES.subsurface((256, 0, 8, 8)),
                       BOLD_SPRITES.subsurface((272, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((256, 16, 8, 8)),
                       BOLD_SPRITES.subsurface((288, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((256, 48, 16, 16))
                       ]
        if type == BRICK or type == BETON:
            self.rect = pygame.Rect(position[0], position[1], 8, 8)
        else:
            self.rect = pygame.Rect(position[0], position[1], 16, 16)
        self.image = self.images[type]
class Castle:
    def __init__(self):
        self.images = [BOLD_SPRITES.subsurface((304, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((320, 32, 16, 16))]
        self.image = self.images[0]
        self.rect = pygame.Rect(96, 208, 16, 16)

    def die(self):
        self.image = self.images[1]
class Tank:
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        self.x = position[0]
        self.y = position[1]
        self.image = SPRITES.subsurface((0, 0, 16, 16))
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.level = level
        self.moving_state = False

    def fire(self):
        if self.direction == DIRECTION_UP:
            bullets.append(Bullet(self.direction, (self.rect.x + 5, self.rect.y), self, self.level))
        if self.direction == DIRECTION_DOWN:
            bullets.append(Bullet(self.direction, (self.rect.x + 5, self.rect.y+12), self, self.level))
        if self.direction == DIRECTION_RIGHT:
            bullets.append(Bullet(self.direction, (self.rect.x + 12, self.rect.y+6), self, self.level))
        if self.direction == DIRECTION_LEFT:
            bullets.append(Bullet(self.direction, (self.rect.x, self.rect.y+6), self, self.level))

    def make_step(self):
        if self.direction == DIRECTION_LEFT:
            self.x -= self.speed
        if self.direction == DIRECTION_RIGHT:
            self.x += self.speed
        if self.direction == DIRECTION_UP:
            self.y -= self.speed
        if self.direction == DIRECTION_DOWN:
            self.y += self.speed
        self.rect.topleft = round(self.x), round(self.y)

    def align_collision(self, entity):
        if self.direction == DIRECTION_DOWN:
            self.rect.bottom = entity.rect.top
        if self.direction == DIRECTION_UP:
            self.rect.top = entity.rect.bottom
        if self.direction == DIRECTION_RIGHT:
            self.rect.right = entity.rect.left
        if self.direction == DIRECTION_LEFT:
            self.rect.left = entity.rect.right
        self.x, self.y = self.rect.topleft

    def turn_back(self):
        self.direction = 2 * (self.direction // 2) + (self.direction + 1) % 2

    def on_map(self):
        return 0 <= self.x <= DISPLAY.get_width() - self.image.get_width() and 0 <= self.y <= DISPLAY.get_height() - self.image.get_height()

    def return_on_map(self):
            if self.x < 0: self.x = 0
            if self.x > DISPLAY.get_width() - self.image.get_width(): self.x = DISPLAY.get_width() - self.image.get_width()
            if self.y < 0: self.y = 0
            if self.y > DISPLAY.get_height() - self.image.get_height(): self.y = DISPLAY.get_height() - self.image.get_height()  
class Player(Tank):
    global enemies, bonuses, castle
    def __init__(self, speed=0.75, direction=DIRECTION_UP, position=(50, 50), level=None):
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
            self.make_step()
            self.return_on_map()
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type != GRASS:
                    self.align_collision(tile)
            for enemy in get_hit_list(self.rect, enemies):
                self.align_collision(enemy)
            for bonus in get_hit_list(self.rect, bonuses):
                if bonus.type == GRENADE:
                    for enemy in enemies[:]:
                        enemy.die()
                bonus.die()
            for c in get_hit_list(self.rect, [castle]):
                self.align_collision(c)
class Enemy(Tank):
    global enemies, player
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, speed, direction, position, level)
        self.enemy_images = [SPRITES.subsurface((128, 0, 16, 16)),
                              SPRITES.subsurface((192, 0, 16, 16)),
                              SPRITES.subsurface((224, 0, 16, 16)),
                              SPRITES.subsurface((160, 0, 16, 16))]

    def move_stupidly(self):
            self.image = self.enemy_images[self.direction]
            if not self.on_map():
                self.return_on_map()
                self.direction = randrange(4)
            self.make_step()
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type != GRASS:
                    self.align_collision(tile)
                    self.direction = randrange(4)
                break
            for enemy in get_hit_list(self.rect, enemies):
                if enemy != self:
                    self.turn_back()
            if len(get_hit_list(self.rect, [player])) != 0:
                    self.align_collision(player)
                    self.direction = randrange(4)
            for bonus in get_hit_list(self.rect, bonuses):
                bonus.die()
            for c in get_hit_list(self.rect, [castle]):
                self.align_collision(c)
                self.direction = randrange(4)

    def die(self):
        enemies.remove(self)
class Bullet:
    global enemies, bullets, castle
    def __init__(self, direction=DIRECTION_UP, position=None, owner=None, level=None):
        self.x = position[0]
        self.y = position[1]
        self.speed = 2
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 4, 4)
        self.images = [SPRITES.subsurface((322, 102, 4, 4)),
                       SPRITES.subsurface((338, 102, 4, 4)),
                       SPRITES.subsurface((346, 102, 4, 4)),
                       SPRITES.subsurface((330, 102, 4, 4))]
        self.image = self.images[self.direction]
        self.owner = owner
        self.level = level

    def fly(self):
        self.image = self.images[self.direction]
        if 0 < self.rect.x < DISPLAY.get_width() - self.image.get_width() and 0 < self.rect.y < DISPLAY.get_height() - self.image.get_height():
            if self.direction == DIRECTION_LEFT:
                self.x -= self.speed
            if self.direction == DIRECTION_RIGHT:
                self.x += self.speed
            if self.direction == DIRECTION_UP:
                self.y -= self.speed
            if self.direction == DIRECTION_DOWN:
                self.y += self.speed
            self.rect.topleft = round(self.x), round(self.y)
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type == BRICK:
                    self.level.kill_tile(tile)
                if tile.type != GRASS:
                    self.die()
            for enemy in get_hit_list(self.rect, enemies):
                enemy.die()
                self.die()
            for c in get_hit_list(self.rect, [castle]):
                self.die()
                c.die()
        else:
            self.die()

    def die(self):
        if self in bullets:
            bullets.remove(self)
class Level:
    def __init__(self, game_map):
        self.map = []
        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x] != '.':
                    type = int(game_map[y][x])
                    if type == BRICK or type == BETON:
                        for i in range(4):
                            self.map.append(Tile(type, (x * 16 + 8 * (i % 2), y * 16 + 8 * (i // 2))))
                    else:
                        self.map.append(Tile(type, (x * 16, y * 16)))
        self.protecting_blocks = ((88, 200), (88, 208), (88, 216), (96, 200), (104, 200), (112, 200), (112, 208), (112, 216))
        for protecting_block in self.protecting_blocks:
            self.map.append(Tile(BRICK, protecting_block))
    def kill_tile(self, tile):
        self.map.remove(tile)
class Bonus:
    def __init__(self, type, position):
        self.type = type
        self.images = [BOLD_SPRITES.subsurface((255, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((271, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((287, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((303, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((319, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((335, 111, 16, 15))]
        self.image = self.images[type]
        self.rect = pygame.Rect(position[0], position[1], 16, 15)

    def die(self):
        if self in bonuses:
            bonuses.remove(self)
bullets = []
current_level = Level(game_map)
player = Player(3/4, 0, (64, 208), current_level)
enemies = [Enemy(1/2, 0, (80, 32), current_level),
           Enemy(1/2, 0, (100, 150), current_level),
           Enemy(1/2, 0, (100, 200), current_level)]
bonuses = [Bonus(GRENADE, (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15))),
           Bonus(GRENADE, (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15)))]

castle = Castle()

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

    for bonus in bonuses:
        draw(bonus)
    
    draw(castle)
    

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
