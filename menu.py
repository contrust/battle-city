import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 480), 0, 32)
font = pygame.font.SysFont(None, 60)
mainClock = pygame.time.Clock()

def draw_text(text, font, color, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (screen.get_width()/2, screen.get_height()/6)
    surface.blit(textobj, textrect)

def main_menu():
    click = False
    screen.fill((0, 0, 0))
    while 1:
        draw_text('Battle city', font, (160, 54, 35), screen)
        text = font.render('Play', True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.x = (screen.get_width()-textRect.width)/2
        textRect.y = screen.get_width()/4
        mx, my = pygame.mouse.get_pos()
        if textRect.collidepoint((mx, my)):
            if click:
                return
        screen.blit(text, textRect)
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
