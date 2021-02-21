import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)    # figure out the full window size
        # self.settings.screen_width = self.screen.get_rect().width   # update screen width to full screen
        # self.settings.screen_height = self.screen.get_rect().height  # update screen height to full screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))    # smaller window
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)  # ship instance
        self.bullets = pygame.sprite.Group()    # store bullets; sprite.group behaves like a list
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button, an instance of Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:  # if the game is still active
                self.ship.update()
                self._update_bullets()
                self._update_aliens()   # update position of all aliens

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # MouseButtonDown event
                mouse_pos = pygame.mouse.get_pos()  # get cursor's x- and y-coordinates
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)   # check if button is clicked
        if button_clicked and not self.stats.game_active:   # game start when it's inactive
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor when the game is active
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:  # press Q to exit the game
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:  # release the right arrow key
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:   # check how many bullets exist (length < 3)
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)    # add new_bullet instance in to the group

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # update bullet positions
        self.bullets.update()  # update each sprite in the group

        # Get rid of bullets that have disappeared (top of the screen)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:  # check if bullet disappeared off the top of the screen
                self.bullets.remove(bullet)  # remove it if it's disappeared from the top of the screen
        # print(len(self.bullets))      # total number of bullets on the screen
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # check for any bullets that have hit aliens. If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:     # check whether the aliens group is empty
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()    # remove any existing bullets
            self._create_fleet()    # New set of aliens
            self.settings.increase_speed()   # level up the speed

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # spritecollideany stops looping through the group when collision detected; return None if no collision
            self._ship_hit()  # first collision

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:   # if any ships left
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False  # no ships left
            pygame.mouse.set_visible(True)  # set mouse cursor active when the game is inactive

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:     # if an alien reaches to the bottom of the screen
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)     # instance of Alien
        alien_width, alien_height = alien.rect.size   # size: tuple with the width and height of a rect object
        available_space_x = self.settings.screen_width - (2 * alien_width)  # Horizontal space available for aliens
        number_alien_x = available_space_x // (2 * alien_width)     # number of aliens can fit into the space

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        # available vertical space
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Creat the full fleet of aliens.
        for row_number in range(number_rows):   # counts from 0 to the number of rows we want
            # Create the first row of aliens.
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)     # new alien
        alien_width, alien_height  = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number  # set its x-coordinate value in the row
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():   # if alien is at an edge
                self._change_fleet_direction()  # change direction
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():   # bullets.sprites() returns a list of all sprites in the group bullets
            bullet.draw_bullet()
        self.aliens.draw(self.screen)       # draw aliens on the screen

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
