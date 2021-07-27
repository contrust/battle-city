import json

from game import Game

if __name__ == '__main__':
    g = Game()
    try:
        with open('settings.txt') as json_file:
            data = json.load(json_file)
            g.__dict__.update(data)
    except IOError:
        pass
    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()
