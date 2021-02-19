import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):  # Sprites can group related elements in your game and act on all the grouped elements at once.
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """create a bullet object at the ship's current position"""
        super().__init__()     # inherit properly from Sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop # match ship's midtop attribute

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y) # can make fine adjustments to the bullet's speed

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed    # fired the bullet upward
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
