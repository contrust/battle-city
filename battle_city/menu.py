import json
import sys

import pygame

from battle_city.enemy import Enemy
from battle_city.level import Level

players_count = 1


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = (self.game.DISPLAY_W / 2,
                                  self.game.DISPLAY_H / 2)
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 75
        pygame.mixer.music.load('../sounds/main_theme.ogg')
        pygame.mixer.music.set_volume(self.game.volume_level)
        pygame.mixer.music.play()

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.background, (0, 0))
        self.game.background.fill(self.game.BLACK)
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "1 Player"
        self.oneplayerx, self.oneplayery = self.mid_w, self.mid_h - 10
        self.twoplayersx, self.twoplayersy = self.mid_w, self.mid_h + 10
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 30
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 50
        self.exitx, self.exity = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (
            self.oneplayerx + self.offset, self.oneplayery)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('Battle City', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 40)
            self.game.draw_text("1 Player", 15, self.oneplayerx,
                                self.oneplayery)
            self.game.draw_text("2 Players", 15, self.twoplayersx,
                                self.twoplayersy)
            self.game.draw_text("Options", 15, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 15, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 15, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == '1 Player':
                self.cursor_rect.midtop = (
                    self.twoplayersx + self.offset, self.twoplayersy)
                self.state = '2 Players'
            elif self.state == '2 Players':
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset,
                                           self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (
                    self.oneplayerx + self.offset, self.oneplayery)
                self.state = '1 Player'
        elif self.game.UP_KEY:
            if self.state == '1 Player':
                self.cursor_rect.midtop = (self.exitx + self.offset,
                                           self.exity)
                self.state = 'Exit'
            elif self.state == '2 Players':
                self.cursor_rect.midtop = (
                    self.oneplayerx + self.offset, self.oneplayery)
                self.state = '1 Player'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.twoplayersx + self.offset, self.twoplayersy)
                self.state = '2 Players'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        global players_count
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == '1 Player':
                players_count = 1
                self.game.curr_menu = self.game.level_selection
            elif self.state == '2 Players':
                players_count = 2
                self.game.curr_menu = self.game.level_selection
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                with open('settings.txt', mode='w') as file:
                    json.dump({
                        'toggle_fullscreen': self.game.toggle_fullscreen,
                        'unlocked_levels': self.game.unlocked_levels,
                        'volume_level': self.game.volume_level
                    }, file, indent=4)
                self.game.window = pygame.display.set_mode(
                    (self.game.DISPLAY_W, self.game.DISPLAY_H),
                    pygame.SCALED)
                pygame.quit()
                sys.exit()
            self.run_display = False


class LevelSelection(Menu):
    global players_count

    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = '1 Level'
        self.firstlevelx, self.firstlevely = self.mid_w, self.mid_h - 40
        self.secondlevelx, self.secondlevely = self.mid_w, self.mid_h - 20
        self.thirdlevelx, self.thirdlevely = self.mid_w, self.mid_h
        self.fourthlevelx, self.fourthlevely = self.mid_w, self.mid_h + 20
        self.fifthlevelx, self.fifthlevely = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (
            self.firstlevelx + self.offset, self.firstlevely)
        self.max_position = (self.firstlevelx + self.offset, self.firstlevely)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.small_display.fill((0, 0, 0))
            self.game.draw_text('Select level', 18, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 70)
            self.game.draw_text("1 Level", 15, self.firstlevelx,
                                self.firstlevely)
            if self.game.unlocked_levels > 1:
                self.game.draw_text("2 Level", 15, self.secondlevelx,
                                    self.secondlevely)
                self.max_position = (
                    self.secondlevelx + self.offset, self.secondlevely)
            if self.game.unlocked_levels > 2:
                self.game.draw_text("3 Level", 15, self.thirdlevelx,
                                    self.thirdlevely)
                self.max_position = (
                    self.thirdlevelx + self.offset, self.thirdlevely)
            if self.game.unlocked_levels > 3:
                self.game.draw_text("4 Level", 15, self.fourthlevelx,
                                    self.fourthlevely)
                self.max_position = (
                    self.fourthlevelx + self.offset, self.fourthlevely)
            if self.game.unlocked_levels > 4:
                self.game.draw_text("5 Level", 15, self.fifthlevelx,
                                    self.fifthlevely)
                self.max_position = (
                    self.fifthlevelx + self.offset, self.fifthlevely)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.DOWN_KEY:
            if self.state == (str(self.game.unlocked_levels) + ' Level'):
                self.cursor_rect.midtop = (
                    self.firstlevelx + self.offset, self.firstlevely)
                self.state = '1 Level'
            elif self.state == '1 Level' and self.game.unlocked_levels > 1:
                self.cursor_rect.midtop = (
                    self.secondlevelx + self.offset, self.secondlevely)
                self.state = '2 Level'
            elif self.state == '2 Level' and self.game.unlocked_levels > 2:
                self.cursor_rect.midtop = (
                    self.thirdlevelx + self.offset, self.thirdlevely)
                self.state = '3 Level'
            elif self.state == '3 Level' and self.game.unlocked_levels > 3:
                self.cursor_rect.midtop = (
                    self.fourthlevelx + self.offset, self.fourthlevely)
                self.state = '4 Level'
            elif self.state == '4 Level':
                self.cursor_rect.midtop = (
                    self.fifthlevelx + self.offset, self.fifthlevely)
                self.state = '5 Level'
            elif self.state == '5 Level':
                self.cursor_rect.midtop = (
                    self.firstlevelx + self.offset, self.firstlevely)
                self.state = '1 Level'
        if self.game.UP_KEY:
            if self.state == '1 Level':
                self.cursor_rect.midtop = self.max_position
                self.state = str(self.game.unlocked_levels) + ' Level'
            elif self.state == '2 Level':
                self.cursor_rect.midtop = (
                    self.firstlevelx + self.offset, self.firstlevely)
                self.state = '1 Level'
            elif self.state == '3 Level' and self.game.unlocked_levels > 1:
                self.cursor_rect.midtop = (
                    self.secondlevelx + self.offset, self.secondlevely)
                self.state = '2 Level'
            elif self.state == '4 Level' and self.game.unlocked_levels > 2:
                self.cursor_rect.midtop = (
                    self.thirdlevelx + self.offset, self.thirdlevely)
                self.state = '3 Level'
            elif self.state == '5 Level' and self.game.unlocked_levels > 2:
                self.cursor_rect.midtop = (
                    self.fourthlevelx + self.offset, self.fourthlevely)
                self.state = '4 Level'
        if self.game.START_KEY:
            if self.state == "1 Level":
                self.game.level = Level(1, players_count, self.game)
                self.game.playing = True
            elif self.state == "2 Level":
                self.game.level = Level(2, players_count, self.game)
                self.game.playing = True
            elif self.state == "3 Level":
                self.game.level = Level(3, players_count, self.game)
                self.game.playing = True
            elif self.state == "4 Level":
                self.game.level = Level(4, players_count, self.game)
                self.game.playing = True
            elif self.state == "5 Level":
                self.game.level = Level(5, players_count, self.game)
                self.game.playing = True
        self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Fullscreen'
        self.fullscreenx, self.fullscreeny = self.mid_w, self.mid_h + 20
        self.fsstatusx, self.fsstatusy = self.mid_w + 84, self.mid_h + 20
        self.volx, self.voly = self.mid_w, self.mid_h + 40
        self.volstatusx, self.volstatusy = self.mid_w + 84, self.mid_h + 40
        self.cursor_rect.midtop = (
            self.fullscreenx + self.offset, self.fullscreeny)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.small_display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Fullscreen", 12, self.fullscreenx,
                                self.fullscreeny)
            if self.game.toggle_fullscreen:
                self.game.draw_text("On", 12, self.fsstatusx, self.fsstatusy)
            else:
                self.game.draw_text("Off", 12, self.fsstatusx, self.fsstatusy)
            self.game.draw_text("Volume", 12, self.volx, self.voly)
            self.game.draw_text(str(round(self.game.volume_level * 10)), 12,
                                self.volstatusx, self.volstatusy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Fullscreen':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            elif self.state == 'Volume':
                self.state = 'Fullscreen'
                self.cursor_rect.midtop = (
                    self.fullscreenx + self.offset, self.fullscreeny)
        if self.game.START_KEY:
            if self.state == 'Fullscreen':
                if self.game.toggle_fullscreen:
                    for x in range(2):
                        self.game.window = pygame.display.set_mode(
                            (self.game.DISPLAY_W, self.game.DISPLAY_H),
                            pygame.SCALED)
                    self.game.toggle_fullscreen = False
                else:
                    self.game.window = pygame.display.set_mode(
                        (self.game.DISPLAY_W, self.game.DISPLAY_H),
                        pygame.SCALED | pygame.FULLSCREEN | pygame.NOFRAME)
                    self.game.toggle_fullscreen = True
        if self.state == 'Volume':
            if self.game.RIGHT_KEY:
                self.game.volume_level = round(self.game.volume_level + 0.1, 1)
            if self.game.LEFT_KEY:
                if self.game.volume_level >= 0.1:
                    self.game.volume_level = round(self.game.volume_level - 0.1,
                                                   1)


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
                self.game.level = Level(1, players_count, self.game)
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Artyom Borisov', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Artyom Burgart', 15, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 40)
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
                self.game.level = Level(1, players_count, self.game)
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('GAME OVER', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2)
            self.blit_screen()


class NextRoundMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.enemies = [Enemy(0, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6,
                                            self.game.DISPLAY_H / 2 - 6), 0,
                              self.game.level),
                        Enemy(1, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6,
                                            self.game.DISPLAY_H / 2 + 14), 0,
                              self.game.level),
                        Enemy(2, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6,
                                            self.game.DISPLAY_H / 2 + 34), 0,
                              self.game.level),
                        Enemy(3, 1 / 2, 0, (self.game.DISPLAY_W / 2 - 6,
                                            self.game.DISPLAY_H / 2 + 54), 0,
                              self.game.level)]

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
                    if player.number == 0:
                        player.to_start(64, 208)
                    if player.number == 1:
                        player.to_start(128, 208)
                self.game.level = Level(self.game.level.number + 1,
                                        players_count, self.game)
            self.game.small_display.fill(self.game.BLACK)
            self.game.draw_text('Victory', 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 40)
            for i in range(len(self.game.level.players)):
                for j in range(4):
                    self.game.background.blit(self.enemies[j].image,
                                              self.enemies[j].rect.topleft)
                    if self.game.level.players[i].score[j] == 0:
                        self.game.draw_text("O", 15,
                                            (self.game.DISPLAY_W / 2 -
                                             50 + 100 * i),
                                            self.game.DISPLAY_H / 2 + 20 * j)
                    else:
                        self.game.draw_text(
                            str(self.game.level.players[i].score[j]), 15,
                            self.game.DISPLAY_W / 2 - 50 + 100 * i,
                            self.game.DISPLAY_H / 2 + 20 * j)
            self.blit_screen()
