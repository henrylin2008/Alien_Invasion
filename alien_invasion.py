import sys
import pygame
from settings import Settings
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

        self.ship = Ship(self)  # ship instance
        self.bullets = pygame.sprite.Group()    # store bullets; sprite.group behaves like a list
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
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

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():   # bullets.sprites() returns a list of all sprites in the group bullets
            bullet.draw_bullet()
        self.aliens.draw(self.screen)       # draw aliens on the screen

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
