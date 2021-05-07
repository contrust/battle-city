import pygame
import sys
from level import Level
from enemy import Enemy
from random import randrange

players_count = 1


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 75

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.small_display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "1 Player"
        self.oneplayerx, self.oneplayery = self.mid_w, self.mid_h + 10
        self.twoplayersx, self.twoplayersy = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.oneplayerx + self.offset, self.oneplayery)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('Battle City', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("1 Player", 15, self.oneplayerx, self.oneplayery)
            self.game.draw_text("2 Players", 15, self.twoplayersx, self.twoplayersy)
            self.game.draw_text("Options", 15, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 15, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 15, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == '1 Player':
                self.cursor_rect.midtop = (self.twoplayersx + self.offset, self.twoplayersy)
                self.state = '2 Players'
            elif self.state == '2 Players':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.oneplayerx + self.offset, self.oneplayery)
                self.state = '1 Player'
        elif self.game.UP_KEY:
            if self.state == '1 Player':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == '2 Players':
                self.cursor_rect.midtop = (self.oneplayerx + self.offset, self.oneplayery)
                self.state = '1 Player'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.twoplayersx + self.offset, self.twoplayersy)
                self.state = '2 Players'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        global players_count
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == '1 Player':
                players_count = 1
                self.game.level = Level(1, players_count, self.game)
                self.game.playing = True
            elif self.state == '2 Players':
                players_count = 2
                self.game.level = Level(1, players_count, self.game)
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                pygame.quit()
                sys.exit()
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.small_display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # Здесь можно сделать контролы и громкость, но мне лень, да и это в принципе не нужно
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        global players_count
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.level = Level(1, players_count, self)
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Artyom Borisov', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Artyom Burgart', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.blit_screen()

class GameOverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        global players_count
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.level = Level(1, players_count, self)
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('GAME OVER', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.blit_screen()

class NextRoundMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.enemies = [Enemy(0, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6, self.game.DISPLAY_H / 2 - 6), 0, self.game.level),
                        Enemy(1, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6, self.game.DISPLAY_H / 2 + 14), 0, self.game.level),
                        Enemy(2, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6, self.game.DISPLAY_H / 2 + 34), 0, self.game.level),
                        Enemy(3, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6, self.game.DISPLAY_H / 2 + 54), 0, self.game.level)]


    def display_menu(self):
        global players_count
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.playing = True
                for player in self.game.level.players:
                        player.score = [0, 0, 0, 0]
                        player.to_start()
                self.game.level = Level(self.game.level.number + 1, players_count, self)
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('Victory', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            for i in range(len(self.game.level.players)):
                for j in range(4):
                    self.game.draw(self.enemies[j])
                    self.game.draw_text(str(self.game.level.players[i].score[j]), 15, self.game.DISPLAY_W / 2 - 50 + 100 * i, self.game.DISPLAY_H / 2 + 20 * j)
            self.blit_screen()