import json

import pygame

from game import Game

if __name__ == '__main__':
    g = Game()
    try:
        with open('settings.txt') as json_file:
            data = json.load(json_file)
            g.__dict__.update(data)
            if g.toggle_fullscreen:
                g.window = pygame.display.set_mode(
                    (g.DISPLAY_W, g.DISPLAY_H),
                    pygame.SCALED | pygame.FULLSCREEN | pygame.NOFRAME)
    except IOError:
        pass
    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()
