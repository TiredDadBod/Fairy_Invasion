import pygame
import sys
import os
import fireball

def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 820
        self.bg_color = (255, 255, 255)

        # Monkey settings
        self.monkey_limit = 3

        # Fireball settings
        self.fireball = pygame.image.load(resource_path('alien_invasion/fireball.bmp'))
        self.fireball_rect = self.fireball.get_rect()
        self.fireball_allowed = 5

        # Enemy Settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the enemy point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the game's dynamic settings."""
        self.monkey_speed = 3
        self.fireball_speed = 2.5
        self.enemy_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings
        self.enemy_points = 25

    def increase_speed(self):
        """Increase speed settings and enemy point values."""
        self.monkey_speed *= self.speedup_scale
        self.fireball_speed *= self.speedup_scale
        self.enemy_speed *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)
        