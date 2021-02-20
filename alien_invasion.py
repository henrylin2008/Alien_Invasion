import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


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

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()       # update each sprite in the group
            self._update_screen()

            # Get rid of bullets that have disappeared (top of the screen)
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:     # check if bullet disappeared off the top of the screen
                    self.bullets.remove(bullet)     # remove it if it's disappeared from the top of the screen
            # print(len(self.bullets))      # total number of bullets on the screen

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
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)    # add new_bullet instance in to the group

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():   # bullets.sprites() returns a list of all sprites in the group bullets
            bullet.draw_bullet()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
