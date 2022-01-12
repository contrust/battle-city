import pygame

from battle_city.explosion import Explosion
from battle_city.globals import DISPLAY, get_hit_list
from battle_city.sprites import BULLET_IMAGES
from battle_city.tile import BRICK, GRASS, BETON, WATER

(DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT) = range(4)


class Bullet:
    def __init__(self, kind, direction=DIRECTION_UP,
                 position=None, owner=None, level=None):
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
        if (0 < self.rect.x < DISPLAY.get_width() - self.image.get_width() and
                (0 < self.rect.y < DISPLAY.get_height() -
                 self.image.get_height())):
            if self.direction == DIRECTION_LEFT:
                self.x -= self.speed
            if self.direction == DIRECTION_RIGHT:
                self.x += self.speed
            if self.direction == DIRECTION_UP:
                self.y -= self.speed
            if self.direction == DIRECTION_DOWN:
                self.y += self.speed
            self.rect.topleft = round(self.x), round(self.y)
            for tile in get_hit_list(self.rect, self.level.game_map):
                if tile.type == BRICK:
                    self.level.kill_tile(tile)
                if tile.type == BETON and self.kind == 1:
                    self.level.kill_tile(tile)
                if tile.type not in {GRASS, WATER}:
                    self.die()
                elif tile.type in {WATER}:
                    self.level.game.draw(self)
            if self.owner.role == 0:
                for enemy in get_hit_list(self.rect, self.level.enemies):
                    enemy.health -= 1
                    if enemy.health == 0:
                        enemy.die()
                        self.owner.score[enemy.kind] += 1
                    self.die()
            else:
                for player in get_hit_list(self.rect, self.level.players):
                    player.health -= 1
                    if player.health == 0:
                        player.die()
                    self.die()
            for castle in get_hit_list(self.rect, [self.level.castle]):
                self.die()
                castle.die()
            for bullet in get_hit_list(self.rect, self.level.bullets[:]):
                if self != bullet and self.owner.role != bullet.owner.role:
                    self.die()
                    bullet.die()
        else:
            self.die()

    def die(self):
        if self in self.level.bullets:
            self.level.explosions.append(Explosion(self.rect.topleft, 0))
            self.level.bullets.remove(self)
            self.owner.current_bullets += 1
