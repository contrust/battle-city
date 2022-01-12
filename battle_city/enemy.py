from queue import Queue
from random import randrange

import pygame

from battle_city.explosion import Explosion
from battle_city.globals import DISPLAY
from battle_city.globals import get_hit_list
from battle_city.sprites import TANKS_IMAGES
from battle_city.tank import (Tank, DIRECTION_UP, DIRECTION_DOWN,
                              DIRECTION_RIGHT, DIRECTION_LEFT)
from battle_city.tile import GRASS


class Node:
    def __init__(self, value, previous=None):
        self.value = value
        self.previous = previous


def get_point(path_point):
    a = []
    while path_point.previous is not None:
        a.append(path_point.value)
        path_point = path_point.previous
    return a[::-1]


def find_path(path_point, target, rect, game_map, protecting_blocks):
    path = []
    start_point = Node(rect.topleft)
    point = (rect.x - rect.x % 8,
             rect.y - rect.y % 8)
    path_point = (path_point[0] - path_point[0] % 8,
                  path_point[1] - path_point[1] % 8)
    rect = pygame.Rect(rect.x, rect.y, 16, 16)
    paths = {point: Node(point, start_point)}
    points = Queue()
    points.put(point)
    while not points.empty():
        point = points.get()
        if (0 <= point[0] <= DISPLAY.get_width() - 16 and
                0 <= point[1] <= DISPLAY.get_height() - 16):
            for dx in range(-8, 16, 8):
                for dy in range(-8, 16, 8):
                    moved_point = (point[0] + dx, point[1] + dy)
                    rect.x, rect.y = moved_point
                    if dx != 0 and dy != 0 or moved_point in paths.keys():
                        continue
                    if target == 0:
                        for entity in get_hit_list(rect, game_map):
                            if entity.type != GRASS:
                                break
                        else:
                            points.put(moved_point)
                            paths[moved_point] = (
                                Node(moved_point, paths[point]))
                            if path_point == moved_point:
                                path = (
                                    get_point(paths[path_point]))
                    if target == 1:
                        for entity in get_hit_list(rect, game_map):
                            if (entity.type != GRASS and
                                    (entity.rect.topleft not in
                                     protecting_blocks)):
                                break
                        else:
                            points.put(moved_point)
                            paths[moved_point] = (
                                Node(moved_point, paths[point]))
                            if path_point == moved_point:
                                path = (
                                    get_point(paths[path_point]))
    return path


class Enemy(Tank):
    def __init__(self, kind, speed=2, direction=DIRECTION_UP,
                 position=(50, 50), target=0, level=None):
        Tank.__init__(self, 1, kind, speed, direction, position, level)
        self.path = []
        self.target = target
        self.is_moving_to_target = False

    def move(self):
        self.image = TANKS_IMAGES[1][self.kind][self.direction]
        if not self.on_map():
            self.return_on_map()
            self.direction = randrange(4)
        self.make_step()
        for _ in get_hit_list(self.rect, self.level.players):
            self.is_moving_to_target = False
            self.align_dynamic_collision()
            return
        for tile in get_hit_list(self.rect, self.level.game_map):
            if tile.type != GRASS:
                self.align_static_collision(tile)
                self.direction = randrange(4)
                self.is_moving_to_target = False
                break
        for castle in get_hit_list(self.rect, [self.level.castle]):
            self.align_static_collision(castle)
            self.direction = randrange(4)
            self.is_moving_to_target = False
        for bonus in get_hit_list(self.rect, self.level.bonuses):
            bonus.die()
        for enemy in get_hit_list(self.rect, self.level.enemies):
            if enemy != self:
                self.is_moving_to_target = False
                if (self.direction == 2 * (enemy.direction // 2) +
                        (enemy.direction + 1) % 2):
                    self.turn_back()
                else:
                    self.align_static_collision(enemy)
                    self.direction = randrange(4)
                self.make_step()
        if self.is_moving_to_target:
            self.get_direction_to_target(self.target)

    def get_direction_to_target(self, target):
        if len(self.path) != 0:
            if (self.rect.x == self.path[0][0] and
                    self.rect.y == self.path[0][1]):
                self.path.pop(0)
        if len(self.path) != 0:
            change = (self.path[0][0] - self.rect.x,
                      self.path[0][1] - self.rect.y)
            if change[0] > 0:
                self.direction = DIRECTION_RIGHT
            if change[0] < 0:
                self.direction = DIRECTION_LEFT
            if change[1] > 0:
                self.direction = DIRECTION_DOWN
            if change[1] < 0:
                self.direction = DIRECTION_UP
        else:
            live_players = []
            for player in self.level.players:
                if player.is_alive:
                    live_players.append(player.number)
            if target == 0:
                if target in live_players:
                    self.find_path(self.level.players[0].rect.topleft, 0)
                elif len(self.level.players) > 1:
                    self.find_path(self.level.players[1].rect.topleft, 0)
            if target == 1:
                if target in live_players and len(self.level.players) > 1:
                    self.find_path(self.level.players[1].rect.topleft, 0)
                else:
                    self.find_path(self.level.players[0].rect.topleft, 0)
            if target == 2:
                self.find_path((96, 208), 1)

    def find_path(self, path_point, target):
        self.path = find_path(path_point, target, self.rect,
                              self.level.game_map, self.level.protecting_blocks)
        if self.path:
            self.is_moving_to_target = True

    def die(self):
        pygame.mixer.music.load('../sounds/tank_explosion.ogg')
        pygame.mixer.music.set_volume(self.level.volume_level)
        pygame.mixer.music.play()
        self.level.explosions.append(Explosion(self.rect.topleft, 1))
        self.level.enemies.remove(self)
