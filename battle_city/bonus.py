from battle_city.sprites import BOLD_SPRITES
import pygame
(SHOVEL, STAR, GRENADE, TANK_BONUS) = range(4)


class Bonus:
    def __init__(self, bonus_type, position, level):
        self.type = bonus_type
        self.level = level
        self.images = [BOLD_SPRITES.subsurface((287, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((303, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((319, 111, 16, 15)),
                       BOLD_SPRITES.subsurface((335, 111, 16, 15))]
        self.image = self.images[bonus_type]
        self.rect = pygame.Rect(position[0], position[1], 16, 15)

    def die(self):
        if self in self.level.bonuses:
            self.level.bonuses.remove(self)
