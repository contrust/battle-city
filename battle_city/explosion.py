from battle_city.sprites import BOLD_SPRITES
import pygame


class Explosion:
    def __init__(self, position, explosion_type=0, stage=0):
        self.images = [BOLD_SPRITES.subsurface((256, 96, 16, 16)),
                       BOLD_SPRITES.subsurface((272, 96, 16, 16)),
                       BOLD_SPRITES.subsurface((288, 96, 16, 16)),
                       BOLD_SPRITES.subsurface((304, 96, 16, 16)),
                       BOLD_SPRITES.subsurface((256, 128, 16, 16)),
                       BOLD_SPRITES.subsurface((272, 128, 16, 16)),
                       BOLD_SPRITES.subsurface((288, 128, 16, 16))]
        self.type = explosion_type
        self.stage = stage
        self.image = self.images[0]
        self.rect = pygame.Rect(position[0] - 4, position[1] - 4, 16, 16)
