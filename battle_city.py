#!/usr/bin/python
# coding=utf-8
from game import Game

if __name__ == '__main__':
    g = Game()
    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()
