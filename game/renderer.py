"""
Visual renderer using Pygame
"""

import pygame
from typing import List, Optional
from game.entities import Balloon, Tower, Projectile, BalloonType
from game.game import BTD6Game


class BTD6Renderer:
    """Pygame-based renderer for BTD6 game"""

    def __init__(self, game: BTD6Game, width: int = 800, height: int = 600):
        self.game = game
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("BTD6 AI - Game Simulation")

        # Colors
        self.BG_COLOR = (34, 139, 34)  # Green
        self.BALLOON_COLORS = {
            BalloonType.RED: (255, 0, 0),
            BalloonType.BLUE: (0, 0, 255),
            BalloonType.GREEN: (0, 128, 0),
            BalloonType.YELLOW: (255, 255, 0),
            BalloonType.PINK: (255, 192, 203),
            BalloonType.BLACK: (0, 0, 0),
            BalloonType.WHITE: (255, 255, 255),
            BalloonType.ZEBRA: (200, 200, 200),
            BalloonType.CERAMIC: (128, 128, 128),
            BalloonType.MOAB: (128, 0, 0),
            BalloonType.BFB: (75, 0, 130),
            BalloonType.ZOMG: (255, 140, 0),
        }
        self.TOWER_COLOR = (139, 69, 19)  # Brown
        self.PROJECTILE_COLOR = (255, 255, 0)  # Yellow
        self.PATH_COLOR = (100, 100, 100)  # Gray

        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)

    def render(self):
        """Render game state"""
        self.screen.fill(self.BG_COLOR)

        # Draw path
        self._draw_path()

        # Draw balloons
        for balloon in self.game.balloons:
            self._draw_balloon(balloon)

        # Draw towers
        for tower in self.game.towers:
            self._draw_tower(tower)

        # Draw projectiles
        for projectile in self.game.projectiles:
            self._draw_projectile(projectile)

        # Draw UI
        self._draw_ui()

        pygame.display.flip()

    def _draw_path(self):
        """Draw balloon path"""
        path = self.game.balloon_path
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            pygame.draw.line(
                self.screen, self.PATH_COLOR, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), 2
            )

    def _draw_balloon(self, balloon: Balloon):
        """Draw a single balloon"""
        color = self.BALLOON_COLORS.get(balloon.balloon_type, (255, 0, 255))
        pygame.draw.circle(
            self.screen,
            color,
            (int(balloon.position.x), int(balloon.position.y)),
            int(balloon.radius),
        )
        # Draw health if damaged
        if balloon.health > 0:
            health_text = self.font.render(str(balloon.health), True, (255, 255, 255))
            self.screen.blit(
                health_text,
                (int(balloon.position.x) - 10, int(balloon.position.y) - 10),
            )

    def _draw_tower(self, tower: Tower):
        """Draw a single tower"""
        pygame.draw.circle(
            self.screen,
            self.TOWER_COLOR,
            (int(tower.position.x), int(tower.position.y)),
            int(tower.radius),
        )
        # Draw range indicator
        pygame.draw.circle(
            self.screen,
            (200, 200, 200),
            (int(tower.position.x), int(tower.position.y)),
            int(tower.range),
            1,
        )

    def _draw_projectile(self, projectile: Projectile):
        """Draw a single projectile"""
        pygame.draw.circle(
            self.screen,
            self.PROJECTILE_COLOR,
            (int(projectile.position.x), int(projectile.position.y)),
            int(projectile.radius),
        )

    def _draw_ui(self):
        """Draw UI elements"""
        # Lives
        lives_text = self.font.render(f"Lives: {self.game.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 10))

        # Round
        round_text = self.font.render(f"Round: {self.game.round}", True, (255, 255, 255))
        self.screen.blit(round_text, (10, 40))

        # Cash
        cash_text = self.font.render(f"Cash: ${self.game.cash}", True, (255, 255, 255))
        self.screen.blit(cash_text, (10, 70))

        # Game state
        state_text = self.font.render(f"State: {self.game.state.name}", True, (255, 255, 255))
        self.screen.blit(state_text, (10, 100))

        # Balloon count
        balloon_text = self.font.render(
            f"Balloons: {len(self.game.balloons)}", True, (255, 255, 255)
        )
        self.screen.blit(balloon_text, (self.width - 200, 10))

        # Tower count
        tower_text = self.font.render(
            f"Towers: {len(self.game.towers)}", True, (255, 255, 255)
        )
        self.screen.blit(tower_text, (self.width - 200, 40))

    def close(self):
        """Close the renderer"""
        pygame.quit()
