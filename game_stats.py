class GameStats:
    """ Handle game's statistics. """

    active: bool
    ship_left: int
    
    def __init__(self, game):
        """ Initialize new game statistics. """
        self.settings = game.settings
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.active = False
