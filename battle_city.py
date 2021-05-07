#!/usr/bin/python
# coding=utf-8
from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()