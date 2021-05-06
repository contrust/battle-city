#!/usr/bin/python
# coding=utf-8
import sys

import pygame
from menu import main_menu
from pygame.locals import *
from random import randrange
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from sprites import SPRITES, BOLD_SPRITES, BULLET_IMAGES, TANKS_IMAGES
from tank import (Tank, BASIC, FAST, RAPID, ARMORED, DIRECTION_UP,
                  DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT)
from settings import WINDOW_SIZE, SCREEN, DISPLAY, get_hit_list
from bullet import Bullet
from enemy import Enemy
from level import Level

CLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Battle City')


def draw(entity):
    DISPLAY.blit(entity.image, entity.rect.topleft)


def win_game():
    global level_number, current_level
    pygame.mixer.music.load('sounds/win_game.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    main_menu(current_level.player[0].score, "You won")
    main_menu()
    level_number = 1
    current_level = Level(1)


level_number = 1
current_level = Level(level_number)
main_menu()

while 1:
    if sum([sum(player.score) for player in current_level.players]) >= 4:
        if level_number == 4:
            win_game()
        else:
            pygame.mixer.music.load('sounds/next_level.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            main_menu(current_level.players[0].score, "Victory")
            level_number += 1
            for player in current_level.players:
                player.score = [0, 0, 0, 0]
                player.to_start()
            current_level = Level(level_number, current_level.players)
    if not current_level.castle.is_alive:
        current_level = Level(1)
        level_number = 1
    if not current_level.players[0].is_alive:
        if current_level.players[0].lifes:
            current_level.players[0].kind = 0
            current_level.players[0].get_type()
            current_level.players[0].is_alive = True
        else:
            current_level = Level(1)
            level_number = 1
    DISPLAY.fill((0, 0, 0))
    for player in current_level.players:
        DISPLAY.blit(player.image, player.rect.topleft)
        player.move()

    if not randrange(250):
        if len(current_level.enemies) < 4:
            if (sum([sum(player.score) for player in current_level.players]) +
               len(current_level.enemies) < 5):
                current_level.enemies.append(Enemy(randrange(4), 1 / 2, 0,
                                                   (96 * randrange(3), 0),
                                                   0, current_level))
            else:
                current_level.enemies.append(Enemy(randrange(4), 1 / 2, 0,
                                                   (96 * randrange(3), 0),
                                                   1, current_level))
    for enemy in current_level.enemies:
        draw(enemy)
        if not randrange(140):
            if enemy.target == 1:
                enemy.find_path((96, 208), 1, current_level)
            else:
                enemy.find_path(current_level.players[0].rect.topleft,
                                0, current_level)
        enemy.move()
        if not randrange(50):
            enemy.fire()

    for bullet in current_level.bullets:
        draw(bullet)

    for tile in current_level.map:
        draw(tile)

    for bonus in current_level.bonuses:
        draw(bonus)

    for bullet in current_level.bullets[:]:
        bullet.fly()

    for explosion in current_level.explosions:
        draw(explosion)
        if explosion.type == 0:
            explosion.image = explosion.images[explosion.stage // 2]
            explosion.stage += 1
            if explosion.stage == 8:
                current_level.explosions.remove(explosion)
        if explosion.type == 1:
            explosion.image = explosion.images[explosion.stage // 3 + 4]
            explosion.stage += 1
            if explosion.stage == 9:
                current_level.explosions.remove(explosion)

    draw(current_level.castle)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            for player in current_level.players:
                if event.key in player.controls.keys():
                    player.pressed_keys[player.controls[event.key]] = True
                if event.key == K_ESCAPE:
                    main_menu()
                    level_number = 1
                    current_level = Level(1)
                if event.key == K_SPACE:
                    player.fire()
                if event.key == K_F9:
                    for enemy in current_level.enemies[:]:
                        enemy.die()
                if event.key == K_F10:
                    if player.kind != 3:
                        player.kind += 1
                if event.key == K_F11:
                    for protecting_block in current_level.protecting_blocks:
                        current_level.map.append(Tile(BETON, protecting_block))
                if event.key == K_F12:
                    level_number += 1
                    if level_number == 5:
                        win_game()
                    else:
                        current_level = Level(level_number)
                        break
        if event.type == KEYUP:
            for player in current_level.players:
                if event.key in player.controls.keys():
                    player.pressed_keys[player.controls[event.key]] = False

    surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
    SCREEN.blit(surf, (0, 0))
    pygame.display.update()
    CLOCK.tick(60)
