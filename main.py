import pygame, sys, threading
from menu import main_menu
from pygame.locals import *
from random import randrange
from queue import Queue
from itertools import chain

CLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Battle City')
WINDOW_SIZE = (400, 400)
SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
DISPLAY = pygame.Surface((208, 224))
SPRITES = pygame.image.load('sprite.png').convert_alpha()
BOLD_SPRITES = pygame.image.load('sprite1.png')
(BASIC, FAST, RAPID, ARMORED) = range(4)
(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)
(BRICK, GRASS, BETON, ICE, WATER) = range(5)
(HELMET, TIMES, SHOVEL, STAR, GRENADE, TANK_BONUS) = range(6)
BULLET_IMAGES = [SPRITES.subsurface((322, 102, 4, 4)),
                       SPRITES.subsurface((338, 102, 4, 4)),
                       SPRITES.subsurface((346, 102, 4, 4)),
                       SPRITES.subsurface((330, 102, 4, 4))]
TANKS_IMAGES = [[],[]]
for i in range(2):
    for j in range(4):
        TANKS_IMAGES[i].append([SPRITES.subsurface((128 * i, j * 16, 16, 16)),
                                      SPRITES.subsurface((128 * i + 64, j * 16, 16, 16)),
                                      SPRITES.subsurface((128 * i + 96, j * 16, 16, 16)),
                                      SPRITES.subsurface((128 * i + 32, j * 16, 16, 16))])


game_map = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '0', '0', '0', '0', '0', '.', '0', '0', '0', '0', '0', '.'],
            ['.', '.', '.', '0', '.', '0', '.', '0', '.', '.', '.', '.', '.'],
            ['0', '.', '.', '1', '.', '0', '.', '0', '.', '0', '0', '1', '0'],
            ['1', '1', '.', '1', '.', '0', '.', '.', '.', '.', '0', '1', '0'],
            ['1', '1', '0', '0', '.', '0', '0', '0', '0', '.', '0', '1', '0'],
            ['1', '.', '.', '.', '0', '0', '.', '0', '.', '.', '.', '.', '.'],
            ['0', '.', '0', '.', '0', '0', '.', '0', '.', '0', '0', '0', '.'],
            ['1', '.', '.', '.', '.', '.', '.', '.', '.', '0', '.', '0', '.'],
            ['1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '.', '.', '.'],
            ['1', '.', '.', '.', '0', '.', '0', '.', '.', '0', '.', '0', '0'],
            ['0', '.', '0', '.', '0', '.', '0', '.', '.', '.', '.', '.', '.'],
            ['0', '.', '0', '.', '.', '.', '.', '.', '.', '0', '.', '0', '0'],
            ['0', '.', '.', '.', '.', '.', '.', '.', '.', '0', '.', '.', '.'],
            ]


def draw(entity):
    DISPLAY.blit(entity.image, (entity.rect.x, entity.rect.y))


def get_hit_list(rect, *entities):
    return [entity for entity in list(chain(*entities)) if rect.colliderect(entity.rect)]

class SinglyLinkedList:
    def __init__(self, value, previous=None):
        self.value = value
        self.previous = previous


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
        main_menu(player.score, True)
        create_level()


class Tank:
    def __init__(self, kind=0, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        self.images = [SPRITES.subsurface((0, 0, 16, 16)), SPRITES.subsurface((0, 16, 16, 16)),
                       SPRITES.subsurface((0, 32, 16, 16)), SPRITES.subsurface((0, 48, 16, 16)),
                       SPRITES.subsurface((0, 64, 16, 16)), SPRITES.subsurface((0, 80, 16, 16)),
                       SPRITES.subsurface((0, 96, 16, 16)), SPRITES.subsurface((0, 112, 16, 16))]
        self.x = position[0]
        self.y = position[1]
        self.kind = kind
        self.speed = speed
        self.get_type()
        self.image = self.images[kind]
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.level = level
        self.current_bullets = self.max_bullets
        self.moving_state = False

    def get_type(self):
        if self.kind == 3:
            self.health = 4
            self.bullet_type = 1
        else:
            self.health = 1
            self.bullet_type = 0
        if self.kind == 1:
            self.speed = self.speed * 2
        if self.kind == 2 or self.kind == 3:
            self.max_bullets = 2
        else:
            self.max_bullets = 1

    def fire(self):
        if self.max_bullets >= self.current_bullets > 0:
            if self.direction == DIRECTION_UP:
                bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x + 5, self.rect.y), self, self.level))
            if self.direction == DIRECTION_DOWN:
                bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x + 5, self.rect.y + 12), self, self.level))
            if self.direction == DIRECTION_RIGHT:
                bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x + 12, self.rect.y + 6), self, self.level))
            if self.direction == DIRECTION_LEFT:
                bullets.append(Bullet(self.bullet_type, self.direction, (self.rect.x, self.rect.y + 6), self, self.level))
            self.current_bullets -= 1

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
        if self.rect.bottom >= entity.rect.top and self.rect.bottom <= entity.rect.bottom and self.direction == DIRECTION_DOWN:
            self.rect.bottom = entity.rect.top
        if self.rect.top <= entity.rect.bottom and self.rect.top >= entity.rect.top and self.direction == DIRECTION_UP:
            self.rect.top = entity.rect.bottom
        if self.rect.left <= entity.rect.right and self.rect.left >= entity.rect.left and self.direction == DIRECTION_LEFT:
            self.rect.left = entity.rect.right
        if self.rect.right >= entity.rect.left and self.rect.right <= entity.rect.right and self.direction == DIRECTION_RIGHT:
            self.rect.right = entity.rect.left
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

    def __init__(self, kind, speed=0.75, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, kind, speed, direction, position, level)
        self.pressed_keys = [False] * 4
        self.score = 0

    def move(self):
        for direction in range(4):
            if self.pressed_keys[direction]:
                self.direction = direction
                self.image = TANKS_IMAGES[0][self.kind][direction]
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
                enemy.speed = 0
                if player.direction == 0:
                    enemy.direction = 1
                if player.direction == 1:
                    enemy.direction = 0
                if player.direction == 2:
                    enemy.direction = 3
                if player.direction == 3:
                    enemy.direction = 2
                self.align_collision(enemy)
            for bonus in get_hit_list(self.rect, bonuses):
                if bonus.type == GRENADE:
                    for enemy in enemies[:]:
                        enemy.die()
                if bonus.type == STAR:
                    if self.kind < 3:
                        self.kind += 1
                        self.get_type()
                if bonus.type == SHOVEL:
                    for protecting_block in self.level.protecting_blocks:
                        self.level.map.append(Tile(BETON, protecting_block))
                bonus.die()
            for c in get_hit_list(self.rect, [castle]):
                self.align_collision(c)

    def die(self):
        main_menu(player.score, True)
        create_level()


class Enemy(Tank):
    global enemies, player

    def __init__(self, kind, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, kind, speed, direction, position, level)
        self.pathToPlayer = []
        self.is_moving_to_player = False
        self.is_moving_to_castle = False

    def move(self):
        self.image = TANKS_IMAGES[1][self.kind][self.direction]
        if not self.on_map():
            self.return_on_map()
            self.direction = randrange(4)
        for tile in get_hit_list(self.rect, [player]):
            self.align_collision(tile)
            self.direction = randrange(4)
            self.is_moving_to_player = False
            self.is_moving_to_castle = False
        for tile in get_hit_list(self.rect, self.level.map):
            if tile.type != GRASS:
                self.align_collision(tile)
                self.direction = randrange(4)
                self.is_moving_to_player = False
                self.is_moving_to_castle = False
                break
        for bonus in get_hit_list(self.rect, bonuses):
            bonus.die()
        for enemy in get_hit_list(self.rect, enemies):
            if enemy != self:
                self.align_collision(enemy)
                self.turn_back()
                self.is_moving_to_player = False
                self.is_moving_to_castle = False
        if self.is_moving_to_player:
            self.get_direction_to_target("Player")
        if self.is_moving_to_castle:
            self.get_direction_to_target("Castle")
        self.make_step()
        self.speed = 1/2

    def get_direction_to_target(self, target):
        if len(self.pathToPlayer) != 0:
            if self.rect.x == self.pathToPlayer[0][0] and self.rect.y == self.pathToPlayer[0][1]:
                self.pathToPlayer.pop(0)
        if len(self.pathToPlayer) != 0:
            change = (self.pathToPlayer[0][0] - self.rect.x, self.pathToPlayer[0][1] - self.rect.y)
            if change[0] > 0:
                self.direction = DIRECTION_RIGHT
            if change[0] < 0:
                self.direction = DIRECTION_LEFT
            if change[1] > 0:
                self.direction = DIRECTION_DOWN
            if change[1] < 0:
                self.direction = DIRECTION_UP
        else:
            self.find_path((player.rect.x, player.rect.y))

    def find_path(self, path_point, target, level):
        self.pathToPlayer = []
        start_point = SinglyLinkedList((self.rect.x, self.rect.y))
        point = (self.rect.x - self.rect.x % 8, self.rect.y - self.rect.y % 8)
        path_point = (path_point[0] - path_point[0] % 8, path_point[1] - path_point[1] % 8)
        rect = pygame.Rect(self.rect.x, self.rect.y, 16, 16)
        paths = {}
        paths[point] = SinglyLinkedList(point, start_point)
        points = Queue()
        points.put(point)
        while not points.empty():
            point = points.get()
            if 0 <= point[0] <= DISPLAY.get_width() - 16 and 0 <= point[1] <= DISPLAY.get_height() - 16:
                for dx in range(-8, 16, 8):
                    for dy in range(-8, 16, 8):
                        moved_point = (point[0] + dx, point[1] + dy)
                        rect.x, rect.y = moved_point
                        if dx != 0 and dy != 0 or moved_point in paths.keys():
                            continue
                        if target == "Player":
                            for entity in get_hit_list(rect, self.level.map):
                                if entity.type != GRASS:
                                    break
                            else:
                                points.put(moved_point)
                                paths[moved_point] = SinglyLinkedList(moved_point, paths[point])
                                if path_point == moved_point:
                                    self.pathToPlayer = self.get_point(paths[path_point])
                                    self.is_moving_to_player = True
                                    self.is_moving_to_castle = False
                                    return
                        if target == "Castle":
                            for entity in get_hit_list(rect, self.level.map):
                                if entity.type != GRASS and entity in level.protecting_blocks is False:
                                    break
                            else:
                                points.put(moved_point)
                                paths[moved_point] = SinglyLinkedList(moved_point, paths[point])
                                if path_point == moved_point:
                                    self.pathToPlayer = self.get_point(paths[path_point])
                                    self.is_moving_to_player = False
                                    self.is_moving_to_castle = True
                                    return


    def get_point(self, path_point):
        a = []
        while path_point.previous != None:
            a.append(path_point.value)
            path_point = path_point.previous
        return a[::-1]

    def die(self):
        player.score += 1
        if self in enemies:
            if not randrange(6):
                bonuses.append(Bonus(randrange(6), (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15))))
        enemies.remove(self)


class Bullet:
    global enemies, bullets, castle, player
    def __init__(self, kind, direction=DIRECTION_UP, position=None, owner=None, level=None):
        self.x = position[0]
        self.y = position[1]
        self.speed = 2
        self.direction = direction
        self.kind = kind
        self.rect = pygame.Rect(self.x, self.y, 4, 4)
        self.image = BULLET_IMAGES[self.direction]
        self.owner = owner
        self.level = level

    def fly(self):
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
                if tile.type == BETON and self.kind == 1:
                    self.level.kill_tile(tile)
                if tile.type != GRASS:
                    self.die()
            if type(self.owner) is Player:
                for enemy in get_hit_list(self.rect, enemies):
                    enemy.health -= 1
                    if enemy.health == 0:
                        enemy.die()
                    self.die()
            else:
                for p in get_hit_list(self.rect, [player]):
                    p.health -= 1
                    if p.health == 0:
                        p.die()
                    self.die()
            for c in get_hit_list(self.rect, [castle]):
                self.die()
                c.die()
            for bullet in get_hit_list(self.rect, bullets[:]):
                if self != bullet:
                    self.die()
                    bullet.die()
        else:
            self.die()

    def die(self):
        if self in bullets:
            bullets.remove(self)
            self.owner.current_bullets += 1


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
        self.protecting_blocks = (
        (88, 200), (88, 208), (88, 216), (96, 200), (104, 200), (112, 200), (112, 208), (112, 216))
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


def create_level():
    global bullets, current_level, player, enemies, bonuses, castle, goal
    bullets = []
    current_level = Level(game_map)
    player = Player(0, 3 / 4, 0, (64, 208), current_level)
    enemies = []
    bonuses = [Bonus(randrange(6), (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15))),
               Bonus(randrange(6), (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15)))]
    castle = Castle()
    goal = 1


create_level()
main_menu()

while 1:
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(player.image, (player.rect.x, player.rect.y))
    player.move()

    if not randrange(250):
        if len(enemies) < 4:
            enemies.append(Enemy(randrange(4), 1 / 2, 0, (96 * randrange(3), 0), current_level))
    for enemy in enemies:
        draw(enemy)
        if not randrange(140):
            if enemy.is_moving_to_castle:
                enemy.move()
                continue
            if player.score >= goal and not enemy.is_moving_to_castle:
                enemy.is_moving_to_castle = True
                enemy.is_moving_to_player = False
                enemy.find_path((96, 208), "Castle", current_level)
            if player.score < goal:
                if not enemy.is_moving_to_player:
                    enemy.is_moving_to_player = True
                    enemy.is_moving_to_castle = False
                    enemy.find_path((player.rect.x, player.rect.y), "Player", current_level)
        enemy.move()
        if not randrange(50):
            enemy.fire()

    for bullet in bullets:
        draw(bullet)

    for tile in current_level.map:
        draw(tile)

    for bonus in bonuses:
        draw(bonus)

    draw(castle)

    for bullet in bullets[:]:
        bullet.fly()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
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
                create_level()
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