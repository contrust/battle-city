import pygame
DISPLAY_W, DISPLAY_H = 480, 270
display = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
SPRITES = pygame.image.load('sprite.png').convert_alpha()
BOLD_SPRITES = pygame.image.load('sprite.png')
BULLET_IMAGES = [SPRITES.subsurface((322, 102, 4, 4)),
                 SPRITES.subsurface((338, 102, 4, 4)),
                 SPRITES.subsurface((346, 102, 4, 4)),
                 SPRITES.subsurface((330, 102, 4, 4))]
HEART = pygame.image.load('heart.png').convert_alpha()
TANKS_IMAGES = [[], []]
for i in range(2):
    for j in range(4):
        TANKS_IMAGES[i].append([SPRITES.subsurface((128 * i,
                                                    j * 16, 16, 16)),
                                SPRITES.subsurface((128 * i + 64,
                                                    j * 16, 16, 16)),
                                SPRITES.subsurface((128 * i + 96,
                                                    j * 16, 16, 16)),
                                SPRITES.subsurface((128 * i + 32,
                                                    j * 16, 16, 16)),
                                SPRITES.subsurface((128 * i,
                                                    j * 16 + 128, 16, 16)),
                                SPRITES.subsurface((128 * i + 64,
                                                    j * 16 + 128, 16, 16)),
                                SPRITES.subsurface((128 * i + 96,
                                                    j * 16 + 128, 16, 16)),
                                SPRITES.subsurface((128 * i + 32,
                                                    j * 16 + 128, 16, 16))])
