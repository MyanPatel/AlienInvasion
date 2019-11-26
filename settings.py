class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 650
        self.bg_colour = (230, 230, 230)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3  # 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3  # actual value = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien Settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10  # 10
        # fleet direction 1 = right, -1 = left
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialise settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
    # print("alien points: " + str(self.alien_points))
