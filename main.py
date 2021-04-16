import pygame, sys, threading
from menu import main_menu
from pygame.locals import *
from random import randrange
from queue import Queue

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
            ['0', '0', '0', '0', '.', '.', '.', '.', '.', '.', '0', '0', '0'],
            ['0', '.', '.', '.', '1', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['0', '0', '0', '.', '.', '.', '0', '.', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '.', '0', '0', '0', '0', '.', '.', '.', '.', '.'],
            ['0', '1', '1', '0', '0', '0', '1', '0', '0', '.', '.', '.', '.'],
            ['0', '1', '1', '0', '1', '1', '1', '.', '.', '.', '.', '.', '.'],
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
        main_menu()
        create_level()


class Tank:
    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        self.x = position[0]
        self.y = position[1]
        self.image = SPRITES.subsurface((0, 0, 16, 16))
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 16, 16)
        self.level = level
        self.can_fire = True
        self.moving_state = False

    def fire(self):
        if self.can_fire:
            if self.direction == DIRECTION_UP:
                bullets.append(Bullet(self.direction, (self.rect.x + 5, self.rect.y), self, self.level))
            if self.direction == DIRECTION_DOWN:
                bullets.append(Bullet(self.direction, (self.rect.x + 5, self.rect.y + 12), self, self.level))
            if self.direction == DIRECTION_RIGHT:
                bullets.append(Bullet(self.direction, (self.rect.x + 12, self.rect.y + 6), self, self.level))
            if self.direction == DIRECTION_LEFT:
                bullets.append(Bullet(self.direction, (self.rect.x, self.rect.y + 6), self, self.level))
            self.can_fire = False

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
    global enemies, bonuses, castle, current_level

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

    def die(self):
        main_menu()
        create_level()


class Enemy(Tank):
    global enemies, player

    def __init__(self, speed=2, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, speed, direction, position, level)
        self.enemy_images = [SPRITES.subsurface((128, 0, 16, 16)),
                             SPRITES.subsurface((192, 0, 16, 16)),
                             SPRITES.subsurface((224, 0, 16, 16)),
                             SPRITES.subsurface((160, 0, 16, 16))]
        self.pathToPlayer = []

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

    def move_to_player(self):
        global protecting_blocks
        for c in get_hit_list(self.rect, [castle]):
            self.align_collision(c)
            return
        for tile in get_hit_list(self.rect, self.level.map):
            if (tile.rect.x, tile.rect.y) in protecting_blocks:
                self.align_collision(tile)
                return
        for bonus in get_hit_list(self.rect, bonuses):
            bonus.die()
        #for enemy in get_hit_list(self.rect, enemies):
            #if enemy != self:
                #self.turn_back()
                #return
        #if len(get_hit_list(self.rect, [player])) != 0:
            #self.align_collision(player)
            #return
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
            self.image = self.enemy_images[self.direction]
            self.make_step()
        else:
            self.move_stupidly()

    def die(self):
        enemies.remove(self)

    def find_path(self, path_point, target):
        global protecting_blocks
        point = (self.rect.x - self.rect.x % 16, self.rect.y - self.rect.y % 16)
        path_point = (path_point[0] - path_point[0] % 16, path_point[1] - path_point[1] % 16)
        rect = pygame.Rect(self.rect.x, self.rect.y, 16, 16)
        paths = {}
        paths[point] = SinglyLinkedList(point)
        points = Queue()
        points.put(point)
        while not points.empty():
            point = points.get()
            if 0 <= point[0] <= DISPLAY.get_width() - 16 and 0 <= point[1] <= DISPLAY.get_height() - 16:
                for dx in range(-16, 32, 16):
                    for dy in range(-16, 32, 16):
                        moved_point = (point[0] + dx, point[1] + dy)
                        rect.x, rect.y = moved_point
                        if dx != 0 and dy != 0 or moved_point in paths.keys():
                            continue
                        flag = 0
                        for tile in get_hit_list(rect, self.level.map):
                            if target == "Castle":
                                if tile.type != GRASS and (tile.rect.x, tile.rect.y) not in protecting_blocks:
                                    flag = 1
                            if target == "Player":
                                if tile.type != GRASS:
                                    flag = 1
                        if not len(get_hit_list(rect, self.level.map)) or flag == 0:
                            points.put(moved_point)
                            paths[moved_point] = SinglyLinkedList(moved_point, paths[point])
        self.pathToPlayer = self.get_point(paths[path_point])

    def get_point(self, path_point):
        a = []
        while path_point.previous != None:
            a.append(path_point.value)
            path_point = path_point.previous
        return a[1::-1]

    def get_point(self, path_point):
        a = []
        while path_point.previous != None:
            a.append(path_point.value)
            path_point = path_point.previous
        return a[::-1]


class SinglyLinkedList:
    def __init__(self, value, previous=None):
        self.value = value
        self.previous = previous
        self.length = 1 if previous == None else previous.length + 1

    def enumerator(self):
        yield self.value
        pathItem = self.previous
        while pathItem != None:
            yield pathItem
            pathItem = pathItem.previous

    def die(self):
        enemies.remove(self)


class Bullet:
    global enemies, bullets, castle, player

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
            if type(self.owner) is Player:
                for enemy in get_hit_list(self.rect, enemies):
                    enemy.die()
                    self.die()
            else:
                for p in get_hit_list(self.rect, [player]):
                    p.die()
                    self.die()
            for c in get_hit_list(self.rect, [castle]):
                self.die()
                c.die()
        else:
            self.die()

    def die(self):
        if self in bullets:
            bullets.remove(self)
        self.owner.can_fire = True


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
    global current_level, player, bullets, enemies, bonuses, castle
    current_level = Level(game_map)
    player = Player(3 / 4, 0, (64, 208), current_level)
    bullets = []
    player = Player(3 / 4, 0, (64, 208), current_level)
    enemies = [Enemy(1 / 2, 0, (80, 32), current_level),
               Enemy(1 / 2, 0, (96, 96), current_level),
               Enemy(1 / 2, 0, (112, 64), current_level)]
    bonuses = [Bonus(GRENADE, (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15))),
               Bonus(GRENADE, (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15)))]
    castle = Castle()


current_level = Level(game_map)
player = Player(3 / 4, 0, (64, 208), current_level)
bullets = []
player = Player(3 / 4, 0, (64, 208), current_level)
enemies = [Enemy(1 / 2, 0, (80, 32), current_level),
           Enemy(1 / 2, 0, (96, 96), current_level),
           Enemy(1 / 2, 0, (112, 64), current_level)]
bonuses = [Bonus(GRENADE, (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15))),
           Bonus(GRENADE, (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15)))]
castle = Castle()
protecting_blocks = (88, 200), (88, 208), (88, 216), (96, 200), (104, 200), (112, 200), (112, 208), (112, 216)


main_menu()


while True:
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(player.image, (player.rect.x, player.rect.y))

    for enemy in enemies:
        draw(enemy)
        if randrange(150) == 0:
            enemy.fire()
        if randrange(150) == 0:
            enemy.find_path((castle.rect.x, castle.rect.y), "Castle")

    for bullet in bullets:
        draw(bullet)

    for tile in current_level.map:
        draw(tile)

    for bonus in bonuses:
        draw(bonus)

    draw(castle)

    player.move()
    for enemy in enemies:
        move = 0
        for tile in get_hit_list(enemy.rect, enemy.level.map):
            if (tile.rect.x, tile.rect.y) in protecting_blocks:
                move = 1
        if len(get_hit_list(enemy.rect, [castle])) != 0:
            move = 1
        if move == 1:
            enemy.speed = 0
        else:
            enemy.speed = 1/2
            enemy.move_to_player()
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