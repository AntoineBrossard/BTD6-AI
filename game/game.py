"""
Main game engine and state management
"""

from typing import List, Dict, Tuple
from enum import Enum
from game.entities import Balloon, BalloonType, Projectile, Tower, Vector2


class GameState(Enum):
    """Game state enumeration"""
    RUNNING = 1
    WAVE_END = 2
    LOST = 3
    WON = 4


class BTD6Game:
    """Main game engine"""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        starting_lives: int = 100,
        starting_cash: int = 650,
    ):
        self.width = width
        self.height = height
        self.lives = starting_lives
        self.max_lives = starting_lives
        self.cash = starting_cash
        self.round = 1
        self.state = GameState.RUNNING

        # Game entities
        self.balloons: List[Balloon] = []
        self.towers: List[Tower] = []
        self.projectiles: List[Projectile] = []

        # Path for balloons (simple path across screen)
        self.balloon_path = [
            Vector2(-50, 300),
            Vector2(200, 300),
            Vector2(400, 200),
            Vector2(600, 300),
            Vector2(800, 300),
            Vector2(850, 300),
        ]

        # Wave information
        self.round_waves = self._get_round_waves()
        self.current_wave = 0
        self.balloons_spawned = 0
        self.spawn_index = 0
        self.spawn_timer = 0.0
        self.spawn_delay = 0.5  # Seconds between balloon spawns

    def _get_round_waves(self) -> List[List[Tuple[BalloonType, int]]]:
        """
        Get balloon waves for each round.
        Returns list of waves, each wave is list of (balloon_type, count).
        """
        # For MVP: Just round 1
        return [
            [
                (BalloonType.RED, 6),
            ]
        ]

    def place_tower(self, x: float, y: float) -> bool:
        """Place tower at position. Returns True if successful."""
        pos = Vector2(x, y)

        # Check if position is valid (not colliding with other towers, within bounds)
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return False

        for tower in self.towers:
            if tower.collides_with_point(pos):
                return False

        tower = Tower(pos)
        self.towers.append(tower)
        return True

    def update(self, dt: float):
        """Update game state"""
        if self.state != GameState.RUNNING:
            return

        # Spawn balloons
        self._spawn_balloons(dt)

        # Update balloons
        balloons_to_remove = []
        for balloon in self.balloons:
            if balloon.update(dt):
                # Balloon reached end of path
                balloons_to_remove.append(balloon)
                self.lives -= 1
                if self.lives <= 0:
                    self.state = GameState.LOST

        for balloon in balloons_to_remove:
            self.balloons.remove(balloon)

        # Update towers
        for tower in self.towers:
            new_projectiles = tower.update(dt, self.balloons)
            self.projectiles.extend(new_projectiles)

        # Update projectiles
        projectiles_to_remove = []
        for projectile in self.projectiles:
            should_remove, new_balloons = projectile.update(dt, self.balloons)
            if should_remove:
                projectiles_to_remove.append(projectile)
            self.balloons.extend(new_balloons)

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

        # Remove dead balloons
        self.balloons = [b for b in self.balloons if b.health > 0]

        # Check wave complete: all balloon types spawned AND no balloons/projectiles left
        current_wave = self.round_waves[self.current_wave]
        all_spawned = self.spawn_index >= len(current_wave)
        
        if (
            all_spawned
            and len(self.balloons) == 0
            and len(self.projectiles) == 0
        ):
            self._end_wave()

    def _spawn_balloons(self, dt: float):
        """Spawn balloons from current wave"""
        current_wave = self.round_waves[self.current_wave]

        if self.spawn_index >= len(current_wave):
            return  # Wave complete

        balloon_type, count = current_wave[self.spawn_index]

        if self.balloons_spawned >= count:
            self.spawn_index += 1
            self.balloons_spawned = 0
            self.spawn_timer = 0.0
            return

        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_delay:
            balloon = Balloon(balloon_type, Vector2(-50, 300), self.balloon_path)
            self.balloons.append(balloon)
            self.balloons_spawned += 1
            self.spawn_timer = 0.0

    def _end_wave(self):
        """End current wave and prepare for next"""
        self.current_wave += 1
        if self.current_wave >= len(self.round_waves):
            self.state = GameState.WON
        else:
            self.spawn_index = 0
            self.balloons_spawned = 0
            self.spawn_timer = 0.0

    def get_state_dict(self) -> Dict:
        """Get game state as dictionary for AI"""
        return {
            "round": self.round,
            "lives": self.lives,
            "cash": self.cash,
            "state": self.state,
            "balloons": [
                {
                    "type": b.balloon_type.name,
                    "x": b.position.x,
                    "y": b.position.y,
                    "health": b.health,
                    "radius": b.radius,
                }
                for b in self.balloons
            ],
            "towers": [
                {
                    "x": t.position.x,
                    "y": t.position.y,
                    "range": t.range,
                }
                for t in self.towers
            ],
        }
