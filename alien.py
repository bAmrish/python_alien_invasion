import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ This class manages the alien and its resources. """

    def __init__(self, game):
        """ Initialize the alien"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
