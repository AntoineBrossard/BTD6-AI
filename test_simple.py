"""
Simple non-visual test to verify game mechanics
"""

from game.game import BTD6Game, GameState
from game.entities import BalloonType

# Create game
game = BTD6Game(width=800, height=600)
print("Game initialized")
print(f"Initial state: {game.state.name}")
print(f"Initial lives: {game.lives}")
print(f"Initial cash: ${game.cash}")

# Place tower near the path
# Path goes through (200, 300), (400, 200), (600, 300)
# Let's place near (400, 200)
success = game.place_tower(400, 250)
print(f"\nTower placement: {'Success' if success else 'Failed'}")
print(f"Tower count: {len(game.towers)}")
if success:
    tower = game.towers[0]
    print(f"Tower at ({tower.position.x}, {tower.position.y}) with range {tower.range}")

# Simulate for 10 seconds
dt = 1/60  # 60 FPS
for frame in range(600):  # 10 seconds
    game.update(dt)
    
    if frame % 60 == 0:  # Every second
        print(f"\n[{frame//60}s] State: {game.state.name}, Lives: {game.lives}, Balloons: {len(game.balloons)}, Projectiles: {len(game.projectiles)}")
    
    if game.state != GameState.RUNNING:
        print(f"\nGame ended at frame {frame}")
        break

print("\n=== Final Results ===")
print(f"State: {game.state.name}")
print(f"Lives remaining: {game.lives}/{game.max_lives}")
print(f"Lives lost: {game.max_lives - game.lives}")
print(f"Balloons on field: {len(game.balloons)}")
print(f"Towers placed: {len(game.towers)}")
