class GameStats:
    """ Handle game's statistics. """

    active: bool
    ship_left: int
    score: int
    level: int
    
    def __init__(self, game):
        """ Initialize new game statistics. """
        self.settings = game.settings
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.active = False
        self.score = 0
        self.level = 1
