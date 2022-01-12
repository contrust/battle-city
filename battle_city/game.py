from random import randrange

from pygame.locals import *

from battle_city.menu import *
from battle_city.sprites import HEART
from battle_city.tile import Tile, BETON


class Game:
    def __init__(self):
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, \
            self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = (
                False, False, False, False, False, False)
        pygame.init()
        pygame.display.set_caption('Battle City')
        self.DISPLAY_W, self.DISPLAY_H = 240, 224
        self.small_display = pygame.Surface(
            (self.DISPLAY_W - 32, self.DISPLAY_H))
        self.background = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H),
                                              SCALED)
        self.volume_level = 0.3
        self.level = Level(1, 1, self)
        self.unlocked_levels = 1
        self.toggle_fullscreen = True
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE, self.GRAY = (0, 0, 0), \
                                            (255, 255, 255), \
                                            (60, 60, 60)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.level_selection = LevelSelection(self)
        self.curr_menu = self.main_menu
        self.next_round_menu = NextRoundMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.CLOCK = pygame.time.Clock()
        self.cheat_command = ""

    def draw(self, entity):
        self.small_display.blit(entity.image, entity.rect.topleft)

    def game_loop(self):
        while self.playing:
            self.background.fill(self.GRAY)
            self.small_display.fill(self.BLACK)
            self.check_events()
            if self.level.get_score() >= 10:
                self.process_next_round_transition()
            if not self.level.castle.is_alive:
                self.game_over()
            if not self.level.players:
                continue
            if not self.level.players[0].is_alive:
                self.process_player_death(0)
            if len(self.level.players) == 2:
                if not self.level.players[1].is_alive:
                    self.process_player_death(1)
            for player in self.level.players:
                self.draw(player)
                for i in range(player.lifes):
                    self.background.blit(HEART,
                                         (224 if player.number else 0, i * 16))
                player.move()
            if not randrange(250):
                self.create_random_enemy()
            self.update_enemies()
            for bullet in self.level.bullets:
                self.draw(bullet)
            for tile in self.level.game_map:
                self.draw(tile)
            for bonus in self.level.bonuses:
                self.draw(bonus)
            for bullet in self.level.bullets[:]:
                bullet.fly()
            self.update_explosions()
            self.draw(self.level.castle)
            self.window.blit(self.background, (0, 0))
            self.window.blit(self.small_display, (16, 0))
            pygame.display.update()
            self.reset_keys()
            self.CLOCK.tick(60)

    def process_next_round_transition(self):
        if self.level.number == 5:
            self.win()
        else:
            if self.level.number == self.unlocked_levels:
                self.unlocked_levels += 1
            self.go_to_next_round()

    def process_player_death(self, number):
        if self.level.players[number].lifes:
            self.level.players[number].kind = 0
            self.level.players[number].get_type()
            self.level.players[number].is_alive = True
        else:
            self.game_over()

    def create_random_enemy(self):
        if len(self.level.enemies) < 4:
            if self.level.get_score() + len(self.level.enemies) < 5:
                rnd = randrange(0, 2)
                if rnd == 0:
                    self.level.enemies.append(Enemy(randrange(4), 1 / 2, 0,
                                                    (96 * randrange(3), 0), 0,
                                                    self.level))
                if rnd == 1:
                    self.level.enemies.append(Enemy(randrange(4), 1 / 2, 0,
                                                    (96 * randrange(3), 0), 1,
                                                    self.level))
            else:
                self.level.enemies.append(Enemy(randrange(4), 1 / 2, 0,
                                                (96 * randrange(3), 0), 2,
                                                self.level))

    def update_explosions(self):
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

    def update_enemies(self):
        for enemy in self.level.enemies:
            self.draw(enemy)
            if not randrange(140):
                live_players = []
                for player in self.level.players:
                    if player.is_alive:
                        live_players.append(player.number)
                if enemy.target == 0:
                    if enemy.target in live_players:
                        enemy.find_path(self.level.players[0].rect.topleft, 0)
                    elif len(self.level.players) > 1:
                        enemy.find_path(self.level.players[1].rect.topleft, 0)
                if enemy.target == 1:
                    if enemy.target in live_players and len(
                            self.level.players) > 1:
                        enemy.find_path(self.level.players[1].rect.topleft, 0)
                    else:
                        enemy.find_path(self.level.players[0].rect.topleft, 0)
                if enemy.target == 2:
                    enemy.find_path((96, 208), 1)
            enemy.move()
            if not randrange(50):
                enemy.fire()

    def win(self):
        self.playing = False
        pygame.mixer.music.load('../sounds/win_game.ogg')
        pygame.mixer.music.set_volume(self.volume_level)
        pygame.mixer.music.play()
        self.curr_menu = self.credits

    def go_to_next_round(self):
        self.playing = False
        pygame.mixer.music.load('../sounds/next_level.ogg')
        pygame.mixer.music.set_volume(self.volume_level)
        pygame.mixer.music.play()
        self.curr_menu = self.next_round_menu

    def game_over(self):
        self.playing = False
        pygame.mixer.music.load('../sounds/game_over.ogg')
        pygame.mixer.music.set_volume(self.volume_level)
        pygame.mixer.music.play()
        self.curr_menu = self.game_over_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('settings.txt', mode='w') as file:
                    json.dump({
                        'toggle_fullscreen': self.toggle_fullscreen,
                        'unlocked_levels': self.unlocked_levels,
                        'volume_level': self.volume_level
                    }, file, indent=4)
                self.window = pygame.display.set_mode(
                    (self.DISPLAY_W, self.DISPLAY_H),
                    pygame.SCALED)
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                    self.playing = False
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
            if event.type == KEYDOWN:
                for player in self.level.players:
                    if event.key in player.controls.keys():
                        player.pressed_keys[player.controls[event.key]] = True
                    if event.key == K_SPACE and player.number == 0:
                        player.fire()
                    if event.key == K_RCTRL and player.number == 1:
                        player.fire()
                    if event.key in range(97, 123):
                        self.cheat_command += chr(event.key)
                    else:
                        self.cheat_command = ""
                    if len(self.cheat_command) == 8:
                        self.cheat_command = self.cheat_command[1:]
                    if self.cheat_command == "killfoe":
                        for enemy in self.level.enemies[:]:
                            self.level.players[0].score[enemy.kind] += 1
                            enemy.die()
                        self.cheat_command = ""
                    if self.cheat_command == "improve":
                        if player.kind != 3:
                            player.kind += 1
                            player.get_type()
                        self.cheat_command = ""
                    if self.cheat_command == "protect":
                        for protecting_block in self.level.protecting_blocks:
                            self.level.game_map.append(
                                Tile(BETON, protecting_block))
                        self.cheat_command = ""
                    if (self.cheat_command == "nextlvl" and
                            self.curr_menu != self.next_round_menu):
                        self.cheat_command = ""
                        if self.level.number == 5:
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
        self.UP_KEY, self.DOWN_KEY, self.START_KEY,\
            self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = (
                False, False, False, False, False, False)

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.background.blit(text_surface, text_rect)
