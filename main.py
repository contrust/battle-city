import pygame, sys, threading
from menu import main_menu
from pygame.locals import *
from random import randrange
from tile import Tile, BRICK, GRASS, BETON, ICE, WATER
from sprites import SPRITES, BOLD_SPRITES, BULLET_IMAGES, TANKS_IMAGES
from tank import Tank, BASIC, FAST, RAPID, ARMORED, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_RIGHT, DIRECTION_LEFT
from settings import WINDOW_SIZE, SCREEN, DISPLAY, get_hit_list
from bullet import Bullet
from enemy import Enemy
from level import Level

CLOCK = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Battle City')

def draw(entity):
    DISPLAY.blit(entity.image, (entity.rect.x, entity.rect.y))

current_level = Level()
main_menu()

while 1:
    if not current_level.castle.is_alive:
        current_level = Level()
    if not current_level.player.is_alive:
        if current_level.player.lifes:
            current_level.player.x, current_level.player.y, current_level.player.rect.topleft = 64, 208, (64, 208)
            current_level.player.kind = 0
            current_level.player.get_type()
            current_level.player.is_alive = True
        else:
            current_level = Level()
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(current_level.player.image, (current_level.player.rect.x, current_level.player.rect.y))
    current_level.player.move()

    if not randrange(250):
        if len(current_level.enemies) < 4:
            current_level.enemies.append(Enemy(randrange(4), 1 / 2, 0, (96 * randrange(3), 0), randrange(2), current_level))
    for enemy in current_level.enemies:
        draw(enemy)
        if not randrange(140):
            if enemy.target == 0:
                enemy.find_path((96, 208), 1, current_level)
            else:
                enemy.find_path((current_level.player.rect.x, current_level.player.rect.y), 0, current_level)
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

    draw(current_level.castle)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                current_level.player.pressed_keys[DIRECTION_RIGHT] = True
            if event.key == K_LEFT:
                current_level.player.pressed_keys[DIRECTION_LEFT] = True
            if event.key == K_UP:
                current_level.player.pressed_keys[DIRECTION_UP] = True
            if event.key == K_DOWN:
                current_level.player.pressed_keys[DIRECTION_DOWN] = True
            if event.key == K_ESCAPE:
                main_menu()
                create_level()
            if event.key == K_SPACE:
                current_level.player.fire()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                current_level.player.pressed_keys[DIRECTION_RIGHT] = False
            if event.key == K_LEFT:
                current_level.player.pressed_keys[DIRECTION_LEFT] = False
            if event.key == K_UP:
                current_level.player.pressed_keys[DIRECTION_UP] = False
            if event.key == K_DOWN:
                current_level.player.pressed_keys[DIRECTION_DOWN] = False

    surf = pygame.transform.scale(DISPLAY, WINDOW_SIZE)
    SCREEN.blit(surf, (0, 0))
    pygame.display.update()
    CLOCK.tick(60)
