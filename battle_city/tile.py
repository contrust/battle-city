import pygame
from battle_city.sprites import BOLD_SPRITES
(BRICK, GRASS, BETON, ICE, WATER) = range(5)


class Tile:
    def __init__(self, tile_type, position):
        self.type = tile_type
        self.images = [BOLD_SPRITES.subsurface((256, 0, 8, 8)),
                       BOLD_SPRITES.subsurface((272, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((256, 16, 8, 8)),
                       BOLD_SPRITES.subsurface((288, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((256, 48, 16, 16))
                       ]
        if tile_type == BRICK or tile_type == BETON:
            self.rect = pygame.Rect(position[0], position[1], 8, 8)
        else:
            self.rect = pygame.Rect(position[0], position[1], 16, 16)
        self.image = self.images[tile_type]
