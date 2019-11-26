import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

	def __init__(self, ai_settings, screen):

		super().__init__()

		self.screen = screen
		self.ai_settings = ai_settings

		# Load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# Start each new ship at the bottom centre of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# Store a decimal value for the ship's center
		self.center = float(self.rect.centerx)

		# Movement flags
		self.move_right = False
		self.move_left = False

		# Enable these to unlock the up/dpown movement of the ship
		# self.move_up = False
		# self.move_down = False

	def center_ship(self):
		self.center = self.screen_rect.centerx

	def update(self):
		if self.move_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.move_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		# if self.move_up:
		# 	self.rect.bottom -= 1
		# if self.move_down:
		# 	self.rect.bottom += 1

		# Update rect update from self.center
		self.rect.centerx = self.center

	def blitme(self):
		""" Draw the ship at its current location """
		self.screen.blit(self.image, self.rect)
