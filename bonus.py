from sprites import BOLD_SPRITES
import pygame
(HELMET, TIMES, SHOVEL, STAR, GRENADE, TANK_BONUS) = range(6)

class Bonus:
    def __init__(self, type, position, level):
        self.type = type
        self.level = level
        self.images = [BOLD_SPRITES.subsurface((255, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((271, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((287, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((303, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((319, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((335, 111, 16, 15))]
        self.image = self.images[type]
        self.rect = pygame.Rect(position[0], position[1], 16, 15)

    def die(self):
        if self in self.level.bonuses:
            self.level.bonuses.remove(self)