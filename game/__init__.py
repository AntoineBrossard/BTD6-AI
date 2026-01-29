"""
Game package initialization
"""

from game.entities import Balloon, Tower, Projectile, Vector2, BalloonType
from game.game import BTD6Game, GameState

# Import renderer only if pygame is available
try:
    from game.renderer import BTD6Renderer
    __all__ = [
        "Balloon",
        "Tower",
        "Projectile",
        "Vector2",
        "BalloonType",
        "BTD6Game",
        "GameState",
        "BTD6Renderer",
    ]
except ImportError:
    __all__ = [
        "Balloon",
        "Tower",
        "Projectile",
        "Vector2",
        "BalloonType",
        "BTD6Game",
        "GameState",
    ]
