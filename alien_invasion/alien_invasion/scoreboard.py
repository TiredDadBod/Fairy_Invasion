import pygame.font
from pygame.sprite import Group
from pathlib import Path
import json

from monkey import Monkey

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_monkeys()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw the scores, level, and monkeys to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.monkeys.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        stored_high_score = Path("/Users/tophe/OneDrive/Desktop/alien_invasion/alien_invasion/high_scores.json")
        read_high_score = stored_high_score.read_text()
        load_high_score = json.loads(read_high_score)
        high_score = round(load_high_score)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def _save_high_scores(self):
        """Record high scores for later instances."""
        stored_high_score = Path("/Users/tophe/OneDrive/Desktop/alien_invasion/alien_invasion/high_scores.json")
        new_high_score = json.dumps(self.stats.high_score)
        if not stored_high_score.exists():
            stored_high_score.write_text(new_high_score)
        else:
            current_high_scores = stored_high_score.read_text()
            high_scores = json.loads(current_high_scores)
            if self.stats.high_score > high_scores:
                stored_high_score.write_text(new_high_score)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._save_high_scores()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {str(self.stats.level)}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level in the top left.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 10
        self.level_rect.top = 10

    def prep_monkeys(self):
        """Show how many monkeys are left."""
        self.monkeys = Group()
        for monkey_number in range(self.stats.monkeys_left):
            monkey = Monkey(self.ai_game)
            monkey.rect.x = 10 + monkey_number * monkey.rect.width
            monkey.rect.y = 820 - monkey.rect.height
            self.monkeys.add(monkey)