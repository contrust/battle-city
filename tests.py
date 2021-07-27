import unittest
from level import get_game_map
from enemy import find_path
from pygame.rect import Rect


class TestTest(unittest.TestCase):
    def test_find_path(self):
        game_map = get_game_map(1)
        path = find_path((64, 32), 0, Rect(0, 0, 16, 16), game_map, [])
        self.assertEqual(path,
                         [(0, 0), (8, 0), (16, 0), (24, 0), (32, 0), (40, 0), (48, 0), (56, 0), (64, 0), (64, 8),
                          (64, 16), (64, 24), (64, 32)])
        path = find_path((0, 80), 0, Rect(0, 0, 16, 16), game_map, [])
        self.assertEqual(path,
                         [(0, 0), (0, 8), (0, 16), (0, 24), (0, 32), (0, 40), (0, 48), (0, 56), (0, 64), (0, 72),
                          (0, 80)])
        path = find_path((16, 32), 0, Rect(0, 0, 16, 16), game_map, [])
        self.assertEqual(path, [])


if __name__ == '__main__':
    unittest.main()
