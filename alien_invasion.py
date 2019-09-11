import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """ Overall class to manage game assets and behavior. """

    def __init__(self):
        """ Initialize the game and create game resources. """
        pygame.init()
        self.settings = Settings()

        if self.settings.full_screen_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(self.settings.screen_size)

        pygame.display.set_caption(self.settings.game_caption)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """ Start the main loop for the game. """

        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self.aliens.update()
            self._check_fleet_edge()
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

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

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

        # Detect collision between bullet and aliens
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _create_alien(self, number, row):
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (alien_width * 2 * number)
        alien.y = alien_height + (alien_height * 2 * row)
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

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

        # Make recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make and instance of the game and run the game.
    ai = AlienInvasion()
    ai.run_game()
