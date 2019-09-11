import pygame

class Ship:
    """ This class handles all the game resources for alien ship. """

    def __init__(self, game):
        """ Initialize the ship and it's starting position. """

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        # load ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.center_ship()

        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """ Draw the ship at its current location. """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """ Update the ship's position based on movement flag. """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        # place ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
