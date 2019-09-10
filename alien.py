import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ This class manages the alien and its resources. """

    def __init__(self, game):
        """ Initialize the alien"""

        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """ Update the position of the alien on the screen. """

        self.x += (self.settings.alien_x_speed * self.settings.alien_direction)
        self.rect.x = self.x

    def check_edge(self):
        """ Returns true if the alien is either near the right or left edge of the screen. """

        if self.rect.right >= self.screen_rect.right or \
                self.rect.left <= 0:
            return True
