class Settings:

    score_per_alien: int
    alien_direction: int
    bullet_speed: int
    ship_speed: int
    alien_y_speed: int
    alien_x_speed: int

    def __init__(self):
        """ Initialize game's settings. """

        self.full_screen_mode = True
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_size = (self.screen_width, self.screen_height)
        self.bg_color = (230, 230, 230)
        self.game_caption = 'Alien Invasion'

        # Ship's settings
        self.ship_limit = 3

        # Bullet's settings
        self.bullet_height = 10
        self.bullet_width = 3
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 3
        self.level_alien_speed_increase = 1.2
        self.level_ship_speed_increase = 1.2
        self.level_bullet_speed_increase = 1.2
        self.level_score_increase = 1.5
        self.reinitialize_dynamic_settings()

    def reinitialize_dynamic_settings(self):
        """ Reinitialize the dynamic settings each time the game starts. """

        self.alien_x_speed = 3

        # We don't change the y speed with level  but we will still keep the speed settings together.
        self.alien_y_speed = 10

        self.ship_speed = 10

        self.bullet_speed = 6

        # Alien's setting
        # we use 1 for right and -1 for left direction
        self.alien_direction = 1

        self.score_per_alien = 100
