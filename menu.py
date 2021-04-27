import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 480), 0, 32)
font = pygame.font.SysFont(None, 60)
mainClock = pygame.time.Clock()
SPRITES = pygame.image.load('sprite.png').convert_alpha()
button = None
tanks_images = [pygame.transform.scale(SPRITES.subsurface((128, 0, 16, 16)),
                                       (48, 48)),
                pygame.transform.scale(SPRITES.subsurface((128, 16, 16, 16)),
                                       (48, 48)),
                pygame.transform.scale(SPRITES.subsurface((128, 32, 16, 16)),
                                       (48, 48)),
                pygame.transform.scale(SPRITES.subsurface((128, 48, 16, 16)),
                                       (48, 48))]


def draw_text(text, font, color, surface, x, y, show_stat=False, score=None):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    if show_stat:
        surface.blit(tanks_images[0], (80, 144))
        surface.blit(tanks_images[1], (80, 204))
        surface.blit(tanks_images[2], (80, 264))
        surface.blit(tanks_images[3], (80, 324))
        surface.blit(font.render(str(score[0]), 1,
                                 (255, 255, 255)), (160, 152))
        surface.blit(font.render(str(score[1]), 1,
                                 (255, 255, 255)), (160, 212))
        surface.blit(font.render(str(score[2]), 1,
                                 (255, 255, 255)), (160, 272))
        surface.blit(font.render(str(score[3]), 1,
                                 (255, 255, 255)), (160, 332))


def main_menu(score=None, status="Battle City"):
    click = False
    screen.fill((0, 0, 0))
    global button
    while 1:
        if status == "You won":
            draw_text('You won', font, (160, 54, 35),
                      screen, screen.get_width() / 2,
                      screen.get_height() / 8, True, score)
            button = font.render('Back to menu', True,
                                 (255, 255, 255), (0, 0, 0))
        if status == "Game Over":
            draw_text('Game Over', font, (160, 54, 35),
                      screen, screen.get_width()/2,
                      screen.get_height()/8, True, score)
            button = font.render('Try again', True, (255, 255, 255), (0, 0, 0))
        if status == "Battle City":
            draw_text('Battle City', font, (160, 54, 35),
                      screen, screen.get_width()/2, screen.get_height()/8)
            button = font.render('Play', True, (255, 255, 255), (0, 0, 0))
        if status == "Victory":
            draw_text('Victory', font, (160, 54, 35),
                      screen, screen.get_width()/2,
                      screen.get_height()/8, True, score)
            button = font.render('Next level', True,
                                 (255, 255, 255), (0, 0, 0))
        button_rect = button.get_rect()
        button_rect.x = (screen.get_width() - button_rect.width) / 2
        button_rect.y = screen.get_width() / 4.5
        mx, my = pygame.mouse.get_pos()
        if button_rect.collidepoint((mx, my)):
            if click:
                return
        screen.blit(button, button_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        mainClock.tick(60)


if __name__ == '__main__':
    main_menu()
