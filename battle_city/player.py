import pygame
from pygame.locals import *

from battle_city.bonus import SHOVEL, STAR, GRENADE, TANK_BONUS
from battle_city.explosion import Explosion
from battle_city.globals import get_hit_list
from battle_city.sprites import TANKS_IMAGES
from battle_city.tank import (Tank, DIRECTION_UP, DIRECTION_DOWN,
                              DIRECTION_RIGHT, DIRECTION_LEFT)
from battle_city.tile import Tile, GRASS, BETON


class Player(Tank):
    def __init__(self, number, kind, speed=0.75,
                 direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, 0, kind, speed, direction, position, level)
        self.number = number
        if self.number == 1:
            self.controls = {K_UP: DIRECTION_UP, K_DOWN: DIRECTION_DOWN,
                             K_RIGHT: DIRECTION_RIGHT, K_LEFT: DIRECTION_LEFT}
        elif self.number == 0:
            self.controls = {K_w: DIRECTION_UP, K_s: DIRECTION_DOWN,
                             K_d: DIRECTION_RIGHT, K_a: DIRECTION_LEFT}
        self.pressed_keys = [False] * 4
        self.is_alive = True
        self.lifes = 3
        self.max_lifes = 4
        self.score = [0, 0, 0, 0]

    def collide_with_bonus(self, bonus):
        if bonus.type == GRENADE:
            for enemy in self.level.enemies[:]:
                self.score[enemy.kind] += 1
                enemy.die()
        if bonus.type == STAR:
            if self.kind < 3:
                self.kind += 1
                self.get_type()
        if bonus.type == SHOVEL:
            for protecting_block in self.level.protecting_blocks:
                self.level.game_map.append(Tile(BETON, protecting_block))
        if bonus.type == TANK_BONUS:
            if self.lifes < self.max_lifes:
                self.lifes += 1
        bonus.die()

    def move(self):
        if self.number == 0:
            self.image = TANKS_IMAGES[0][self.kind][self.direction]
        else:
            self.image = TANKS_IMAGES[0][self.kind][self.direction + 4]
        for direction in range(4):
            if self.pressed_keys[direction]:
                self.direction = direction
                self.moving_state = True
                break
        else:
            self.moving_state = False
        if self.moving_state:
            self.make_step()
            self.return_on_map()
            for tile in get_hit_list(self.rect, self.level.game_map):
                if tile.type != GRASS:
                    self.align_static_collision(tile)
            for _ in get_hit_list(self.rect, self.level.enemies):
                self.align_dynamic_collision()
            if len(self.level.players) == 2:
                if self.rect.colliderect(
                        self.level.players[(self.number + 1) % 2]):
                    self.align_static_collision(
                        self.level.players[(self.number + 1) % 2])
            for bonus in get_hit_list(self.rect, self.level.bonuses):
                self.collide_with_bonus(bonus)
            for castle in get_hit_list(self.rect, [self.level.castle]):
                self.align_static_collision(castle)

    def to_start(self, x, y):
        self.x, self.y, self.rect.topleft = x, y, (x, y)
        self.pressed_keys = [False] * 4
        self.direction = DIRECTION_UP

    def die(self):
        pygame.mixer.music.load('../sounds/tank_explosion.ogg')
        pygame.mixer.music.set_volume(self.level.volume_level)
        pygame.mixer.music.play()
        self.level.explosions.append(Explosion(self.rect.topleft, 1))
        self.is_alive = False
        self.lifes -= 1
        if self.number == 0:
            self.to_start(64, 208)
        if self.number == 1:
            self.to_start(128, 208)
        if not self.lifes:
            self.level.kill_player(self)
            if not self.level.players:
                self.level.game.game_over()
