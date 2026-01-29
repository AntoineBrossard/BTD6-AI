"""
Debug test to see tower detection
"""

from game.game import BTD6Game, GameState
from game.entities import BalloonType, Vector2

# Create game
game = BTD6Game(width=800, height=600)

# Place tower near the path
game.place_tower(250, 300)  # Near (200, 300) waypoint
tower = game.towers[0]

print(f"Tower at ({tower.position.x}, {tower.position.y}) with range {tower.range}")
print(f"Path: {[(p.x, p.y) for p in game.balloon_path]}")

# Simulate
dt = 1/60
for frame in range(300):  # 5 seconds
    game.update(dt)
    
    if frame % 30 == 0 and game.balloons:  # Every 0.5 seconds
        balloon = game.balloons[0]
        dist = tower.position.distance_to(balloon.position)
        in_range = dist <= tower.range
        print(f"[{frame//60}s] Balloon at ({balloon.position.x:.1f}, {balloon.position.y:.1f}), dist={dist:.1f}, in_range={in_range}, tower_cooldown={tower.fire_cooldown:.2f}")
        print(f"    Balloons: {len(game.balloons)}, Projectiles: {len(game.projectiles)}, Lives: {game.lives}")

print("\n=== Final ===")
print(f"Lives: {game.lives}, Balloons: {len(game.balloons)}, State: {game.state.name}")
