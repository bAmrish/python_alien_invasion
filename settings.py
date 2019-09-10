class Settings:

    def __init__(self):
        """ Initialize game's settings. """

        self.full_screen_mode = True
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_size = (self.screen_width, self.screen_height)
        self.bg_color = (230, 230, 230)
        self.game_caption = 'Alien Invasion'
        self.ship_speed = 1.5
