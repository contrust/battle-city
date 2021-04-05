import pygame, sys

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *

pygame.init()  # initialize pygame

pygame.display.set_caption('Battle City')  # set the window name

WINDOW_SIZE = (600, 480)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initialize the window

display = pygame.Surface((320, 240))

sprites = pygame.image.load('sprite.png').convert_alpha()
player_image_up = sprites.subsurface((0, 0, 16, 16))
player_image_down = sprites.subsurface((64, 0, 16, 16))
player_image_right = sprites.subsurface((96, 0, 16, 16))
player_image_left = sprites.subsurface((32, 0, 16, 16))
player_image = player_image_up


moving_right = False
moving_left = False
moving_up = False
moving_down = False

grass_image = sprites.subsurface((272, 32, 16, 16))
TILE_SIZE = grass_image.get_width()
brick_image = sprites.subsurface((256, 0, 16, 16))

game_map = [['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1', '2'],
            ['2', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '0', '1', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '2', '1', '1', '2', '0', '2', '0', '2', '2', '2'],
            ['2', '0', '0', '2', '0', '0', '0', '0', '0', '0', '2', '1', '1', '2', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '0', '0', '0', '2', '2', '2', '2', '0', '0', '0', '0', '2', '2'],
            ['2', '0', '0', '0', '1', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '0', '0', '1', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2'],
            ['2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
            ]

player_y_momentum = 0

player_rect = pygame.Rect(50,
                          50,
                          player_image_up.get_width(),
                          player_image_up.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    if movement[0] != 0:
        if 0 <= rect.x + movement[0] <= display.get_width() - player_image.get_width():
            rect.x += movement[0]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if tile[1] != '1':
                if movement[0] > 0:
                    rect.right = tile[0].left
                    collision_types['right'] = True
                else:
                    rect.left = tile[0].right
                    collision_types['left'] = True
    else:
        if 0 <= rect.y + movement[1] <= display.get_height() - player_image.get_height():
            rect.y += movement[1]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if tile[1] != '1':
                if movement[1] > 0:
                    rect.bottom = tile[0].top
                    collision_types['bottom'] = True
                else:
                    rect.top = tile[0].bottom
                    collision_types['top'] = True
    return rect, collision_types


while True:
    display.fill((0, 0, 0))

    display.blit(player_image, (player_rect.x, player_rect.y))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(brick_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append((pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), tile))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
        player_image = player_image_right
    if moving_left == True:
        player_movement[0] -= 2
        player_image = player_image_left
    if moving_up == True:
        player_movement[1] -= 2
        player_image = player_image_up
    if moving_down == True:
        player_movement[1] += 2
        player_image = player_image_down

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255, 0, 0), test_rect)
    else:
        pygame.draw.rect(screen, (0, 0, 0), test_rect)

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                moving_up = True
            if event.key == K_DOWN:
                moving_down = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
