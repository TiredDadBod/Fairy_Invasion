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

class Monkey(Sprite):
    """A class to manage the monkey's behavior in the game."""

    def __init__(self, ai_game):
        """Initialize the monkey and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the monkey image and get its rect.
        self.image = pygame.image.load(resource_path('alien_invasion/monkey_1.bmp'))
        self.rect = self.image.get_rect()

        # Start each new monkey at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the monkey's horizontal and vertical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag; start with the monkey stationary.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the monkey's position based on movement flags."""
        # Update the monkey's x position, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
              self.x += self.settings.monkey_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.monkey_speed

        # Update the rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

    def center_monkey(self):
        """Center the monkey on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the monkey at its current location."""
        self.screen.blit(self.image, self.rect)