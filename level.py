from player import Player
from bonus import Bonus
from castle import *
from random import randrange
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from settings import DISPLAY


class Level:
    def __init__(self, number, player=None):
        self.map = []
        self.number = number
        with open(f'maps/{number}.txt', 'r') as f:
            y = 0
            for line in f:
                line = line.strip()
                for x in range(len(line)):
                    if line[x] != '.':
                        type = int(line[x])
                        if type == BRICK or type == BETON:
                            for i in range(4):
                                self.map.append(Tile(type, (x * 16 + 8 * (i % 2), y * 16 + 8 * (i // 2))))
                        else:
                            self.map.append(Tile(type, (x * 16, y * 16)))
                y += 1
        self.protecting_blocks = (
        (88, 200), (88, 208), (88, 216), (96, 200), (104, 200), (112, 200), (112, 208), (112, 216))
        for protecting_block in self.protecting_blocks:
            self.map.append(Tile(BRICK, protecting_block))
        if player == None:
            self.player = Player(0, 3 / 4, 0, (64, 208), self)
        else:
            self.player = player
            self.player.is_alive = True
            self.player.level = self
        self.bullets = []
        self.enemies = []
        self.bonuses = [Bonus(randrange(6), (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15)), self),
               Bonus(randrange(6), (randrange(DISPLAY.get_width() - 16), randrange(DISPLAY.get_height() - 15)), self)]
        self.castle = Castle(self)
        self.goal = 1

    def kill_tile(self, tile):
        self.map.remove(tile)

