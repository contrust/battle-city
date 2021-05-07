from player import Player
from bonus import Bonus
from castle import *
from random import randrange
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from settings import DISPLAY


class Level:
    def __init__(self, number, count, game, players=None):
        self.map = []
        self.number = number
        self.game = game
        with open(f'maps/{number}.txt', 'r') as f:
            y = 0
            for line in f:
                line = line.strip()
                for x in range(len(line)):
                    if line[x] != '.':
                        type = int(line[x])
                        if type == BRICK or type == BETON:
                            for i in range(4):
                                self.map.append(Tile(type,
                                                     (x * 16 + 8 * (i % 2),
                                                      y * 16 + 8 * (i // 2))))
                        else:
                            self.map.append(Tile(type, (x * 16, y * 16)))
                y += 1
        self.protecting_blocks = (
            (88, 200),
            (88, 208),
            (88, 216),
            (96, 200),
            (104, 200),
            (112, 200),
            (112, 208),
            (112, 216))
        for protecting_block in self.protecting_blocks:
            self.map.append(Tile(BRICK, protecting_block))
        if not players and count == 1:
            self.players = [Player(0, 0, 3 / 4, 0, (64, 208), self)]
        elif count == 1:
            self.players = players
            players[0].is_alive = True
            players[0].current_bullets = players[0].max_bullets
            players[0].level = self
        if not players and count == 2:
            self.players = [Player(0, 0, 3 / 4, 0, (64, 208), self), Player(1, 0, 3 / 4, 0, (128, 208), self)]
        elif count == 2:
            self.players = players
            for player in players:
                player.is_alive = True
                player.current_bullets = player.max_bullets
                player.level = self
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.bonuses = [Bonus(randrange(6),
                              (randrange(DISPLAY.get_width() - 16),
                               randrange(DISPLAY.get_height() - 15)), self),
                        Bonus(randrange(6),
                              (randrange(DISPLAY.get_width() - 16),
                              randrange(DISPLAY.get_height() - 15)), self)]
        self.castle = Castle(self)
        self.goal = 1

    def get_score(self):
        return sum((sum(player.score) for player in self.players))

    def kill_tile(self, tile):
        self.map.remove(tile)

    def kill_player(self, player):
        self.players.remove(player)
