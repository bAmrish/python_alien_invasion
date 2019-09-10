import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Class that manages bullets fired from ship. """

    def __init__(self, game):
        """ Initialize a new bullet. """
        super().__init__()

        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.color = self.settings.bullet_color

        # create the bullet at (0, 0)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_width)

        # move the bullet to the correct position
        self.rect.midtop = game.ship.rect.midtop

        # store the y coordinate of the bullet as a float
        self.y = float(self.rect.y)

    def draw_bullet(self):
        """ Draw bullet on the screen. """
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """ Move the bullet on the screen. """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
