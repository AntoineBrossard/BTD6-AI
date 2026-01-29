"""
Check tower range at specific times
"""

from game.game import BTD6Game

game = BTD6Game(width=800, height=600)
game.place_tower(100, 300)

dt = 1/60
for frame in range(120):  # 2 seconds
    game.update(dt)
    
    tower = game.towers[0]
    
    if game.balloons:
        balloon = game.balloons[0]
        dist = tower.position.distance_to(balloon.position)
        in_range = dist <= tower.range
        
        if frame % 15 == 0:  # Every 0.25 seconds
            print(f"[{frame/60:.2f}s] Balloon at ({balloon.position.x:.1f}, {balloon.position.y:.1f}), dist={dist:.1f}, in_range={in_range}, cooldown={tower.fire_cooldown:.2f}")
            print(f"    Total balloons: {len(game.balloons)}, Projectiles: {len(game.projectiles)}")
