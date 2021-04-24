import pygame
from settings import get_hit_list
from tank import Tank, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT
from sprites import TANKS_IMAGES
from random import randrange, choice
from queue import Queue
from settings import DISPLAY
from tile import BRICK, GRASS, BETON, ICE, WATER
(PLAYER, CASTLE) = range(2)

class SinglyLinkedList:
    def __init__(self, value, previous=None):
        self.value = value
        self.previous = previous

class Enemy(Tank):
    def __init__(self, kind, speed=2, direction=DIRECTION_UP, position=(50, 50), target=0, level=None):
        Tank.__init__(self, 1, kind, speed, direction, position, level)
        self.pathToPlayer = []
        self.target = target
        self.is_moving_to_target = False

    def move(self):
        self.image = TANKS_IMAGES[1][self.kind][self.direction]
        if not self.on_map():
            self.return_on_map()
            self.direction = randrange(4)
        for tile in get_hit_list(self.rect, [self.level.player]):
            self.speed = 0
            if tile.direction == 0:
                self.direction = 1
            if tile.direction == 1:
                self.direction = 0
            if tile.direction == 2:
                self.direction = 3
            if tile.direction == 3:
                self.direction = 2
            self.is_moving_to_target = False
            self.align_collision(tile)
        for tile in get_hit_list(self.rect, self.level.map):
            if tile.type != GRASS:
                self.align_collision(tile)
                self.direction = randrange(4)
                self.is_moving_to_target = False
                break
        for tile in get_hit_list(self.rect, [self.level.castle]):
            self.align_collision(tile)
            self.direction = randrange(4)
            self.is_moving_to_target = False
        for bonus in get_hit_list(self.rect, self.level.bonuses):
            bonus.die()
        for enemy in get_hit_list(self.rect, self.level.enemies):
            if enemy != self:
                self.align_collision(enemy)
                self.direction = randrange(4)
                self.is_moving_to_target = False
        if self.is_moving_to_target and self.target == 0:
            self.get_direction_to_target(PLAYER)
        if self.is_moving_to_target and self.target == 1:
            self.get_direction_to_target(CASTLE)
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
            if target == PLAYER:
                self.find_path((self.level.player.rect.x, self.level.player.rect.y), 0, self.level)
            elif target == CASTLE:
                self.find_path((96, 208), 1, self.level)


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
                        if target == PLAYER:
                            for entity in get_hit_list(rect, self.level.map):
                                if entity.type != GRASS:
                                    break
                            else:
                                points.put(moved_point)
                                paths[moved_point] = SinglyLinkedList(moved_point, paths[point])
                                if path_point == moved_point:
                                    self.pathToPlayer = self.get_point(paths[path_point])
                                    self.is_moving_to_target = True
                                    return
                        if target == CASTLE:
                            for entity in get_hit_list(rect, self.level.map):
                                if entity.type != GRASS and entity in level.protecting_blocks is False:
                                    break
                            else:
                                points.put(moved_point)
                                paths[moved_point] = SinglyLinkedList(moved_point, paths[point])
                                if path_point == moved_point:
                                    self.pathToPlayer = self.get_point(paths[path_point])
                                    self.is_moving_to_target = True
                                    return

    def get_point(self, path_point):
        a = []
        while path_point.previous != None:
            a.append(path_point.value)
            path_point = path_point.previous
        return a[::-1]

    def die(self):
        self.level.player.score[self.kind] += 1
        self.level.enemies.remove(self)
