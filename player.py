import pygame
from pygame.locals import *

from tank import (Tank, DIRECTION_UP, DIRECTION_DOWN,
                  DIRECTION_RIGHT, DIRECTION_LEFT)
from settings import get_hit_list
from sprites import TANKS_IMAGES
from bonus import HELMET, TIMES, SHOVEL, STAR, GRENADE, TANK_BONUS
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from menu import main_menu
from explosion import Explosion


class Player(Tank):
    def __init__(self, number, kind, speed=0.75,
                 direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, 0, kind, speed, direction, position, level)
        self.number = number
        if self.number == 0:
            self.controls = {K_w:DIRECTION_UP, K_s:DIRECTION_DOWN, K_d:DIRECTION_RIGHT, K_a:DIRECTION_LEFT}
        elif self.number == 1:
            self.controls = {K_UP:DIRECTION_UP, K_DOWN:DIRECTION_DOWN, K_RIGHT:DIRECTION_RIGHT, K_LEFT:DIRECTION_LEFT}
        self.pressed_keys = [False] * 4
        self.is_alive = True
        self.lifes = 3
        self.max_lifes = 4
        self.score = [0, 0, 0, 0]

    def move(self):
        self.image = TANKS_IMAGES[0][self.kind][self.direction]
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
            for tile in get_hit_list(self.rect, self.level.map):
                if tile.type != GRASS:
                    self.align_collision(tile)
            for enemy in get_hit_list(self.rect, self.level.enemies):
                self.turn_back()
                self.make_step()
                self.turn_back()
            for bonus in get_hit_list(self.rect, self.level.bonuses):
                if bonus.type == GRENADE:
                    for enemy in self.level.enemies[:]:
                        enemy.die()
                if bonus.type == STAR:
                    if self.kind < 3:
                        self.kind += 1
                        self.get_type()
                if bonus.type == SHOVEL:
                    for protecting_block in self.level.protecting_blocks:
                        self.level.map.append(Tile(BETON, protecting_block))
                if bonus.type == TANK_BONUS:
                    if self.lifes < self.max_lifes:
                        self.lifes += 1
                bonus.die()
            for castle in get_hit_list(self.rect, [self.level.castle]):
                self.align_collision(castle)

    def to_start(self):
        self.x, self.y, self.rect.topleft = 64, 208, (64, 208)
        self.pressed_keys = [False] * 4
        self.direction = DIRECTION_UP

    def die(self):
        pygame.mixer.music.load('sounds/tank_explosion.mp3')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        self.level.explosions.append(Explosion(self.rect.topleft, 1))
        self.is_alive = False
        self.lifes -= 1
        self.to_start()
        if not self.lifes:
            pygame.mixer.music.load('sounds/game_over.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            main_menu(self.score, "Game Over")
