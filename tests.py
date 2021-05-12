import unittest
from game import *


class TestTest(unittest.TestCase):
    def test_game_init(self):
        game = Game()
        self.assertIsInstance(game.level, Level)
        self.assertIsInstance(game.curr_menu, MainMenu)

    def test_level_init(self):
        level = Game().level
        self.assertIsInstance(level.map, list)
        self.assertIsInstance(level.players, list)
        self.assertIsInstance(level.enemies, list)
        self.assertIsInstance(level.number, int)

    def test_find_path(self):
        game = Game()
        enemy = Enemy(randrange(4), 1 / 2, 0, (0, 0), 0, game.level)
        enemy.find_path((32, 48), 0, game.level)
        self.assertEqual(enemy.path, [(0, 0), (0, 8), (0, 16), (8, 16), (16, 16), (16, 24), (16, 32), (16, 40),
                                      (16, 48), (24, 48), (32, 48)])
        enemy.find_path((80, 0), 0, game.level)
        self.assertEqual(enemy.path,
                         [(0, 0), (8, 0), (16, 0), (24, 0), (32, 0), (40, 0), (48, 0), (56, 0), (64, 0), (72, 0),
                          (80, 0)])
        enemy.find_path((32, 16), 0, game.level)
        self.assertEqual(enemy.path, [])


if __name__ == '__main__':
    unittest.main()
