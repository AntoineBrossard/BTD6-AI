"""
Detailed projectile debug
"""

from game.game import BTD6Game, GameState

# Create game
game = BTD6Game(width=800, height=600)
# Place tower right on the path at waypoint 1
game.place_tower(200, 300)

# Simulate
dt = 1/60
projectile_births = []
projectile_deaths = []

for frame in range(300):
    prev_projectiles = len(game.projectiles)
    game.update(dt)
    curr_projectiles = len(game.projectiles)
    
    if curr_projectiles > prev_projectiles:
        projectile_births.append(frame)
        print(f"[{frame/60:.2f}s] Projectile CREATED (total: {curr_projectiles})")
        if game.projectiles:
            p = game.projectiles[-1]
            print(f"    Pos: ({p.position.x:.1f}, {p.position.y:.1f}), Target: ({p.target_balloon.position.x:.1f}, {p.target_balloon.position.y:.1f})")
    
    if curr_projectiles < prev_projectiles:
        projectile_deaths.append(frame)
        print(f"[{frame/60:.2f}s] Projectile REMOVED (total: {curr_projectiles})")
        print(f"    Balloons: {len(game.balloons)}, Lives: {game.lives}")

print(f"\n=== Summary ===")
print(f"Projectiles created: {len(projectile_births)}")
print(f"Projectiles removed: {len(projectile_deaths)}")
print(f"Lives: {game.lives}, Balloons: {len(game.balloons)}")
