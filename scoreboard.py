import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)    # round score value to the nearest 10, 100, 1000, and so on.
        score_str = "{:,}".format(rounded_score)       # insert commas into rounded score; ex: 10,000,000
        # Create an image from the string
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20   # right edge 20 pixels from the right edge of screen
        self.score_rect.top = 20    # 20 pixels down from the top of the screen

    def prep_high_score(self):
        """Turn the high school into a rendered image."""
        high_score = round(self.stats.high_score, -1)   # round high score to the nearest 10, 100, etc.
        high_score_str = "{:,}".format(high_score)     # format high_score with the commas in between
        # generate an image from the high score
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx  # center high score rect horizontally
        self.high_score_rect.top = self.score_rect.top   # top attribute matches the top of the score image

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        # create an image from the value stored in stats.level
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        # set image's right attribute to match the score's right attribute
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10   # space between the score and the level

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()    # empty group to hold the ship instances
        for ship_number in range(self.stats.ships_left):    # every ship the player has left
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width    # 10-pixel margin between ships
            ship.rect.y = 10    # 10 pixels down from the top of the screen, upper-left corner of the screen
            self.ships.add(ship)    # add each new ship to the group ships

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)     # draw current score at top right
        self.screen.blit(self.high_score_image, self.high_score_rect)   # high score at the top center
        self.screen.blit(self.level_image, self.level_rect)     # draw level image to the screen
        self.ships.draw(self.screen)        # draw each ship to the screen

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:   # if current score > high score
            self.stats.high_score = self.stats.score    # set new high score
            self.prep_high_score()      # update the high score's image
