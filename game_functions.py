import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb)
            if stats.game_active:
                fire_bullet(ai_settings, bullets, screen, ship)



def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ Responding to key-presses """
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, bullets, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_m:
        ai_settings.bullet_width = 300


def check_keyup_events(event, ship):
    """ Responding to key-releases """
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False


# def change_play_button(stats, play_button):

#     if stats.ships_left == 0 and not stats.game_active:
#         play_button.prep_msg('Reset')


def check_high_score(stats, sb):
    """ Check if there's a new high-score """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb):
    """ Start new game when player presses play button """

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hiding the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset stats
        stats.reset_stats()
        stats.game_active = True

        # Reset Scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        stats.score = 0
        sb.prep_score()

        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.bullet_width = 3
        ship.center_ship()


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb):
    """ Check if any aliens have reached the bottom of the screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb)
            break


def make_reset_button(play_button):
    play_button.button_colour = (255, 0, 0)
    play_button.prep_msg('Play Again!')


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb):
    """ Respond to a ship being hot by an alien """
    # Take 1 away from the amount of ships left

    if stats.ships_left > 0:

        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the Aliens and Bullets Lists
        aliens.empty()
        bullets.empty()

        # Create a new fleet and centre the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        make_reset_button(play_button)
        # ai_settings.bullet_width = 3

        # Pause.
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_fleet_edges(ai_settings, aliens):
    """ Responding if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ drop the entire fleet and change direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(aliens, ai_settings, ship, stats, screen, bullets, play_button, sb):
    """ Check if the fleet is at an edge
        and update the positions of all the 
        aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb)

    # Checking if alien has reached the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, play_button, sb)


def get_number_aliens_x(ai_settings, alien_width):
    available_space = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space / (2 * alien_width))

    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x = ((2 * alien_width) * alien_number) + alien_width
    alien.rect.x = alien.x
    alien.rect.y = ((2 * alien.rect.height) * row_number) + alien.rect.height
    aliens.add(alien)


# def create_fleet(ai_settings, screen, aliens):
#     alien = Alien(screen, ai_settings)
#     alien_width = alien.rect.width
#     available_space = ai_settings.screen_width - (2*alien_width)
#     number_aliens_x = int(available_space / (2 * alien_width))

#     for alien_number in range(number_aliens_x):
#         alien = Alien(screen, ai_settings)
#         alien.x = ((2 * alien_width) * alien_number) + alien_width
#         alien.rect.x = alien.x
#         aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(screen, ai_settings)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def fire_bullet(ai_settings, bullets, screen, ship):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, scoreboard, stats):
    """ Respond to bullet-alien colliosns"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        # Increase level.
        stats.level += 1
        scoreboard.prep_level()
        # Re-spawns the fleet when the player has defeated the whole fleet
        create_fleet(ai_settings, screen, ship, aliens)




def update_bullets(bullets, aliens, ai_settings, screen, ship, scoreboard, stats):
    """ Update the postion of the bullets """
    bullets.update()

    # Delete old bullets that have left the top of the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, scoreboard, stats)


def update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, scoreboard):
    screen.fill(ai_settings.bg_colour)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()


def ending_condition(aliens):
    if len(aliens) == 0:
        print("GAME OVER!!")
        sys.exit()
