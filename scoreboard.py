import pygame


class ScoreBoard:
    """ This class represents the scoreboard shown in the game. """
    score_image_rect: pygame.Rect
    score_image: pygame.Surface

    def __init__(self, game):
        """ Initialize the scoreboard. """

        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.settings = game.settings
        self.stats = game.stats

        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (0, 0, 0)
        self.background_color = self.settings.bg_color

        self.prepare_score()

    def prepare_score(self):
        score = str(self.stats.score)
        self.score_image = self.font.render(score, True, self.text_color, self.background_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 10
        self.score_image_rect.top = self.screen_rect.top + 10

    def draw(self):
        self.screen.blit(self.score_image, self.score_image_rect)
