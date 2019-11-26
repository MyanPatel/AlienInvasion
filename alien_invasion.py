# Allows the user to quit the game when the while loop breaks
import pygame  # Contains the functionality needed to make a game
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Initialise the game and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(ai_settings, screen)
    # A group to store bullets in
    bullets = Group()
    aliens = Group()

    play_button = Button(ai_settings, screen, "Play!")
    gf.create_fleet(ai_settings, screen, ship, aliens)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    pygame.display.set_caption("Alien Invasion")

    print("\nControls:\n")
    print("Move left = Left Arrow")
    print("Move right = Right Arrow")
    print("Fire bullet = Space-bar/Right mouse-click")

    # Start the main loop for the game
    while True:

        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, sb, stats)
            gf.update_aliens(aliens, ai_settings, ship, stats, screen, bullets, play_button, sb)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)

run_game()
