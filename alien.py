import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, screen, ai_settings):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Loading the aline and setting it's rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Starting each new alien at the top-left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Storing the alien's exact postion
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Return true if an alien has hit the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left < 0:
            return True

    def update(self):
        """ Move the alien right or left """
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
