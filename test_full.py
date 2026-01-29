"""
Full game test with proper tower placement
"""

from game.game import BTD6Game, GameState

# Create game
game = BTD6Game(width=800, height=600)

# Place multiple towers along the path
# Path: (-50, 300) → (200, 300) → (400, 200) → (600, 300) → (800, 300) → (850, 300)
game.place_tower(100, 300)  # Early in path
game.place_tower(300, 250)  # Near middle bend
game.place_tower(500, 250)  # Late in path

print(f"Towers placed: {len(game.towers)}")
for i, t in enumerate(game.towers):
    print(f"  Tower {i+1}: ({t.position.x}, {t.position.y}) range={t.range}")

# Simulate
dt = 1/60
for frame in range(600):  # 10 seconds
    game.update(dt)
    
    if frame % 60 == 0:  # Every second
        pops = sum(1 for b in game.balloons if b.health == 0)
        print(f"[{frame//60}s] Lives: {game.lives}, Balloons: {len(game.balloons)}, Projectiles: {len(game.projectiles)}, State: {game.state.name}")
    
    if game.state != GameState.RUNNING:
        print(f"\nGame ended at {frame/60:.1f}s!")
        break

print(f"\n=== Final Results ===")
print(f"State: {game.state.name}")
print(f"Lives: {game.lives}/{game.max_lives} (lost: {game.max_lives - game.lives})")
print(f"Balloons remaining: {len(game.balloons)}")
