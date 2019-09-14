import pygame


class Button:
    """ This class manages a button on screen. """

    def __init__(self, message: str, game, width: int = 200, height: int = 50):
        """ Initialize a new button. """

        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.settings = game.settings
        self.width = width
        self.height = height
        self.message = message
        self.text_color = (0, 0, 0)
        self.bg_color = (0, 255, 0)
        self.message_image = None
        self.message_image_rect = None

        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = self.screen_rect.center
        self.prepare_message()

    def prepare_message(self):
        """ Prepare message image"""
        self.message_image = self.font.render(self.message, True, self.text_color, self.bg_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw(self):
        """ Draws the button the screen"""

        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
