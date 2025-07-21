import pygame
import sys
import os
from pygame.sprite import Sprite

def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class Fireball(Sprite):
    """A class to manage the fireball's behavior in the game."""

    def __init__(self, ai_game):
        """Create a fireball at the monkey's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the fireball image and get its rect.
        self.image = pygame.image.load(resource_path('alien_invasion/fireball.bmp'))
        self.rect = pygame.Rect(0, 0, self.settings.fireball_rect.width, self.settings.fireball_rect.height)
        self.rect.midtop = ai_game.monkey.rect.midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the fireball up the screen."""
        # Update the fireball's position.
        self.y -= self.settings.fireball_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_fireball(self):
        """Draw the fireball to the screen."""
        self.screen.blit(self.image, self.rect)