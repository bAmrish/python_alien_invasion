import pygame
from enum import Enum


class PowerType(Enum):

    SUPER_BULLET = 1


class Power(pygame.sprite.Sprite):
    """ Manages power up. """

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, power_type: PowerType, game):

        super().__init__()

        self.type = power_type
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.font = pygame.font.SysFont(None, 24)
        self.text_color = (255, 0, 0, 0.5)
        self.bg_color = (0, 0, 0)
        self.power_speed = 10
        self.prepare()
        self.isActive = False
        self.timer = None

    def prepare(self):
        self.image = self.font.render(' P ', True, self.text_color, self.bg_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.top = 100

    def update(self):
        self.rect.y += self.power_speed

