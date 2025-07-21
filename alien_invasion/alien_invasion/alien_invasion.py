import sys
import os
from time import sleep

import pygame
from pygame import mixer

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from monkey import Monkey
from fireball import Fireball
from enemy import Enemy
from pathlib import Path
import json

def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            (self.settings.screen_width, self.settings.screen_height)))
        pygame.display.set_caption("Fairy Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        
        self.monkey = Monkey(self)
        self.fireball = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Ivasion in an inactive state.
        self.game_active = False

        # Make a play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
        
            if self.game_active:
                self.monkey.update()
                self.fireball.update()
                self._update_fireballs()
                self._update_enemies()
                self.scoreboard._save_high_scores()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.scoreboard._save_high_scores()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            pygame.mixer.init()
            self.settings.initialize_dynamic_settings()
            
            # Reset the game statistics.
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_monkeys()
            self.scoreboard.prep_high_score()
            self.game_active = True

            # Get rid of any remaining fireballs and enemies.
            self.fireball.empty()
            self.enemy.empty()

            # Create a new fleet and center the monkey.
            self._create_fleet()
            self.monkey.center_monkey()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.monkey.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.monkey.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_fireball()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.monkey.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.monkey.moving_left = False

    def _fire_fireball(self):
        """Create a new fireball and add it to the fireball group."""
        fireball_launch = pygame.mixer.Sound(resource_path("alien_invasion/fireball_noise.mp3"))
        if len(self.fireball) < self.settings.fireball_allowed:
            new_fireball = Fireball(self)
            self.fireball.add(new_fireball)
            pygame.mixer.Sound.play(fireball_launch)

    def _update_fireballs(self):
        """Update the position of fireball and remove old ones."""
        # Update the position of each fireball.
        self.fireball.update()

        # Get rid of any fireball that have disappeared.
        for fireball in self.fireball.copy():
            if fireball.rect.bottom <= 0:
                self.fireball.remove(fireball)

        self._check_bullet_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        """Check for any fireball that have hit an enemy."""
        # Check for collisions between fireballs and enemies.
        # If a fireball hits an enemy, remove both the fireball and the enemy.
        collisions = pygame.sprite.groupcollide(
            self.fireball, self.enemy, True, True)
        fairy_sound = pygame.mixer.Sound(resource_path("alien_invasion/fairy_death.mp3"))
        
        if collisions:
            for enemies in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemies)
            self.stats.score += self.settings.enemy_points
            mixer.Sound.play(fairy_sound)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.enemy:
            # Destroy existing fireballs and create a new fleet.
            self.fireball.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_enemies(self):
        """Check if the fleet is at an edge, and update the positions of all enemies in the fleet."""
        self._check_fleet_edges()
        self.enemy.update()

        # Look for monkey-enemy collisions.
        if pygame.sprite.spritecollideany(self.monkey, self.enemy):
            self._monkey_hit()
            # Here you could implement what happens when the monkey is hit.
            # For example, you could reset the game or reduce the monkey's health.

        # Look for enemies hitting the bottom of the screen.
        self._check_enemys_bottom()

    def _create_fleet(self):
        """Create a fleet of enemies."""
        # Make an enemy and keep adding until there's no room left.
        # Spacing between enemies is on enemy width and one enemy height.
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size

        current_x, current_y = enemy_width, enemy_height
        while current_y < (self.settings.screen_height - 5 * enemy_height):
            while current_x < (self.settings.screen_width - 2 * enemy_width):
                self._create_enemy(current_x, current_y)
                current_x += 2 * enemy_width

            # Finisher a row; reset x value, and increment y value.
            current_x = enemy_width
            current_y += 2 * enemy_height

    def _create_enemy(self, x_position, y_position):
            """Create an enemy and place it in the fleet."""
            new_enemy = Enemy(self)
            new_enemy.x = x_position
            new_enemy.rect.x = x_position
            new_enemy.rect.y = y_position
            self.enemy.add(new_enemy)

    def _check_fleet_edges(self):
        """Respond appropriately if any enemies have reached an edge."""
        for enemy in self.enemy.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for enemy in self.enemy.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _monkey_hit(self):
        """Respond to the monkey being hit by enemy."""
        if self.stats.monkeys_left > 0:
            # Decrement monkeys_left, and update scoreboard.
            self.stats.monkeys_left -= 1
            self.scoreboard.prep_monkeys()

            # Get rid of any remaining bullets and enemies.
            self.fireball.empty()
            self.enemy.empty()

            # Create a new fleet and center the monkey.
            self._create_fleet()
            self.monkey.center_monkey()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_enemys_bottom(self):
        """Check if any enemies have reached the bottom of the screen."""
        for enemy in self.enemy.sprites():
            if enemy.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the monkey got hit
                self._monkey_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        if self.game_active == True:
            for fireball in self.fireball.sprites():
                fireball.draw_fireball()
            self.monkey.blitme()
            self.enemy.draw(self.screen)
            self.scoreboard.show_score()
        else:
            if not self.game_active:
                self.play_button.draw_button()
                self.scoreboard.show_score()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()