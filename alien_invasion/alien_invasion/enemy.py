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

class Enemy(Sprite):
    """A class to represent a single enemy in the game."""
    
    def __init__(self, ai_game):
        """Initialize the enemy and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the enemy image and set its rect attribute.
        self.image = pygame.image.load(resource_path('alien_invasion/enemy.bmp'))
        self.rect = self.image.get_rect()
        
        # Start each new enemy near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the enemy's exact horizontal position.
        self.x = float(self.rect.x)

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def check_edges(self):
        """Return True if the enemy is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the enemy to the right or left."""
        self.x += self.settings.enemy_speed * self.settings.fleet_direction
        self.rect.x = self.x