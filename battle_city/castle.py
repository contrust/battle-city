from battle_city.sprites import BOLD_SPRITES
import pygame


class Castle:
    def __init__(self, level=None):
        self.images = [BOLD_SPRITES.subsurface((304, 32, 16, 16)),
                       BOLD_SPRITES.subsurface((320, 32, 16, 16))]
        self.level = level
        self.image = self.images[0]
        self.is_alive = True
        self.rect = pygame.Rect(96, 208, 16, 16)

    def die(self):
        self.image = self.images[1]
        self.is_alive = False
        pygame.mixer.music.load('../sounds/game_over.ogg')
        pygame.mixer.music.set_volume(self.level.volume_level)
        pygame.mixer.music.play()
