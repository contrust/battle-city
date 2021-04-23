from tank import Tank, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT
from settings import get_hit_list
from sprites import TANKS_IMAGES
from bonus import HELMET, TIMES, SHOVEL, STAR, GRENADE, TANK_BONUS
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from menu import main_menu

class Player(Tank):
    def __init__(self, kind, speed=0.75, direction=DIRECTION_UP, position=(50, 50), level=None):
        Tank.__init__(self, 0, kind, speed, direction, position, level)
        self.pressed_keys = [False] * 4
        self.is_alive = True
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
            for enemy in get_hit_list(self.rect, self.level.enemies):
                enemy.speed = 0
                if self.direction == 0:
                    enemy.direction = 1
                if self.direction == 1:
                    enemy.direction = 0
                if self.direction == 2:
                    enemy.direction = 3
                if self.direction == 3:
                    enemy.direction = 2
                self.align_collision(enemy)
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
                bonus.die()
            for c in get_hit_list(self.rect, [self.level.castle]):
                self.align_collision(c)

    def die(self):
        self.is_alive = False
        main_menu(self.score, True)
