import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from power import Power, PowerType
from random import choices
from activated_powers import ActivatedPowers

class AlienInvasion:
    """ Overall class to manage game assets and behavior. """

    def __init__(self):
        """ Initialize the game and create game resources. """
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)
        if self.settings.full_screen_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(self.settings.screen_size)

        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption(self.settings.game_caption)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button('Play', self)
        self.scoreboard = ScoreBoard(self)
        self.powers = pygame.sprite.Group()
        self.timer = None
        self.activated_powers = ActivatedPowers(self)

    def run_game(self):
        """ Start the main loop for the game. """

        while True:
            self._check_events()

            if self.stats.active:
                self._update_powers()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # Watch of keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_down_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_mouse_down_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self._check_play_button_click(mouse_pos)

    def _start_game(self):
        self.settings.reinitialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.active = True
        self.aliens.empty()
        self.bullets.empty()
        self.ship.center_ship()
        self.scoreboard.update()
        self._create_fleet()

    def _check_play_button_click(self, mouse_pos):

        if self.play_button.rect.collidepoint(mouse_pos)\
                and not self.stats.active:
            self._start_game()

    def _update_powers(self):

        if self.powers:
            for power in self.powers:
                power.update()
                if power.rect.bottom >= self.screen_rect.bottom:
                    self.powers.remove(power)
        else:
            population = [0, 1]
            weight = [0.99, 0.01]
            the_choice = choices(population, weight)
            show_power = the_choice[0]

            if show_power:
                self.powers.add(Power(PowerType.SUPER_BULLET, self))

        self._check_power_ship_collision()

    def _check_power_ship_collision(self):
        captured_powers = pygame.sprite.spritecollide(self.ship, self.powers, True)

        if captured_powers:
            for power in captured_powers:
                self.activated_powers.activate(power.type)
                print("You picked up the power: " + str(power.type))

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update the position of the bullets and get rid of the old bullets. """
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._detect_bullet_alien_collision()

    def _detect_bullet_alien_collision(self):
        # Detect collision between bullet and aliens

        delete_bullets = not self.activated_powers.is_active(PowerType.SUPER_BULLET)

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, delete_bullets, True)
        
        if collisions:
            for aliens in collisions.values():
                self._update_score(len(aliens))

        if not self.aliens:
            self._level_up()

    def _level_up(self):
        self.stats.level += 1
        self.bullets.empty()
        self._create_fleet()
        self.settings.alien_x_speed *= self.settings.level_alien_speed_increase
        self.settings.ship_speed *= self.settings.level_ship_speed_increase
        self.settings.bullet_speed *= self.settings.level_bullet_speed_increase

        # round the score per alien to the nearest 10.
        self.settings.score_per_alien *= int(round(self.settings.level_score_increase, -1))
        self.scoreboard.update()

    def _update_score(self, aliens_killed):
        self.stats.score += self.settings.score_per_alien * aliens_killed
        if self.stats.high_score < self.stats.score:
            self.stats.high_score = self.stats.score

        self.scoreboard.update()

    def _create_alien(self, number, row):
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (alien_width * 2 * number)
        alien.y = alien_height + (alien_height * 2 * row)
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _update_aliens(self):
        """ checks the position of ship and aliens and detects alien collisions. """

        self.aliens.update()
        self._check_fleet_edge()
        self._check_alien_collision()

    def _check_alien_collision(self):
        """ checks collision between alien and ship. """

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        for alien in self.aliens:
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """ Handle a scenario where player looses a ship. """
        self.stats.ship_left -= 1

        if self.stats.ship_left > 0:
            self._reset_wave()
            sleep(1)
        else:
            self.stats.active = False
        pass

    def _reset_wave(self):
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.scoreboard.update()

    def _create_fleet(self):
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        available_width = self.settings.screen_width - (2 * alien_width)
        available_height = self.settings.screen_height - (3 * alien_height) - ship_height

        total_aliens_per_row = available_width // (alien_width * 2)
        total_rows = available_height // (alien_height * 2)

        for row_number in range(total_rows):
            for alien_number in range(total_aliens_per_row):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edge(self):
        for alien in self.aliens:
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        self.settings.alien_direction *= -1
        for alien in self.aliens:
            alien.rect.y += self.settings.alien_y_speed

    def _update_screen(self):
        # Redraw the screen during each pass of the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        if not self.stats.active:
            # Only show the play button if the game is not active.
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

        self.scoreboard.draw()

        # for power in self.powers:
        #     power.draw()
        self.powers.draw(self.screen)

        # Make recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make and instance of the game and run the game.
    ai = AlienInvasion()
    ai.run_game()
