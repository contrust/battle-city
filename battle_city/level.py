from battle_city.player import Player
from battle_city.bonus import Bonus
from battle_city.castle import *
from random import randrange
from battle_city.tile import Tile, BRICK, BETON
from battle_city.globals import DISPLAY


def get_game_map(number):
    game_map = []
    with open(f'maps/{number}.txt', 'r') as f:
        y = 0
        for line in f:
            line = line.strip()
            for x in range(len(line)):
                if line[x] != '.':
                    tile_type = int(line[x])
                    if tile_type == BRICK or tile_type == BETON:
                        for i in range(4):
                            game_map.append(Tile(tile_type,
                                                 (x * 16 + 8 * (i % 2),
                                                  y * 16 + 8 * (i // 2))))
                    else:
                        game_map.append(Tile(tile_type, (x * 16, y * 16)))
            y += 1
    return game_map


class Level:
    def __init__(self, number, count, game, players=None):
        self.game_map = get_game_map(number)
        self.number = number
        self.game = game
        self.volume_level = self.game.volume_level
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
            self.game_map.append(Tile(BRICK, protecting_block))
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
        self.bonuses = [Bonus(randrange(4),
                              (randrange(DISPLAY.get_width() - 16),
                               randrange(DISPLAY.get_height() - 15)), self),
                        Bonus(randrange(4),
                              (randrange(DISPLAY.get_width() - 16),
                              randrange(DISPLAY.get_height() - 15)), self)]
        self.castle = Castle(self)
        self.goal = 1

    def get_score(self):
        return sum((sum(player.score) for player in self.players))

    def kill_tile(self, tile):
        self.game_map.remove(tile)

    def kill_player(self, player):
        self.players.remove(player)
