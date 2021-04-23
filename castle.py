from sprites import BOLD_SPRITES
import pygame
from menu import main_menu

class Castle:
    def __init__(self, level=None):
        self.images = [BOLD_SPRITES.subsurface((304, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((320, 32, 16, 16))]
        self.level = level
        self.image = self.images[0]
        self.rect = pygame.Rect(96, 208, 16, 16)

    def die(self):
        self.image = self.images[1]
        self.level.castle = None
        main_menu(self.level.player.score, True)