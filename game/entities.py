"""
Core game entities: Balloons, Towers, Projectiles
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class BalloonType(Enum):
    """Different balloon types"""
    RED = 1  # Weakest, split into 2 blues
    BLUE = 2  # Split into 2 greens
    GREEN = 4  # Split into 2 yellows
    YELLOW = 8  # Split into 2 pinks
    PINK = 16  # Split into 2 reds
    BLACK = 32  # Immune to normal bullets, has 1 health
    WHITE = 32  # Immune to explosive, has 1 health
    ZEBRA = 64  # Immune to normal and explosive, has 1 health
    CERAMIC = 10  # Cannot be split, has 10 health
    MOAB = 40  # Armored, has 40 health
    BFB = 80  # Boss, has 80 health
    ZOMG = 120  # Ultimate, has 120 health


@dataclass
class Vector2:
    """2D Vector"""
    x: float
    y: float

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def distance_to(self, other) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def normalize(self):
        dist = math.sqrt(self.x ** 2 + self.y ** 2)
        if dist == 0:
            return Vector2(0, 0)
        return Vector2(self.x / dist, self.y / dist)


class Balloon:
    """Represents a balloon in the game"""

    def __init__(
        self,
        balloon_type: BalloonType,
        position: Vector2,
        path: List[Vector2],
        speed: float = 50,  # pixels per second
    ):
        self.balloon_type = balloon_type
        self.position = position
        self.path = path  # List of waypoints
        self.path_index = 0  # Current waypoint index
        self.progress_on_path = 0.0  # How far between current and next waypoint (0-1)
        self.speed = speed
        self.radius = self._get_radius()
        self.health = self._get_health()

    def _get_radius(self) -> float:
        """Get balloon radius based on type"""
        radius_map = {
            BalloonType.RED: 8,
            BalloonType.BLUE: 7,
            BalloonType.GREEN: 6,
            BalloonType.YELLOW: 5,
            BalloonType.PINK: 5,
            BalloonType.BLACK: 8,
            BalloonType.WHITE: 8,
            BalloonType.ZEBRA: 8,
            BalloonType.CERAMIC: 10,
            BalloonType.MOAB: 15,
            BalloonType.BFB: 20,
            BalloonType.ZOMG: 25,
        }
        return radius_map.get(self.balloon_type, 8)

    def _get_health(self) -> int:
        """Get initial health based on type"""
        health_map = {
            BalloonType.RED: 1,
            BalloonType.BLUE: 1,
            BalloonType.GREEN: 1,
            BalloonType.YELLOW: 1,
            BalloonType.PINK: 1,
            BalloonType.BLACK: 1,
            BalloonType.WHITE: 1,
            BalloonType.ZEBRA: 1,
            BalloonType.CERAMIC: 10,
            BalloonType.MOAB: 40,
            BalloonType.BFB: 80,
            BalloonType.ZOMG: 120,
        }
        return health_map.get(self.balloon_type, 1)

    def update(self, dt: float) -> bool:
        """
        Update balloon position along path.
        Returns True if balloon reached end of path.
        """
        if self.path_index >= len(self.path) - 1:
            return True  # Reached end

        # Calculate distance to travel this frame
        distance_to_travel = self.speed * dt

        while distance_to_travel > 0 and self.path_index < len(self.path) - 1:
            current_pos = self.position
            target_pos = self.path[self.path_index + 1]

            distance_to_next = current_pos.distance_to(target_pos)

            if distance_to_travel >= distance_to_next:
                # Move to next waypoint
                distance_to_travel -= distance_to_next
                self.path_index += 1
                self.progress_on_path = 0.0
                if self.path_index < len(self.path):
                    self.position = self.path[self.path_index]
            else:
                # Move partway to next waypoint
                direction = (target_pos - current_pos).normalize()
                self.position = current_pos + direction * distance_to_travel
                self.progress_on_path = distance_to_travel / distance_to_next
                distance_to_travel = 0

        return self.path_index >= len(self.path) - 1

    def take_damage(self, damage: int) -> List["Balloon"]:
        """
        Apply damage to balloon.
        Returns list of new balloons created by splitting (or empty list).
        """
        self.health -= damage
        if self.health <= 0:
            return self._split()
        return []

    def _split(self) -> List["Balloon"]:
        """Split balloon into children"""
        children = []
        # In BTD6: PINK->BLACK, BLACK->WHITE, WHITE->PINK, PINK->YELLOW, YELLOW->GREEN, GREEN->BLUE, BLUE->RED, RED->pop
        # For MVP: simplified hierarchy
        split_map = {
            BalloonType.BLUE: BalloonType.RED,
            BalloonType.GREEN: BalloonType.BLUE,
            BalloonType.YELLOW: BalloonType.GREEN,
            BalloonType.PINK: BalloonType.YELLOW,
            # RED doesn't split - just pops
        }

        if self.balloon_type in split_map:
            child_type = split_map[self.balloon_type]
            # Split into 1 child (simplified for MVP)
            child = Balloon(
                child_type,
                Vector2(self.position.x, self.position.y),
                self.path[self.path_index :],
                self.speed,
            )
            child.path_index = self.path_index
            child.progress_on_path = self.progress_on_path
            children.append(child)

        return children

    def collides_with_point(self, point: Vector2) -> bool:
        """Check if point is inside balloon"""
        return self.position.distance_to(point) <= self.radius


class Projectile:
    """Projectile fired by towers"""

    def __init__(
        self,
        position: Vector2,
        target_balloon: Balloon,
        speed: float = 300,
        damage: int = 1,
    ):
        self.position = position
        self.target_balloon = target_balloon
        self.speed = speed
        self.damage = damage
        self.radius = 3

    def update(self, dt: float, balloons: List[Balloon]) -> Tuple[bool, List[Balloon]]:
        """
        Update projectile position and check for collisions.
        Returns (should_remove, new_balloons_created)
        """
        # Check if target is still valid
        if self.target_balloon not in balloons or self.target_balloon.health <= 0:
            # Target is dead or removed, find nearest alive target
            alive_balloons = [b for b in balloons if b.health > 0]
            if not alive_balloons:
                return True, []
            
            self.target_balloon = min(
                alive_balloons,
                key=lambda b: self.position.distance_to(b.position),
            )

        # Move towards target
        direction = (
            self.target_balloon.position - self.position
        ).normalize()
        self.position = self.position + direction * self.speed * dt

        # Check collision with target
        if self.position.distance_to(
            self.target_balloon.position
        ) <= self.target_balloon.radius + self.radius:
            new_balloons = self.target_balloon.take_damage(self.damage)
            return True, new_balloons

        return False, []


class Tower:
    """Dart Monkey tower"""

    def __init__(self, position: Vector2, range: float = 150, fire_rate: float = 1.0):
        self.position = position
        self.range = range
        self.fire_rate = fire_rate  # Shots per second
        self.fire_cooldown = 0.0
        self.damage = 1
        self.radius = 10

    def update(self, dt: float, balloons: List[Balloon]) -> List[Projectile]:
        """
        Update tower and return list of new projectiles fired.
        """
        self.fire_cooldown -= dt

        projectiles = []

        # Find targets in range
        targets = [
            b
            for b in balloons
            if self.position.distance_to(b.position) <= self.range
            and b.health > 0
        ]

        if not targets:
            return projectiles

        # Sort targets by path progress (prioritize balloons FIRST to enter range)
        targets.sort(
            key=lambda b: (b.path_index, b.progress_on_path), reverse=False
        )

        # Fire at the most advanced target
        if self.fire_cooldown <= 0:
            target = targets[0]
            projectile = Projectile(
                Vector2(self.position.x, self.position.y),
                target,
                damage=self.damage,
            )
            projectiles.append(projectile)
            self.fire_cooldown = 1.0 / self.fire_rate

        return projectiles

    def collides_with_point(self, point: Vector2) -> bool:
        """Check if point is inside tower placement area"""
        return self.position.distance_to(point) <= self.radius
