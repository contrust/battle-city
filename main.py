import pygame, sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import *
pygame.init() # initialize pygame

pygame.display.set_caption('Battle City')  # set the window name

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initialize the window

display = pygame.Surface((320, 200))

player_image = pygame.image.load('gold_player.png')

moving_right = False
moving_left = False

grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
brick_image = pygame.image.load('full_brick.png')

game_map = [['0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '1'],
            ['1', '1', '1', '1', '1', '1'],
            ['2', '2', '2', '2', '2', '2'],
            ['2', '2', '2', '2', '2', '2']]

player_location = [50, 50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0],
                          player_location[1],
                          player_image.get_width(),
                          player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

while True:
    display.fill((0, 0, 0))

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
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1


    display.blit(player_image, player_location)

    #player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255,0,0), test_rect)
    else:
        pygame.draw.rect(screen, (0,0,0), test_rect)


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False


    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)