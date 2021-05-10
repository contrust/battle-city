import pygame
from menu import *
import sys

from pygame.locals import *
from random import randrange
from sprites import SPRITES, BOLD_SPRITES, BULLET_IMAGES, TANKS_IMAGES
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from tank import (Tank, BASIC, FAST, RAPID, ARMORED, DIRECTION_UP,
            DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT)
from settings import WINDOW_SIZE, SCREEN, DISPLAY, get_hit_list
from bullet import Bullet
from enemy import Enemy
from level import Level


class Game():
    def __init__(self):
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        pygame.init()
        pygame.display.set_caption('Battle City')
        self.DISPLAY_W, self.DISPLAY_H = 208, 224
        self.small_display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H), pygame.SCALED)
        self.level = Level(1, 1, self)
        self.unlocked_levels = 1
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.level_selection = LevelSelection(self)
        self.curr_menu = self.main_menu
        self.next_round_menu = NextRoundMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.CLOCK = pygame.time.Clock()

    def draw(self, entity):
        self.small_display.blit(entity.image, entity.rect.topleft)

    def game_loop(self):
        while self.playing:
            self.small_display.fill(self.BLACK)
            self.check_events()
            if self.level.get_score() >= 4:
                if self.level.number == 4:
                    self.win()
                else:
                    if self.level.number == self.unlocked_levels:
                        self.unlocked_levels += 1
                    self.go_to_next_round()
            if not self.level.castle.is_alive:
                self.game_over()
            if not self.level.players:
                continue
            if not self.level.players[0].is_alive:
                if self.level.players[0].lifes:
                    self.level.players[0].kind = 0
                    self.level.players[0].get_type()
                    self.level.players[0].is_alive = True
                else:
                    self.game_over()
            if len(self.level.players) == 2:
                if not self.level.players[1].is_alive:
                    if self.level.players[1].lifes:
                        self.level.players[1].kind = 0
                        self.level.players[1].get_type()
                        self.level.players[1].is_alive = True
                    else:
                        self.game_over()
            for player in self.level.players:
                self.draw(player)
                player.move()

            if not randrange(250):
                if len(self.level.enemies) < 4:
                    if self.level.get_score() + len(self.level.enemies) < 5:
                        rnd = randrange(0, 2)
                        if rnd == 0:
                            self.level.enemies.append(Enemy(randrange(4), 1 / 2, 0, (96 * randrange(3), 0), 0, self.level))
                        if rnd == 1:
                            self.level.enemies.append(Enemy(randrange(4), 1 / 2, 0, (96 * randrange(3), 0), 1, self.level))
                    else:
                        self.level.enemies.append(Enemy(randrange(4), 1 / 2, 0, (96 * randrange(3), 0), 2, self.level))
            for enemy in self.level.enemies:
                self.draw(enemy)
                if not randrange(140):
                    if enemy.target == 2:
                        enemy.find_path((96, 208), 1, self.level)
                    if enemy.target == 0:
                        try:
                            enemy.find_path(self.level.players[0].rect.topleft, 0, self.level)
                        except IndexError:
                            enemy.find_path(self.level.players[1].rect.topleft, 0, self.level)
                    if enemy.target == 1:
                        try:
                            enemy.find_path(self.level.players[1].rect.topleft, 0, self.level)
                        except IndexError:
                            enemy.find_path(self.level.players[0].rect.topleft, 0, self.level)
                enemy.move()
                if not randrange(50):
                    enemy.fire()

            for bullet in self.level.bullets:
                self.draw(bullet)

            for tile in self.level.map:
                self.draw(tile)

            for bonus in self.level.bonuses:
                self.draw(bonus)

            for bullet in self.level.bullets[:]:
                bullet.fly()

            for explosion in self.level.explosions:
                self.draw(explosion)
                if explosion.type == 0:
                    explosion.image = explosion.images[explosion.stage // 2]
                    explosion.stage += 1
                    if explosion.stage == 8:
                        self.level.explosions.remove(explosion)
                if explosion.type == 1:
                    explosion.image = explosion.images[explosion.stage // 3 + 4]
                    explosion.stage += 1
                    if explosion.stage == 9:
                        self.level.explosions.remove(explosion)

            self.draw(self.level.castle)
            if self.BACK_KEY:
                self.playing = False
            self.window.blit(self.small_display, (0, 0))
            pygame.display.update()
            self.reset_keys()
            self.CLOCK.tick(60)

    def win(self):
        self.playing = False
        pygame.mixer.music.load('sounds/win_game.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.curr_menu = self.credits

    def go_to_next_round(self):
        self.playing = False
        pygame.mixer.music.load('sounds/next_level.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.curr_menu = self.next_round_menu

    def game_over(self):
        self.playing = False
        pygame.mixer.music.load('sounds/game_over.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.curr_menu = self.game_over_menu



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == KEYDOWN:
                for player in self.level.players:
                    if event.key in player.controls.keys():
                        player.pressed_keys[player.controls[event.key]] = True
                    if event.key == K_SPACE and player.number == 0:
                        player.fire()
                    if event.key == K_LALT and player.number == 1:
                        player.fire()
                    if event.key == K_F9:
                        for enemy in self.level.enemies[:]:
                            self.level.players[0].score[enemy.kind] += 1
                            enemy.die()
                    if event.key == K_F10:
                        if player.kind != 3:
                            player.kind += 1
                    if event.key == K_F11:
                        for protecting_block in self.level.protecting_blocks:
                            self.level.map.append(Tile(BETON, protecting_block))
                    if event.key == K_F12 and self.curr_menu != self.next_round_menu:
                        if self.level.number == 4:
                            self.win()
                        else:
                            if self.level.number == self.unlocked_levels:
                                self.unlocked_levels += 1
                            self.go_to_next_round()
                            break
            if event.type == KEYUP:
                for player in self.level.players:
                    if event.key in player.controls.keys():
                        player.pressed_keys[player.controls[event.key]] = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.small_display.blit(text_surface,text_rect)