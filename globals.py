import pygame
from itertools import chain
WINDOW_SIZE = (400, 400)
SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
DISPLAY = pygame.Surface((208, 224))


def get_hit_list(rect, *entities):
    return [entity for entity in list(chain(*entities))
            if rect.colliderect(entity.rect)]
