import pygame
from ship import Ship


class ScoreBoard:
    """ This class represents the scoreboard shown in the game. """

    level_image_rect: pygame.Rect
    level_image: pygame.Surface
    score_image_rect: pygame.Rect
    score_image: pygame.Surface

    def __init__(self, game):
        """ Initialize the scoreboard. """

        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.settings = game.settings
        self.stats = game.stats

        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (0, 0, 0)
        self.background_color = self.settings.bg_color
        self.ships = pygame.sprite.Group()

        self.update()

    def update(self):
        self.prepare_score()
        self.prepare_level()
        self.prepare_ships()

    def prepare_score(self):
        score = str(self.stats.score)
        self.score_image = self.font.render('Score: ' + score, True, self.text_color, self.background_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 10
        self.score_image_rect.top = self.screen_rect.top + 10

    def prepare_level(self):
        level = str(self.stats.level)
        self.level_image = self.font.render('Level: ' + level, True, self.text_color, self.background_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.top = self.score_image_rect.top
        self.level_image_rect.right = self.score_image_rect.left - 10

    def prepare_ships(self):
        self.ships.empty()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.game)
            ship_rect = ship.rect
            ship_rect.left = 10 + (ship_rect.width + 10) * ship_number
            ship_rect.top = 10
            self.ships.add(ship)

    def draw(self):
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)
